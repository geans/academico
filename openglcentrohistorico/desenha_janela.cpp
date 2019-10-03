#include "desenho.h"

void Desenho::desenha_janela (float pos_x, float pos_y, float pos_z) {
    float cor_janela[3] = {0x23/256.0, 0x36/256.0, 0x4f/256.0};
    float janela_largura = 0.15;
    float janela_comprimento = 1.0;
    float janela_altura = 3.0;
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);

    // janela
    glColor3f ( cor_janela[0], cor_janela[1], cor_janela[2] );
    gl.define_deslocamento (0, janela_altura / 2, 0);
    gl.define_escala (janela_comprimento, janela_altura, janela_largura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
}