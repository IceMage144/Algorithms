#include <iostream>
#include <map>
#include <cmath>

/*
This program was made with the purpose of finding primes of the form 4x+1 using
the sum of two squares. I excluded the sums of the form odd^2+odd^2 and
even^2+even^2, because their results are both even, and put an option to exclude
the results that are multiple of five. A year before I made this, I found this
page https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares

Esse programa foi feito com o intuito de achar primos da forma 4x+1 usando uma
soma de dois quadrados. Eu excluí as somas da forma ímpar^2+ímpar^2 e
par^2+par^2, porque seus resultados serão sempre par, e também coloquei uma
opção para excluir os resultados múltiplos de cinco. Um ano depois de fazer esse
programa eu achei essa página https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares
*/

using namespace std;

//Verifica se x^2+y^2!=primo, x!=y(mod 2), x,y \in N

map<int,int> primesInv;
int primes[11234];
int notPrimes[11234];
int factors1[11234];
int factors2[11234];
int md[11234];

bool isPrime(int num){
	int div = 3;
	int lim = sqrt(num);
	bool res;
	if ((num%2 == 0 && num != 2) || (num == 1)){
		res = false;
	}
	else{
		while (num%div != 0 && div <= lim){
			div += 2;
		}
		if (div > lim || num == 2){
			res = true;
		}
		else{
			res = false;
		}
	}
	return res;
}

void swap(int* num1, int* num2){
	int aux = *num1;
	*num1 = *num2;
	*num2 = aux;
}

int leastDiv(int num){
	int lim = sqrt(num);
	int div = 3;
	if (num%2 == 0){
		return 2;
	}
	else{
		while(div <= lim && num%div != 0){
			div += 2;
		}
		return div;
	}
}

int main(){
	int lim, counter = 1, temp = 0, k = 0;
	int square;
	string showFives;
	cout << "What's the superior limit? (max = 30000)" << endl;
	cin >> lim;
	cout << "Show multiples of 5? (yes/no/only)" << endl;
	cin >> showFives;
	primes[0] = 2;
	primesInv[2] = 0;

	for (int i = 3; i < lim; i += 2){
		if (isPrime(i) == true){
			primes[counter] = i;
			primesInv[i] = counter;
			counter++;
		}
	}
	notPrimes[0] = 2;
	factors1[0] = 1;
	factors2[0] = 1;
	md[0] = 2;
	counter = 1;
	for (int i = 1; i < (int)ceil(sqrt(lim)); i++){
		for (int j = (i%2==0)? 1 : 2; j < i; j += 2){
			square = pow((double)i,2.0)+pow((double)j,2.0);
			if (/*primes[primesInv[square]] != square &&*/ square <= lim){
				notPrimes[counter] = square;
				factors1[counter] = i;
				factors2[counter] = j;
				md[counter] = leastDiv(square);
				counter++;
			}
		}
	}
	//insertion sort
	while (temp != counter){
		k = 0;
		temp++;
		while (k < temp){
			if (notPrimes[temp-k] < notPrimes[temp-k-1]){
				swap(&notPrimes[temp-k], &notPrimes[temp-k-1]);
				swap(&factors1[temp-k], &factors1[temp-k-1]);
				swap(&factors2[temp-k], &factors2[temp-k-1]);
				swap(&md[temp-k], &md[temp-k-1]);
			}
			k++;
		}
	}
	for (int i = 1; i <= counter; i++){
		if ((showFives == "only" || showFives == "yes") && notPrimes[i]%5 == 0){
			cout << notPrimes[i] << " = " << factors1[i] << "^2 + " << factors2[i] << "^2";
			if (notPrimes[i] == 5){
				cout << endl;
			}
			else {
				cout << " <-- mod " << md[i] << endl;
			}
		}
		else if ((showFives == "yes" || showFives == "no") && notPrimes[i]%5 != 0){
			cout << notPrimes[i] << " = " << factors1[i] << "^2 + " << factors2[i] << "^2";
			if (primes[primesInv[notPrimes[i]]] != notPrimes[i]){
				cout << " <-- mod " << md[i] << endl;
			}
			else{
				cout << endl;
			}
		}
	}
	return 0;
}
