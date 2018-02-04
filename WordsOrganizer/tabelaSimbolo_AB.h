/*
    Biblioteca feita por João Gabriel Basi
*/

#ifndef __TABELASIMBOLO_AB_H__
#define __TABELASIMBOLO_AB_H__

#include "auxfuncs.h"

/*Biblioteca com funções sobre a tabela de símbolos implementada com
árvore de busca binária*/

/*Nó para árvore binária*/
typedef struct btnode_t {
    char *key;
    int value;
    struct btnode_t *left;
    struct btnode_t *right;
} BTNode;

/*Raiz para árvore binária*/
typedef struct btst_t {
    int top;
    BTNode *root;
} BinaryTreeSTable;

#define BTST BinaryTreeSTable

/*Retorna um ponteiro para uma nova tabela de símbolos, do tipo árvore de
busca binária*/
BTST *BSTTableCreate ();

/*Desaloca uma tabela de símbolos "Table", do tipo árvore de busca
binária*/
void BSTTableDestroy (BTST *Table);

/*Adiciona uma chave "key" à uma tablela de símbolos "Table", do tipo
árvore de busca binária, e retorna um InsertionResult, com um ponteiro
para o campo value associado à "key" e com a variável new igual à 1 se
a chave é nova, ou 0 caso contrário*/
InsertionResult *BSTAdd (BTST *Table, const char *key);

/*Função recursiva que imprime a tabela de símbolos "Table", do tipo
árvore de busca binária, na saída padrão, com seus elementos ordenados
por ordem alfabética*/
void BSTPrintLexi (BTNode *Table, int topChar);

/*Função recursiva que imprime a tabela de símbolos "Table", do tipo
árvore de busca binária, na saída padrão, com seus elementos ordenados
por ordem de ocorrência*/
void BSTPrintVal (BTST *Table, int topChar);

#endif