/*
    Biblioteca feita por João Gabriel Basi
*/

#ifndef __AUXFUNCS_H__
#define __AUXFUNCS_H__

/*Biblioteca de funções que ajudam o programa a manusear a memória e
resumir operações*/

/*Estrutura utilizada para retornar o resultado de uma inserção na
tabela de símbolos. A variável "new" indica se foi adicionada uma
chave nova na tabela, e o ponteiro "value" aponta para o endereço
relacionado à chave adicionada*/
typedef struct insresll_t {
    int new;
    int *value;
} InsertionResult;

/*Aloca espaço de tamanho "size" na memória, e, se a alocação falhar,
mostra a mensagem "msg" na saída de erros*/
void *emalloc (size_t size, const char *msg);

/*Recebe uma string "str" e devolve um ponteiro para uma cópia dela.
Se a função não conseguir alocar espaço na memória, encerra o programa
e mostra uma mensagem de erro na saída de erro*/
char *estrdup (const char *str);

#endif