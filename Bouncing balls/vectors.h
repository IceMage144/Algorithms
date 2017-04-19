#ifndef __VECTORS_H__
#define __VECTORS_H__

inline float sq(float num) {
    return num*num;
}

inline float sign(float num) {
    return ((num > 0) - (num < 0));
}

struct Vector2d {
    double x, y;
    Vector2d(): x(0), y(0) {};
    Vector2d(double x, double y): x(x), y(y) {};
    Vector2d operator + (const Vector2d&);
    Vector2d operator += (const Vector2d&);
    Vector2d operator - (const Vector2d&);
    Vector2d operator -= (const Vector2d&);
    Vector2d operator * (double);
    double operator * (const Vector2d&);
    Vector2d operator *= (double);
    Vector2d operator / (double);
    Vector2d operator /= (double);
    Vector2d operator - ();
};

#endif
