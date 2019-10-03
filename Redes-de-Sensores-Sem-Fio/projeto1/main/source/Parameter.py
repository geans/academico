

class Parameter:
    def __init__(self):
        self.__nodes = []
        self.__range = []
        self.__speed = []
        self.__area = []
        self.__route = []
        self.__scenarios = 0
        self.__RIGHT = 0
        self.__UP1 = 1
        self.__LEFT = 2
        self.__UP2 = 3
        self.__descriptor = []
        self.current = 0

        # Cenário 1
        self.__scenarios += 1
        self.__nodes += [10]
        self.__range += [20]
        self.__speed += [1]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 2
        self.__scenarios += 1
        self.__nodes += [10]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 3
        self.__scenarios += 1
        self.__nodes += [100]
        self.__range += [20]
        self.__speed += [1]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 4
        self.__scenarios += 1
        self.__nodes += [100]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 5
        self.__scenarios += 1
        self.__nodes += [1000]
        self.__range += [20]
        self.__speed += [1]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 6
        self.__scenarios += 1
        self.__nodes += [1000]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 7
        self.__scenarios += 1
        self.__nodes += [1000]
        self.__range += [20]
        self.__speed += [1]
        x_max, y_max = 100, 100
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 8
        self.__scenarios += 1
        self.__nodes += [1000]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 100, 100
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 9
        self.__scenarios += 1
        self.__nodes += [10000]
        self.__range += [20]
        self.__speed += [1]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 10
        self.__scenarios += 1
        self.__nodes += [10000]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 1000, 1000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 11
        self.__scenarios += 1
        self.__nodes += [100]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 10000, 10000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 12
        self.__scenarios += 1
        self.__nodes += [1000]
        self.__range += [20]
        self.__speed += [10]
        x_max, y_max = 10000, 10000
        self.__area += [[x_max, y_max]]
        r = [[0, 0]]
        direction = self.__RIGHT
        while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
            tmp = list(r[-1])
            if direction == self.__RIGHT:
                tmp[0] = x_max
            elif direction == self.__UP1 or direction == self.__UP2:
                tmp[1] += 2 * self.__range[-1]
            elif direction == self.__LEFT:
                tmp[0] = 0
            r.append(tmp)
            direction = (direction + 1) % 4
        self.__route += [r]
        self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
                              'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
                              'velocidade: '+str(self.__speed[-1])+' m/s']

        # Cenário 13
        # self.__scenarios += 1
        # self.__nodes += [10000]
        # self.__range += [20]
        # self.__speed += [10]
        # x_max, y_max = 10000, 10000
        # self.__area += [[x_max, y_max]]
        # r = [[0, 0]]
        # direction = self.__RIGHT
        # while r[-1][0] < x_max or r[-1][1] < y_max and len(r) < 1000000:
        #     tmp = list(r[-1])
        #     if direction == self.__RIGHT:
        #         tmp[0] = x_max
        #     elif direction == self.__UP1 or direction == self.__UP2:
        #         tmp[1] += 2 * self.__range[-1]
        #     elif direction == self.__LEFT:
        #         tmp[0] = 0
        #     r.append(tmp)
        #     direction = (direction + 1) % 4
        # self.__route += [r]
        # self.__descriptor += ['sensores: ' + str(self.__nodes[-1]) + ', ' +
        #                       'área: (' + str(x_max) + ' x ' + str(y_max) + ') m², ' +
        #                       'velocidade: '+str(self.__speed[-1])+' m/s']

        # Fim de cenários

    def next(self):
        if self.__scenarios:
            self.current += 1
            # del self.__nodes[0]
            # del self.__range[0]
            # del self.__speed[0]
            # del self.__area[0]
            # del self.__route[0]
            # del self.__descriptor[0]
            # self.__scenarios -= 1

    @property
    def list_scenarios(self):
        table = '| Cenário | Sensores |          Área           | Velocidade |\n'
        for i in range(self.__scenarios):
            table += '| {:^7} | {:^8} | {:^11}x{:^11} | {:^10} |\n'.format(
                i+1, self.__nodes[i], self.__area[i][0], self.__area[i][1], self.__speed[i])
        return table

    @property
    def number_node(self):
        return self.__nodes[self.current]

    @property
    def trans_range(self):
        return self.__range[self.current]

    @property
    def speed_sink(self):
        return self.__speed[self.current]

    @property
    def size_area(self):
        return self.__area[self.current]

    @property
    def sink_route(self):
        return self.__route[self.current]

    @property
    def descriptor(self):
        return self.__descriptor[self.current]

    @property
    def scenarios(self):
        return self.__scenarios
