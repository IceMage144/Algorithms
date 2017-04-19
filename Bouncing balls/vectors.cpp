#include <cmath>
#include "vectors.h"

Vector2d Vector2d::operator + (const Vector2d& other) {
    return Vector2d(x+other.x, y+other.y);
}

Vector2d Vector2d::operator += (const Vector2d& other) {
    *this = *this + other;
}

Vector2d Vector2d::operator - (const Vector2d& other) {
    return Vector2d(x-other.x, y-other.y);
}

Vector2d Vector2d::operator -= (const Vector2d& other) {
    *this = *this - other;
}

Vector2d Vector2d::operator * (double num) {
    return Vector2d(num*x, num*y);
}

double Vector2d::operator * (const Vector2d& other) {
    return x*other.x + y*other.y;
}

Vector2d Vector2d::operator *= (double num) {
    *this = (*this)*num;
}

Vector2d Vector2d::operator / (double num) {
    return Vector2d(x/num, y/num);
}

Vector2d Vector2d::operator /= (double num) {
    *this = (*this)/num;
}

Vector2d Vector2d::operator - () {
    return Vector2d(-x, -y);
}

double snorm(const Vector2d v) {
    return sq(v.x)+sq(v.y);
}

double direction(const Vector2d v) {
    if (v.x != 0 && v.y != 0)
        return atan2(v.y, v.x);
    return 0;
}
