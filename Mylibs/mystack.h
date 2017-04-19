/*
    Funções de pilha feitas por mim
*/

#ifndef __MYSTACK_H__
#define __MYSTACK_H__

#include <stdio.h>
#include <stdlib.h>

/*Define uma pilha como sendo uma estrutura com um vetor para
guardar a pilha em si, uma variável inteira para guardar a posição
de seu topo e uma para guardar o seu tamanho máximo*/
typedef struct {
    int topo, pMax;
    int *v;
} pilha;

/*Aloca a pilha e retorna um ponteiro para ela*/
pilha *criaPilha (int tam);

/*retorna 1 se a pilha "p" estiver vazia ou 0 caso contrário*/
int pilhaVazia (pilha *p);

/*Retorna 1 se a pilha estiver cheia ou 0 caso contrário*/
int pilhaCheia (pilha *p);

/*empilha "num" na pilha "p". Retorna 1 se conseguiu empilhar ou 0 caso
contrário*/
int empilha (pilha *p, int num);

/*Desempilha e retorna o elemento do topo da pilha "p"*/
int desempilha (pilha *p);

/*Imprime os elementos da pilha "p"*/
void imprimePilha (pilha *p);

/*Desaloca uma pilha de tamanho tam*/
void freePilha (pilha *p);

#endif