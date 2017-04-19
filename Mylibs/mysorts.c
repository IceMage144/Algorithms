/*

*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "myvector.h"

void troca (int *num1, int *num2) {
	*num1 ^= *num2;
	*num2 ^= *num1;
	*num1 ^= *num2;
}

void bubbleSort(int v[], int tam) {
	int count;
	while (count != tam-1) {
		count = 0;
		for (int i = 0; i < tam-1; i++)
			if (v[i] > v[i+1])
				troca(&v[i], &v[i+1]);
			else
				count++;
	}
}

void selectionSort (int v[], int tam) {
	for (int i = 0; i < tam-1; i++)
		for (int j = i+1; j < tam; j++)
			if (v[i] > v[j])
				troca(&v[i], &v[j]);
}

int buscaBin(int v[], int tam, int num) {
	int fim = tam-1, ini = 0, meio;
	while (fim >= ini){
		meio = (fim+ini)/2;
		if (v[meio] == num)
			return meio;
		if (v[meio] > num)
			fim = meio-1;
		else if (v[meio] < num)
			ini = meio+1;
	}
	return fim;
}

void insertionSort (int v[], int tam) {
	int j, acc;
	for (int i = 0; i < tam; i++){
		acc = v[i];
		j = i;
		while (j > 0 && v[j] < v[j-1]){
			troca(&v[j], &v[j-1]);
			j--;
		}
	}
}

void quickSort (int v[], int ini, int fim) {
	int pivo = v[ini], ini2 = ini, fim2 = fim;
	if (fim2 > ini2){
		while (fim2 > ini2){
			while (v[fim2] > pivo && fim2 > ini2)
				fim2--;
			troca(&v[fim2], &v[ini2]);
			while (v[ini2] <= pivo && fim2 > ini2)
				ini2++;
			troca(&v[fim2], &v[ini2]);
		}
		v[ini2] = pivo;
		quickSort(v, ini, fim2-1);
		quickSort(v, ini2+1, fim);
	}
}

void rebaixa (int v[], int tam, int pos) {
	int pai = pos, filho = 2*pai+1;
	while (filho < tam){
		if (filho+1 < tam && v[filho] < v[filho+1])
			filho++;
		if (v[filho] < v[pai])
			break;
		troca(&v[filho], &v[pai]);
		pai = filho;
		filho = 2*pai+1; 
	}
}

void heapifica (int v[], int tam) {
	for (int i = (tam-2)/2; i >= 0; i--)
		rebaixa(v, tam, i);
}

void heapSort (int v[], int tam) {
	heapifica(v, tam);
	for (int i = tam-1; i > 0; i--){
		troca(&v[0], &v[i]);
		rebaixa(v, i, 0);
	}
}

void intercala (int v[], int ini, int meio, int fim){
    int pos = 0, aux1 = ini, aux2 = meio+1, i;
    int *Vaux;
    Vaux = criaVetor(fim-ini+1);
    while (aux1 <= meio && aux2 <= fim){
        if (v[aux1] > v[aux2]){
            Vaux[pos] = v[aux2];
            aux2++;
        }
        else {
            Vaux[pos] = v[aux1];
            aux1++;
        }
        pos++;
    }
    while (aux1 <= meio){
        Vaux[pos] = v[aux1];
        aux1++;
        pos++;
    }
    while (aux2 <= fim){
        Vaux[pos] = v[aux2];
        aux2++;
        pos++;
    }
    for (aux1 = 0; aux1 < pos; aux1++)
        v[aux1+ini] = Vaux[aux1];
    free(Vaux);
}

void mergeSort (int v[], int ini, int fim){
    int meio;
    if (ini < fim){
        meio = (ini+fim)/2;
        mergeSort(v, ini, meio);
        mergeSort(v, meio+1, fim);
        intercala(v, ini, meio, fim);
    }
}

int pegaDig (int num, float dig) {
	float div = pow(10.0, dig-1);
	float mod = pow(10.0, dig);
	return (int)(num/div)%(int)mod;
}

void radixSort (int v[], int tam, int digs) {
	int dig, pos = 0;
	int *topos;
	int **mat;
	topos = criaVetor(10);
	mat = criaMatriz(10, tam);
	for (int i = 0; i < 10; i++)
		topos[i] = 0;
	for (int i = 1; i <= digs; i++) {
		for (int j = 0; j < tam; j++) {
			dig = pegaDig(v[j], i);
			printf("dig = %d\n", dig);
			mat[dig][topos[dig]] = v[j];
			topos[dig]++;
		}
		for (dig = 0; dig < 10; dig++) {
			for (int j = 0; j < topos[dig]; j++){
				v[pos] = mat[dig][j];
				pos++;
			}
		}
		for (int j = 0; j < 10; j++)
			topos[j] = 0;
	}
	free(topos);
	printf("TOPER\n");
	freeMatriz(mat, 10);
}

int main () {
	int tam, digs;
	int *v;
	scanf("%d", &tam);
	scanf("%d", &digs);
	v = criaVetor(tam);
	for (int i = 0; i < tam; i++)
		scanf("%d", &v[i]);
	radixSort(v, tam, 2.0);
	imprimeVetor(v, tam);
	return 0;
}