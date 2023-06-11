#ifndef __PARAMS__
#define __PARAMS__

typedef struct {
    // number of IP3R
    int nip3r;
    // number of PLC
    int nplc;
    // Size of IP3R affinity zone
    int size;

    // Environment size 
    double wx;
    double wy;

    // Diffusion parameters 
    double Dca;
    double Dip3;

    // Temporal parameters
    double dt;
    double sdt;

    // ODE parameters 
    double mu;
    double alpha;
    double a1, b1, a2, b2, a3, b3;
    double beta;
    double delta;
    double gamma;
    double rgamma;
} params;

#endif
