/*
    EP4 - MAC0121
    João Gabriel Basi
    N° USP: 9793801
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "buffer.h"
#include "auxfuncs.h"
#include "tabelaSimbolo_AB.h"

/*Este arquivo contém a main do programa.*/
/*O programa consiste na implementação de 5 tipos de tabelas de símbolos,
que contam a ocorrência de cada palavra em um texto. O programa recebe na
linha de comando o nome do arquivo que será lido, o tipo de tabela, e a
ordem em que os elemetos da tabela devem ser impressos. As tabelas podem ser
implementadas com: vetor ordenado (VO), vetor desordenado (VD), lista ligada
oredenada (LO), lista ligada desordenada (LD) e árvore de busca binária (AB).
A tabela é impressa na saída padrão ordenada por ordem de ocorrência (O) ou
por ordem alfabética (A)*/

/*Função que mostra alguns erros na saída padrão, caso o programa não
tenha recebido os argumentos certos na linha de comando*/
static void show_usage (int num){
    switch (num) {
        case 0:
            fprintf(stderr, "Uso: ep4 <arquivo> <tipo da tabela> <ordem>\n");
            break;
        case 1:
            fprintf(stderr, "Os tipos de tabela podem ser:\n");
            fprintf(stderr, "   VO: Vetor ordenado\n");
            fprintf(stderr, "   VD: Vetor desordenado\n");
            fprintf(stderr, "   LO: Lista ligada ordenada\n");
            fprintf(stderr, "   LD: Lista ligada desordenada\n");
            fprintf(stderr, "   AB: Árvore de busca binária\n");
            break;
        case 2:
            fprintf(stderr, "A ordenação da saída pode ser:\n");
            fprintf(stderr, "   O: Ordem de ocorrência\n");
            fprintf(stderr, "   A: Ordem alfabética\n");
            break;
        case 3:
            fprintf(stderr, "O arquivo não pode ser localizado\n");
            break;
    }
}

/*Função que executa o programa no arquivo "input", utilizando árvore de 
busca binária, e imprime na saída padrão a tabela ordenada de acordo com
o valor "ordType" recebido*/
void executeBST (FILE *input, char ordType) {
    const char errmsg[] = "A string auxiliar não pode ser alocada\n";
    int beg = 0, len = 0, redChars, i, topChar = 0;
    InsertionResult *res;
    Buffer *Buff;
    BTST *Table;
    char *strAux;
    Table = BSTTableCreate();
    Buff = BufferCreate();
    redChars = readLine(input, Buff);
    while (redChars) {
        while (beg < Buff->top) {
            while (beg < Buff->top && !isalpha(Buff->data[beg]))
                beg++;
            while (beg+len < Buff->top && isalnum(Buff->data[beg+len]))
                len++;
            if (!len)
                break;
            if (len > topChar)
                topChar = len;
            strAux = emalloc((len+1)*sizeof(char), errmsg);
            strAux[len] = 0;
            for (i = 0; i < len; i++)
                strAux[i] = tolower(Buff->data[beg+i]);
            res = BSTAdd(Table, strAux);
            (*(res->value))++;
            beg += len;
            len = 0;
            free(strAux);
            free(res);
        }
        redChars = readLine(input, Buff);
        beg = 0;
    }
    BSTPrintLexi(Table->root, topChar);
    printf("%d\n", Table->top);
    BufferDestroy(Buff);
    BSTTableDestroy(Table);
}

int main (int argc, char **argv) {
    FILE *input;
    if (argc != 4) {
        show_usage(0);
        exit(1);
    }
    if (argv[3][0] != 'A' && argv[3][0] != 'O') {
        show_usage(2);
        exit(1);
    }
    input = fopen(argv[1], "r");
    if (input == NULL) {
        show_usage(3);
        exit(1);
    }
    if (strcmp(argv[2], "AB") == 0)
        executeBST(input, argv[3][0]);

    else {
        show_usage(1);
        exit(1);
    }
    fclose(input);
    return 0;
}