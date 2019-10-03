#include "janela.h"

Janela::Janela() {
    glutInitWindowPosition (0,0);
    glutInitWindowSize (1024, 800);
    glutInitDisplayMode (GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE);
    glColorMaterial ( GL_FRONT, GL_AMBIENT_AND_DIFFUSE );
    glEnable (GL_TEXTURE_2D);
    glEnable (GL_DEPTH_TEST); // Habilita comparação de profundidade

    // INICIALIZAÇÃO DE VARIÁVEIS
    proporcao = 5; // fator de aumento
    desenhista = Desenho(proporcao); // coleção de funções que desenha os objetos
    fullscreenmode = false;
    // posição
    vetor_x = 0.0;
    vetor_y = 0.0;
    vetor_z = -1.0;
    x = 0.0 * proporcao;
    y = 1.7 * proporcao;
    z = 10.0 * proporcao;
    // movimentação
    deltaMove = 0.0;
    lateralMove = 0.0;
    deltaAngle = 0.0;
    verticalMove = 0.0;
    aberturaPorta = 0.0;
    aberturaPortaLateral = 0.0;
    // iluminação
    ambiente[0] = ambiente[1] = ambiente[2] = 0;
    comIluminacao = true;
}

// Essa função é chamada quando alguma dimensão da janela é alterada
void Janela::reajusteJanela (int largura, int altura){
    glViewport (0, 0, largura, altura);
    glMatrixMode (GL_PROJECTION);
    glLoadIdentity();
    gluPerspective (80.0, largura / (float)altura, 0.1, 600.0);
    glMatrixMode (GL_MODELVIEW);
}

void Janela::exibir(void){
    if (deltaMove) { // mover camera para frente e traz
        x += deltaMove * vetor_x;
        z += deltaMove * vetor_z;
        deltaMove = 0;
    }
    if (lateralMove) { // mover camera para esquerda e direita
        x += lateralMove * (sin(deltaAngle + PI / 2));;
        z += lateralMove * (-cos(deltaAngle + PI / 2));
        lateralMove = 0;
    }
    if (verticalMove) { // vira a camera em torno do eixo vertical
        y += verticalMove;
        verticalMove = 0;
    }

    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glClearColor (ambiente[0]+0.32, ambiente[1]+0.57, ambiente[2]+0.88, 0);//(0.32,0.57,0.88,0);
    glLoadIdentity(); // Reinicia matriz de transformação

    // Escolha da iluminação
    if (comIluminacao)
      iluminacao();
    else
      glDisable (GL_LIGHTING);

    // empilha matriz atual (anterior à chamada da função)
    glPushMatrix();
    // define câmera
    gluLookAt (x, y, z, x+vetor_x, y+sin(vetor_y), z+vetor_z, 0.0, 1.0, 0.0);

    // Desenha a modelagem
    desenhista.geraModelagem (aberturaPorta, aberturaPortaLateral);
    
    // desempilha matriz anterior à chamada da função
    glPopMatrix();
    glutSwapBuffers();
}

void Janela::teclasEspeciais(int key, int x, int y){
    switch (key) {
    case GLUT_KEY_UP: if (vetor_y <= 1.6) vetor_y += 0.1;
        break;
    case GLUT_KEY_DOWN: if (vetor_y >= -1.6) vetor_y -= 0.1;
        break;
    case GLUT_KEY_LEFT: deltaAngle -= 0.1;
        break;
    case GLUT_KEY_RIGHT: deltaAngle += 0.1;
        break;
    }

    // atualiza direção da câmera
    vetor_x = sin (deltaAngle);
    vetor_z = -cos (deltaAngle);
    glutPostRedisplay();
}

void Janela::teclado(unsigned char key, int x, int y){
    switch (key) {
    case 'w': deltaMove = 3;
        break;
    case 's': deltaMove = -3;
        break;
    case 'a': lateralMove = -3;
        break;
    case 'd': lateralMove = 3;
        break;
    case 'r': verticalMove = 3;
        break;
    case 'f': verticalMove = -3;
        break;
    case 'W': deltaMove = 0.1;
        break;
    case 'S': deltaMove = -0.1;
        break;
    case 'A': lateralMove = -0.1;
        break;
    case 'D': lateralMove = 0.1;
        break;
    case 'R': verticalMove = 0.1;
        break;
    case 'F': verticalMove = -0.1;
        break;
    case 'O':
    case 'o': if (aberturaPorta <= 90 - 3) aberturaPorta += 3;
        break;
    case 'P':
    case 'p': if (aberturaPorta >= 3) aberturaPorta -= 3;
        break;
    case 'K':
    case 'k': if (aberturaPortaLateral <= 90 - 3) aberturaPortaLateral += 3;
        break;
    case 'L':
    case 'l': if (aberturaPortaLateral >= 3) aberturaPortaLateral -= 3;
        break;
    case '1': vetor_y = 0; y = 10; verticalMove = 0;
        break;
    case 27: // esc
        fullscreenmode = !fullscreenmode;
        if (fullscreenmode) glutFullScreen();
        else glutReshapeWindow (1024, 800);
        break;
    case '0': comIluminacao = ! comIluminacao;
        break;
    case '+':
        if (ambiente[0] < 0.5) {
            ambiente[0] +=0.01;
            ambiente[1] +=0.01;
            ambiente[2] +=0.01;
        }
        break;
    case '-':
        if (ambiente[0] > -0.5) {
            ambiente[0] -=0.01;
            ambiente[1] -=0.01;
            ambiente[2] -=0.01;
        }
        break;
    }
    glutPostRedisplay();
}

void Janela::iluminacao() {
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glShadeModel(GL_SMOOTH); // Flat shading for speed
    glDepthMask (GL_TRUE);

    // Define cores para um objeto dourado
    GLfloat LuzAmbiente[]   = {0.24725, 0.1995, 0.07};
    LuzAmbiente[0] += ambiente[0];
    LuzAmbiente[1] += ambiente[1];
    LuzAmbiente[2] += ambiente[2];
    GLfloat LuzDifusa[]    = {0.75164, 0.60648, 0.22648, 1 };
    GLfloat LuzEspecular[] = {0,0,0, 0};
    GLfloat PosicaoLuz0[]  = {0.0,  2, -25, 100};

    glEnable (GL_COLOR_MATERIAL );
    glEnable (GL_BLEND);
    glEnable (GL_LIGHTING); // Habilita o uso de iluminação


    // Define os parametros da Luz número Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa);
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular);
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0);
    glLightModeli (GL_LIGHT_MODEL_TWO_SIDE, 0);
    glEnable (GL_LIGHT0); // Habilita Luz Zero
    glEnable (GL_AUTO_NORMAL);
    glEnable (GL_NORMALIZE);

    glEnable(GL_COLOR_MATERIAL);
}