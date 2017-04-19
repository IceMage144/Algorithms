/*
    Funções de vetores feitas por mim
*/

#ifndef __MYVECTOR_H__
#define __MYVECTOR_H__

#include <stdio.h>
#include <stdlib.h>

/*Cria um vetor de tamanho "tam" e retorna um ponteiro para ele*/
int *criaVetor (int tam);

/*Imprime um vetor "v" de tamanho "tam"*/
void imprimeVetor (int *v, int tam);

/*Aloca uma matriz com "m" linhas e "n" colunas e retorna um ponteiro
para ela*/
int **criaMatriz (int m, int n);

/*Imprime uma matriz "mat" de "m" linhas por "n" colunas*/
void imprimeMatriz (int **mat, int m, int n);

/*Desaloca uma matriz de m linhas*/
void freeMatriz (int **mat, int m);

#endif