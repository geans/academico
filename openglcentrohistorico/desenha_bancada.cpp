#include "desenho.h"

void Desenho::desenha_bancada (float pos_x, float pos_y, float pos_z) {
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);
    float corMadeira[3] = {0x5f/256.0, 0x1d/256.0, 0x07/256.0};
    float corMarmore[3] = {0x35/256.0, 0x35/256.0, 0x35/256.0};
    float mesaComp = 2.2;
    float mesaLargura = 1;
    float mesaEspessura = 0.07;
    float pernaMesaAltura = 0.82;
    float pernaMesaLado = 0.07;
    float mesaAltura = pernaMesaAltura + mesaEspessura / 2;
    float x, y, z;

    // duas pernas direitas
    x = mesaComp / 2 - pernaMesaLado / 2;
    y = pernaMesaAltura / 2;
    z = mesaLargura / 2 - pernaMesaLado / 2;
    glColor3f ( corMadeira[0], corMadeira[1], corMadeira[2] );
    gl.define_rotacao (0, 0, 0, 0);
    gl.define_escala (pernaMesaLado, pernaMesaAltura, pernaMesaLado);
    gl.define_deslocamento (x, y, -z);
    gl.desenha_cubo();
    gl.define_deslocamento (x, y,  z);
    gl.desenha_cubo();
    
    // duas pernas esquerdas
    gl.define_deslocamento (-x, y, -z);
    gl.desenha_cubo();
    gl.define_deslocamento (-x, y,  z);
    gl.desenha_cubo();

    // base horizontal
    x = 0;
    y = pernaMesaAltura - pernaMesaLado / 2;
    z = mesaLargura / 2 - pernaMesaLado / 2;
    gl.define_escala (mesaComp, pernaMesaLado, 0.03);
    gl.define_deslocamento (x, y, -z);
    gl.desenha_cubo(); // primeira base de maior comprimento
    gl.define_deslocamento (x, y,  z);
    gl.desenha_cubo(); // segunda base de maior comprimento
    y = 0.2;
    z = 0;
    gl.define_escala (mesaComp-pernaMesaLado/2, pernaMesaLado, 0.03);
    gl.define_deslocamento (x, y, z);
    gl.desenha_cubo(); // base próxima ao chão de maior comprimento
    x = mesaComp / 2 - pernaMesaLado / 2;
    y = pernaMesaAltura - pernaMesaLado / 2;
    z = 0;
    gl.define_escala (0.03, pernaMesaLado, mesaLargura);
    gl.define_deslocamento (-x, y, -z);
    gl.desenha_cubo(); // primeira base de menor comprimento
    gl.define_deslocamento ( x, y, -z);
    gl.desenha_cubo(); // segunda base de menor comprimento
    y = 0.2;
    gl.define_deslocamento (-x, y, -z);
    gl.desenha_cubo(); // primeira base próxima ao chão de menor comprimento
    gl.define_deslocamento ( x, y, -z);
    gl.desenha_cubo(); // segunda base próxima ao chão de menor comprimento
    
    // tampo da mesa
    glColor3f (corMarmore[0], corMarmore[1], corMarmore[2]);
    gl.define_deslocamento (0, mesaAltura, 0);
    gl.define_escala (mesaComp, mesaEspessura, mesaLargura);
    gl.desenha_cubo();

    // borda ao redor do tampo
    glColor3f ( corMadeira[0], corMadeira[1], corMadeira[2] );
    z = (mesaLargura+0.03) / 2;
    gl.define_escala (mesaComp+0.03, mesaEspessura, 0.03);
    gl.define_deslocamento (0, mesaAltura, -z);
    gl.desenha_cubo(); // borda de comprimento maior
    gl.define_deslocamento (0, mesaAltura,  z);
    gl.desenha_cubo(); // borda de comprimento maior
    x = mesaComp/2;
    gl.define_escala (0.03, mesaEspessura, mesaLargura);
    gl.define_deslocamento (-x, mesaAltura, 0);
    gl.desenha_cubo(); // borda de comprimento menor
    gl.define_deslocamento ( x, mesaAltura, 0);
    gl.desenha_cubo(); // borda de comprimento menor
}