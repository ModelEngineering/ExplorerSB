objects = sample.o abscissa.o uq_ET.o uq_processTrace.o

uq: $(objects)
	mpicc -o uq $(objects) -lgsl -lgslcblas -lm -fopenmp

uq_ET.o: uq_ET.c
	cc -c uq_ET.c -lgsl -lgslcblas -lm
uq_processTrace.o: uq_processTrace.c
	cc -c uq_processTrace.c
sample.o: sample.c
	mpicc -c sample.c -fopenmp
abscissa.o: abscissa.c
	cc -c abscissa.c -lm

.PHONY: clean
clean:
	rm uq $(objects)
	rm -rf data
