# Simulador de Escalonamento de Tarefa

## Requisito para execução do programa

Ter o interpretador Python 3 e utilizar o comando correspondente ao Python 3. Versão recomendada: 3.4.3

### Instalação do Python 3 no Ubuntu

Normalmente o python já é instalado por padrão na distribuição Ubuntu, onde o comando ```python``` 
executa a versão Python 2 e o comando ```python3``` executa a versão Python 3.

Caso não esteja instalado, abra um terminal e digite o seguinte comando:

```sudo apt-get install python3```

## Instruções para execução do programa

Navegue até o diretório  ```app``` que contem o arquivo ```tss_run.py``` e execute no terminal:  

```python tss_run.py [arg1] [arg2] [opções]```

Onde:

* **[arg1]**: é um arquivo com os dados dos processos
* **[arg2]**: é o nome da política de escalonamento conforme sigla definida; lista das siglas está disponível no arquivo  ```help.txt``` ou executando: ```python tss_run.py -h```
* **[opções]**: pode ser parâmetros adicionais; podem ser vistos no arquivo ```help.txt``` ou executando: ```python tss_run.py -h```

### Exemplo

Pode ser testado utilizando arquivos de entrada de exemplos que estam no diretório ```app/input_example```:

```python tss_run.py input_example/10.tasks rr```
