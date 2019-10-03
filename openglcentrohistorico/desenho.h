#ifndef DESENHISTA_H
#define DESENHISTA_H

#include <iostream>
using namespace std;
#include <GL/glut.h>
#include <cmath>
#include "SOIL.h"

#ifndef PI
#define PI 3.1415926535897932
#endif
#define NUMERO_DE_TEXTURAS 5
enum : unsigned int {piso_entrada, piso_interno, grama, parede_externa, porta};

/*
 * Classe com funções que desenham objetos
 */
class Desenho
{
public:
    Desenho (float proporcao = 5) : proporcao (proporcao) {
        glGenTextures(1, textura_id);
        /*
        carrega_texturas_arquivo ((char*)"imagens/piso_entrada.jpg", &(textura_id[piso_entrada]));
        carrega_texturas_arquivo ((char*)"imagens/piso_interno.jpg", &(textura_id[piso_interno]));
        carrega_texturas_arquivo ((char*)"imagens/grama.jpg", &(textura_id[grama]));
        carrega_texturas_arquivo ((char*)"imagens/parede_externa.jpg", &(textura_id[parede_externa]));
        carrega_texturas_arquivo ((char*)"imagens/porta.jpg", &(textura_id[porta]));
        */
    }
    void geraModelagem (float anguloPortaGaragem, float anguloPortaLateral);

private:
    GLuint textura_id[NUMERO_DE_TEXTURAS] = {0,1,2,3,4};
    void desenha_predio (float x, float y, float z, float anguloPortaGaragem, float anguloPortaLateral);
    void desenha_mesa (float x, float y, float z);
    void desenha_cadeira (float x, float y, float z);
    void desenha_quadro (float x, float y, float z);
    void desenha_computador (float x, float y, float z);
    void desenha_bancada (float x, float y, float z);
    void desenha_janela (float x, float y, float z);
    void carrega_texturas_arquivo (char *nomeArquivo, GLuint *textura);
    float proporcao;
};


 /*
  * Classe para aulixiar uso do OpenGL na implementação da classe Desenho
  */
class Desenha_gl
{
public:
    Desenha_gl (float pos_x, float pos_y, float pos_z, float _proporcao) :
        x (pos_x), y (pos_y), z (pos_z), proporcao (_proporcao)
    {textura_id = NULL;}
    ~Desenha_gl(){}
    void define_deslocamento (float _desloc_x, float _desloc_y, float _desloc_z) {
        desloc_x = x + proporcao * _desloc_x;
        desloc_y = y + proporcao * _desloc_y;
        desloc_z = z + proporcao * _desloc_z;
    }
    void define_escala (float _escala_x, float _escala_y, float _escala_z) {
        escala_x = _escala_x;
        escala_y = _escala_y;
        escala_z = _escala_z;
    }
    void define_rotacao (float _angulo, float vx, float vy, float vz) {
        angulo = _angulo;
        vetor_x = vx;
        vetor_y = vy;
        vetor_z = vz;
    }
    void desenha_cubo() {
        glPushMatrix();
        glEnable (GL_TEXTURE_GEN_S);
        glEnable (GL_TEXTURE_GEN_T);
        glTranslatef (desloc_x, desloc_y, desloc_z);
        glRotatef (angulo, vetor_x, vetor_y, vetor_z);
        glScalef (escala_x, escala_y, escala_z);
        /*
        if (textura_id != NULL)
            glBindTexture (GL_TEXTURE_2D, (GLuint) textura_id);
        */
        glutSolidCube (proporcao);
        glDisable (GL_TEXTURE_GEN_S);
        glDisable (GL_TEXTURE_GEN_T);
        glPopMatrix ();
    }
    void define_textura (GLint textura) {*textura_id = textura;}
    void remove_textura(){textura_id = NULL;}
private:
    float x, y, z, proporcao;
    float desloc_x, desloc_y, desloc_z;
    float escala_x, escala_y, escala_z;
    float angulo, vetor_x, vetor_y, vetor_z;
    GLuint *textura_id;
};

#endif