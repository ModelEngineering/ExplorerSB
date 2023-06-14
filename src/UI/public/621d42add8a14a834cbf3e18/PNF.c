#ifdef SIZE_DEFINITIONS
#define N_METABS 5
#define N_ODE_METABS 0
#define N_INDEP_METABS 5
#define N_COMPARTMENTS 1
#define N_GLOBAL_PARAMS 11
#define N_KIN_PARAMS 12
#define N_REACTIONS 10
#endif // SIZE_DEFINITIONS

#ifdef TIME
#define T  <set here a user name for the time variable> 
#endif // TIME

#ifdef INITIAL
x[0] = 0.102583;	//metabolite 'M': reactions
x[1] = 0.0899344;	//metabolite 'Pc': reactions
x[2] = 0.0640356;	//metabolite 'P': reactions
x[3] = 0.0622499;	//metabolite 'A': reactions
x[4] = 0.371178;	//metabolite 'R': reactions
#endif INITIAL

#ifdef FIXED
p[0] = 1;	//compartment 'Cell':fixed
p[1] = 1;	//global quantity 'ao':fixed
p[2] = 1;	//global quantity 'at':fixed
p[3] = 1;	//global quantity 'ah':fixed
p[4] = 1;	//global quantity 'bo':fixed
p[5] = 1;	//global quantity 'bt':fixed
p[6] = 1;	//global quantity 'bh':fixed
p[7] = 1e-05;	//global quantity 'kd':fixed
p[8] = 1;	//global quantity 'ro':fixed
p[9] = 0.0395;	//global quantity 'rt':fixed
p[10] = 0.2;	//global quantity 'do':fixed
p[11] = 0.2;	//global quantity 'dt':fixed
p[12] = 0.1;	//reaction 'Translation':  kinetic parameter 'k'
p[13] = 0.1;	//reaction 'Activation':  kinetic parameter 'k'
p[14] = 0.1;	//reaction 'Transcription':  kinetic parameter 'ao'
p[15] = 0.1;	//reaction 'Transcription':  kinetic parameter 'Kd'
p[16] = 0.1;	//reaction 'Degradation_M':  kinetic parameter 'k1'
p[17] = 0.1;	//reaction 'Degradation_Pc':  kinetic parameter 'k1'
p[18] = 0.1;	//reaction 'Degradation_P':  kinetic parameter 'k1'
p[19] = 0.1;	//reaction 'Transcription_two':  kinetic parameter 'ao'
p[20] = 0.1;	//reaction 'Transcription_two':  kinetic parameter 'Kd'
p[21] = 0.1;	//reaction 'Translation_two':  kinetic parameter 'k'
p[22] = 0.1;	//reaction 'Degradation_R':  kinetic parameter 'k1'
p[23] = 0.1;	//reaction 'Degradation_A':  kinetic parameter 'k1'
#endif FIXED

#ifdef ASSIGNMENT
x_c[0] = x[0]/p[0];	//concentration of metabolite 'M': reactions
x_c[1] = x[1]/p[0];	//concentration of metabolite 'Pc': reactions
x_c[2] = x[2]/p[0];	//concentration of metabolite 'P': reactions
x_c[3] = x[3]/p[0];	//concentration of metabolite 'A': reactions
x_c[4] = x[4]/p[0];	//concentration of metabolite 'R': reactions
#endif ASSIGNMENT

#ifdef  FUNCTIONS_HEADERS
double linearActivation(double param_0, double modif_0); 
double Transcription_2(double param_0, double modif_0, double modif_1, double param_1); 
#endif FUNCTIONS_HEADERS

#ifdef  FUNCTIONS
double linearActivation(double param_0, double modif_0) 	//linear activation
{return  param_0*modif_0;} 
double Transcription_2(double param_0, double modif_0, double modif_1, double param_1) 	//Transcription_2
{return  param_0*(1-modif_0/modif_1-param_1/modif_1+pow((pow((1-modif_0/modif_1-param_1/modif_1),2)+4*param_1/modif_1),0.5))/2;} 
#endif FUNCTIONS

#ifdef ODEs
dx[0] = Transcription_2(p[1], x_c[2], x_c[3], p[7])*p[0]-(p[4] * x_c[0]) *p[0];	// 
dx[1] = linearActivation(p[2], x_c[0])*p[0]-(p[5] * x_c[1]) *p[0];	// 
dx[2] = linearActivation(p[3], x_c[1])*p[0]-(p[6] * x_c[2]) *p[0];	// 
dx[3] = linearActivation(p[9], x_c[4])*p[0]-(p[11] * x_c[3]) *p[0];	// 
dx[4] = Transcription_2(p[8], x_c[2], x_c[3], p[7])*p[0]-(p[10] * x_c[4]) *p[0];	// 
#endif ODEs
