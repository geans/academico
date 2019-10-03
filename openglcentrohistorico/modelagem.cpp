#include "desenho.h"

void Desenho::geraModelagem (float anguloPortaGaragem, float anguloPortaLateral) {
    // inicia organização da modelagem
    desenha_predio (0, 0, 0, anguloPortaGaragem, anguloPortaLateral);
    desenha_mesa (-proporcao*1.5, 0, -proporcao*5);
    desenha_mesa (0, 0, -proporcao*5);
    desenha_mesa (proporcao*1.5, 0, -proporcao*5);
    desenha_mesa (-proporcao*1.5, 0, -proporcao*3.5);
    desenha_mesa (0, 0, -proporcao*3.5);
    desenha_mesa (proporcao*1.5, 0, -proporcao*3.5);
    desenha_mesa (-proporcao*1.5, 0, -proporcao*2);
    desenha_mesa (0, 0, -proporcao*2);
    desenha_mesa (proporcao*1.5, 0, -proporcao*2);
    desenha_cadeira (-proporcao*1.5, 0, -proporcao*4.5);
    desenha_cadeira (0, 0, -proporcao*4.5);
    desenha_cadeira (proporcao*1.5, 0, -proporcao*4.5);
    desenha_cadeira (-proporcao*1.5, 0, -proporcao*3);
    desenha_cadeira (0, 0, -proporcao*3);
    desenha_cadeira (proporcao*1.5, 0, -proporcao*3);
    desenha_cadeira (-proporcao*1.5, 0, -proporcao*1.5);
    desenha_cadeira (0, 0, -proporcao*1.5);
    desenha_cadeira (proporcao*1.5, 0, -proporcao*1.5);
    desenha_quadro (0, 0.5, -proporcao*7.0+proporcao*0.05);
    desenha_bancada (-15, 0, -proporcao*7.0+4);
    desenha_bancada (-15, 0, -4);
}