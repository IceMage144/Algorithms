/*
    Biblioteca feita por João Gabriel Basi
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*Biblioteca de funções que ajudam o programa a manusear a memória*/

/*Aloca espaço de tamanho "size" na memória, e, se a alocação falhar,
mostra a mensagem "msg" na saída de erros*/
void *emalloc (size_t size, const char *msg) {
    int *Ret;
    Ret = malloc(size);
    if (Ret == NULL) {
        fprintf(stderr, "%s", msg);
        exit(1);
    }
    return Ret;
}

/*Recebe uma string "str" e devolve um ponteiro para uma cópia dela.
Se a função não conseguir alocar espaço na memória, encerra o programa
e mostra uma mensagem de erro na saída de erro*/
char *estrdup (const char *str) {
    const char errmsg[] = "A string auxiliar não pode ser alocada\n";
    char *aux;
    int len;
    len = strlen(str);
    aux = emalloc((len+1)*sizeof(char), errmsg);
    if (aux == NULL) {
        fprintf(stderr, "%s", errmsg);
        exit(1);
    }
    strcpy(aux, str);
    return aux;
}