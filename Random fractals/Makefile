CC = g++

%.o: %.cpp
	$(CC) -c $<

exec: main.o
	$(CC) $^ -o $@ -lsfml-graphics -lsfml-window -lsfml-system
	rm -f *.o
