#include <iostream>
#include "myfractioncpp.h"

using namespace std;

int mmc (int, int);
int mdc (int, int);

class fraction{
	public:
		int den, num, maxi;
		fraction () {};
		fraction (int a, int b) : num(a), den(b) {
			if (b < 0){
				a = -a;
				b = -b;
			}
			maxi = mdc(a, b);
			if (maxi != 1){
				a /= maxi;
				b /= maxi;
			}
		}
		~fraction () {};
		double value () const;
		fraction operator + (const fraction&);
		fraction operator - (const fraction&);
		fraction operator * (const fraction&);
		fraction operator / (const fraction&);
		fraction operator += (const fraction&);
		fraction operator -= (const fraction&);
		fraction operator *= (const fraction&);
		fraction operator /= (const fraction&);
		int operator == (const fraction&);
		int operator < (const fraction&);
		int operator > (const fraction&);
		int operator >= (const fraction&);
		int operator <= (const fraction&);
		int operator != (const fraction&);
};

double fraction::value () const{
	return (double)num/(double)den;
}

fraction fraction::operator + (const fraction& param){
	fraction temp;
	int mini, maxi;
	mini = mmc(param.den, den);
	temp.num = param.num*mini/param.den + num*mini/den;
	temp.den = mini;
	maxi = mdc(temp.den, temp.num);
	if (maxi != 1){
		temp.den /= maxi;
		temp.num /= maxi;
	}
	return temp;
}

fraction fraction::operator - (const fraction& param){
	fraction temp;
	int mini, maxi;
	mini = mmc(param.den, den);
	temp.num = param.num*mini/param.den - num*mini/den;
	temp.den = mini;
	maxi = mdc(temp.den, temp.num);
	if (maxi != 1){
		temp.den /= maxi;
		temp.num /= maxi;
	}
	return temp;
}

fraction fraction::operator * (const fraction& param){
	fraction temp;
	temp.den = param.den * den;
	temp.num = param.num * num;
	maxi = mdc(temp.den, temp.num);
	return temp;
}

fraction fraction::operator / (const fraction& param){
	fraction temp;
	temp.den = den * param.num;
	temp.num = num * param.den;
	return temp;
}

fraction fraction::operator += (const fraction& param){
	return (*this + param);
}

fraction fraction::operator -= (const fraction& param){
	return (*this - param);
}

fraction fraction::operator *= (const fraction& param){
	return (*this * param);
}

fraction fraction::operator /= (const fraction& param){
	return (*this / param);
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


int mdc (int n, int s) {
	int aux;
	while (s != 0){
		aux = s;
		s = n%s;
		n = aux;
	}
	return n;
}

int mmc(int n, int s) {
	int ret, gcd;
	gcd = mdc(n, s);
	ret = (n/gcd) * (s/gcd) * gcd;
	return ret;
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