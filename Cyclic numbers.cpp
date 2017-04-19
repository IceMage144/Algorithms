#include <iostream>
#include <cmath>

/*
This program tells if a number is a cyclic number or not (https://en.wikipedia.org/wiki/Cyclic_number)

Esse programa fala se um número é um número cíclico ou não (https://en.wikipedia.org/wiki/Cyclic_number)
*/

using namespace std;

int main(){
      int num;
      cout << "Give a number to anilyze:\n";
      cin >> num;
      int digits = (int)log10((double)num) + 1;
      int r = 1, loops = 0, q = 9;
      if (num%2 == 0 || num%5 == 0){
          q = 10;
          while (r != 0 && loops != num){
              r = q % num;
              q = 10*r;
              loops++;
          }
      }
      else{
          while (r != 0 && loops != num){
              r = q % num;
              q = 10*r + 9;
              loops++;
          }
      }
      if (loops == num-1){
          cout << num << " is cyclic: " << loops << endl;
      }
      else{
          if (num%3 == 0){cout << "periodic" << endl;}
          cout << num << " is not cyclic: " << loops << endl;
      }
      return 0;
}
