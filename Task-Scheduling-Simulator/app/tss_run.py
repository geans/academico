import sys
from os import system
import time
sys.path.append('scheduler')
from scheduler import Scheduler
HELP_FILE_NAME = 'help.txt'


if sys.platform[0:3] == 'win':
    CLEAR_SCREEM = 'cls'
elif sys.platform[0:5] == 'linux':
	CLEAR_SCREEM = 'clear' 
else:
	CLEAR_SCREEM = ''

# Analysis help parameter
if any(i == '-h' or i == '--help' for i in sys.argv):
    help_text = open(HELP_FILE_NAME, 'r')
    print(help_text.read())
    help_text.close()
    exit()


class parameter():
    stage = False
    cores = 1
    debug = False
    quantum_size = 2


# Analysis parameters
argv_updated = sys.argv
if len(sys.argv) > 3:
    argv_updated = [sys.argv[0]]
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '-s' or arg == '--stage':
            parameter.stage = True
        elif arg == '-d' or arg == '--debug':
            parameter.debug = True
        elif arg[:3] == '-c=':
            try:
                parameter.cores = abs(int(float(arg[3:])))
            except:
                print('Error: invalid data to -c=, integer value requiried')
                exit()
        elif arg[:8] == '--cores=':
            try:
                parameter.cores = abs(int(float(arg[8:])))
            except:
                print('Error: invalid data to --cores=, integer value requiried')
                exit()
        elif arg[:3] == '-q=':
            try:
                parameter.quantum_size = abs(int(float(arg[3:])))
            except:
                print('Error: invalid data to -q=, integer value requiried')
                exit()
        elif arg[:10] == '--quantum=':
            try:
                parameter.quantum_size = abs(int(float(arg[10:])))
            except:
                print('Error: invalid data to --quantum=, integer value requiried')
                exit()
        else:
            argv_updated.append(arg)

# Create and running scheduler
sc = Scheduler(argv_updated, parameter)
if parameter.stage:
    while sc.step_run():
        system(CLEAR_SCREEM)
        sc.usage_report()
        sc.print_execution_status()
        time.sleep(1)
else:
    sc.run()
