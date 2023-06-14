#
LIBS= -lm
all: d4s_spont.out

d4s_spont.out: d4s_spont.c utils.o clist.o part.o receptor.o cell.o
	gcc -O2 -g -Wall -o d4s_spont.out d4s_spont.c utils.o clist.o part.o receptor.o cell.o $(LIBS)

utils.o: utils.h utils.c
	gcc -c -O2 -g -Wall utils.c
clist.o: clist.h clist.c
	gcc -c -O2 -g -Wall clist.c
part.o: part.h part.c
	gcc -c -O2 -g -Wall part.c
receptor.o: receptor.h receptor.c
	gcc -c -O2 -g -Wall receptor.c
cell.o: cell.h cell.c 
	gcc -c -O2 -g -Wall cell.c


clean:
	rm -f *.o *.out 
