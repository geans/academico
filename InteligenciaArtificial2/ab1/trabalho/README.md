# Atividade Avaliativa para composição da AB1

## Objetivo da atividade
*Trabalhar a metodologia e as técnicas para sistema multiagente*

## Requisitos

- Linguagem Python 3
- Biblioteca **pandas**: `python -m pip install pandas`
- Biblioteca **sklearn**: `python -m pip install -U scikit-learn`
    
## Mode de uso

- No diretório do programa, execute: `python -W ignore classification.py`

## Descrição dos agentes

Nesse trabalho, os agentes são responsáveis por treinar um classificador e definir seus parâmetros. Este classifica o molusco Abalone em três tipos: 1, 2 e 3. Por meio de processo evolutivo, os agentes cruzam seus parâmetros com os de outros agentes para gerar novos agentes.

Para cada interação entre os agente é escrito uma mensagem na tela iniciando a linha com **[!]**.

O ambiente descreve o número máximo de agentes, o número de gerações, e a geração atual. Cada agente executa o seguinte algorítmo em cada geração:

1. Obtem a base de treinamento
2. Treina o classificador
3. Submete o classificador para avaliação e obtem sua pontuação. A pontuação pode variar entre: 0 e 100
4. Efetua processo de cruzamento

### Interface

Esse sistema de agentes, possui três tipos de interação:

- Entre os agentes Treinadores (que treinam os classificadores)
- Entre um Treinador e o agente de Validação (que fornece a base de treinamento e avalia o classificador)
- Com o ambiente

**Entre os Treinadores**

A interface dessa interação é feita por chamada de função. As seguinte funções são utilizadas:

- *Trainer.population*: lista estática na qual os agentes são inseridos para serem localizados por outros agentes
- *score*: potuação do classificador do agente, utilizado os agentes classificarem uns aos outros.
- *apply_for_partner*: utilizado quando um agente quer candidatar-se a cruzamento com outro agente.

**Entre Treinador e Validação**

A classe *Validation* fornece duas funções para interação com os agentes Treinadores:

- *get_xy*: retorna duas listas, uma com os valores das caracteristicas e outra com a classificação da espécie.
- *score(classifier)*: o agente Treinador submete seu classificador como parâmetro e obtem a potuação dele: um valor entre 0 e 100.

**Ambiente**

O ambiente é uma classe (*Eviroment*) com dois atributos estáticos:

- *is_cross_time*: atributo booleano que se verdadeiro permite que os agentes façam o processo de cruzamento.
- *generate_counter*: valor inteiro que indica a geração atual.

## Descrição da base de dados

Esse conjunto de dados foi modificado a partir da base encontrada no [UCI Machine Learning Repository: Abalone Data Set](http://archive.ics.uci.edu/ml/datasets/Abalone).
Que foi originalmente utilizado no estudo Warwick J Nash, Tracy L Sellers, Simon R Talbot, Andrew J Cawthorn and Wes B Ford (1994) "The Population Biology of Abalone (Haliotis species) in Tasmania. I. Blacklip Abalone (H. rubra) from the North Coast and Islands of Bass Strait", Sea Fisheries Division, Technical Report No. 48 (ISSN 1034-3288).

A base consiste de informações de um molusco chamado Abalone, e o objetivo do classificador é identificar o tipo do exemplar (entre as classes I, II e III) utilizando as informações fornecidas e detalhadas a seguir.

#### Abalone
(Origem: [Wikipédia, a enciclopédia livre](https://pt.wikipedia.org/wiki/Abalone))
"Haliotis (popularmente conhecidos em português e inglês por abalone, também em inglês por ear shell ou ormer, em espanhol por oreja de mar e abulone, em francês por oreille de mer, em italiano por abaloni e em alemão por seeohren) é um gênero de moluscos gastrópodes marinhos da família Haliotidae e o único gênero catalogado desta família. Foi proposto por Linnaeus em 1758 e contém diversas espécies em águas costeiras de quase todo o mundo. Na gastronomia, o abalone é um molusco valorizado em países asiáticos. Suas dimensões variam de dois a trinta centímetros."

#### Atributos do dataset:
1. **Sex**: M, F e I (infantil)
2. **Length**: maior medida em mm da concha
3. **Diameter**: diametro em mm perpendicular a medida Length
4. **Height**: altura em mm com a carne dentro da concha
5. **Whole weight**: peso em gramas de toda a abalone
6. **Shucked weight**: peso em gramas da carne
7. **Viscera weight**: peso em gramas das víceras após escorrer
8. **Shell weight**: peso em gramas para a concha após estar seca
9. **Type**: variável de classe (1, 2 ou 3) para o abalone
