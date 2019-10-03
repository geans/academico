#include "desenho.h"

void Desenho::desenha_mesa (float pos_x, float pos_y, float pos_z) {
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);
    float cor_mesa[3] = {0x56/256.0, 0x56/256.0, 0x56/256.0};
    float cor_mesa_pernas[3] = {0x27/256.0, 0x28/256.0, 0x22/256.0};
    float mesa_comprimento = 1;
    float mesa_largura = 0.5;
    float mesa_espessura = 0.05;
    float perna_mesa_altura = 0.7;
    float perna_mesa_lado = 0.05;
    float perna_mesa_largura = 0.1;
    float mesa_altura = perna_mesa_altura + mesa_espessura / 2;

    // perna direita
    glColor3f ( cor_mesa_pernas[0], cor_mesa_pernas[1], cor_mesa_pernas[2] );
    gl.define_deslocamento (mesa_comprimento / 2 - perna_mesa_lado, perna_mesa_altura / 2, -perna_mesa_largura);
    gl.define_escala (perna_mesa_lado, perna_mesa_altura, perna_mesa_largura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    // base
    gl.define_deslocamento (mesa_comprimento / 2 - perna_mesa_lado, perna_mesa_lado / 2, 0);
    gl.define_escala (perna_mesa_lado + 0.01, perna_mesa_lado, mesa_largura);
    gl.desenha_cubo();
    
    // perna esquerda
    gl.define_deslocamento (-mesa_comprimento / 2 + perna_mesa_lado, perna_mesa_altura/2, -perna_mesa_largura);
    gl.define_escala (perna_mesa_lado, perna_mesa_altura, perna_mesa_largura);
    gl.desenha_cubo();
    // base
    gl.define_deslocamento (-mesa_comprimento / 2 + perna_mesa_lado, perna_mesa_lado / 2, 0);
    gl.define_escala (perna_mesa_lado + 0.01, perna_mesa_lado, mesa_largura);
    gl.desenha_cubo();
    
    // tampo da mesa
    glColor3f (cor_mesa[0], cor_mesa[1], cor_mesa[2]);
    gl.define_deslocamento (0, mesa_altura, 0);
    gl.define_escala (mesa_comprimento, mesa_espessura, mesa_largura);
    gl.desenha_cubo();
}