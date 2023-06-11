#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "part.h"


part *create_part(double x, double y) {
    // a particle (IP3 or Ca) is defined by its position in x and y and its bound state (see part.h fore details)
    part *p = (part *) malloc(sizeof(part));
    p->x = x;
    p->y = y;
    p->bound = -1;
    return p;
}

void move_part(part *p, double wx, double wy, double D, double sdt) {
    // Definition of Particles diffusion
    double nx, ny;
    if (D < 0)     
    {
	// if diffusion defined as infinite
        nx = wx * box_noise();
        ny = wy * box_noise();

    }
    else {
	// Brownian dynamics
        nx = p->x + sdt * D * white_noise();
        ny = p->y + sdt * D * white_noise();    
    }

    if (nx < 0) nx = 0;
    if (nx > wx) nx = wx;
    if (ny < 0) ny = 0;
    if (ny > wy) ny = wy;

    p->x = nx;
    p->y = ny;
}


