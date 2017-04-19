/*
    Biblioteca feita por João Gabriel Basi
*/

#ifndef __BUFFER_H__
#define __BUFFER_H__

#include <stdio.h>

/*Biblioteca de funções sobre a estrutura Buffer, que guarda caracteres
lidos da entrada padrão*/

typedef struct {
  char *data;
  int maxPos, top;
} Buffer;

/*Retorna um ponteiro para um buffer novo*/
Buffer *BufferCreate();

/*Desaloca um buffer "Buff"*/
void BufferDestroy(Buffer *Buff);

/*Zera um buffer "Buff"*/
void BufferReset(Buffer *Buff);

/*Adiciona o caractere "c" à um buffer "Buff"*/
void BufferPush(Buffer *Buff, char c);

/*Lê uma linha de um arquivo "input" e guarda em um buffer "Buff",
incluindo o caractere final "\n"*/
int readLine(FILE *input, Buffer *Buff);

#endif
