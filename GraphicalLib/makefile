CC = g++
DEPS = polygons.h pgmdrawer.h
CFLAGS = -I.

%.o: %.cpp $(DEPS)
	$(CC) -c $< $(CFLAGS)

master.o: master.cpp
	$(CC) -c $< $(CFLAGS)

exec: polygons.o master.o pgmdrawer.o
	$(CC) $^ -o $@ $(CFLAGS)
