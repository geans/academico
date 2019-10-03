#include "desenho.h"

void Desenho::desenha_quadro (float pos_x, float pos_y, float pos_z) {
    float cor_quadro[3] = {1, 1, 1};
    float cor_borda[3] = {0.6, 0.6, 0.6};
    float quadro_espessura = 0.03;
    float quadro_comprimento = 3.0;
    float quadro_altura = 1.25;
    float altura_meio_quadro = (quadro_altura / 2) + 1;
    float borda_largura = 0.05;
    float borda_espessura = quadro_espessura + 0.01;
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);

    // quadro
    glColor3f ( cor_quadro[0], cor_quadro[1], cor_quadro[2] );
    gl.define_deslocamento (0, altura_meio_quadro, 0);
    gl.define_escala (quadro_comprimento, quadro_altura, quadro_espessura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // bordas do quadro
    glColor3f ( cor_borda[0], cor_borda[1], cor_borda[2] );
    /// superior
    gl.define_deslocamento (0, quadro_altura + 1, 0);
    gl.define_escala (quadro_comprimento + borda_largura, borda_largura, borda_espessura);
    gl.desenha_cubo();
    /// inferior
    gl.define_deslocamento (0, 1, 0);
    gl.define_escala (quadro_comprimento + borda_largura, borda_largura, borda_espessura);
    gl.desenha_cubo();
    /// esquerda
    gl.define_deslocamento (-quadro_comprimento/2, altura_meio_quadro, 0);
    gl.define_escala (borda_largura, quadro_altura, borda_espessura);
    gl.desenha_cubo();
    /// direita
    gl.define_deslocamento ( quadro_comprimento/2, altura_meio_quadro, 0);
    gl.define_escala (borda_largura, quadro_altura, borda_espessura);
    gl.desenha_cubo();
}