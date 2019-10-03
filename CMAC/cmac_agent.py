from random import random, randint
# from numpy import *
# from numpy.random import *
import numpy


class PongConfig:
    def __init__(self, width=64, height=48, speed=.75):
        self.w = width
        self.h = height
        self.s = speed


class CmacAgent:
    def __init__(self, action_set, learning_ratio=0.01, gama=0.8, epsilon=0.01,
        nlevels=32):
        self.action_set = action_set
        self.learning_ratio = learning_ratio
        self.gama = gama
        self.epsilon = epsilon
        self.nlevels = nlevels
        #self.coords = self.__create_coord_space_state()
        self.weights = {}

    def pick_action(self, state):
        best_a = None
        best_r = -99999
        for a in self.action_set:
            prediction = self.__peek_prediction(state, a)[0]
            if prediction > best_r:
                best_a = a
                best_r = prediction

        if best_a == 0:
            best_a = None
        return best_a

    def update_q_function(self, state, action, reward, next_state):
        q, coords = self.__peek_prediction(state, action)
        _q = self.__peek_prediction(next_state, action)[0]
        for a in self.action_set:
            prediction = self.__peek_prediction(state, a)[0]
            if prediction > _q:
                _q = prediction
        new_q = q + self.learning_ratio * (reward + self.gama * (_q - q))
        for pt in coords:
            self.weights[pt] = new_q 


    def __peek_prediction(self, state, action):  # q value
        vd = abs(int(state['ball_y']) - int(state['player_y']))
        vds = 1 if int(state['ball_y']) - int(state['player_y']) > 0 else 0
        hd = int(state['ball_x'])
        bvx = 1 if int(state['ball_velocity_x']) > 0 else 0
        if action == None:
            action = 0
        point = numpy.array([vd, vds, hd, bvx, action])
        point = (point/0.01).astype(int)
        coords = []
        for i in range(self.nlevels):  # Each 'i' is a tiling
            tile_point = list(point - (point - i) % self.nlevels)
            tile_point += [i]
            coords.append( tuple(tile_point) )
        prediction = sum([self.weights.setdefault(pt, 0.0) for pt in coords])
        return prediction, coords
