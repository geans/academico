Projeto Computação Gráfica
==========================

Turma 2015.2
Professor Marcelo  
Alunos: Gean Santos

Modelagem de Centro Histórico com OpenGL
----------------------------------------

## Compilação

Utilize comando `make` para executa o arquivo `Makefile` para compilar e executar o código.

## Comandos:

* **w/W:** move para frente.
* **s/S:** move para trás.
* **a/A:** move para esquerda.
* **d/D:** move para direita.
* **Seta para esquerda:** vira para esquerda.
* **Seta para direita:** vira para direita.
* **Seta para cima:** "olhar para cima".
* **Seta para baixo:** "olhar para baixo".
* **r/R:** subir.
* **f/F:** descer.
* **o/O:** abrir porta da garagem.
* **p/P:** fechar porta da garagem.
* **k/K:** abrir porta do predio..
* **l/L:** fechar porta do predio..
* **1:** centralizar visão vertical ("olhar para frente").
* **ESC:** habilita/desabilita modo de tela cheia.

## Requisitos Plataforma GNU/Linux

1. **Compilador C++:** `sudo apt-get install g++`
2. **Biblioteca OpenGL:** `sudo apt-get install freeglut3 freeglut3-dev binutils-gold`
3. `Make` (construtor automático) para execução do arquivo MakeFile (opcional): `sudo apt-get install make`

Observações:

* **Bibliotecas:** `-lglut -lGL -lGLU`.
* Mais detalhes ver arquivo `Makefile`.
* Bibliotecas `-lSOIL` e `-lpthread` não utilizada;
  * Biblioteca `-lSOIL`: `sudo apt-get install libsoil-dev`, carregamento de imagens para textura.
  * Biblioteca `-lpthread`: instalada por parão no linux, utilizado para fazer sombras com textura.

## Requisitos Plataforma Windows / MAC

Não Avaliada.
