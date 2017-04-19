#include <SFML/Graphics.hpp>
#include <iostream>
#include "physical_objects.h"
#include "vectors.h"

////// ==================== PHYSICAL OBJECT FUNCTIONS ========================

Vector2d PhysicalObject::get_pos() {
    return Vector2d(x, y);
}

Vector2d PhysicalObject::get_velocity() {
    return Vector2d(velocity.x, velocity.y);
}

double PhysicalObject::get_mass() {
    return mass;
}

void PhysicalObject::set_pos(double ax, double ay) {
    x = ax;
    y = ay;
}

void PhysicalObject::gravity(bool boo) {
    grav = boo;
}

void PhysicalObject::air_resistance(bool boo) {
    airres = boo;
}

void PhysicalObject::bouyancy(bool boo) {
    buoy = boo;
}

void PhysicalObject::apply_e_gravity() {
    if (grav)
        velocity.y += g/500;
}

void PhysicalObject::apply_g_gravity(PhysicalObject& other) {
    if (grav) {
        double omass = other.get_mass();
        Vector2d diff = Vector2d(x-other.x, y-other.y);
        double sdist = snorm(diff);
        double dir = direction(diff);
        double coss = cos(dir);
        double sine = sin(dir);
        double tforce = (G*omass)/sdist;
        double oforce = (G*mass)/sdist;
        velocity.x -= tforce*coss/100;
        velocity.y -= tforce*sine/100;
        other.velocity.x += oforce*coss;
        other.velocity.y += oforce*sine;
    }
}

void PhysicalObject::apply_buoyancy() {
    if (buoy)
        velocity.y -= airden*g*volume/10000000;
}

void PhysicalObject::apply_velocity() {
    x += velocity.x/100;
    y += velocity.y/100;
}

void PhysicalObject::add_velocity(Vector2d vec) {
    velocity += vec;
}

void PhysicalObject::change_velocity(Vector2d vec)   {
    velocity = vec;
}

////// ======================== BALL FUNCTIONS ============================

Ball::Ball() {
    x = 0;
    y = 0;
    radius = 1;
    mass = 1;
    grav = true;
    airres = true;
    buoy = true;
    airrescons = circcons*airden*PI*radius/(mass*10000);
    volume = PI*sq(radius);
    velocity = Vector2d();
    fig = new sf::CircleShape(radius);
    ((sf::CircleShape*)fig)->setPosition(x-radius, y-radius);
    ((sf::CircleShape*)fig)->setFillColor(MBlack);
}

Ball::Ball(double ax, double ay, double r, double m, sf::Color col, bool forces) {
    x = ax;
    y = ay;
    radius = r;
    mass = m;
    grav = forces;
    airres = forces;
    buoy = forces;
    airrescons = circcons*airden*PI*radius/(mass*10000);
    volume = PI*sq(radius);
    velocity = Vector2d();
    fig = new sf::CircleShape(radius);
    ((sf::CircleShape*)fig)->setPosition(x-radius, y-radius);
    ((sf::CircleShape*)fig)->setFillColor(col);
}

char Ball::type() {
    return 'b';
}

double Ball::get_radius() {
    return radius;
}

void Ball::apply_air_resistance() {
    if (airres) {
        double acc = airrescons*snorm(velocity);
        double dir = direction(velocity);
        velocity.x -= acc*cos(dir)/500;
        velocity.y -= acc*sin(dir)/500;
    }
}

void Ball::wall_collision(double xmax, double ymax) {
    if (x < radius || x > xmax - radius) {
        velocity.x = -85*velocity.x/100;
        double sgn = sign(velocity.y);
        velocity.y -= sgn*8*g/1000;
    }
    if (y < radius || y > ymax - radius) {
        velocity.y = -85*velocity.y/100;
        double sgn = sign(velocity.x);
        velocity.x -= sgn*8*g/1000;
    }
    x = fmax(radius, fmin(x, xmax - radius));
    y = fmax(radius, fmin(y, ymax - radius));
}

void Ball::other_collision(PhysicalObject& other) {
    if (other.type() == 'b') {
        double oradius = ((Ball*)&other)->get_radius();
        Vector2d opos = other.get_pos();
        Vector2d pos = Vector2d(x, y);
        double dist = sqrt(snorm(pos - opos));
        if (dist < radius + oradius) {
            Vector2d vel = velocity;
            Vector2d ovel = other.get_velocity();
            double omass = other.get_mass();
            Vector2d vf1 = (pos-opos)*(((vel-ovel)*(pos-opos))/snorm(pos-opos));
            vf1 = vf1*(2*omass/(omass+mass));
            Vector2d vf2 = (opos-pos)*(((ovel-vel)*(opos-pos))/snorm(opos-pos));
            vf2 = vf2*(2*mass/(omass+mass));
            velocity -= vf1;
            other.add_velocity(-vf2);
        }
    }
}

void Ball::draw(sf::RenderWindow& window) {
    ((sf::CircleShape*)fig)->setPosition(x-radius, y-radius);
    window.draw(*fig);
}
