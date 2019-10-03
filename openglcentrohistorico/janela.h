#ifndef JANELA_H
#define JANELA_H

#include <cmath>
#include <iostream>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#include "desenho.h"
#include "SOIL.h"

#define PI 3.1415926535897932

class Janela {
public:
    Janela();
    void reajusteJanela (int largura, int altura);
    void exibir (void);
    void teclasEspeciais (int key, int x, int y);
    void teclado (unsigned char key, int x, int y);
private:
    void iluminacao ();
    float proporcao;
    Desenho desenhista; // coleção de funções que desenha os objetos
    bool fullscreenmode;
    float vetor_x, vetor_y, vetor_z; // vetor direção da câmera
    float x, y, z; // posição da câmera
    float deltaMove;
    float lateralMove;
    float deltaAngle;
    float verticalMove;
    float aberturaPorta;
    float aberturaPortaLateral;
    GLfloat ratio;
    float ambiente[3];
    bool comIluminacao;
};

#endif