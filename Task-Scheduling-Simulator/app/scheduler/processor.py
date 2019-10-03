from status import Status
from task import Task
from policy import Policy
DEBUG=False


def d(content):
    if DEBUG:
        print (str(content))


class Processor():
    def __init__(self, policy, cores=1, quantum_size=2):
        self.__policy = policy
        self.__status = Status.free
        self.__clock = 0
        self.__used_cores = []
        self.__number_of_cores = cores
        self.__free_cores = cores
        self.__finished_task_list = []
        self.__finished_quantum_list = []
        self.__quantum_size = quantum_size
        self.__used_tasking = 0
    
    def set_task(self, tasks):
        ret = []
        if self.__free_cores > 0:
            n_tasks = len(tasks)
            if self.__free_cores < n_tasks:
                ret = tasks[self.__free_cores:]
                tasks = tasks[:self.__free_cores]
                self.__free_cores = 0
            else:
                self.__free_cores -= n_tasks
            for task in tasks:
                task.status = Status.running
                self.__used_cores.append(task)
        return ret
    
    def next_clock(self):
        self.__used_tasking += len(self.__used_cores)
        self.__clock += 1
        tasks_list_updated = []
        while self.__used_cores:
            task_running = self.__used_cores.pop(0)
            task_running.lifetime -= 1
            task_running.quantum += 1
            # Check end of this task
            if task_running.lifetime <= 0:
                self.__finished_task_list.append(task_running)
                task_running.status = Status.finished
                if task_running.end_date is None:
                    task_running.end_date = self.__clock
            # Check end of quantum of this task
            elif (self.__policy == Policy().rr or self.__policy == Policy().rrta) and task_running.quantum >= self.__quantum_size:
                self.__finished_quantum_list.append(task_running)
                task_running.status = Status.waiting
                task_running.quantum = 0 # reset quantum
            # Update list in running
            else:
                tasks_list_updated.append(task_running)
        self.__used_cores = tasks_list_updated

    def __free_finished(self, task_list_to_exit):
        self.__free_cores += len(task_list_to_exit)
        return task_list_to_exit

    def free_finished_task(self):
        task_list_to_exit = self.__finished_task_list
        self.__finished_task_list = []
        return self.__free_finished(task_list_to_exit)

    def free_finished_quantum(self):
        task_list_to_exit = self.__finished_quantum_list
        self.__finished_quantum_list = []
        return self.__free_finished(task_list_to_exit)
    
    def get_clock(self):
        return self.__clock

    def some_task_ended(self):
        return len(self.__finished_task_list) > 0
    
    def some_quantum_ended(self):
        return len(self.__finished_quantum_list) > 0
    
    def free_cores(self):
        return self.__free_cores
    
    def peek_task(self):
        return self.__used_cores

    def remove(self, task):
        self.__used_cores.remove(task)
        self.__free_cores += 1
    
    def get_average_usege(self):
        return self.__used_tasking/self.__clock
    
    def get_number_cores(self):
        return self.__number_of_cores
