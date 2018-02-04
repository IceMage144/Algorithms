CC = g++
DEPS = physical_objects.h vectors.h

%.o: %.cpp $(DEPS)
	$(CC) -c $<

exec: main.o physical_objects.o vectors.o
	$(CC) $^ -o $@ -lsfml-graphics -lsfml-window -lsfml-system
	rm -f *.o
