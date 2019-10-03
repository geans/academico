#include "desenho.h"

void Desenho::desenha_cadeira (float pos_x, float pos_y, float pos_z) {
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);

    float cor_cadeira[3] = {0x27/256.0, 0x28/256.0, 0x22/256.0};
    float cadeira_comprimento_acento = 0.5;
    float cadeira_largura_acento = 0.5;
    float cadeira_espessura = 0.02;
    float perna_cadeira_altura = 0.5;
    float perna_cadeira_lado = 0.02;
    float encosto_cadeira_altura = 0.5;
    float encosto_cadeira_lagura = 0.5;

    // perna 1 da cadeira
    glColor3f ( cor_cadeira[0], cor_cadeira[1], cor_cadeira[2] );
    gl.define_deslocamento (cadeira_comprimento_acento/2 - perna_cadeira_lado, perna_cadeira_altura/2, cadeira_largura_acento/2 - perna_cadeira_lado);
    gl.define_escala (perna_cadeira_lado, perna_cadeira_altura, perna_cadeira_lado);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // perna 2 da cadeira
    gl.define_deslocamento (-cadeira_comprimento_acento/2 + perna_cadeira_lado, perna_cadeira_altura/2, cadeira_largura_acento/2 - perna_cadeira_lado);
    gl.define_escala (perna_cadeira_lado, perna_cadeira_altura, perna_cadeira_lado);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // perna 3 da cadeira
    gl.define_deslocamento (cadeira_comprimento_acento/2 - perna_cadeira_lado, perna_cadeira_altura/2, -cadeira_largura_acento/2 + perna_cadeira_lado);
    gl.define_escala (perna_cadeira_lado, perna_cadeira_altura, perna_cadeira_lado);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // perna 4 da cadeira
    gl.define_deslocamento (-cadeira_comprimento_acento/2 + perna_cadeira_lado, perna_cadeira_altura/2, -cadeira_largura_acento/2 + perna_cadeira_lado);
    gl.define_escala (perna_cadeira_lado, perna_cadeira_altura, perna_cadeira_lado);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // banco da cadeira
    gl.define_deslocamento (0, perna_cadeira_altura + cadeira_espessura/2, 0);
    gl.define_escala (cadeira_comprimento_acento, cadeira_espessura, cadeira_largura_acento);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // encosto da cadeira
    gl.define_deslocamento (0, perna_cadeira_altura + cadeira_espessura + encosto_cadeira_altura/2, cadeira_largura_acento/2);
    gl.define_escala (encosto_cadeira_lagura, encosto_cadeira_altura, cadeira_espessura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
}