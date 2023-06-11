#ifndef __PARTH__
#define __PARTH__


/* simple particle struct */
typedef struct {
    // position of particle
    double x;
    double y;
    /* bound state -> depends on the id I of the receptor bound
       -1 if unbound
       I: if IP3 site is bound 
       2*I if first Ca site bound
       2*I + 1 if second Ca site bound
    */
    int bound;
} part;

// Particle constructor 
part *create_part(double x, double y);

// Particle diffusion function
void move_part(part *p, double wx, double wy, double D,
               double dt);   

#endif
