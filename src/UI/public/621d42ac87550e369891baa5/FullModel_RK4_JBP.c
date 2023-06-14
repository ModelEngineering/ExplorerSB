#include <stdio.h>
#include <stdlib.h> /* for the rand function */
#include <math.h>
#include "nrutil.h"

/*

This is code used in:

E. Barreto and J.R. Cressman, "Ion Concentration Dynamics as a Mechanism for Neuronal Bursting",
Journal of Biological Physics 37, 361-373 (2011).

Link to the paper: http://www.springerlink.com/content/v52215p195159211/
Author-generated version available at: http://arxiv.org/abs/1012.3124


*/


const double PIOVERTWO = 1.57079632679489661923;
const double PI = 3.14159265358979323846;
const double TWOPI = 6.28318520717958647692;

void FullModel(double x, double y[], double dydx[]);
void rk4(double [], double [], int, double, double, double [],
    void (*derivs)(double, double [], double []));

/* Global variables */
double alpha_n, alpha_m, alpha_h, beta_n, beta_m, beta_h, m_inf,
	Kin, Naout, E_k, E_na, E_cl, E_ca, Ina, Ik, Icl, Itildepump, Itildeglia, Itildediffusion,
	Cm, g_na, g_naL, g_k, g_kL, g_ahp, g_clL, g_ca, gamma, beta, tau, phi,
	rho, glia, epsilon, kbath;

main()
{
	int i, j, seconds, totalsteps, skip;
    double *y, *derivs, time, timestep;
    FILE *fp;

	printf("Integrate for how many seconds? ");
	scanf("%ld", &seconds);

	/*
	y[1]=V, the membrane voltage
	y[2]=n, gating variable
	y[3]=h, gating variable
	y[4]=[K]_o, the extracellular potassium concentration
	y[5]=[Na]_i, the intracellular sodium concentration
	*/
	y = dvector(1, 5);
    derivs = dvector(1, 5);

    /* set initial conditions
	y[1]=-50;
	y[2]=0.08553;
	y[3]=0.96859;
	y[4]=7.8;
	y[5]=15.5;*/

	y[1]=-74.138;
	y[2]=0.0389;
	y[3]=0.9923;
	y[4]=40.0;
	y[5]=38.55;

	/* set parameters */

	tau = 1000.0;
	beta = 7.0;

	/* type A 
	gamma = 0.044494542;
	rho = 1.25;
	glia = 200.0/3.0;
	epsilon = 4.0/3.0;
	kbath = 8.0; */

	/* type B 
	gamma = 0.044494542;
	rho = 1.25;
	glia = 20.0;
	epsilon = 0.133;
	kbath = 22.0; */

	/* type C
	gamma = 0.044494542;
	rho = 1.25;
	glia = 6.0;
	epsilon = 0.7;
	kbath = 22.0; */

	/* type D
	gamma = 1.0;
	rho = 0.9;
	glia = 10.0;
	epsilon = 0.5;
	kbath = 20.0;*/

	/* type E
	gamma = 0.25;
	rho = 0.9;
	glia = 10.0;
	epsilon = 0.5;
	kbath = 20.0; */

	gamma = 0.25;
	rho = 0.9;
	glia = 10.0;
	epsilon = 0.5;
	kbath = 20.0;

	E_cl = 26.64*log(6.0/130.0);
	E_ca = 120.0;

	Cm = 1.0;
	g_na = 100.0;
	g_naL = 0.0175;
	g_k = 40.0;
	g_kL = 0.05;
	g_ahp = 0.01;
	g_clL = 0.05;
	g_ca = 0.1;
	phi = 3.0;

	/* integration parameters */
    time = 0.0;
	timestep = 0.01;
	skip = 100;
	totalsteps = (int)(1000*seconds/timestep);

	/* preintegrate to remove transients */
	for (j=1; j<=100000; j++) {
		FullModel(time, y, derivs);
		rk4(y, derivs, 5, time, timestep, y, FullModel);
		time = time + timestep;
	}

	time = 0.0;
 
    fp = fopen("dataoutput.dat", "w");
	fprintf(fp, "%lf %lf %lf %lf\n", time/1000.0, y[1], y[4], y[5]);
	/* fprintf(fp, "%lf %lf %lf %lf %lf %lf %lf\n", time, y[1], y[2], y[3], y[4], y[5], y[6]); */

    for (i=1; i<=(totalsteps/skip); i++) {

		for (j=1; j<=skip; j++) {
			FullModel(time, y, derivs);
			rk4(y, derivs, 5, time, timestep, y, FullModel);
			time = time + timestep;
		}

		fprintf(fp, "%lf %lf %lf %lf\n", time/1000.0, y[1], y[4], y[5]);
		/* fprintf(fp, "%lf %lf %lf %lf %lf %lf %lf\n", time, y[1], y[2], y[3], y[4], y[5], y[6]); */
		fflush(fp);
	}

    fclose(fp);

    printf("Done!\n"); 
    
    return 0;
}

/*****/

void FullModel(double x, double y[], double dydx[])
{
	alpha_n = 0.01 * (y[1]+34.0)/( 1.0 - exp(-0.1 * (y[1]+34.0)) );
    beta_n = 0.125 * exp(-(y[1]+44.0)/80.0);
	alpha_m = 0.1 * (y[1]+30.0)/( 1.0 - exp(-0.1 * (y[1]+30.0)) );
	beta_m = 4.0 * exp(-(y[1]+55.0)/18.0);
	alpha_h = 0.07 * exp(-(y[1]+44.0)/20.0);
	beta_h = 1.0/( 1.0 + exp(-0.1 * (y[1]+14.0)) );

	m_inf = alpha_m/(alpha_m + beta_m);

	Kin = 158.0-y[5];
	Naout = 144.0-beta*(y[5]-18.0);

	E_k = 26.64 * log((y[4]/Kin));
	E_na = 26.64 * log((Naout/y[5])); 

	Ina = g_na*(m_inf*m_inf*m_inf)*y[3]*(y[1]-E_na) + g_naL*(y[1]-E_na);
	Ik = (g_k*y[2]*y[2]*y[2]*y[2])*(y[1]-E_k) + g_kL*(y[1]-E_k);
	Icl = g_clL*(y[1]-E_cl);

	Itildepump = (rho/(1.0+exp((25.0-y[5])/3.0)))*(1/(1+exp(5.5-y[4])));
	Itildeglia = (glia/(1.0+exp((18.0-y[4])/2.5)));
	Itildediffusion = epsilon*(y[4]-kbath);

	/*
	y[1]=V, the membrane voltage
	y[2]=n, gating variable
	y[3]=h, gating variable
	y[4]=[K]_o, the extracellular potassium concentration
	y[5]=[Na]_i, the intracellular sodium concentration
	*/
	dydx[1] = (1.0/Cm)*(-Ina -Ik -Icl);
	dydx[2] = phi*(alpha_n*(1-y[2])-beta_n*y[2]);
	dydx[3] = phi*(alpha_h*(1-y[3])-beta_h*y[3]);
	dydx[4] = (1/tau)*(gamma*beta*Ik -2.0*beta*Itildepump -Itildeglia -Itildediffusion);
	dydx[5] = (1/tau)*(-gamma*Ina -3.0*Itildepump);

}

