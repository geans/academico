from random import randint
from time import sleep
from threading import Thread

DEBUG = True


def debug(value):
    if DEBUG:
        print('\t\t<', value, '>', sep='')

def sqrt(value):
    return int(value) ** (1 / 2)


class Node(Thread):
    # atributos estaticos
    count = 0
    energy_begin = 604800
    cost_beacon_waiting = 10
    cost_send_package = 20
    cost_radio = 20
    environment = []
    duty_cycle_window = 8
    BEACON = 'beacon'
    nodes_discharged = []
    sink_position = [-1000, -1000]
    is_run = True

    def __init__(self, position, enable_duty_cycle = True, transmission_range = 20):
        """
        :type position: a list of two numbers
        :type duty_cicle: a boolean, enable duty-cicle strategy
        """
        Thread.__init__(self)
        self.__id = Node.count
        Node.count += 1
        self.energy = Node.energy_begin
        self.position = position
        self.__dc_enable = enable_duty_cycle
        self.__duty_cycle = -1
        self.__mod_7 = 0b111
        self.clock = 0
        self.__radio_on = False
        self.transmission_range = transmission_range

    def wait_beacon(self, clock):
        if self.energy >= Node.cost_beacon_waiting:
            if self.__dc_enable:
                if self.__mod(clock) == self.__duty_cycle:
                    self.energy -= Node.cost_beacon_waiting
                    return True
            else:
                self.energy -= Node.cost_beacon_waiting
                return True

        if self.energy < Node.cost_send_package:
            self.energy = 0
        return False

    def package_transmission(self):
        if self.energy > 0:
            self.energy -= Node.cost_send_package
            return 1
        else:
            return 0

    def pass_clock(self):
        self.clock += 1
        if self.energy:
            self.energy -= 1
            if self.__radio_on :
                self.energy -= Node.cost_radio
            sleep(0.001)
            if self.energy < 0:
                self.energy = 0

    def listen_other_nodes(self):
        self.__radio_on = True
        free_env = True
        for node in Node.environment:
            if type(node) == Node:
                x = node.position[0] - self.position[0]
                y = node.position[1] - self.position[1]
                distance = sqrt(x ** 2 + y ** 2)
                if distance > self.transmission_range:
                    free_env = False
                    break
        self.pass_clock()
        self.__radio_on = False
        return free_env

    def check_sink_beacon(self):
        ret = False
        self.__radio_on = True

        beacon = self.BEACON in Node.environment
        free_env = True
        for node in Node.environment:
            if type(node) == Node:
                x = node.position[0] - self.position[0]
                y = node.position[1] - self.position[1]
                distance = sqrt(x ** 2 + y ** 2)
                if distance > self.transmission_range:
                    free_env = False
                    break
        if beacon and free_env:
            x = Node.sink_position[0] - self.position[0]
            y = Node.sink_position[1] - self.position[1]
            distance = sqrt(x ** 2 + y ** 2)
            if distance > self.transmission_range:
                ret = True

        self.pass_clock()
        self.__radio_on = False
        return ret

    def send_package(self):
        self.__radio_on = True
        Node.environment.append(self)
        self.pass_clock()
        Node.environment.remove(self)
        self.__radio_on = False

    def run(self):
        self.__duty_cycle = -1
        #debug('Node ' + str(self.__id) + ' em execução')
        while self.energy and self.__duty_cycle == -1 and Node.is_run:
            for i in range(200):
                if self.listen_other_nodes():
                    self.__duty_cycle = self.__mod(self.clock)
                    debug('Node ' + str(self.__id) + ' encontrou momento para duty-cycle')
                if self.__duty_cycle != -1:
                    if self.__mod(self.clock):
                        self.send_package()  # envia sinal para marcar tempo do duty-cycle
        while self.energy and Node.is_run:
            if self.__mod(self.clock) == self.__duty_cycle:
                if self.check_sink_beacon():
                    self.send_package()
                    debug('Node ' + str(self.__id) + ' enviou pacote')
            else:
                self.pass_clock()
            if self.clock % (1000 * self.duty_cycle_window):
                self.send_package()  # envia sinal para marcar tempo do duty-cycle
        if self.energy <= 0:
            Node.nodes_discharged.append(self)
            debug('\tNode '+str(self.__id) + ' descarregado')
        debug('Node '+str(self.__id) + ' desligando')

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return 'id: ' + str(self.__id)\
               + ', pos: ' + str(self.position)

    def __mod(self, value):
        return value & self.__mod_7
