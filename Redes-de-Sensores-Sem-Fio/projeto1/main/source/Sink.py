from math import ceil

DEBUG_SINK = False


def debug(value):
    if DEBUG_SINK:
        print('\t\t<', value, '>', sep='')


def sqrt(value):
    return int(value) ** (1 / 2)


class Sink:
    # atributos estaticos
    count = 0

    def __init__(self, init_position, speed, target_position):
        """
        :type init_position: a list of two numbers
        :type speed: a number
        :type target_position: a list of two numbers
        """
        self.__id = Sink.count
        Sink.count += 1
        self.__position = init_position
        self.__speed = speed
        self.__x_target = target_position[0]
        self.__y_target = target_position[1]
        self.__in_target = False

    def reached_target(self):
        current_x, current_y = self.__position
        x = self.__x_target - current_x
        y = self.__y_target - current_y
        debug('x, y = '+str((x, y)))
        distance = sqrt(x ** 2 + y ** 2)

        if distance:
            x_move = (x * self.__speed) / distance
            y_move = (y * self.__speed) / distance
            if -1 < x_move < 0:
                x_move = -1
            if -1 < y_move < 0:
                y_move = -1
            x_move = ceil(x_move)
            y_move = ceil(y_move)
        else:
            x_move = 1
            y_move = 1
        if x >= 0:
            # correction to reached exactly on target to x > 0
            if current_x + x_move > self.__x_target:
                x_move = self.__x_target - current_x
        else:
            # correction to reached exactly on target to x < 0
            if current_x + x_move < self.__x_target:
                x_move = current_x - self.__x_target
        # correction to reached exactly on target
        if current_y + y_move > self.__y_target:
            y_move = self.__y_target - current_y
        self.__position[0] += x_move
        self.__position[1] += y_move

        # check if position exactly on target
        if self.__position[0] == self.__x_target and self.__position[1] == self.__y_target:
            self.__in_target = True
        else:
            self.__in_target = False

        debug('Posição sink: ' + str(self.__position))
        debug('Posição alvo: ' + str([self.__x_target, self.__y_target]))
        debug('Alvo alcançado? ' + str(self.__in_target))

    def update_target(self, new_target):
        self.__x_target = new_target[0]
        self.__y_target = new_target[1]

    @property
    def id(self):
        return self.__id

    @property
    def in_target(self):
        return self.__in_target

    @property
    def position(self):
        return self.__position
