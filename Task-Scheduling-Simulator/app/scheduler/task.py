from status import Status


class Task():
    def __init__(self, pid, creation_date, time_required, priority):
        self.pid = pid
        self.creation_date = creation_date
        self.end_date = None
        self.time_required = time_required
        self.lifetime = time_required
        self.priority = priority
        self.status = Status.uninitialized
        self.quantum = 0
        self.wait_time = 0

    def __str__(self):
        return str(self.pid)
