#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
from threading import Thread
from random import randint
import requests
import sys

def debug(value):
    f = open('debug.txt', 'a')
    f.write(value)
    f.write('\n')
    f.close()

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
        try:
            self.ganho = float(r.text.split()[0])
        except Exception as e:
            debug(str(e))
            self.ganho = 0

    def __gt__(self, other):
        return self.ganho > other.ganho

    def __lt__(self, other):
        return self.ganho < other.ganho

class Enconsta(Thread):
    populacao = []
    progresso = []
    melhor = 0

    def __init__(self, ciclos, id, largura_passo):
        Thread.__init__(self)
        self.id = id
        cromossomo = []
        for i in range(6):
            cromossomo += [randint(0,359)]
        self.individuo = Individuo(cromossomo)
        self.ciclos = ciclos  # limite de tempo
        self.i = 0
        self.passo = largura_passo

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
        
    def procura_sucessor(self):
        crom_atual = self.individuo.crom
        sucessores = []
        for i in range(6):
            crom = list(crom_atual)  # copy
            crom[i] += self.passo
            sucessores += [Individuo(crom)]
        for i in range(6):
            crom = list(crom_atual)  # copy
            crom[i] -= self.passo
            sucessores += [Individuo(crom)]
        return max(sucessores)

    def run(self):
        i = 0
        for i in range(self.ciclos):
            sucessor = self.procura_sucessor()
            if self.individuo < sucessor:
                self.individuo = sucessor
            else:
                break
            if Enconsta.melhor < self.individuo.ganho:
                Enconsta.melhor = self.individuo.ganho
            Enconsta.progresso += [True]
        for j in range(self.ciclos - i):
            Enconsta.progresso += [True]
        Enconsta.populacao += [self.individuo]

        
class Progresso(Thread):
    def __init__(self, tam_progresso):
        Thread.__init__(self)
        self.t = tam_progresso
    def run(self):
        # Impressão de progresso
        p=0
        out = ''
        while len(Enconsta.progresso) < self.t:
            s = len(Enconsta.progresso)*100.0/self.t
            diff = int(s-p)
            if diff > 1:
                for i in range(diff>>1):
                    out += '#'
                print(' {:5.2f} [{:.<50}] {:5.2f}%'.format(Enconsta.melhor, out, s), end='\r', flush=True)
                p += diff
        print('')

def run():
    argv = sys.argv
    if len(argv) < 3:
        print('Modo de uso: {} <tam_população> <num_ciclos> [<largura_passo>]'.format(argv[0]))
        exit()
    try:
        tam_população = int(argv[1])
        num_ciclos = int(argv[2])
        if len(argv) >= 4:
            l_passo = int(argv[3])
        else:
            l_passo = 20
    except:
        print('Argumento inválido: informar números inteiros.')
        exit()
    if tam_população < 0:
        tam_população = -tam_população
    tam_progresso = tam_população * num_ciclos
    p = Progresso(tam_progresso)
    p.start()
    threads = []
    for i in range(tam_população):
        t = Enconsta(num_ciclos, i, l_passo)
        t.start()
        threads += [t]

    for t in threads:
        t.join()
    p.join()
    if len(Enconsta.populacao) <= 0:
        debug('População vazia')
        return
    melhor = max(Enconsta.populacao)
    myprint('\nMelhor: {} \nURL: {}'.format(melhor.ganho, melhor.oficial_url))


if __name__ == "__main__":
    run()
