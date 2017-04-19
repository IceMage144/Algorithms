#ifndef __MYFRACTIONCPP_H__
#define __MYFRACTIONCPP_H__

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

#endif