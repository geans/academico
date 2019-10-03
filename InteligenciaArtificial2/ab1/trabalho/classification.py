#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Use:
    python -W ignore classification.py

Requiriment:
    python -m pip install pandas
    python -m pip install -U scikit-learn
    
@author: Gean Santos <geans.santos@gmail.com>
"""
from pandas import read_csv, isna, concat
from sklearn.model_selection import train_test_split
from random import choice, randint
from threading import Thread, Event
from time import sleep
from enum import Enum
from atexit import register

# Classifier
from sklearn.neural_network import MLPClassifier

history = open('history.txt', 'w')

def close_file():
    try:
        history.close()
    except Exception:
        pass
        
def debug(value='', end='\n', to_file=True):
    DEBUG = True
    if DEBUG:
        print(value, end=end)
        if to_file:
            history.write(value)
            history.write(end)

        
class Status(Enum):
    alive = 1
    inactive = 2
    dead = 3
    
class Trainer(Thread):
    counter = 0
    max_population = 10
    borns = 0
    monster = 0
    duplicate = 0
    alive = True
    population = []
    trained = []
    map_id = {}
    parameter = [ 
                    [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,),
                        (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19,), (20,)
                    ]  # hidden_layer_sizes 
                    ,['identity', 'logistic', 'tanh', 'relu']  # activation
                    ,['lbfgs', 'sgd']  # solver
                    ,[0.1, 0.01, 0.001, 0.0001]  # learning_rate_init
                ]

    @staticmethod
    def generate_random_chromossome():
        return [choice(parameter) for parameter in Trainer.parameter]
    
    @staticmethod
    def generation_init(chromosomes):
        for chr in chromosomes:
            individual = Trainer.new_individual(chr)
            if not individual is None:
                individual.start()
            
    @staticmethod
    def generation_end():
        chr = []
        score = []
        population_size = 0
        for individual in Trainer.population:
            population_size += 1
            individual.status = Status.dead
            chr += [individual.chromosome]
            score += [individual.score]
        return chr, score, population_size
    
    @staticmethod
    def join_threads():
        for individual in Trainer.population:
            individual.join()
    
    @staticmethod
    def new_individual(chromosome):
        if len(Trainer.population) < (Trainer.max_population << 1):
            ind = Trainer(chromosome)
            Trainer.population += [ind]
            return ind
        return None
    
    def __init__(self, chromosome):
        Thread.__init__(self)
        self.status = Status.alive
        self.score = 0
        self.chromosome = chromosome
        self.classifier = MLPClassifier(
                                        hidden_layer_sizes = self.chromosome[0],
                                        activation = self.chromosome[1],
                                        solver = self.chromosome[2],
                                        learning_rate_init = self.chromosome[3],
                                        max_iter = 50
                                       )
        self.candidate = []
        self.last_generation = 0
        if str(chromosome) in Trainer.map_id:
            self.id = Trainer.map_id[str(chromosome)]
        else:
            Trainer.counter += 1
            self.id = Trainer.counter
            Trainer.map_id[str(chromosome)] = self.id
        
    def __str__(self):
        return str(self.chromosome)

    def apply_for_partner(self, candidate):
        self.candidate += [candidate]

    def fit(self):
        X, y = Validation.get_xy()
        
        try:
            self.classifier.fit(X,y)
        except Exception:
            Trainer.monster += 1
            self.status = Status.dead
            debug('[!] Indivíduo monstro detectado')
        
        score = Validation.score(self.classifier)
        if not score is None:
            self.score = score
        Trainer.trained += [self]
        debug('[!] Classificador de {} treinado, {}'.format(self.id, self.chromosome))

    def generate_children(self, pair):
        if len(self.chromosome) != len(pair.chromosome):
           return
        if self.chromosome == pair.chromosome:
            self.status = Status.dead
            self.score = 0
            try:
                Trainer.population.remove(self)
            except Exception as e:
                #debug(e)
                pass
            debug('[!] Indivíduo {} morto por ser duplicata de {}'.format(self.id, pair.id))
            return
        p_a = self.chromosome
        p_b = pair.chromosome
        pivot = randint(1, len(p_a)-1)
        c1 = p_a[:pivot] + p_b[pivot:]
        c2 = p_b[:pivot] + p_a[pivot:]

        # mutation
        for c in [c1, c2]:
            if randint(1,10) == 1:  # 10% of chance
                index = randint(0,len(Trainer.parameter)-1)
                c[index] = choice(Trainer.parameter[index])
            duplicate = None
            for ind in Trainer.population:
                if ind.chromosome == c:
                    duplicate = ind
                    break
            if not duplicate is None:
                Trainer.duplicate += 1
                debug('[!] {} e {} geraram duplicata de {}'.format(self.id, pair.id, duplicate.id))
            else:
                child = Trainer.new_individual(c)
                if not child is None:
                    child.start()
                    Trainer.borns += 1
                    debug('[!] {} nasceu de: {} e {}'.format(child.id, self.id, pair.id))
        
    def run(self):
        apply = False
        while self.status != Status.dead:
            if self.status == Status.alive:
                if self.last_generation < Environment.generation_counter or self.score == 0:
                    self.fit()
                    self.last_generation = Environment.generation_counter
                    apply = True
                if Environment.is_cross_time and len(Trainer.population) < (Trainer.max_population << 1):
                    for c in self.candidate:
                        if not c is None:
                            if c.score >= randint(1, 100):
                                self.generate_children(c)
                            else:
                                debug('[!] {} foi rejeitado por {}'.format(c.id, self.id))
                    self.candidate = []
                    if apply:
                        s = sorted(Trainer.population, key=lambda x: x.score, reverse=True)
                        for c in s[:len(Trainer.population) >> 1]:
                            if not c is self:
                                c.apply_for_partner(self)
                        apply = False
        try:
            Trainer.population.remove(self)
        except Exception:
            pass


class Validation:
    data = read_csv('lite_dataset.csv')
    features = list(data)[1:-1]
    y = data.type
    X = data[features]
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.5)

    @staticmethod
    def get_xy():
        return Validation.X_train, Validation.y_train

    @staticmethod
    def score(classifier):
        y_pred = classifier.predict(Validation.X_test)
        hit , total = 0, 0
        for real, predict in zip(Validation.y_test, y_pred):
            if real == predict: hit += 1
            total += 1
        return (hit * 100.0) / total


class Environment:
    validation_on = True
    is_cross_time = False
    generation_counter = 0


def main():
    Trainer.max_population = 5
    number_generations = 3

    chromosomes = []
    score = []
    p_sorted = []
    for i in range(Trainer.max_population):
        chromosomes += [Trainer.generate_random_chromossome()]

    population = []
    for i in range(number_generations):
        debug('[.] Início da generação {} de {}\n'.format(i+1, number_generations) )
        Trainer.trained = []
        Environment.generation_counter += 1
        
        Trainer.generation_init(chromosomes)
        
        debug('[*] Esperando {} classificadores serem treinados\n'.format(
            len(Trainer.population) - len(Trainer.trained)))
        while len(Trainer.population) - len(Trainer.trained) > 0:
            pass
        
        # Iniciando época de cruzamento
        Environment.is_cross_time = True
        sleep(2)
        Environment.is_cross_time = False
        # Fim da época de cruzamento
        
        debug('\n[*] Esperando {} classificadores serem treinados\n'.format(
            len(Trainer.population) - len(Trainer.trained)))
        while len(Trainer.population) - len(Trainer.trained) > 0:
            pass
            
        debug('\n[*] {:^2} {:^28} {:^9}'.format('ID','Cromossomo','Pontuação'))
        for ind in Trainer.population:
            debug('[*] {:2} {:28} {:9.1f}'.format(ind.id, str(ind.chromosome), ind.score))
        debug('')
            
        chromosomes, score, p_size = Trainer.generation_end()
        Trainer.join_threads()
        
        p_sorted = [(chr, scr) for chr, scr in sorted(zip(chromosomes, score), key=lambda pair: pair[1], reverse=True)]
        chromosomes = []
        for chr,_ in p_sorted:
            chromosomes += [ chr ]
        chromosomes = chromosomes[:Trainer.max_population]
        
        debug('----------------------------------------------------------')

    Environment.validation_on = False
    Environment.is_cross_time = False
    
    debug('\n##########################################################\n')
    debug('Nascimentos: {}'.format(Trainer.borns))
    debug('Duplicatas: {}'.format(Trainer.duplicate))
    debug('Monstros: {}'.format(Trainer.monster))
    
    debug('\n{:^2} {:^28} {:^9}'.format('ID', 'Cromossomo','Pontuação'))
    for chr, scr in p_sorted:
        debug('{:2} {:28} {:9.1f}'.format(Trainer.map_id[str(chr)], str(chr), scr))
    debug('')

register(close_file)
        
if __name__ == '__main__':
    main()
    history.close()