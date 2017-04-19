#include <stdio.h>
#include <stdlib.h>
#include "myvector.h"

/*Cria um vetor de tamanho "tam" e retorna um ponteiro para ele*/
int *criaVetor (int tam) {
    int *v;
    v = malloc(tam*sizeof(int));
    if (!v)
        exit(1);
    return v;
}

/*Imprime um vetor "v" de tamanho "tam"*/
void imprimeVetor (int *v, int tam) {
    int i;
    printf("[");
    for (i = 0; i < tam-1; i++)
        printf("%d, ", v[i]);
    printf("%d]\n", v[i]);
}

/*Aloca uma matriz com "m" linhas e "n" colunas e retorna um ponteiro
para ela*/
int **criaMatriz (int m, int n){
    int **mat;
    int i, j;
    mat = malloc(m*sizeof(int*));
    if (mat == NULL){
        free(mat);
        exit(1);
    }
    for (i = 0; i < m; i++){
        mat[i] = malloc(n*sizeof(int));
        if (mat[i] == NULL){
            for (j = 0; j <= i; j++)
                free(mat[j]);
            free(mat);
            exit(1);
        }
    }
    return mat;
}

/*Imprime uma matriz "mat" de "m" linhas por "n" colunas*/
void imprimeMatriz (int **mat, int m, int n) {
    int i, j;
    printf("[");
    for (i = 0; i < m; i++){
        printf("[");
        for (j = 0; j < n-1; j++)
            printf("%d, ", mat[i][j]);
        printf("%d]%c", mat[i][j], "\n]"[i == m-1]);
    }
    printf("\n");
}

/*Desaloca uma matriz de m linhas*/
void freeMatriz (int **mat, int m){
    int i;
    for (i = 0; i < m; i++)
        free(mat[i]);
    free(mat);
}