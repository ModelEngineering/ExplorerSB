#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "clist.h"
#include "params.h"
#include "utils.h"
#include "cell.h"


/*
 Particle-based IP3R-mediated calcium signaling model
Implemented by A. DENIZOT, published in Denizot et al, 2019
audrey.denizot@inria.fr
 */



/*
 This code is a tool to investigate spontaneous calcium signals
 depending on the size of IP3R clusters and on Ca diffusion
 */


int main(int argc, char **argv) {

    //Parameters initialization
    params *pr = (params *) malloc(sizeof(params));

    // number of IP3R
    pr->nip3r = 1000;

    // size of affinity zone for IP3R
    pr->size = 1;

    // cell size 
    pr->wx = 200;
    pr->wy = 200;

    // simulation time steps
    pr->dt = 0.01;
    double dt = pr->dt;
    pr->sdt = sqrt(pr->dt);


    double Dca = atof(argv[2]);
    double Dip3 = atof(argv[3]);

    // Diffusion
    pr->Dca = Dca;
    pr->Dip3 = Dip3;

    // Initial amount of Ca and IP3
    int ca0 = 50;
    int free_ca = ca0;
    int ip0 = 15;

    //ode parameters - see model 
    pr->mu = 50 * dt;
    pr->alpha = 1.0 * dt;
    pr->gamma = ca0 * dt / 1000;
    pr->rgamma = atof(argv[4]);
    pr->a1 = 1.0 * dt;
    pr->b1 = 0.1 * dt;
    pr->a2 = 1.0 * dt;
    pr->b2 = 0.1 * dt;
    pr->a3 = 0.1 * dt;
    pr->b3 = 0.1 * dt;
    pr->beta = 0.01 * dt;

    // plc-related parameters 
    pr->nplc = 1000;
    pr->delta = 0.1 * dt;

    // Random number generation (see utils.c)
    int seed = atoi(argv[argc - 1]);
    initialize_rng(seed);


    char map_name[100];
    strcpy(map_name, argv[1]);

    /*
     cell creation (allocation + parameters)
     initial amount of particles creation
     */
    cell *c = create_cell(ip0, ca0, free_ca, pr);
    /*
     receptors initialization
     from map file loaded, cl1000.map in the example
     */
    FILE *f = fopen(map_name, "r");
    if (f == NULL) {
        printf("receptor map doesn't exist");
        exit(EXIT_FAILURE);
    }
    int i;
    for (i = 0; i < pr->nip3r; i++) {

        double x, y;
        fscanf(f, "%lg %lg\n", &x, &y);
        int ix = (int) floor(x / pr->size);
        int iy = (int) floor(y / pr->size);
        int size = pr->size;
        receptor *r = create_receptor(ix, iy, size);
        c->recs[i] = r;
        int iwx = (int) floor(pr->wx / pr->size) + 1;
        c->rmap[ix + iwx * iy] = i;
    }

    // Start main loop until time of simulation (total_time) is reached

    double t = 0.0;
    double total_time = 100000.0;
    
    
    while (t < total_time) {
        // Main loop
        cycle(c);
        // Increase time step
        t += pr->dt;

        /*
         display information at time t
	 - t
         - # free Ca via list size
         - # IP3 via list size
         - # of open IP3R
         */
	
	printf("%lg %d %d %d\n", t, c->free_ca, c->ip3->size, get_bindings(c));


    }
    return 0;
}
