#ifndef __PHYSICAL_OBJECTS_H__
#define __PHYSICAL_OBJECTS_H__

#include <SFML/Graphics.hpp>
#include <cmath>
#include "vectors.h"

// Colors
#define MWhite sf::Color(255, 255, 255)
#define MBlack sf::Color(0, 0, 0)
#define Blue sf::Color(0, 0, 255)
#define Red sf::Color(255, 0, 0)

// Physical constants
#define TAU 6.283185
#define PI 3.141592
#define g 9.80665
#define airden 1.225
#define circcons 0.47
#define G 0.00000000006674
#define MMass 1000000000000000.0

class PhysicalObject {
public:
    double x, y, mass, airrescons, volume;
    bool grav, airres, buoy;
    sf::Drawable *fig;
    Vector2d velocity;
    // Returns the position vector of the object
    Vector2d get_pos();
    // Returns the velocity vector of the object
    Vector2d get_velocity();
    // Returns the mass of the object
    double get_mass();
    // Sets the position of the object to the input coords
    void set_pos(double, double);
    // Sets if the object is affected by gravitational forces to true/false
    void gravity(bool);
    // Sets if the object is affected by air_resistance to true/false
    void air_resistance(bool);
    // Sets if the object is affected by air buoyancy force to true/false
    void bouyancy(bool);
    // Applies the earth's gravity to the calling object's velocity
    void apply_e_gravity();
    // Applies the gravity generated by two objects' masses to themselves
    void apply_g_gravity(PhysicalObject&);
    // Applies the bouancy force acceleration to the velocity
    void apply_buoyancy();
    // Applies the velocity to object's coords
    void apply_velocity();
    // Adds a vector to the velocity vector
    void add_velocity(Vector2d);
    // Changes the velocity vector to an input vector
    void change_velocity(Vector2d);
    // Returns the type of the object
    virtual char type() = 0;
    // Applies the air resistence acceleration to the velocity
    virtual void apply_air_resistance() = 0;
    // Changes the velocity when the object collides with window's borders
    virtual void wall_collision(double, double) = 0;
    // Changes the velocity of this object and the one it's colliding
    virtual void other_collision(PhysicalObject&) = 0;
    // Draws the object's image
    virtual void draw(sf::RenderWindow&) = 0;
};

class Ball : public PhysicalObject {
    double radius;
public:
    // Constructors
    Ball();
    Ball(double x, double y, double r, double mass, sf::Color col = MBlack,
         bool forces = true);
    // Returns the radius of the ball
    double get_radius();
    // Defining Physical Object's virtual methods
    char type();
    void apply_air_resistance();
    void wall_collision(double, double);
    void other_collision(PhysicalObject&);
    void draw(sf::RenderWindow&);
};

// Returns the square of the norm of a vector
double snorm(const Vector2d);

// Returns the direction of a vector in radians
double direction(const Vector2d);

#endif
