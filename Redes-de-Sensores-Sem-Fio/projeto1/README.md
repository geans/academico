# RSSF #

Implementação de uma simulação de Rede de Sensores Sem Fio com Sink móvel.

## Requisitos ##

* Python 3

**Opcional:**
* PyCharm Community Edition 2016.2
  * Abrir diretório `main/source`

## Como Executar ##

1. Navegar para diretório `main/source`;
2. Executar arquivo `__init__.py`:
  
```
.../RSSF/main/source $ python3 __init__.py
```

## Classes ##

* **Node**
* **Sink**
* **Environment**
* **Simulator**
* **Parameter**

## Descrição ##

1. Distribuir nós aleatoriamente em uma área de tamanho pre-determinado.
2. Definir rota e velocidade em m/s do *sink* móvel.
3. Utilizar *onehop* (único salto) para transmissão entre um nó e o *sink*.
4. Em cada transmissão é transmitido 1 pacote.
5. Cada pacote precisa de 1 segundo para ser transmitido
6. Utilizar classe *Environment* para ter os dados de todos os nós e do *sink*.
7. Utilizar classe *Simulator* para marcar o tempo, definir os parâmetros e obter os dados.
8. Utilizar classe *Parameter* para descrever os parâmetros.
