#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include "utils.h"

int seed;

long SEED, Tp;

double ran1(long *idum)                     
{
    /*
	Pseudo-random nb generator:
	Park and Miller algorithm
	with Bays and Durham shuffling algo
	-> Numerical recipies book, Press et al, second edition page 280
    */
    int IA = 16807;
    double IM = 2147483647;
    double AM;
    int IQ = 127773;
    int IR = 2836;
    int NDIV;
    double EPS = 1.2e-7;
    double RNMX;
    double NTAB = 32;

    int j;
    long k;
    static long iy = 0;
    static long iv[32];
    double temp;

    NDIV = (1 + (IM - 1) / NTAB);
    AM = (1.0 / IM);
    RNMX = (1.0 - EPS);

    if (*idum <= 0 || !iy) {
        if (-(*idum) < 1) *idum = 1;
        else *idum = -(*idum);
        for (j = NTAB + 7; j >= 0; j--) {
            k = (*idum) / IQ;
            *idum = IA * (*idum - k * IQ) - IR * k;
            if (*idum < 0) *idum += IM;
            if (j < NTAB) iv[j] = *idum;
        }
        iy = iv[0];
    }
    k = (*idum) / IQ;
    *idum = IA * (*idum - k * IQ) - IR * k;
    if (*idum < 0) *idum += IM;
    j = iy / NDIV;
    iy = iv[j];
    iv[j] = *idum;
    if ((temp = AM * iy) > RNMX) return RNMX;
    else return temp;
}

double gasdev(long *idum) {
    /*
	Normal (Gaussian) Deviates
	-> Numerical recipies book, Press et al, second edition page 288
    */
    static int iset = 0;
    static double gset;
    double fac, r, v1, v2;

    if (iset == 0) {
        do {
            v1 = 2.0 * ran1(idum) - 1.0;
            v2 = 2.0 * ran1(idum) - 1.0;
            r = v1 * v1 + v2 * v2;
        } while (r >= 1.0 || r == 0.0);
        fac = sqrt(-2.0 * log(r) / r);
        gset = v1 * fac;
        iset = 1;
        return v2 * fac;
    } else {
        iset = 0;
        return gset;
    }
}


void initialize_rng(long seed) {
    // seed random number generator 
    if (seed == 0) {
        SEED = -(time(&Tp));      
        SEED %= 100000;
    }
    else
        SEED = -seed;              

}


double box_noise()            
{
    //uniform law between 0 and 1
    return (ran1(&SEED));
}

double white_noise()          
{
    // Uncorrelated gaussian law
    return (gasdev(&SEED));
}




