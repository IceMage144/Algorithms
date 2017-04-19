#include <stdio.h>
#include <stdlib.h>
#include "mystack.h"

/*Aloca a pilha e retorna um ponteiro para ela*/
pilha *criaPilha (int tam){
    pilha *p;
    p = malloc(sizeof(pilha));
    if (p == NULL){
        printf("A pilha não pode ser alocada\n");
        exit(1);
    }
    p->v = malloc(tam*sizeof(int));
    if (p->v == NULL){
        printf("A pilha não pode ser alocada\n");
        free(p);
        exit(1);
    }
    p->topo = 0;
    p->pMax = tam;
    return p;
}

/*retorna 1 se a pilha "p" estiver vazia ou 0 caso contrário*/
int pilhaVazia (pilha *p){
    return (p->topo == 0);
}

/*Retorna 1 se a pilha estiver cheia ou 0 caso contrário*/
int pilhaCheia (pilha *p){
    return (p->topo == p->pMax);
}

/*empilha "num" na pilha "p". Retorna 1 se conseguiu empilhar ou 0 caso
contrário*/
int empilha (pilha *p, int num){
    int i;
    int *v;
    if (pilhaCheia(p)) {
        v = malloc(2*p->pMax*sizeof(int));
        if (v == NULL)
            return 0;
        for (i = 0; i < p->pMax; i++)
            v[i] = p->v[i];
        free(p->v);
        p->v = v;
        p->pMax *= 2;
    }
    p->v[p->topo] = num;
    p->topo++;
    return 1;
}

/*Desempilha e retorna o elemento do topo da pilha "p"*/
int desempilha (pilha *p){
    p->topo--;
    return p->v[p->topo];
}

/*Imprime os elementos da pilha "p"*/
void imprimePilha (pilha *p){
    int i;
    for (i = 0; i < p->topo; i++){
        printf("%d\n", p->v[i]);
    }
}

/*Desaloca uma pilha de tamanho tam*/
void freePilha (pilha *p){
    free(p->v);
    free(p);
}