from status import Status
from operator import attrgetter
from task import Task
from processor import Processor
from manager import TaskQueueManager
from policy import Policy

# Names to output files
OUTPUT_NAME='output' # Main file
REPORT_NAME='report' # Extra file


class Scheduler():
    def __init__(self, argv, parameter):
        self.set_print_on_screen = True
        self.policy_list = Policy()
        # Analize Scheduling Policy
        if not any(arg == argv[2] for arg in self.policy_list.listed()):
            msg = 'Error: Invalid Scheduling Policy.\n'
            msg += 'Use a of the following options:\n'
            for pol in self.policy_list.listed():
                msg += ' ' + pol + '\n'
            msg += 'Example:\n'
            msg += ' python ' + argv[0] + ' ' + argv[1] + ' rr\n'
            msg += 'For help use:\n'
            msg += ' python ' + argv[0] + ' -h'
            self.__print_on_screen(msg)
            exit()

        # Starts files
        init_execution_file = open(OUTPUT_NAME, 'w')
        init_execution_file.close()
        init_report_file = open(REPORT_NAME, 'w')
        init_report_file.close()

        # Starts default value of the attributes
        self.policy = argv[2]
        self.set_print_on_screen = parameter.stage or parameter.debug
        self.executing_diagram = ''
        self.current_status = ''
        self.number_of_finished_tasks = 0
        self.quantum_size = parameter.quantum_size
        self.processor = Processor(self.policy, parameter.cores, parameter.quantum_size)
        self.number_of_tasks = None
        self.optimal_response_time = 0

        # Reads input
        self.task_input = self.__read_input(argv[1])

        # Starts Task Queue Manager with read values
        self.task_queue_manager = TaskQueueManager(argv[2], self.number_of_tasks)
        self.task_queue_manager.new_task(self.task_input)

    def run(self):
        'Runs without pauses'
        while self.step_run():
            self.usage_report()
            self.print_execution_status()

    def step_run(self):
        'Runs with pauses at each clock of 1 or more seconds'
        self.__check_new_task()

        # Check end task
        if self.processor.some_task_ended():
            for task_finished in self.processor.free_finished_task():
                self.task_queue_manager.put_on_finished(task_finished)
        
        # Check end quantum
        if self.processor.some_quantum_ended():
            for task_stopped in self.processor.free_finished_quantum():
                self.task_queue_manager.put_on_ready(task_stopped)

        # Checks for low-priority tasks on the processor to "pp policy"
        if self.policy == self.policy_list.pp:
            ready_list = self.task_queue_manager.get_ready_list()
            running_tasks = self.processor.peek_task()
            for ready in ready_list:
                for running in running_tasks:
                    if running.priority < ready.priority:
                        self.processor.remove(running)
                        self.task_queue_manager.put_on_ready(running)
                        self.processor.set_task([ready])
                        self.task_queue_manager.placed_on_processor(ready)
        
        # Check processor to put task
        free_cores = self.processor.free_cores()
        if free_cores > 0:
            next_task = self.task_queue_manager.get_next_task(free_cores)
            if next_task: # Case even there is task
                self.processor.set_task(next_task)

        self.task_queue_manager.increase_wait_time();
        if self.task_queue_manager.there_task():
            self.__screenshot()
            self.processor.next_clock()
            return True
        else:
            return False

    def print_execution_status(self):
        'Print execution status on file and screen (if set)'
        self.__print_on_screen(self.executing_diagram)
        self.__print_on_file(self.current_status, OUTPUT_NAME)

    def usage_report(self):
        'Print usage report on file and screen (if set)'
        # Get values and rounded to 2 or 4 decimal places
        rt = round(self.__average_response_time(), 4)
        usage, cores = self.__average_usege()
        usage = round(usage, 2)
        percentage_use = round(usage*100/cores, 2)
        wt = round(self.__average_wait_time(), 4)
        current_clock = self.processor.get_clock()
        
        # Builds report pieces
        processor_usage = 'Processor usage percentage:\t'
        processor_usage += str(percentage_use)
        processor_usage += '% (' + str(usage) + ' of '
        processor_usage += str(cores) + ' cores in ' + str(current_clock) + ' s)'
        response_time = 'Average response time:\t\t' + str(rt) + ' s'
        response_time += ' (optimal response time: '
        response_time += str(round(self.optimal_response_time, 4)) + ' s)'
        wait_time = 'Average time waiting:\t\t' + str(wt) + ' s'
        
        # Builds end report
        report = '\t# Report, total time (clock): '
        report += str(current_clock) + '\n'
        report += processor_usage + '\n'
        report += response_time + '\n'
        report += wait_time + '\n'
        
        # Print report
        self.__print_on_screen(report)
        self.__print_on_file(report, REPORT_NAME, 'w')

    def __print_on_file(self, content, file_name, mode='a'):
        'Print on file'
        print_file = open(file_name, mode)
        print_file.write(content + '\n')
        print_file.close()

    def __screenshot(self):
        'Get status of running on this cicle of clock'
        clock = self.processor.get_clock()
        if clock < 9:
            output_line = ' ' + str(clock) + '- ' + str(clock+1)
        elif clock < 10:
            output_line = ' ' + str(clock) + '-' + str(clock+1)
        else:
            output_line = str(clock) + '-' + str(clock+1)
        for task in self.task_input:
            if task.status == Status.waiting:
                output_line += '\t--'
            elif task.status == Status.running:
                output_line += '\t##'
            elif task.status == Status.uninitialized or task.status == Status.finished:
                output_line += '\t  '
        self.current_status = output_line
        self.executing_diagram += output_line + '\n'

    def __check_new_task(self):
        'Checks new task on this cicle of clock'
        new_task = []
        current_clock = self.processor.get_clock()
        for i in range(0, len(self.task_input)):
            if self.task_input[i].creation_date == current_clock:
                self.task_input[i].status = Status.waiting
                new_task.append(self.task_input[i])
        for task in sorted(new_task, key=attrgetter('priority'), reverse=True):
            self.task_queue_manager.put_on_ready(task)

    def __read_input(self, file_path):
        'Reads input with information of tasks'
        i = 1
        output_header = 'tempo'
        task_input = []
        file = open(file_path, 'r')
        input_lines = file.readlines()
        file.close()
        for line in input_lines:
            creation_date, time_required, priority = line.split()
            task = Task(i, int(creation_date), int(time_required), int(priority))
            task_input.append(task)
            output_header += '\tP' + str(i)
            i += 1
            self.optimal_response_time += task.time_required
        self.optimal_response_time = self.optimal_response_time/len(task_input)
        task_input.sort(key=attrgetter('creation_date'))
        self.__print_on_file(output_header, OUTPUT_NAME)
        self.executing_diagram += output_header + '\n'
        self.number_of_tasks = len(task_input)
        return task_input
    
    def __increase_wait_time(self):
        'Increases counter of wait time of each task in waiting'
        for i in range(0, len(self.ready_task_queue)):
            self.ready_task_queue[i].wait_time += 1
    
    def __average_response_time(self):
        'Calculates average response time'
        total = 0
        finished_task = 0
        for task in self.task_input:
            if task.end_date != None:
                # Sum current average with response time this task
                total += (task.end_date - task.creation_date)
                finished_task += 1
        if finished_task != 0:
            return total/finished_task
        else:
            return 0
    
    def __average_usege(self):
        'Calculates and return average use of the processor and amount of  cores'
        return self.processor.get_average_usege(), self.processor.get_number_cores()
    
    def __average_wait_time(self):
        'Calculates average wait time'
        n_tasks = 0
        total_wait = 0
        for task in self.task_queue_manager.get_task_list():
            if task.status != Status.uninitialized:
                total_wait += task.wait_time
                n_tasks += 1
        if n_tasks != 0:
            return total_wait/n_tasks
        else:
            return 0
    
    def __print_on_screen(self, content):
        'Print parameter on screen if set'
        if self.set_print_on_screen:
            print (str(content))
