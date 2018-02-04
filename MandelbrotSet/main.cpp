#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;

#define PIXEL_SIZE 2
#define W 800

class IPoint {
    sf::RectangleShape rect;
public:
    IPoint() {
        rect = sf::RectangleShape();
    }
    IPoint(sf::Vector2f pos, sf::Color col) {
        rect = sf::RectangleShape();
        rect.setFillColor(col);
        rect.setPosition(pos);
        rect.setSize(sf::Vector2f(PIXEL_SIZE, PIXEL_SIZE));
    }
    void draw(sf::RenderWindow& window) {
        window.draw(rect);
    }
};


int main() {
    sf::RenderWindow window(sf::VideoMode(W, W), "Mandelbrot set");
    sf::VertexArray window_bg(sf::Quads, 4);
    sf::View view1(sf::FloatRect(-W, -W, 2*W, 2*W));
    vector<sf::Color> croma;
    //vector<IPoint> points;
    IPoint point;
    vector<float> val;
    float ptrx = -W, ptry = -W;
    int n = 0;
    bool plot = true;

    // Setting window background color
    //window_bg[0].position = sf::Vector2f(-W, -W);
    //window_bg[1].position = sf::Vector2f(W, -W);
    //window_bg[2].position = sf::Vector2f(W, W);
    //window_bg[3].position = sf::Vector2f(-W, W);

    //for (int i = 0; i < 4; i++)
    //    window_bg[i].color = sf::Color(0, 0, 0);

    //window.draw(window_bg);

    for (int i = 0; i < 255; i += 15)
        croma.push_back(sf::Color(i, i, 255));
    for (int i = 255; i > 0; i -= 15)
        croma.push_back(sf::Color(255, 255, i));
    for (int i = 255; i >= 0; i -= 15)
        croma.push_back(sf::Color(i, i, 0));

    window.setView(view1);

    val.resize(2);
    val[0] = 0.0;
    val[1] = 0.0;

    while (window.isOpen()) {
        sf::Event event;

        // Events handling
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
        }

        if (plot) {
            int iterr = 0;
            float wptrx = 2*ptrx/W;
            float wptry = 2*ptry/W;
            float dist = 0.0;
            float tmp = 0.0;
            val[0] = 0.0;
            val[1] = 0.0;
            while (dist < 4 && iterr < 51) {
                tmp = val[0]*val[0] - val[1]*val[1] + wptrx;
                val[1] = 2*val[0]*val[1] + wptry;
                val[0] = tmp;
                dist = val[0]*val[0] + val[1]*val[1];
                iterr++;
            }
            point = IPoint(sf::Vector2f(ptrx, ptry), croma[iterr]);
            //points.push_back(IPoint(sf::Vector2f(ptrx, ptry), croma[iterr]));
            if (ptrx > W && ptry > W)
                plot = !plot;
            ptrx += PIXEL_SIZE;
            if (ptrx > W) {
                ptrx = -W;
                ptry += PIXEL_SIZE;
            }
            n++;
        }

        //window.clear();
        //for (int i = 0; i < n; i++)
        //points[n-1].draw(window);
        point.draw(window);
        window.display();
    }
    return 0;
}
