CC = g++
CFLAGSF = -I../../SFML-2.4.0/include
CFLAGSS = -L../../SFML-2.4.0/lib
DEPS = physical_objects.h vectors.h

%.o: %.cpp $(DEPS)
	$(CC) -c $< $(CFLAGSF)

teste: main.o physical_objects.o vectors.o
	$(CC) $^ -o $@ $(CFLAGSS) -lsfml-graphics -lsfml-window -lsfml-system
	rm -f *.o

exec: teste
	export LD_LIBRARY_PATH=./../../SFML-2.4.0/lib && ./teste
