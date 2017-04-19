#include <cmath>
#include <iostream>
#include <map>
#include <vector>

/*
This program were made with the purpose of anilyzing the veracity of the video
https://www.youtube.com/watch?v=6KHTrLEfHIM , about an alleged "pattern" of the
primes.

Esse programa foi feito com o intuito de analizar a veracidade do vídeo
https://www.youtube.com/watch?v=6KHTrLEfHIM , que fala sobre um suposto "padrão"
nos números primos.
*/

using namespace std;

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

int main(){
	map<int, bool> primes;
	int echo[2000];
	int count = 0;
	char aux;
	cout << "Calculating primes..." << endl;
	for (int i = 1; i <= 1031; i+=2){
		primes[i] = isPrime(i);
	}
	cout << "Center 30 exceptions:" << endl;
	for (int i = 31; i <= 1031; i+=2){
		if ((primes[(int)fabs((float)(60-i))] == 1 && primes[i] != 1) || (primes[(int)fabs((float)(60-i))] != 1 && primes[i] == 1)){
			aux = primes[i] == 1? '<' : '\0';
			cout << "(" << i << aux;
			aux = primes[(int)fabs((float)(60-i))] == 1? '<' : '\0';
			cout << "," << 60-i << aux;
			cout << ") ";
		}
		if (primes[(int)fabs((float)(60-i))] == 1 || primes[i] == 1){
			echo[count] = i-30;
			count++;
		}
	}
	cout << endl;
	cout << "Center 0 exceptions:" << endl;
	for (int i = 0; i < count; i++){
		if (primes[echo[i]] == 0){
			cout << "(" << echo[i] << ") ";
		}
	}
	cout << endl;
}
