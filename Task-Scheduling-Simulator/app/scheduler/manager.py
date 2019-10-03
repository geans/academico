from status import Status
from policy import Policy


class TaskQueueManager():
    def __init__(self, policy, number_of_tasks=None):
        self.__policy_list = Policy()
        self.__policy = policy
        self.__by_priority = any(self.__policy == pol for pol in self.__policy_list.uses_priority())
        self.__setted_sort = self.__by_priority or policy == self.__policy_list.sjf
        self.__all = []
        self.__ready = []
        self.__finished = 0
        self.__number_of_tasks = number_of_tasks

    def new_task(self, task):
        if type(task) == list:
            self.__all += task
        else:
            self.__all.append(task)
    
    def put_on_ready(self, task):
        index = self.__all.index(task)
        self.__all[index].status = Status.waiting
        self.__ready.append(index)
        
        # Sort ready list according with policy scheduling
        if self.__setted_sort:
            if self.__by_priority:
                self.__ready.sort(key=self.__sort_by_priority(self.__all), reverse=True)
            else:
                self.__ready.sort(key=self.__sort_by_duration(self.__all))
    
    def put_on_finished(self, task):
        index = self.__all.index(task)
        self.__all[index].status = Status.finished
        self.__finished += 1

    def placed_on_processor(self, task):
        index = self.__all.index(task)
        self.__all[index].status = Status.running
        try:
            self.__ready.remove(index)
        except:
            None
    
    def get_next_task(self, amount=1):
        task_to_run = []
        for i in range(0, amount):
            if self.__ready:
                index = self.__ready.pop(0)
                self.__all[index].status = Status.running
                task_to_run.append(self.__all[index])
        return task_to_run
    
    def there_task(self):
        if self.__number_of_tasks is None:
            return True
        else:
            return self.__finished < self.__number_of_tasks
    
    def increase_wait_time(self):
        if self.__policy == self.__policy_list.rrta:
            for i in self.__ready:
                self.__all[i].wait_time += 1
                self.__all[i].priority += 1 # To Task Aging
        else:
            for i in self.__ready:
                self.__all[i].wait_time += 1

    def get_task_list(self):
        return self.__all

    def get_ready_list(self):
        ready_list = []
        for index in self.__ready:
            ready_list.append(self.__all[index])
        return ready_list

    def __sort(self):
        'Sort ready list according with policy scheduling'
        if self.__setted_sort:
            if self.__by_priority:
                self.__ready.sort(key=self.__sort_by_priority(self.__all), reverse=True)
            else:
                self.__ready.sort(key=self.__sort_by_duration(self.__all))

    def __sort_by_priority(self, task_list):
        'Used to sort "self.__ready" by priority of the items of "self.__all"'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return task_list[self.obj].priority < task_list[other.obj].priority
            def __gt__(self, other):
                return task_list[self.obj].priority > task_list[other.obj].priority
        return K

    def __sort_by_duration(self, task_list):
        'Used to sort "self.__ready" by time_required of the items of "self.__all"'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return task_list[self.obj].time_required < task_list[other.obj].time_required
            def __gt__(self, other):
                return task_list[self.obj].time_required > task_list[other.obj].time_required
        return K
