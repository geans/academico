class Policy():
    fcfs = 'fcfs'   # First Come First Served
    rr = 'rr'       # Round-Robin
    rrta = 'rrta'   # Round-Robin with Task Aging
    sjf = 'sjf'     # Shortest Job First
    pp = 'pp'       # Priority Preemption
    pwp = 'pwp'     # Priority Without Preemption
    def listed(self):
        return [self.fcfs, self.rr, self.rrta, self.sjf, self.pp, self.pwp]
    def uses_priority(self):
        return [self.rrta, self.pp, self.pwp]
