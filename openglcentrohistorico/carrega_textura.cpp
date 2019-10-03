#include "desenho.h"

void Desenho::carrega_texturas_arquivo (char *nomeArquivo, GLuint *textura) {
    /*
    int largura, altura;
    unsigned char* imagem =
            SOIL_load_image(nomeArquivo, &largura, &altura, 0, SOIL_LOAD_RGBA);

    glGenTextures(1, textura);
    glBindTexture(GL_TEXTURE_2D, *textura);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, imagem);
    glBindTexture(GL_TEXTURE_2D, 0);
    */
}