#include "desenho.h"

void Desenho::desenha_predio (float pos_x, float pos_y, float pos_z, float aberturaPorta = 0, float aberturaPortaLateral = 0) {
    Desenha_gl gl (pos_x, pos_y, pos_z, proporcao);

    // variáveis auxiliares de posição
    float x, y, z;

    float corParede[3] = {0xa3/256.0, 0x90/256.0, 0x7f/256.0};
    float corPortao[3] = {0x23/256.0, 0x36/256.0, 0x4f/256.0};
    float corTelhado[3] = {0x61/256.0, 0x2c/256.0, 0x1c/256.0};
    
    float paredeLargura = 0.1;
    float frontalComp = 15.0, frontalAltura = 6.5;
    float lateralComp = 7.0, lateralAltura = 5.0;
    float entradaGaragemAltura = 2.7;
    float entradaGaragemLargura = 4;
    float portaoGaragemAltura = 2.2;
    float portaoGaragemLargura = 1;
    float portaoGaragemEspessura = 0.05;
    float portaLateralAltura = 2;
    float portaLateralLargura = 1;
    float portaLateralEspessura = 0.03;

    // inicia a composicao do predio

    // Desenha chão
    glColor3f (0.0, 0.29, 0.0);
    glBegin (GL_QUADS);
        glVertex3f (-10000, 0, -10000);
        glVertex3f (-10000, 0,  10000);
        glVertex3f ( 10000, 0,  10000);
        glVertex3f ( 10000, 0, -10000);
    glEnd();
    // Desenha chão no interior do prédio
    glColor3f (0.8, 0.8, 0.8);
    glBegin (GL_QUADS);
        x = proporcao * frontalComp / 2;
        z = proporcao * lateralComp;
        y = 0.05;
        glVertex3f (-x, y, -z);
        glVertex3f (-x, y,  0);
        glVertex3f ( x, y,  0);
        glVertex3f ( x, y, -z);
    glEnd();
    // Desenha forro no interior do prédio
    glColor3f ( corParede[0], corParede[1], corParede[2] );
    glBegin (GL_QUADS);
        y = proporcao * (lateralAltura - 0.1);
        glVertex3f (-x, y,  0);
        glVertex3f (-x, y, -z);
        glVertex3f ( x, y, -z);
        glVertex3f ( x, y,  0);
    glEnd();
    
    // parede frontal
    gl.define_deslocamento (0, frontalAltura / 2, 0);
    gl.define_escala (frontalComp + paredeLargura, frontalAltura, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    // desenha janelas
    desenha_janela (0, proporcao * 1.5, 0);
    desenha_janela (-proporcao * (1.4), proporcao * 1.5, 0);
    desenha_janela ( proporcao * (1.4), proporcao * 1.5, 0);
    desenha_janela (-proporcao * (frontalComp / 4 - 0.5), proporcao * 1.5, 0);
    desenha_janela ( proporcao * (frontalComp / 4 - 0.5), proporcao * 1.5, 0);
    desenha_janela (-proporcao * (frontalComp / 2.6), proporcao * 1.5, 0);
    desenha_janela ( proporcao * (frontalComp / 2.6), proporcao * 1.5, 0);
    glColor3f ( corParede[0], corParede[1], corParede[2] );

    // parede de fundo
    y = lateralAltura / 2;
    gl.define_deslocamento (0, y, -lateralComp);
    gl.define_escala (frontalComp, lateralAltura, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    
    // parede lateral esquerda
    gl.define_deslocamento (-frontalComp / 2, y, -lateralComp / 2);
    gl.define_escala (paredeLargura, lateralAltura, lateralComp);
    gl.desenha_cubo();

    // parede lateral direita
    /// parte de cima
    y = (lateralAltura - portaLateralAltura) / 2;
    y += portaLateralAltura;
    gl.define_deslocamento (frontalComp / 2, y, -lateralComp / 2);
    y = lateralAltura - portaLateralAltura;
    gl.define_escala (paredeLargura, y, lateralComp);
    gl.desenha_cubo();
    /// parte esquerda
    y = portaLateralAltura / 2;
    z = (-lateralComp + portaLateralLargura) / 4;
    gl.define_deslocamento (frontalComp / 2, y, z);
    gl.define_escala (paredeLargura, y * 2, z * 2);
    gl.desenha_cubo();
    /// parte direita
    z = (-3*lateralComp - portaLateralLargura) / 4;
    gl.define_deslocamento (frontalComp / 2, y, z);
    z = (-lateralComp + portaLateralLargura) / 4;
    gl.define_escala (paredeLargura, y * 2, z * 2);
    gl.desenha_cubo();

    // porta lateral
    glColor3f ( corPortao[0], corPortao[1], corPortao[2] );
    x = frontalComp / 2 + portaLateralLargura * (cos (aberturaPortaLateral * PI / 180) - 1) / 2;
    y = portaLateralAltura / 2;
    z = -lateralComp / 2 + portaLateralLargura * sin (aberturaPortaLateral * PI / 180) / 2;
    gl.define_deslocamento (x, y, z);
    gl.define_escala (portaLateralEspessura, portaLateralAltura, portaLateralLargura);
    gl.define_rotacao (aberturaPortaLateral, 0, 1, 0);
    gl.desenha_cubo();
    glColor3f ( corParede[0], corParede[1], corParede[2] );
    gl.define_rotacao (0, 0, 0, 0);

    // parede lateral da garagem
    x = frontalComp / 2 + entradaGaragemLargura;
    gl.define_deslocamento (x, entradaGaragemAltura / 2, -lateralComp / 2);
    gl.define_escala (paredeLargura, entradaGaragemAltura, lateralComp);
    gl.desenha_cubo();
    // contorno sobre o muro
    glColor3f ( corParede[0]-0.1, corParede[1]-0.1, corParede[2]-0.1 );
    y = entradaGaragemAltura + paredeLargura / 4;
    gl.define_deslocamento (x, y, -lateralComp / 2);
    gl.define_escala (paredeLargura, paredeLargura / 2, lateralComp);
    gl.desenha_cubo();
    glColor3f ( corParede[0], corParede[1], corParede[2] );

    // parede do fundo da garagem
    x = frontalComp / 2 + entradaGaragemLargura / 2;
    gl.define_deslocamento (x, entradaGaragemAltura / 2, -lateralComp);
    gl.define_escala (entradaGaragemLargura, entradaGaragemAltura, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    // contorno sobre o muro
    glColor3f ( corParede[0]-0.1, corParede[1]-0.1, corParede[2]-0.1 );
    gl.define_deslocamento (x, y, -lateralComp);
    gl.define_escala (entradaGaragemLargura, paredeLargura / 2, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    glColor3f ( corParede[0], corParede[1], corParede[2] );
    
    // entrada da garagem
    /// lado esquerdo
    x = frontalComp + entradaGaragemLargura / 2;
    x = (x + 0.4 - portaoGaragemLargura) / 2;
    gl.define_deslocamento (x, entradaGaragemAltura / 2, 0);
    x = entradaGaragemLargura / 2 + 0.4 - portaoGaragemLargura;
    gl.define_escala (x, entradaGaragemAltura, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    ///lado direito
    x = frontalComp + 3 * entradaGaragemLargura / 2;
    x = (x + 0.4 + portaoGaragemLargura) / 2;
    gl.define_deslocamento (x, entradaGaragemAltura / 2, 0);
    x = entradaGaragemLargura / 2 - 0.4 - portaoGaragemLargura;
    gl.define_escala (x, entradaGaragemAltura, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    /// lado superior
    x = (frontalComp + entradaGaragemLargura) / 2 + 0.4;
    y = (entradaGaragemAltura + portaoGaragemAltura) / 2;
    gl.define_deslocamento (x, y, 0);
    y = entradaGaragemAltura - portaoGaragemAltura;
    gl.define_escala (portaoGaragemLargura * 2, y, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    // contorno sobre o muro
    glColor3f ( corParede[0]-0.1, corParede[1]-0.1, corParede[2]-0.1 );
    x = (frontalComp + entradaGaragemLargura) / 2;
    gl.define_deslocamento (x, entradaGaragemAltura + paredeLargura / 4, 0);
    gl.define_escala (entradaGaragemLargura, paredeLargura / 2, paredeLargura);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    glColor3f ( corParede[0], corParede[1], corParede[2] );

    // portão da garagem
    /// portão 1
    glColor3f ( corPortao[0], corPortao[1], corPortao[2] );
    y = portaoGaragemAltura;
    z = portaoGaragemEspessura;
    x = frontalComp / 2 + entradaGaragemLargura / 2 + 0.4;
    x += -1 + portaoGaragemLargura * cos (aberturaPorta * PI / 180) / 2;
    gl.define_deslocamento ( x, portaoGaragemAltura / 2, -sin (aberturaPorta * PI / 180) / 2 );
    gl.define_escala (portaoGaragemLargura, y, z);
    gl.define_rotacao ( aberturaPorta, 0, 1, 0);
    gl.desenha_cubo();
    /// portão 2
    x = frontalComp / 2 + entradaGaragemLargura / 2 + 0.4;
    x += 1 - portaoGaragemLargura * cos (aberturaPorta * PI / 180) / 2;
    gl.define_deslocamento ( x, portaoGaragemAltura / 2, -sin (aberturaPorta * PI / 180) / 2 );
    gl.define_escala (portaoGaragemLargura, y, z);
    gl.define_rotacao (-aberturaPorta, 0, 1, 0);
    gl.desenha_cubo();

    //// pilares frontais
    // pilar lateral esquerda
    glColor3f ( corParede[0]+0.1, corParede[1]+0.1, corParede[2]+0.1 );
    gl.define_deslocamento (-frontalComp / 2 + 0.15, frontalAltura / 2, 0.05);
    gl.define_escala (0.3, frontalAltura, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // pilar lateral direita
    gl.define_deslocamento (frontalComp / 2 - 0.15, frontalAltura / 2, 0.05);
    gl.define_escala (0.3, frontalAltura, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // segundo pilar lateral esquerdo
    gl.define_deslocamento (-frontalComp / 3.5 + 0.15, frontalAltura / 2, 0.05);
    gl.define_escala (0.3, frontalAltura, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // segundo pilar lateral direita
    gl.define_deslocamento (frontalComp / 3.5 - 0.15, frontalAltura / 2, 0.05);
    gl.define_escala (0.3, frontalAltura, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // pilar do meio lateral esquerdo
    gl.define_deslocamento (-frontalComp / 6 + 0.15, frontalAltura / 2 -0.25, 0.05);
    gl.define_escala (0.3, frontalAltura-2.5, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // pilar do meio lateral direita
    gl.define_deslocamento (frontalComp / 6 - 0.15, frontalAltura / 2 -0.25, 0.05);
    gl.define_escala (0.3, frontalAltura-2.5, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // viga inferior
    gl.define_deslocamento (0, 1, 0.05);
    gl.define_escala (frontalComp, 0.3, 0.05);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // viga superior (esta é detalhada)
    glColor3f ( corParede[0]+0.16, corParede[1]+0.16, corParede[2]+0.16 );
    gl.define_deslocamento (0, frontalAltura - 1.3, 0.12);
    gl.define_escala (frontalComp, 0.1, 0.09);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    glColor3f ( corParede[0]+0.13, corParede[1]+0.13, corParede[2]+0.13 );
    gl.define_deslocamento (0, frontalAltura - 1.4, 0.09);
    gl.define_escala (frontalComp, 0.1, 0.07);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();
    glColor3f ( corParede[0]+0.1, corParede[1]+0.1, corParede[2]+0.1 );
    gl.define_deslocamento (0, frontalAltura - 1.5, 0.06);
    gl.define_escala (frontalComp, 0.1, 0.06);
    gl.define_rotacao (0, 0, 0, 0);
    gl.desenha_cubo();

    // telhado
    glColor3f ( corTelhado[0], corTelhado[1], corTelhado[2] );
    gl.define_deslocamento (0, lateralAltura-0.3+sin(-60)*lateralComp/4, -lateralComp/4);
    gl.define_escala (frontalComp, 0.05+lateralComp/(2*cos(-60)), 0.05);
    gl.define_rotacao (-80, 1, 0, 0);
    gl.desenha_cubo();
    gl.define_deslocamento (0, lateralAltura-0.3+sin(-60)*lateralComp/4, -lateralComp*3/4);
    gl.define_escala (frontalComp, 0.05+lateralComp/(2*cos(-60)), 0.05);
    gl.define_rotacao (80, 1, 0, 0);
    gl.desenha_cubo();

    // Detalhe sobre os muros laterais 
    // muro esquerdo
    glBegin (GL_POLYGON);
        glColor3f ( corParede[0], corParede[1], corParede[2] );
        x = -proporcao * frontalComp / 2 - proporcao * paredeLargura / 2;
        y = proporcao * lateralAltura;
        z = -proporcao * paredeLargura / 2;
        glVertex3f (x, y, z);
        y = proporcao * frontalAltura;
        glVertex3f (x, y, z);
        z -= proporcao * 0.5;
        y -= proporcao * 0.8;
        glVertex3f (x, y, z);
        z -= proporcao * 0.4;
        y -= proporcao * 0.1;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.9);
        glVertex3f (x, y, z);
        z -= proporcao * 0.3;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.9);
        glVertex3f (x, y, z);
        z -= proporcao * 2;
        y += proporcao * 0.7;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.2);
        glVertex3f (x, y, z);
        z = -proporcao * lateralComp;
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    // Detalhe sobre os muros laterais 
    // muro direito
    glBegin (GL_POLYGON);
        glColor3f ( corParede[0], corParede[1], corParede[2] );
        x = proporcao * frontalComp / 2 + proporcao * paredeLargura / 2;
        y = proporcao * lateralAltura;
        z = -proporcao * paredeLargura / 2;
        glVertex3f (x, y, z);
        y = proporcao * frontalAltura;
        glVertex3f (x, y, z);
        z -= proporcao * 0.5;
        y -= proporcao * 0.8;
        glVertex3f (x, y, z);
        z -= proporcao * 0.4;
        y -= proporcao * 0.1;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.9);
        glVertex3f (x, y, z);
        z -= proporcao * 0.3;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.9);
        glVertex3f (x, y, z);
        z -= proporcao * 2;
        y += proporcao * 0.7;
        glVertex3f (x, y, z);
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();
    glBegin (GL_POLYGON);
        glVertex3f (x, y, z);
        y = proporcao * (frontalAltura - 0.2);
        glVertex3f (x, y, z);
        z = -proporcao * lateralComp;
        y = proporcao * lateralAltura;
        glVertex3f (x, y, z);
    glEnd();

    // desenha lâmpadas
    x = -6;
    y =lateralAltura - 0.1;
    z = lateralComp / 2;
    gl.define_escala (1.2, 0.03, 0.03);
    gl.define_rotacao (0, 0, 0, 0);
    for (x = -6; x <= 6; x += 3) {
        for (z = lateralComp / 2 - 3; z <= lateralComp / 2 + 3; z += 3) {
            glColor3f (1, 1, 1);
            gl.define_deslocamento (x, y, -z-0.03);
            gl.desenha_cubo();
            gl.define_deslocamento (x, y, -z+0.03);
            gl.desenha_cubo();
            glColor3f (0.8, 0.8, 0.8);
            glBegin (GL_POLYGON);
                glVertex3f (pos_x+proporcao*(x-0.7), pos_y+proporcao*(y-0.01), pos_z+proporcao*(-z-0.08));
                glVertex3f (pos_x+proporcao*(x-0.7), pos_y+proporcao*(y-0.01), pos_z+proporcao*(-z+0.08));
                glVertex3f (pos_x+proporcao*(x+0.7), pos_y+proporcao*(y-0.01), pos_z+proporcao*(-z+0.08));
                glVertex3f (pos_x+proporcao*(x+0.7), pos_y+proporcao*(y-0.01), pos_z+proporcao*(-z-0.08));
            glEnd();
        }
    }
}