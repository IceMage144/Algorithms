#include <stdio.h>

struct fraction{
	int den, num;
};

int mdc (int n1, int n2) {
	int aux;
	while (n2 != 0){
		aux = n2;
		n2 = n1%n2;
		n1 = aux;
	}
	return n1;
}

int mmc(int n1, int n2) {
	int ret, gcd;
	gcd = mdc(n1, n2);
	ret = (n1/gcd) * (n2/gcd) * gcd;
	return ret;
}

function *fcreate (int num, int den) {
	fraction *aux;
	aux = malloc(sizeof(fraction));
	if (aux == NULL)
		return NULL;
	aux->num = num;
	aux->den = den;
	return aux;
}

double fvalue (fraction *f){
	return (double)f->num/(double)f->den;
}

void fsum (fraction *f1, fraction *f2, fraction *ret) {
	int mini, maxi;
	mini = mmc(f1->den, f2->den);
	ret->num = f2->num*mini/f2->den + f1->num*mini/f1->den;
	ret->den = mini;
	maxi = mdc(ret->den, ret->num);
	if (maxi != 1){
		ret->den /= maxi;
		ret->num /= maxi;
	}
}

void fsub (fraction *f1, fraction *f2, fraction *ret) {
	int mini, maxi;
	mini = mmc(f1->den, f2->den);
	ret->num = f1->num*mini/f1->den - f2->num*mini/f2->den;
	ret->den = mini;
	maxi = mdc(ret->den, ret->num);
	if (maxi != 1){
		ret->den /= maxi;
		ret->num /= maxi;
	}
}

void fmult (fraction *f1, fraction *f2, fraction *ret) {
	ret->den = f1->den * f2->den;
	ret->num = f1->num * f2->num;
}

void fdiv (fraction *f1, fraction *f2, fraction *ret) {
	ret->den = f1->den * f2->num;
	ret->num = f2->num * f1->den;
}

int fraction::operator == (const fraction& param){
	return (den == param.den && num == param.num);
}

int fraction::operator > (const fraction& param){
	int comp1, comp2, comp3;
	comp1 = (param.den == den) & (param.num < num);
	comp2 = (param.den > den) & (param.num == num);
	comp3 = (param.value() < this->value());
	return (comp1 | comp2 | comp3);
}

int fraction::operator < (const fraction& param){
	int comp1, comp2, comp3;
	comp1 = (param.den == den) & (param.num > num);
	comp2 = (param.den < den) & (param.num == num);
	comp3 = (param.value() > this->value());
	return (comp1 | comp2 | comp3);
}

int fraction::operator >= (const fraction& param){
	return (*this > param || *this == param);
}

int fraction::operator <= (const fraction& param){
	return (*this < param || *this == param);
}

int fraction::operator != (const fraction& param){
	return (!(*this == param));
}

int main (){
	fraction frac1(1,3);
	fraction frac2(4,5);
	fraction frac3(0,1);
	cout << frac1.value() << endl;
	cout << frac2.value() << endl;
	cout << (frac1 == frac2) << endl;
	cout << (frac1 >= frac2) << endl;
	cout << (frac1 <= frac2) << endl;
	cout << (frac1 < frac2) << endl;
	cout << (frac1 > frac2) << endl;
	cout << (frac1 != frac2) << endl;
	frac3 = frac1 + frac2;
	cout << frac3.num << '/' << frac3.den << endl;
	frac3 = frac1 - frac2;
	cout << frac3.num << '/' << frac3.den << endl;
	frac3 = frac1 * frac2;
	cout << frac3.num << '/' << frac3.den << endl;
	frac3 = frac1 / frac2;
	cout << frac3.num << '/' << frac3.den << endl;
}