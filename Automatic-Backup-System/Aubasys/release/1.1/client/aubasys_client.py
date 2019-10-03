# -*- coding: utf-8 -*-
####################### APLICATION CLIENT ###########################
#                                                                   #
# Coded by: Gean da Silva Santos [gss@ic.ufal.br]                   #
#                                                                   #
#   Aubasys - Automatic Backup System                               #
# The Automatic Backup System helps you keep what is important      #
# to you on a local host that can be your PC or your work computer. #
#                                                                   #
#####################################################################

import socket
import os
import json
import sys
from settingsclient import Config
from constantmessage import *
from tools import debugme, myprint
from time import sleep
from datetime import datetime
from headers import Construct
from platform import system

reload(sys)
sys.setdefaultencoding('utf-8')

auba_version = MSG.auba_version

INTERFACE = socket.AF_INET     # interface type
TRANSPORT = socket.SOCK_STREAM # transport type: aka TCP
LF = '\n' # line feed

if (system() == 'Windows'):
    os_separator = '\\'
    import ctypes # to create symbolic link
elif (system() == 'Linux'):
    os_separator = '/'
else:
    debugme("CRITICAL ERROR: system operation not supported. Availability: Unix, Windows")
    exit()

class ClientAUBA:
    def __init__(self):
        self.last_state_path = '.last-state.auba'
        self.map_updates_save = '.map-update-file.auba'
        self.size_buffer_recv = 1024
        self.directory_path = Config.DIRECTORY_TO_BACKUP
        self.client_name = Config.CLIENT_NAME
        self.host = Config.HOST_SERVER
        self.port = Config.PORT
        self.user = Config.CLIENT_NAME
        self.passwd = Config.PASSWD_SERVER
        self.time_check = Config.TIME_CHECK
        
        self.addr = (Config.HOST_SERVER, Config.PORT)
        self.connection = socket.socket(INTERFACE, TRANSPORT)
        self.construct = Construct()
        self.map_updates = {}
        self.map_last_state = {}
        self.error = False
        
    def get_server(self):
        return self.host
        
    def is_error(self):
        return self.error
    
    def __has_update(self):
        ret = False
        map_current_state = {}
        map_updates = {}
        directory = self.directory_path
        if (directory == ''):
            debugme('Directory to backup has not setting')
            self.error = True
            return ret
        if (not os.path.exists(directory)):
            os.makedirs(directory)
        files = os.listdir(directory)
        if (not os.path.exists(self.last_state_path) and files != []):
            for file in files:
                full_path_file = directory + os_separator + file
                map_updates[file] = MSG.ADDITION, os.path.getsize(full_path_file), str(datetime.fromtimestamp(os.path.getmtime(full_path_file)))
            ret = True
        elif (os.path.exists(self.last_state_path)):
            last_state = open(self.last_state_path, 'r')
            map_last_state = json.load(last_state)
            last_state.close()
            for file in files:
                full_path_file = directory + os_separator + file
                dt = datetime.fromtimestamp(os.path.getmtime(full_path_file))
                map_current_state[file] = str(dt)
            if (map_last_state != map_current_state):
                ret = True
                for file in map_current_state.keys():
                    full_path_file = directory + os_separator + file
                    if (not map_last_state.has_key(file)):
                        size_file = os.path.getsize(full_path_file)
                        map_updates[file] = MSG.ADDITION, size_file, map_current_state[file]
                    else:
                        if (map_last_state[file] != map_current_state[file]):
                            size_file = os.path.getsize(full_path_file)
                            map_updates[file] = MSG.CHANGES, size_file, map_current_state[file]
                        # Remove of map_last_state the intersection between:
                        #     map_last_state and map_current_state
                        del(map_last_state[file]) 
                for file in map_last_state:
                    map_updates[file] = MSG.REMOVAL, None, '0 0'
        self.map_updates = map_updates
        self.map_last_state = map_current_state
        return ret
    
    def wait_for_updates(self):
        ret = False
        while not self.is_error():
            if (self.__has_update()):
                ret = True
                break
            sleep(self.time_check)
        return ret
    def connect(self):
        return self.connection.connect((self.host, self.port))
        
    def close(self):
        return self.connection.close()
        
    def __send(self, msg):
        return self.connection.sendall(msg)
        
    def __recv(self):
        return self.connection.recv(self.size_buffer_recv)
        
    def request_backup(self):
        total_size = self.construct.computer_size(self.map_updates)
        main_header = self.construct.backup_header(self.client_name, total_size)
        self.__send(main_header)
        return self.__recv()
        
    def request_register(self):
        register_header = self.construct.register_header(self.user, self.passwd)
        self.__send(register_header)
        return self.__recv()

    def send_updates(self):
        count_file = len(self.map_updates)
        myprint('Number of files to to send: ' + str(count_file))
        for file in self.map_updates.keys():
            occurred = self.map_updates[file][0]
            size_file = self.map_updates[file][1]
            datetime = self.map_updates[file][2]
            full_path_file = self.directory_path + os_separator + file
            try:
                f = open(full_path_file, 'r')
                content = f.read()
                f.close()
            except Exception, e:
                content = ''
                size_file = '0'
            header_file = self.construct.single_file_transmit(count_file, file, datetime,
                                                                  occurred, size_file, content)
            count_file -= 1
            self.__send(header_file)
            recv = self.__recv()
            myprint('  File: "' + file + '", occurred: ' + occurred + ', status: ' + recv[:-1])
        recv_finish_confirm = self.__recv()
        if (recv_finish_confirm == MSG.COMPLETE_UPDATE):
            # Save current map states
            update_last_state_file = open(self.last_state_path, 'w')
            update_last_state_file.write(json.dumps(self.map_last_state))
            update_last_state_file.close()
        return recv_finish_confirm

is_error = False
myprint('\nStart client AUBA ' + auba_version + '\n\n')
while not is_error:
    client = ClientAUBA()
    myprint('Wait for updates')
    client.wait_for_updates()
    is_error = client.is_error()
    if (not is_error):
        myprint('* Update detected\n')
        client.connect()
        recv = client.request_backup()
        myprint('Status for request backup: ' + recv[:-1])
        if (recv == MSG.I_DONT_KNOW_YOU):
            myprint('Request register to: ' + Config.CLIENT_NAME)
            recv = client.request_register()
            if (recv == MSG.REGISTER_OK):
                myprint('Register success')
                myprint('* Request backup again\n\n')
                recv = client.request_backup()
            elif (recv == MSG.WRONG_PASSWD):
                debugme('Error (-1): invalid password for server: ' + client.get_server())
            else:
                debugme('Error (-2): unknow message: ' + recv)
        elif (recv == MSG.OK):
            myprint('Start to send files')
            recv = client.send_updates()
            myprint('Result of send updates: ' + recv)
        else:
            debugme('Error: message from server unknow: ' + recv)
        client.close()
        myprint('* Finish operation\n\n')
myprint('\nStop client AUBA ' + auba_version + '\n\n')
    
