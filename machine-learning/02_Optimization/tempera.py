#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
from threading import Thread
from random import randint
import requests
import sys

def myprint(value):
    print(value)
    f = open('output.txt', 'a')
    f.write(value)
    f.write('\n')
    f.close()

class Individuo:
    def __init__(self, cromossomo):
        if len(cromossomo) != 6:
            raise Exception('"cromossomo" deve ter 6 elementos')
        self.crom = cromossomo
        self.calc_ganho()        
        self.oficial_url = 'https://aydanomachado.com/mlclass/02_Optimization.php?'+\
        'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}&dev_key={}'.format(
            self.crom[0],self.crom[1],self.crom[2],
            self.crom[3],self.crom[4],self.crom[5], 'Equipe%20K')

    def calc_ganho(self):
        self.url = 'http://localhost:8080/antenna/simulate?'+\
        'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(
            self.crom[0],self.crom[1],self.crom[2],
            self.crom[3],self.crom[4],self.crom[5])
        r = requests.post(url = self.url)
        self.ganho = float(r.text.split()[0])

    def __gt__(self, other):
        return self.ganho > other.ganho

    def __lt__(self, other):
        return self.ganho < other.ganho

class Tempera(Thread):
    populacao = []
    progresso = []
    melhor = 0

    def __init__(self, ciclos, id):
        Thread.__init__(self)
        self.id = id
        cromossomo = []
        for i in range(6):
            cromossomo += [randint(0,359)]
        self.individuo = Individuo(cromossomo)
        self.ciclos = ciclos
        self.i = 0

    def move(self):
        passo = randint(-30,30)
        crom = list(self.individuo.crom)  # copy
        i = self.i
        crom[i] += passo
        if crom[i] < 0:
            crom[i] += 360
        if crom[i] > 359:
            crom[i] -= 360
        return crom

    def run(self):
        for i in range(self.ciclos):
            g_atual = self.individuo.ganho
            novo_crom = self.move()
            novo_individuo = Individuo(novo_crom)
            if g_atual < novo_individuo.ganho:
                self.individuo = novo_individuo
            else:
                # tenta mudar outro índice
                self.i = (self.i + 1) % 6  # max posições no cromossomo
            Tempera.progresso += [True]
            if Tempera.melhor < self.individuo.ganho:
                Tempera.melhor = self.individuo.ganho
        Tempera.populacao += [self.individuo]

        
class Progresso(Thread):
    def __init__(self, tam_progresso):
        Thread.__init__(self)
        self.t = tam_progresso
    def run(self):
        # Impressão de progresso
        p=0
        out = ''
        while len(Tempera.progresso) < self.t:
            s = len(Tempera.progresso)*100/self.t
            diff = int(s-p)
            if diff > 1:
                for i in range(diff>>1):
                    out += '#'
                print(' {: 2.2f} [{:.<50}] {: 2.2f}%'.format(Tempera.melhor, out, s), end='\r', flush=True)
                p += diff
        print('')

def run():
    argv = sys.argv
    if len(argv) < 3:
        print('Modo de uso: {} <tam_população> <num_ciclos>'.format(argv[0]))
        exit()
    try:
        tam_população = int(argv[1])
        num_ciclos = int(argv[2])
    except:
        print('Argumento inválido: informar números inteiros.')
        exit()
    tam_progresso = tam_população * num_ciclos
    if tam_progresso < 0:
        tam_progresso = -tam_progresso
    p = Progresso(tam_progresso)
    p.start()
    threads = []
    for i in range(tam_população):
        t = Tempera(num_ciclos, i)
        t.start()
        threads += [t]

    for t in threads:
        t.join()
    p.join()
    if len(Tempera.populacao) <= 0:
        debug('População vazia')
        return
    melhor = max(Tempera.populacao)
    myprint('\nMelhor: {} \nURL: {}'.format(melhor.ganho, melhor.oficial_url))


if __name__ == "__main__":
    run()
