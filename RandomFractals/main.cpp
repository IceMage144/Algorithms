#include <SFML/Graphics.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>
#include <sstream>

using namespace std;

// Colors
#define MWhite sf::Color(255, 255, 255)
#define MBlack sf::Color(0, 0, 0)
#define Blue sf::Color(0, 0, 255)
#define Red sf::Color(255, 0, 0)
#define Green sf::Color(0, 255, 0)

#define W 500
#define H 500

template <typename T>
std::string NumberToString ( T Number ) {
    std::ostringstream ss;
    ss << Number;
    return ss.str();
}

void Triangle() {
    sf::RenderWindow window(sf::VideoMode(W, H), "Random fractals");
    sf::VertexArray window_bg(sf::Quads, 4);
    vector<sf::CircleShape> poly;
    vector<sf::CircleShape*> vec;
    sf::CircleShape* prev;
    sf::CircleShape* next;
    sf::Vector2f newPos;
    sf::Font font;
    sf::Text text, pause;
    bool plot = true;
    int polyLen = 3;
    int n = 1;
    int r;

    srand(time(NULL));

    if (!font.loadFromFile("font.ttf")) {
        std::cout << "Erro ao importar a fonte" << endl;
        return;
    }

    // Setting window background color
    window_bg[0].position = sf::Vector2f(0, 0);
    window_bg[1].position = sf::Vector2f(W, 0);
    window_bg[2].position = sf::Vector2f(W, H);
    window_bg[3].position = sf::Vector2f(0, H);

    for (int i = 0; i < 4; i++)
        window_bg[i].color = MWhite;

    text.setString("Counter: " + NumberToString(n));
    text.setCharacterSize(15);
    text.setFont(font);
    text.setColor(MBlack);
    text.setPosition(0, 0);

    pause.setString("Press P to pause");
    pause.setCharacterSize(15);
    pause.setFont(font);
    pause.setColor(MBlack);
    pause.setPosition(0, H-20);

    next = new sf::CircleShape(1.0);
    next->setPosition(rand()%W, rand()%H);
    next->setFillColor(Red);
    vec.push_back(next);

    poly.resize(polyLen);
    for (int i = 0; i < polyLen; i++) {
        poly[i] = sf::CircleShape(1.0);
        poly[i].setFillColor(MBlack);
    }
    poly[0].setPosition(250, 100);
    poly[1].setPosition(400, 400);
    poly[2].setPosition(100, 400);

    while (window.isOpen()) {
        sf::Event event;

        // Events handling
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::P))
                plot = false;
        }

        if (plot) {
            prev = next;
            prev->setFillColor(Blue);
            r = rand()%polyLen;
            newPos = poly[r].getPosition() + prev->getPosition();
            newPos.x /= 2.0;
            newPos.y /= 2.0;
            next = new sf::CircleShape(1.0);
            next->setPosition(newPos);
            next->setFillColor(Red);
            vec.push_back(next);
            n++;
            text.setString("Counter: " + NumberToString(n));
        }

        window.clear();
        window.draw(window_bg);
        window.draw(text);
        if (plot)
            window.draw(pause);
        for (int i = 0; i < polyLen; i++)
            window.draw(poly[i]);
        for (int i = 0; i < n; i++)
            window.draw(*(vec[i]));
        window.display();
        sf::sleep(sf::seconds(0.01));
    }
}

void Fern() {
    sf::RenderWindow window(sf::VideoMode(W, H), "Random fractals");
    sf::View view1(sf::FloatRect(-7.5, -3.75, 15, 15));
    sf::VertexArray window_bg(sf::Quads, 4);
    vector<sf::CircleShape*> vec;
    sf::CircleShape* prev;
    sf::CircleShape* next;
    sf::Vector2f newPos, mem;
    sf::Font font;
    sf::Text text, pause;
    bool plot = true;
    int n = 1;
    int r;

    srand(time(NULL));

    if (!font.loadFromFile("font.ttf")) {
        std::cout << "Erro ao importar a fonte" << endl;
        return;
    }

    view1.setRotation(180);
    window.setView(view1);

    // Setting window background color
    window_bg[0].position = sf::Vector2f(-W, -H);
    window_bg[1].position = sf::Vector2f(W, -H);
    window_bg[2].position = sf::Vector2f(W, H);
    window_bg[3].position = sf::Vector2f(-W, H);

    for (int i = 0; i < 4; i++)
        window_bg[i].color = MWhite;

    text.setString("Counter: " + NumberToString(n));
    text.setCharacterSize(15);
    text.setScale(0.04, 0.04);
    text.setRotation(180);
    text.setFont(font);
    text.setColor(MBlack);
    text.setPosition(7.5, 11.25);

    pause.setString("Press P to pause");
    pause.setCharacterSize(15);
    pause.setScale(0.04, 0.04);
    pause.setRotation(180);
    pause.setFont(font);
    pause.setColor(MBlack);
    pause.setPosition(7.5, -3);

    next = new sf::CircleShape(0.05);
    next->setPosition(0, 0);
    next->setFillColor(Red);
    vec.push_back(next);

    while (window.isOpen()) {
        sf::Event event;

        // Events handling
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::P))
                plot = false;
        }

        if (plot) {
            prev = next;
            prev->setFillColor(Green);
            r = rand()%100;
            mem = prev->getPosition();
            newPos = sf::Vector2f();
            if (r == 0) {
                newPos.x = 0.0;
                newPos.y = 0.16*mem.y;
            }
            else if (r < 8) {
                newPos.x = 0.2*mem.x - 0.26*mem.y;
                newPos.y = 0.23*mem.x + 0.22*mem.y + 1.6;
            }
            else if (r < 15) {
                newPos.x = -0.15*mem.x + 0.28*mem.y;
                newPos.y = 0.26*mem.x + 0.24*mem.y + 0.44;
            }
            else {
                newPos.x = 0.85*mem.x + 0.04*mem.y;
                newPos.y = -0.04*mem.x + 0.85*mem.y + 1.6;
            }
            next = new sf::CircleShape(0.05);
            next->setPosition(newPos);
            next->setFillColor(Red);
            vec.push_back(next);
            n++;
            text.setString("Counter: " + NumberToString(n));
        }

        window.clear();
        window.draw(window_bg);
        window.draw(text);
        if (plot)
            window.draw(pause);
        for (int i = 0; i < n; i++)
            window.draw(*(vec[i]));
        window.display();
        sf::sleep(sf::seconds(0.01));
    }
}

int main() {
    string s;
    cout << "Select the fractal you want to plot:" << endl;
    cout << "   - Sierpinski's triangle (t)" << endl;
    cout << "   - Barnsley's fern (f)" << endl;
    cin >> s;
    if (!s.compare("t"))
        Triangle();
    else if (!s.compare("f"))
        Fern();
    else
        cout << "Not a valid input" << endl;
    return 0;
}
