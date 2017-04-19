/*
    Biblioteca feita por João Gabriel Basi
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "tabelaSimbolo_AB.h"
#include "auxfuncs.h"

/*Biblioteca com funções sobre a tabela de símbolos implementada com
árvore de busca binária*/

/*Retorna um ponteiro para uma nova tabela de símbolos, do tipo árvore de
busca binária*/
BTST *BSTTableCreate () {
    const char errmsg[] = "A tabela de símbolos não pode ser alocada\n";
    BTST *newTable;
    newTable = emalloc(sizeof(BTST), errmsg);
    newTable->top = 0;
    newTable->root = NULL;
    return newTable;
}

/*Função recursiva auxiliar da BSTTableDestroy que desaloca os nós
filhos de um nó "Node"*/
void BSTTableDestroyNode (BTNode *Node) {
    if (Node != NULL) {
        BSTTableDestroyNode(Node->left);
        BSTTableDestroyNode(Node->right);
        free(Node->key);
        free(Node);
    }
}

/*Desaloca uma tabela de símbolos "Table", do tipo árvore de busca
binária*/
void BSTTableDestroy (BTST *Table) {
    BSTTableDestroyNode(Table->root);
    free(Table);
}

/*Adiciona uma chave "key" à uma tablela de símbolos "Table", do tipo
árvore de busca binária, e retorna um InsertionResult, com um ponteiro
para o campo value associado à "key" e com a variável new igual à 1 se
a chave é nova, ou 0 caso contrário*/
InsertionResult *BSTAdd (BTST *Table, const char *key) {
    const char errmsg1[] = "A chave não pode ser adicionada na tabela\n";
    const char errmsg2[] = "Uma estrutura auxiliar não pode ser alocada\n";
    BTNode *auxNode, *newNode;
    InsertionResult *res;
    int comp;
    res = emalloc(sizeof(InsertionResult), errmsg2);
    auxNode = Table->root;
    newNode = NULL;
    if (auxNode != NULL) {
        comp = strcmp(key, auxNode->key);
        if (comp > 0)
            newNode = auxNode->right;
        else if (comp < 0)
            newNode = auxNode->left;
        else {
            res->new = 0;
            res->value = &(auxNode->value);
        }
        while (newNode != NULL && comp != 0) {
            comp = strcmp(key, newNode->key);
            if (comp > 0){
                auxNode = newNode;
                newNode = newNode->right;
            }
            else if (comp < 0) {
                auxNode = newNode;
                newNode = newNode->left;
            }
            else {
                res->new = 0;
                res->value = &(newNode->value);
            }
        }
        if (newNode == NULL && comp != 0) {
            newNode = emalloc(sizeof(BTNode), errmsg1);
            newNode->value = 0;
            newNode->key = estrdup(key);
            newNode->right = NULL;
            newNode->left = NULL;
            if (comp < 0)
                auxNode->left = newNode;
            else
                auxNode->right = newNode;
            res->new = 1;
            res->value = &(newNode->value);
            (Table->top)++;
        }
    }
    else {
        newNode = emalloc(sizeof(BTNode), errmsg1);
        newNode->value = 0;
        newNode->key = estrdup(key);
        newNode->right = NULL;
        newNode->left = NULL;
        Table->root = newNode;
        res->new = 1;
        res->value = &(newNode->value);
        (Table->top)++;
    }
    return res;
}

/*Função recursiva que imprime a tabela de símbolos "Table", do tipo
árvore de busca binária, na saída padrão, com seus elementos ordenados
por ordem alfabética*/
void BSTPrintLexi (BTNode *Table, int topChar) {
    int i;
    if (Table != NULL) {
        BSTPrintLexi(Table->right, topChar);
        for (i = 0; i < Table->value; i++) {
            printf("%s ", Table->key);
            if (i%1000 == 0)
                printf("\n");
        }
        printf("%d\n", Table->value);
        BSTPrintLexi(Table->left, topChar);
    }
}