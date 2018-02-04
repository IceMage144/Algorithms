/*
    Biblioteca feita por João Gabriel Basi
*/

#include <stdio.h>
#include <stdlib.h>
#include "buffer.h"
#include "auxfuncs.h"

/*Biblioteca de funções sobre a estrutura Buffer, que guarda caracteres
lidos da entrada padrão*/

/*Retorna um ponteiro para um novo buffer*/
Buffer *BufferCreate (){
    const char errmsg[] = "O Buffer não pode ser criado\n";
    Buffer *Buff;
    Buff = emalloc(sizeof(Buffer), errmsg);
    Buff->data = emalloc(1024 * sizeof(char), errmsg);
    Buff->top = 0;
    Buff->maxPos = 1024;
    return Buff;
}

/*Desaloca um buffer "Buff"*/
void BufferDestroy (Buffer *Buff){
    free(Buff->data);
    free(Buff);
}

/*Zera um buffer "Buff"*/
void BufferReset(Buffer *Buff){
    int i;
    for (i = 0; i < Buff->top; i++){
        Buff->data[i] = 0;
    }
    Buff->top = 0;
}

/*Adiciona o caractere "c" à um buffer "Buff"*/
void BufferPush(Buffer *Buff, char c){
    int i;
    char *Vaux;
    const char errmsg[] = "O Buffer não pode ser extendido\n";
    Buff->data[Buff->top] = c;
    (Buff->top)++;
    if (Buff->top == Buff->maxPos){
        Vaux = emalloc(2 * Buff->maxPos * sizeof(char), errmsg);
        for (i = 0; i < Buff->maxPos; i++)
            Vaux[i] = Buff->data[i];
        free(Buff->data);
        Buff->data = Vaux;
        Buff->maxPos *= 2;
    }
}

/*Lê uma linha de um arquivo "input" e guarda em um buffer "Buff",
incluindo o caractere final "\n"*/
int readLine(FILE *input, Buffer *Buff){
    char c = fgetc(input);
    int charCount = 0;
    BufferReset(Buff);
    while (c != EOF && c != '\n'){
        BufferPush(Buff, c);
        charCount++;
        c = fgetc(input);
    }
    if (c == '\n'){
        BufferPush(Buff, c);
        charCount++;
    }
    return charCount;
}