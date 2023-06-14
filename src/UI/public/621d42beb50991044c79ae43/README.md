uq is a program to sample a system of differential equations over Guassian quadrature points in a specified parameter space.

The user must specify the number of parameters and parameter ranges, as well as the number of blocks and order of the quadrature following the example in the script. The user must also explicitly code a way for the main method to interact with the system of differential equations by writing a function call to the system. There is no API.

sampling data, and final metric data will be stored in a directory named "data".

One of the following three arguments is necessary to run uq.

-s -- Sample at each grid point, process raw trace data, and integrate processed data.
-p -- Process and integrate only
-i -- Integrate only

To build, use the makefile. Note that GSL (GNU Scientific Library), openMP and MPI are required. You may need to change the flags in the makefile to include any necessary flags to compile the system of ODEs along with the solver. For example, in the example script, -lgsl -lgslcblas, and -lm are used. The code was compiled with the included makefile on Ubuntu 16.04 with OpenMP, OpenMPI, and GSL installed.

To run, type

mpirun -N int uq [flag]

where int specifies the number of nodes that will be used to sample and integrate, and [flags] are one of the three flags specified above.
