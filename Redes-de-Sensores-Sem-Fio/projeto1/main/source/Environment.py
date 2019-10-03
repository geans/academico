from random import randint
from Node import Node
from Sink import Sink, sqrt
from time import sleep

DEBUG = False


def debug(value):
    if DEBUG:
        print('\t<', value, '>', sep='')


class Environment:
    NEAR = 'near'
    ENERGY = 'energy'
    DUTY_CICLE = 'duty_cicle'

    def __init__(self, number_of_nodes, transmission_range, speed_sink, size_area, sink_route, strategy, duty_cycle):
        """
        :type number_of_nodes: a integer number
        :type transmission_range: a number, given in meters
        :type speed_sink: a number, speed given in meters per second
        :type size_area: a list of two numbers, the values in meters
        :type sink_route: a list of list of two numbers referring to the each target position
        :type strategy: a string, use static variable on class Environment
        :type duty_cycle: a boolean, enable duty-cicle on nodes
        """
        self.sink = None
        self.define_sink_route(sink_route, speed_sink)
        self.transmission_range = transmission_range
        self.size_x = size_area[0]
        self.size_y = size_area[1]
        self.sink_route = sink_route
        self.strategy = strategy
        self.duty_cicle = duty_cycle
        self.nodes = []
        Node.is_run = True
        for i in range(number_of_nodes):
            x_pos = randint(0, self.size_x)
            y_pos = randint(0, self.size_y)
            pos = (x_pos, y_pos)
            node = Node(pos, duty_cycle)
            node.start()
            self.nodes.append(node)

    def define_sink_route(self, sink_route, speed_sink):
        if len(sink_route) < 2:
            raise Exception('Esperado, ao menos, lista com duas listas contendo posição inicial e destino')
        init_sink_position = sink_route[0]
        del sink_route[0]
        target_sink_position = (sink_route[0])
        del sink_route[0]
        self.sink = Sink(init_sink_position, speed_sink, target_sink_position)
        self.sink_route = sink_route

    def check_nodes_in_sink_radius(self, clock):
        packets_transmitted = 0
        packets_lost = 0
        nodes_founds = []
        nodes_lost = []
        more_energy = [0, None]
        more_close = [self.transmission_range + 1, None]
        for node in self.nodes:
            node_on = node.wait_beacon(clock)
            if self.strategy == Environment.DUTY_CICLE:
                if not node_on:
                    continue
            x = node.position[0] - self.sink.position[0]
            y = node.position[1] - self.sink.position[1]
            distance = sqrt(x ** 2 + y ** 2)
            if distance <= self.transmission_range:
                nodes_founds.append(node.id)
                if node.energy < Node.cost_send_package:
                    nodes_lost.append(node.id)
                else:
                    if more_energy[0] < node.energy:
                        more_energy[0] = node.energy
                        more_energy[1] = node
                    if more_close[0] > distance:
                        more_close[0] = distance
                        more_close[1] = node
        if self.strategy == Environment.ENERGY:
            if more_energy[0] >= Node.cost_send_package:
                if more_energy[1].package_transmission():
                    packets_transmitted += 1
                packets_lost = len(nodes_founds) - len(nodes_lost) - 1
        else:  # self.strategy == Environment.NEAR:
            if more_close[0] <= self.transmission_range:
                if more_close[1].package_transmission():
                    packets_transmitted += 1
                packets_lost = len(nodes_founds) - len(nodes_lost) - 1

    def check_environment(self):
        packets_lost = 0
        sink_pos = self.sink.position
        nodes_founds = []

        Node.sink_position = self.sink.position  # atualiza posição do sink
        Node.environment.append(Node.BEACON)
        nodes_in_radius = 0
        for node in Node.environment:
            if type(node) == Node:
                x = node.position[0] - sink_pos[0]
                y = node.position[1] - sink_pos[1]
                distance = sqrt(x ** 2 + y ** 2)
                if distance <= self.transmission_range:
                    nodes_founds.append(node.id)
                    nodes_in_radius += 1
                    debug('Nó ' + str(node.id) + ' encontrado pelo Sink')
        if nodes_in_radius > 1:
            packets_transmitted = 0
            packets_lost = nodes_in_radius
        else:
            packets_transmitted = nodes_in_radius

        Node.environment.remove(Node.BEACON)
        self.sink.reached_target()  # movimentação do sink
        if self.sink.in_target and len(self.sink_route):
            self.sink.update_target(self.sink_route[0])
            del self.sink_route[0]

        return packets_transmitted, packets_lost, nodes_founds, Node.nodes_discharged

    def end_sink_turn(self):
        if len(self.sink_route) == 0 and self.sink.in_target:
            return True
        else:
            return False

    def energy_network_level(self):
        energy = 0
        for node in self.nodes:
            energy += node.energy
        return energy

    def nodes_lost(self):
        return len(Node.nodes_discharged)

    def finalize(self):
        Node.is_run = False
        sleep(0.01)