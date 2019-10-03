#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
from random import randint
import requests
import sys


class Individuo:
    def __init__(self, cromossomo):
        if len(cromossomo) != 6:
            raise Exception('"cromossomo" deve ter 6 elementos')
        self.crom = cromossomo
        
        self.url = 'http://localhost:8080/antenna/simulate?'+\
        'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(
            self.crom[0],self.crom[1],self.crom[2],
            self.crom[3],self.crom[4],self.crom[5])
        r = requests.post(url = self.url)
        self.ganho = float(r.text.split()[0])
        
        self.oficial_url = 'https://aydanomachado.com/mlclass/02_Optimization.php?'+\
        'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}&dev_key={}'.format(
            self.crom[0],self.crom[1],self.crom[2],
            self.crom[3],self.crom[4],self.crom[5], 'Equipe%20K')

    def __gt__(self, other):
        return self.ganho > other.ganho

    def __lt__(self, other):
        return self.ganho < other.ganho

def mutacao(cromossomo):
    i1 = randint(0,5)
    cromossomo[i1] = randint(0,359)

def gerar_nova_populacao(num=8):
    populacao = []
    for i in range(num):
        cromossomo = []
        for i in range(6):
            cromossomo += [randint(0,359)]
        populacao += [Individuo(cromossomo)]
    return populacao

def gerar_filhos(pai, mae):
    # Cruzamento
    crom_pai = pai.crom
    crom_mae = mae.crom
    c1 = crom_pai[:2] + crom_mae[2:]
    c2 = crom_mae[:2] + crom_pai[2:]
    c3 = crom_pai[:4] + crom_mae[4:]
    c4 = crom_mae[:4] + crom_pai[4:]
    c5 = crom_pai[:2] + crom_mae[2:4] + crom_pai[4:]
    c6 = crom_mae[:2] + crom_pai[2:4] + crom_mae[4:]
    
    # Aplica mutações em todos indivíduos
    mutacao(c1);mutacao(c2);mutacao(c3)
    mutacao(c4);mutacao(c5);mutacao(c6)
    
    # nova população
    return [Individuo(crom_pai),
            Individuo(crom_mae),
            Individuo(c1),
            Individuo(c2),
            Individuo(c3),
            Individuo(c4),
            Individuo(c5),
            Individuo(c6)]

def run():
    if len(sys.argv) < 2:
        print('Modo de uso: {} <numero de geracoes>'.format(sys.argv[0]))
        exit()
    n_geracoes = int(sys.argv[1])

    # Inicia população
    populacao = gerar_nova_populacao()

    melhor = populacao[0]
    p = 0
    out = ''
    for i in range(n_geracoes):
        # Seleção dos dois melhores indivíduos
        pai = max(populacao)
        populacao.remove(pai)
        mae = max(populacao)

        if melhor < pai:
            melhor = pai

        populacao = gerar_filhos(pai, mae)
        populacao += gerar_nova_populacao()
        
        s = (i+1)*100.0/n_geracoes
        diff = int(s-p)
        if diff > 1:
            for i in range(diff>>1):
                out += '#'
            print(' {:5.2f} [{:.<50}] {:5.2f}%'.format(melhor.ganho, out, s), end='\r', flush=True)
            p += diff
        elif s > p:
            print(' {:5.2f} [{:.<50}] {:5.2f}%'.format(melhor.ganho, out, s), end='\r', flush=True)
    
    print('\n\n  Melhor resultado:')
    print('{}   {}'.format('Ganho', 'Cromossomo'))
    print('{:.2f}   {}'.format(melhor.ganho, melhor.crom))
    print('\n{}'.format(melhor.oficial_url))

if __name__ == "__main__":
    run()