/*
 * Modelagem externa do Antigo Grupo Escolar Ladislau Neto, Maceió - AL
 * Feito por Gean Santos
 */

#include <GL/glut.h>
#include "janela.h"

static Janela janela;

void reajusteJanela (int largura, int altura);
void exibir (void);
void teclasEspeciais (int key, int x, int y);
void teclado (unsigned char key, int x, int y);

int main (int argc,char **argv){
    glutInit (&argc, argv);
    glutCreateWindow ("Antigo Grupo Escolar Ladislau Neto, Maceió - AL");

    janela = Janela(); // executa comando gl no construtor da classe
    
    glutKeyboardFunc (teclado);
    glutSpecialFunc (teclasEspeciais);
    glutDisplayFunc (exibir);
    glutReshapeFunc (reajusteJanela);
    glutIdleFunc (exibir);

    glutMainLoop();

    return 0;
}

void reajusteJanela (int largura, int altura) {
    janela.reajusteJanela (largura, altura);
}
void exibir (void) {
    janela.exibir();
}
void teclasEspeciais (int key, int x, int y) {
    janela.teclasEspeciais (key, x, y);
}
void teclado (unsigned char key, int x, int y) {
    janela.teclado (key, x, y);
}
