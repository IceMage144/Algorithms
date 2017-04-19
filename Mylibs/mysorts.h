#ifndef __MYSORTS_H__
#define __MYSORTS_H__

#include <stdio.h>
#include <stdlib.h>
#include "myvector.h"

/*Ordenação por bolhas*/
void bubbleSort(int v[], int tam);

/*Ordenação por seleção*/
void selectionSort (int v[], int tam);

/*Ordenação por inserção*/
void insertionSort (int v[], int tam);

/*Ordenação por divisão e conquista do tipo "quick"*/
void quickSort (int v[], int ini, int fim);

/*Ordenação por fila de prioridade*/
void heapSort (int v[], int tam);

/*Ordenação por divisão e conquista do tipo "merge"*/
void mergeSort (int v[], int ini, int fim);

#endif