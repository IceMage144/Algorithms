#include <stdio.h>
#include <wctype.h>
#include <wchar.h>
#include <locale.h>

/*
This program takes out all non-ASCII characters of a file provided as a
parameter at the comand line.

Esse programa tira todos os caracteres que não são da tabela ASCII de um arquivo
fornecido como parâmetro na linha de comando.
*/
int main (int argc, char *argv[]) {
    setlocale (LC_ALL, "pt_BR.UTF-8");
    wint_t wc;
    FILE *fin = fopen (argv[1], "r");
    if fin == NULL {
        return 0;
    }
    do {
        wc = fgetwc (fin);
        if (wc <= L'~')
          wprintf(L"%lc", wc);
    } while (wc != WEOF);
    fclose (fin);
    return 0;
}
