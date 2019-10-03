# -*- coding: utf-8 -*-
####################### APLICATION SERVER ###########################
#                                                                   #
# Coded by: Gean da Silva Santos [gss@ic.ufal.br]                   #
#                                                                   #
#   Aubasys - Automatic Backup System                               #
# The Automatic Backup System helps you keep what is important      #
# to you on a local host that can be your PC or your work computer. #
#                                                                   #
#####################################################################

import os
import socket
import sys
from settingsserver import Config
from constantmessage import *
from tools import debugme, myprint
from threading import Thread
from datetime import datetime
from string import split, join, maketrans
from platform import system
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')

auba_version = MSG.auba_version
block_size = 4096 # number of byte to receiver for time

## CONSTANT SETTINGS
LF        = '\n' # line feed
SEPARATOR = ' '
INTERFACE = socket.AF_INET     # interface type
TRANSPORT = socket.SOCK_STREAM # transport type: aka TCP
FOLDER_BACK = 'current' # Folder with link to update files
PREVIOUS = 'previous' # Folder with other folder that contains the previous files
REG_USERS_FILE ='.reg-users.auba' # Name of file to register user. Default: reg-users.auba

hosts_accepts = Config.HOSTS
port = Config.PORT
number_of_users = Config.NUMBER_OF_USERS
directory = Config.DIRECTORY_BACKUP_SERVER
if (system() == 'Windows'):
    os_separator = '\\' # backslash
    import ctypes # to create symbolic link
elif (system() == 'Linux'):
    os_separator = '/' # slash
else:
    debugme("CRITICAL ERROR: system operation not supported. Availability: Unix, Windows")
    exit()

class SingleConnection(Thread):
    def __init__ (self, conn, client):
        myprint("Init Single Connection")
        super(SingleConnection, self).__init__()
        
        self.directory_path = directory

        self.conn = conn
        self.client = client
        self.free_size = -1
        self.user_name = ''
        self.last_folder = ''
        self.finish_conection = False
        self.os_separator = os_separator

        f = open(REG_USERS_FILE, 'a')
        f.close()

        if (system() != 'Linux' and system() != 'Windows'):
            debugme("CRITICAL ERROR: system operation not supported. Availability: Unix, Windows")
            self.finish_conection = True
            exit()
        if (self.directory_path == ''):
            self.directory_path = 'automatic backup'
        if (not os.path.exists(self.directory_path)):
            os.mkdir(self.directory_path)
        
    def __check_user_space(self):
        if (system() == 'Windows'):
            full_path_user = self.directory_path
            f = join(os.popen("dir " + full_path_user).readlines(),'')
            stats = split(f,'\n')
            self.free_size = join(split(split(stats[-2],' ')[-3],'.'),'')
            self.free_size = int(self.free_size)
        elif (system() == 'Linux'):
            full_path_user = self.directory_path
            myprint('Full path client ' + self.user_name + ': ' + full_path_user)
            f = os.popen("df " + full_path_user).read().split(' ')[-4]
            self.free_size = int(f)
        else:
            debugme("CRITICAL ERROR: system operation not supported. Availability: Unix, Windows")
            self.finish_conection = True
            self.free_size = -1
            exit()
        return self.free_size
        
    def __check_user_register(self):
        reg_users = open(REG_USERS_FILE, 'r')
        users_list = reg_users.read().split(LF)
        reg_users.close()
        return self.user_name in users_list
    
    def __check_header(self):
        # read header
        header = self.conn.recv(1024).decode()
        header = header.split(LF)
        ret = MSG.I_DONT_KNOW_YOU
        try:
            auba, version = header[0].split(SEPARATOR)
        except Exception, e:
            debugme("Error: header not accepted.\n" + join(header, LF) + '\n' + str(e))
            return MSG.CONTRACT_ERROR
        if (auba != MSG.AUBA or len(header) != 3):
            ret = MSG.CONTRACT_ERROR
        else:
            try:
                request, self.user_name = header[1].split(SEPARATOR)
                parameter1, parameter2 = header[2].split(SEPARATOR)
            except Exception, e:
                debugme("Error: header not accepted.\n" + join(header, LF) + '\n' + str(e))
                return MSG.CONTRACT_ERROR

            # Check user
            check_user = self.__check_user_register()
            if (request != MSG.REGISTER_ME and not check_user):
                self.conn.send(MSG.I_DONT_KNOW_YOU)
                debugme('Unknow user request backup')
                header = self.conn.recv(1024)
                header = header.split(LF)
                try:
                    request, self.user_name = header[1].split(SEPARATOR)
                    parameter1, parameter2 = header[2].split(SEPARATOR)
                except Exception, e:
                    debugme("Error: header not accepted.\n" + join(header, LF) + '\n' + str(e))
                    return MSG.CONTRACT_ERROR
            
            # Execute register
            if (request == MSG.REGISTER_ME):
                pw = parameter2
                myprint("User request register: " + self.user_name)
                if (pw == Config.PASSWD_SERVER):
                    reg_users = open(REG_USERS_FILE, 'a')
                    reg_users.write(self.user_name + LF)
                    new_directory = self.directory_path + self.os_separator
                    new_directory += self.user_name + self.os_separator
                    new_directory += FOLDER_BACK
                    if (not os.path.exists(new_directory)):
                        os.makedirs(new_directory)
                    ret = MSG.REGISTER_OK
                    myprint("User registered")
            
            # Execute backup
            elif (request == MSG.BACKUP_TO):
                if (not check_user):
                    check_user = self.__check_user_register()
                if (check_user):
                    total_size = int(parameter2)
                    space_free = total_size + 1 #self.__check_user_space()
                    if (space_free == -1):
                        ret = MSG.INTERNAL_ERRO
                    elif (space_free < total_size):
                        ret = MSG.INSUFFICIENT_SPACE
                        debugme('Space request: ' + total_size + ', space free: ' + space_free)
                    else:
                        now = datetime.now()
                        date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
                        time = str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
                        self.last_folder = self.directory_path + self.os_separator
                        self.last_folder += self.user_name + self.os_separator
                        self.last_folder += PREVIOUS + self.os_separator
                        self.last_folder += date + ' ' + time
                        if (not os.path.exists(self.last_folder)):
                            os.makedirs(self.last_folder)
                        ret = MSG.OK
                        myprint("Update of date: " + date + ", time: " + time)
                else:
                    ret = MSG.I_DONT_KNOW_YOU
            else:
                ret = MSG.CONTRACT_ERROR
                debugme('Unknow message to request: ' + request)
        return ret

    def __save_file(self, content, f_name, f_occurred):
        ret = MSG.OK
        if (f_occurred == MSG.REMOVAL):
            myprint('Remove file: ' + f_name)
            link_name = self.directory_path + self.os_separator
            link_name += self.user_name + self.os_separator
            link_name += FOLDER_BACK + self.os_separator + f_name
            try:
                os.remove(link_name)
            except Exception, e:
                pass
        else:
            # save in permanent folder
            path_file = self.last_folder + self.os_separator + f_name
            try:
                f = open (path_file, 'w')
                f.write(content)
                f.close()
                myprint('File: "' + f_name + '" saved in "' + path_file + '"')
            except Exception, e:
                debugme('Unpossible to save file "'+f_name+'" in "'+path_file + '"\n' + str(e))
                return MSG.INTERNAL_ERRO
            #try:
            ret = self.__create_link(path_file, f_name)
            #except Exception, e:
            #    debugme('No create link' + '\n' + str(e))
            #    ret = MSG.INTERNAL_ERRO
            
        return ret
        
    def __create_link(self, source, f_name):
        ret = MSG.OK
        link_name = self.directory_path + self.os_separator
        link_name += self.user_name + self.os_separator
        link_name += FOLDER_BACK + self.os_separator + f_name
        try:
            os.remove(link_name)
            myprint('Updating symbolic link')
        except Exception, e:
            myprint('Creating symbolic link')
        if (system() == 'Windows'):
            csl = ctypes.windll.kernel32.CreateSymbolicLinkW
            csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
            csl.restype = ctypes.c_ubyte
            flags = 1 if os.path.isdir(source) else 0
            if (csl(link_name, source, flags) == 0):
                ret = MSG.INTERNAL_ERRO
                debugme('Error to create symbolic link: ' + str(ctypes.WinError()))
                debugme('** You maybe not permition to create symbolic link')
            myprint('Link created: "' + link_name + '"\n      source: "' + source + '"')
        elif (system() == 'Linux'):
            os.symlink(source, link_name)
            myprint('Link created: "' + link_name + '"\n      source: "' + source + '"')
        else:
            debugme("CRITICAL ERROR: system operation not supported. Availability: Unix, Windows")
            self.finish_conection = True
            exit()
        return ret

    def __handle_file(self):
        # read header file
        header_file = ''
        while True:
            block = self.conn.recv(block_size)
            header_file += block
            if ((not block) or len(block) < block_size):
                break
        header_file = header_file.split(LF)
        
        ret = MSG.OK
        try:
            auba, version = header_file[0].split(SEPARATOR)
        except Exception, e:
            debugme("Error: header not accepted" + join(header_file, LF) + '\n' + str(e))
            return MSG.CONTRACT_ERROR
        if (auba != MSG.AUBA or len(header_file) < 7):
            ret = MSG.CONTRACT_ERROR
        else:
            try:
                file_count, f_count = header_file[1].split(SEPARATOR)
                file_name, f_name = header_file[2].split(SEPARATOR, 1)
                file_datetime, f_date, f_time = header_file[3].split(SEPARATOR)
                file_occurred, f_occurred = header_file[4].split(SEPARATOR)
                file_size, f_size = header_file[5].split(SEPARATOR)
            except Exception, e:
                debugme("Error: header not accepted" + join(header_file, LF) + '\n' + str(e))
                return MSG.CONTRACT_ERROR
            if (self.last_folder == '' or not os.path.exists(self.last_folder)):
                now = datetime.now()
                date = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
                time = str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
                self.last_folder = self.directory_path + self.os_separator
                self.last_folder += self.user_name + self.os_separator
                self.last_folder += PREVIOUS + self.os_separator
                self.last_folder += data + ' ' + time
        
        # read content file
            content = join(header_file[7:], LF)
            if (len(content) != int(f_size)):
                debugme("Error: file corrupted, content size: "+str(len(content))+", expected size: "+f_size)
            ret = self.__save_file(content, f_name, f_occurred)
            if (f_count == '1'):
                self.finish_conection = True
        return ret

    def run(self):
        status = self.__check_header()
        self.conn.send(status)
        if (status == MSG.REGISTER_OK):
            self.conn.send(status)
            myprint('Send register ok')
        else:
            while (status == MSG.OK and not self.finish_conection):
                myprint('Receiving files')
                status = self.__handle_file()
                self.conn.send(status)
            myprint('Finish receiver files, status: ' + status)
            if (status == MSG.OK):
                self.conn.send(MSG.COMPLETE_UPDATE)
            else:
                self.conn.send(MSG.ERROR_IN_UPDATE)
        if (status == MSG>INTERNAL_ERRO):
            sleep(300) # wait 5 minutes
        return status

# Init program

myprint('\nStart server AUBA ' + auba_version + '\n\n')

addr = (hosts_accepts, port)
serv_socket = socket.socket(INTERFACE, TRANSPORT)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_socket.bind(addr)
serv_socket.listen(number_of_users)
while True:
    con, client = serv_socket.accept()
    myprint("    Connection accept to " + client[0] + '\n')
    connection = SingleConnection(con, client)
    connection.start()
serv_socket.close()

myprint('\nStop server AUBA ' + auba_version + '\n\n')



