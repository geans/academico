<p align="center">
Universidade Federal de Alagoas</br>
Instituto de Computação</br>
</p>

# Trabalho Prático AB2

Disciplina: Sistemas Operacionais  
Semestre letivo: 2015.1  
Professor: André Lage Freitas  
Aluno: Gean da Silva Santos  

## Objetivo

O trabalho consiste em simular o escalonamento de um conjunto de tarefas usando algoritmos de escalonamento [1].

## Como executar o programa

Vide arquivo INSTALL.md

## Funcionalidade mínima

O programa desenvolvido cumpre as funcionalidades mínimas requeridas que é simular um escalonamento de um conjunto de tarefas usando os seguintes algoritmos de escalonamento de tarefas:

* **FCFS (First Come, First Served):** as tarefas são ordenadas por ordem de chegada numa fila de prontos para ter acesso ao processador e cada uma ocupa o processador até ser terminada.
* **Round-Robin com quantum de 2s:** as tarefas também são ordenadas por ordem de chegada, mas, se passar 2 segundos e a tareda não fora terminada, ela sai do processador dando lugar à próxima tarefa e segue para o fim da fila de prontos.

E segue o formato de entrada pedido que contém, no mínimo, dois parâmetros de entrada:

* ```arg1```: o primeiro parâmetro de entrada é um arquivo contendo os dados dos processos
* ```arg2```: o segundo parâmetro de entrada é a política de escalonamento de tarefas

O arquivo contendo os dados dos processos (```arg1```) é dividido da seguinte forma e pode conter mais de nove processos: cada linha da entrada corresponde a um processo com os seguintes dados fornecidos como inteiros separados por um ou mais espaços em branco:

* data de criação;
* duração em segundos;
* prioridade estática (escala de prioridades positiva).

A saída do programa produz um diagrama de tempo de execução e é gravado em arquivo com nome: ```output```. O diagrama de tempo de cada execução é gerado na vertical, de cima para baixo (uma linha por segundo), conforme mostra o exemplo a seguir para um escalonamento Round-Robin:

```
tempo	P1	P2	P3	P4
 0- 1	--	##	  	  
 1- 2	--	##	--	  
 2- 3	##	  	--	  
 3- 4	##	  	--	--
 4- 5	--	  	##	--
 5- 6	--	  	##	--
 6- 7	--	  	--	##
 7- 8	--	  	--	##
 8- 9	##	  	--	--
 9-10	##	  	--	--
10-11	--	  	##	--
11-12	--	  	##	--
12-13	--	  	  	##
13-14	##	  	  	  
```

Para o seguinte conteúdo do arquivo de entrada:

```
0 5 2
0 2 3
3 3 4
1 4 1
```

## Funcionalidade extra

O programa tem como funcionalidades adicionais a implemetação de mais algoritmos de escalonamento de tarefas e o suporte a mais parâmentro.

Nota: para qualquer política de escalonamento, o simulador escolhe primeiro a tarefa de maior prioridade caso tenham mesma data de criação.

### Algoritmos adicionais

* **rrta** (Round-Robin with Task Aging): implementa revesamento a cada 2 segundos como o Round-Robin, mas a fila de prontos é ordenada por prioridade, considerando maior prioridade, e as tarefas mais antigas têm sua prioridade aumentada com o passar do tempo (evelhecimento de tarefa); o surgemento de tarefas de maior prioridade não interrompe a tarefa em execução.
* **sjf** (Shortest Job First): executa primeiro a que tem menor duração, ou seja, a fila de prontos é ordenada de acordo com o tempo necessário para cada tarefa ser terminada, esta política é não preemptiva.
* **pwp** (Priority Without Preemption): a ordem de execução segue unicamente a maior prioridade, contudo essa política não interrompe a tarefa em execução.
* **pp** (Priority Preemption): a ordem de execução segue unicamente a maior prioridade e essa política interrompe a tarefa em execução caso haja uma tarefa de maior prioridade chegndo à fila de prontos.

### Parâmetros adicionais

* **```-c=<integer> or --cores=<integer>```:** Defini o número de núcleos no processado; isso possibilida a execução de mais de uma tarefa por vez.
* **```-q=<integer> or --quantum=<integer>```:** Defini o tamanho do quantum para as políticas do tipo Round-Robin, isto é, o tempo em segundos que irá durar o quantum.
* **```-s or --stage```:** Mostra os passos da execução no terminal com pausas de um segundo.
* **```-d or --debug```:** Mostra os passos da execução no terminal sem pausas.
* **```-h or --help```:** Mostra a mensagem de ajuda e sai do programa.

### Relatório de métricas

Além do arquivo de saída principal (```output```) que contém o diagrama de execução, é gravado em um arquivo chamado ```report``` o cálculo das seguintes métricas:

* **Porcentagem de uso do processador:** calcula quantos segundos cada tarefa utilizou o processador e divide pelo tempo que o processador está "ligado", isto é, o tempo do início ao fim da simulação. Como o programa permite definir o número de núcleos no processador, esse calculo também é dividido pelo número de núcleos.
* **Média do tempo de resposta:** soma as diferenças do tempo de criação e de término, e divide pelo número de tarefas (processos), isto é: 
<p align="center">```média = [(término de P1 - criação de P1) + (término de P2 - criação de P2) + ...] / número de tarefas```
</p>
Mostra ainda o tempo mínimo para essa média, ou seja, o tempo ótimo de resposta.
* **Média do tempo de espera:** soma o tempo em que cada tarefa passo na fila de prontos e divide pelo número de tarefas:
<p align="center">```média = [(tempo em espera de P1) + (tempo em espera de P2) + ...] / número de tarefas```
</p>

## Referências

[1] Maziero, Carlos A. [Algoritmos de escalonamento](http://wiki.inf.ufpr.br/maziero/doku.php?id=so:algoritmos_de_escalonamento)  

[2] Maziero, Carlos A. [Sistemas Operacionais: Conceitos e Mecanismos](http://wiki.inf.ufpr.br/maziero/lib/exe/fetch.php?media=so:so-livro.pdf). 2013.  

## Disclaimer

O material base desse trabalho foi elaborado pelo [Prof. André Lage Freitas](https://sites.google.com/a/ic.ufal.br/andrelage/) e foi baseado no projeto Algoritmos de Escalonamento da [disciplina IF66D](http://dainf.ct.utfpr.edu.br/~maziero/doku.php/so:algoritmos_de_escalonamento) (DAINF-UFTPR), de autoria do Prof. Maziero, que está licenciado sob a licença [Creative Commons BY-NC-SA](http://creativecommons.org/licenses/by-nc-sa/3.0/br/). 
