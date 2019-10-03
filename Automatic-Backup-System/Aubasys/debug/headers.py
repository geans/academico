# -*- coding: utf-8 -*-
from constantmessage import MSG
from settingsclient import Config
auba_version='0.1'

class Construct:
    def register_header(self, user, passwd):
        header = MSG.AUBA + ' ' + auba_version + '\n'
        header += MSG.REGISTER_ME + ' ' + user + '\n'
        header += MSG.PASSWD + ' ' + Config.PASSWD_SERVER
        return header

    def backup_header(self, user, total_size):
        header = MSG.AUBA + ' ' + auba_version + '\n'
        header += MSG.BACKUP_TO + ' ' + user + '\n'
        header += MSG.TOTAL_SIZE + ' ' + str(total_size)
        return header

    def single_file_transmit(self, f_count, f_name, datetime, 
                             f_occurred, f_size, f_content):
        transmit = MSG.AUBA + ' ' + auba_version + '\n'
        transmit += MSG.FILE_COUNT + ' ' + str(f_count) + '\n'
        transmit += MSG.FILE_NAME + ' ' + f_name + '\n'
        transmit += MSG.FILE_DATETIME_UPDATE + ' ' + str(datetime) + '\n'
        transmit += MSG.FILE_OCCURRED + ' ' + f_occurred + '\n'
        transmit += MSG.FILE_SIZE + ' ' + str(f_size) + '\n'
        transmit += '\n'
        transmit += f_content
        return transmit
    
    def computer_size(self, map_updates):
        total_size = 0
        for file in map_updates:
            # The position 2 map_updates is the size of file
            size_single_file = map_updates[file][1]
            if (size_single_file):
                total_size += int()
        return total_size
