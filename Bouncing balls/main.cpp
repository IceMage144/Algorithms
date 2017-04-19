#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <cmath>
#include "physical_objects.h"
#include "vectors.h"

using namespace std;

// Display constants
#define video_max_x 1000
#define video_max_y 600

int main() {
    sf::RenderWindow window(sf::VideoMode(video_max_x, video_max_y),
                            "Bouncing balls");
    sf::VertexArray window_bg(sf::Quads, 4);
    sf::Vector2i mousePosition;
    vector<PhysicalObject*> objs;
    Vector2d vect;
    double mx, my, rad;
    int siz;

    // Setting window background color
    window_bg[0].position = sf::Vector2f(0, 0);
    window_bg[1].position = sf::Vector2f(video_max_x, 0);
    window_bg[2].position = sf::Vector2f(video_max_x, video_max_y);
    window_bg[3].position = sf::Vector2f(0, video_max_y);

    for (int i = 0; i < 4; i++)
    window_bg[i].color = MWhite;

    // Setting test balls
    objs.resize(3);

    objs[0] = new Ball(200.0, 200.0, 20.0, 50000.0, Blue);
    objs[0]->add_velocity(Vector2d(20.0, 0.0));

    objs[1] = new Ball(400.0, 400.0, 20.0, 20.0, Red);
    objs[1]->add_velocity(Vector2d(-20.0, -20.0));

    objs[2] = NULL;

    siz = objs.size();

    // Looping
    while (window.isOpen()) {
        sf::Event event;

        // Events handling
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
            if (sf::Mouse::isButtonPressed(sf::Mouse::Left)) {
                if (objs[siz-1] == NULL) {
                    mousePosition = sf::Mouse::getPosition(window);
                    mx = mousePosition.x;
                    my = mousePosition.y;
                    objs[siz-1] = new Ball(mx, my, 30.0, MMass, MBlack, false);
                }
                else {
                    mousePosition = sf::Mouse::getPosition(window);
                    mx = mousePosition.x;
                    my = mousePosition.y;
                    objs[siz-1]->set_pos(mx, my);
                    objs[siz-1]->change_velocity(Vector2d(0.0, 0.0));
                }
            }
            else if (objs[siz-1] != NULL)
                objs[siz-1] = NULL;
        }

        // Calculating new positions
        for (int i = 0; i < siz && objs[i] != NULL; i++) {
            objs[i]->apply_e_gravity();
            objs[i]->apply_air_resistance();
            objs[i]->apply_buoyancy();
            objs[i]->wall_collision(video_max_x, video_max_y);
            for (int j = i+1; j < siz && objs[j] != NULL; j++) {
                objs[i]->other_collision(*(objs[j]));
                objs[i]->apply_g_gravity(*(objs[j]));
            }
            objs[i]->apply_velocity();
        }

        // Drawing everything
        window.clear();
        window.draw(window_bg);
        for (int i = 0; i < siz && objs[i] != NULL; i++)
            objs[i]->draw(window);
        window.display();
    }
}
