# -*- coding: utf-8 -*-
active_debug = True
active_print = True
file_name = 'deubg.txt'

from datetime import datetime

LF        = '\n' # line feed
BACKSLASH = '\\'

def debugme(msg):
    if (active_debug):
        f = open (file_name, 'a')
        now = datetime.now()
        date = str(now.day) + '-' + str(now.month) + '-' + str(now.year) + ' '
        time = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + ' - '
        f.write(date + time)
        f.write(str(msg))
        f.write(LF)
        f.close()
    myprint("debug - " + str(msg))
        
def myprint(msg):
    if (active_print):
        print msg
