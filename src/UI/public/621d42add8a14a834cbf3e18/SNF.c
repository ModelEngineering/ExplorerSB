#ifdef SIZE_DEFINITIONS
#define N_METABS 4
#define N_ODE_METABS 0
#define N_INDEP_METABS 3
#define N_COMPARTMENTS 1
#define N_GLOBAL_PARAMS 7
#define N_KIN_PARAMS 7
#define N_REACTIONS 6
#endif // SIZE_DEFINITIONS

#ifdef TIME
#define T  <set here a user name for the time variable> 
#endif // TIME

#ifdef INITIAL
x[0] = 0.04305394409;	//metabolite 'M': reactions
x[1] = 0.07727418961;	//metabolite 'Pc': reactions
x[2] = 0.08021988537999999;	//metabolite 'P': reactions
#endif INITIAL

#ifdef FIXED
p[0] = 0.0659;	//metabolite 'A': fixed
p[1] = 1;	//compartment 'Cell':fixed
p[2] = 1;	//global quantity 'ao':fixed
p[3] = 1;	//global quantity 'at':fixed
p[4] = 1;	//global quantity 'ah':fixed
p[5] = 1;	//global quantity 'bo':fixed
p[6] = 1;	//global quantity 'bt':fixed
p[7] = 1;	//global quantity 'bh':fixed
p[8] = 1e-05;	//global quantity 'kd':fixed
p[9] = 0.1;	//reaction 'Translation':  kinetic parameter 'k'
p[10] = 0.1;	//reaction 'Activation':  kinetic parameter 'k'
p[11] = 0.1;	//reaction 'Transcription':  kinetic parameter 'ao'
p[12] = 0.1;	//reaction 'Transcription':  kinetic parameter 'Kd'
p[13] = 0.1;	//reaction 'Degradation_M':  kinetic parameter 'k1'
p[14] = 0.1;	//reaction 'Degradation_Pc':  kinetic parameter 'k1'
p[15] = 0.1;	//reaction 'Degradation_P':  kinetic parameter 'k1'
#endif FIXED

#ifdef ASSIGNMENT
x_c[0] = x[0]/p[1];	//concentration of metabolite 'M': reactions
x_c[1] = x[1]/p[1];	//concentration of metabolite 'Pc': reactions
x_c[2] = x[2]/p[1];	//concentration of metabolite 'P': reactions
p_c[0] = p[0]/p[1];	//concentration of metabolite 'A': fixed
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
dx[0] = Transcription_2(p[2], x_c[2], p_c[0], p[8])*p[1]-(p[5] * x_c[0]) *p[1];	// 
dx[1] = linearActivation(p[3], x_c[0])*p[1]-(p[6] * x_c[1]) *p[1];	// 
dx[2] = linearActivation(p[4], x_c[1])*p[1]-(p[7] * x_c[2]) *p[1];	// 
#endif ODEs
