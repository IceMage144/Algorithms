#ifndef __PGMDRAWER_H__
#define __PGMDRAWER_H__

#include "polygons.h"
#include <cstdio>

/*
Canvas class:
Use this object and it's function save_pgm to generate the image file
	- save_pgm:
		Saves
    	- Inputs:
	  		- obj: The object it'll draw (can be a Group object);
	  		- output: File for the output image;
	  		- pix_per_unit: How many pixels will correspond to a unit;
	  		- sample_size: The square root of how many samples the program will
take from each pixel to define it's color.
		- Output:
	  		- The function will output True if nothing got wrong, of False
otherwise.

Classe Canvas:
Use esse objeto e sua função save_pgm para gerar o arquivo da imagem
  	- save_pgm:
    	Entradas:
	  		- obj: O ojeto que será desenhado (pode ser um objeto Group);
	  		- output: Arquivo de saída da imagem;
	  		- pix_per_unit: Quantos pixels vão corresponder à uma unidade;
	  		- sample_size: A raiz quadrada da quantidade de amostras que o
programa irá retirar de cada pixel para definir sua cor.
	Saída:
	  - A saída da função será True se nada de errado aconteceu, ou False caso
contrário.
*/

class Canvas {
public:
	bool save_pgm (const GraphicalObject& obj, FILE *output,
					int pix_per_unit, int sample_size) const;
};

#endif
