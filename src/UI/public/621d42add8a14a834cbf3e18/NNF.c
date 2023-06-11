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
x[0] = 0.131989;	//metabolite 'M': reactions
x[1] = 0.0884607;	//metabolite 'Pc': reactions
x[2] = 0.061432;	//metabolite 'P': reactions
x[3] = 0.0656595;	//metabolite 'A': reactions
x[4] = 0.409108;	//metabolite 'R': reactions
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
p[9] = 0.0043;	//global quantity 'rt':fixed
p[10] = 0.2;	//global quantity 'do':fixed
p[11] = 0.2;	//global quantity 'dt':fixed
p[12] = 1;	//reaction 'Translation':  kinetic parameter 'parameter_2'
p[13] = 1;	//reaction 'Activation':  kinetic parameter 'parameter_3'
p[14] = 1;	//reaction 'Transcription':  kinetic parameter 'parameter_1'
p[15] = 1;	//reaction 'Transcription':  kinetic parameter 'parameter_7'
p[16] = 1;	//reaction 'Degradation_M':  kinetic parameter 'k1'
p[17] = 1;	//reaction 'Degradation_Pc':  kinetic parameter 'k1'
p[18] = 1;	//reaction 'Degradation_P':  kinetic parameter 'k1'
p[19] = 1;	//reaction 'Transcription_two':  kinetic parameter 'parameter_7'
p[20] = 1;	//reaction 'Transcription_two':  kinetic parameter 'parameter_8'
p[21] = 1;	//reaction 'Translation_two':  kinetic parameter 'parameter_9'
p[22] = 1;	//reaction 'Degradation_R':  kinetic parameter 'k1'
p[23] = 1;	//reaction 'Degradation_A':  kinetic parameter 'k1'
#endif FIXED

#ifdef ASSIGNMENT
x_c[0] = x[0]/p[0];	//concentration of metabolite 'M': reactions
x_c[1] = x[1]/p[0];	//concentration of metabolite 'Pc': reactions
x_c[2] = x[2]/p[0];	//concentration of metabolite 'P': reactions
x_c[3] = x[3]/p[0];	//concentration of metabolite 'A': reactions
x_c[4] = x[4]/p[0];	//concentration of metabolite 'R': reactions
#endif ASSIGNMENT

#ifdef  FUNCTIONS_HEADERS
double function_4_Translation(double param_0, double modif_0); 
double function_4_Activation(double param_0, double modif_0); 
double function_4_Transcription(double param_0, double param_1, double modif_0, double modif_1); 
double function_4_Transcription_two(double param_0, double param_1, double modif_0, double modif_1); 
double function_4_Translation_two(double param_0, double modif_0); 
#endif FUNCTIONS_HEADERS

#ifdef  FUNCTIONS
double function_4_Translation(double param_0, double modif_0) 	//function_4_Translation
{return  param_0*modif_0;} 
double function_4_Activation(double param_0, double modif_0) 	//function_4_Activation
{return  param_0*modif_0;} 
double function_4_Transcription(double param_0, double param_1, double modif_0, double modif_1) 	//function_4_Transcription
{return  param_0*(1-modif_0/modif_1-param_1/modif_1+pow((pow((1-modif_0/modif_1-param_1/modif_1),2)+4*param_1/modif_1),0.5))/2;} 
double function_4_Transcription_two(double param_0, double param_1, double modif_0, double modif_1) 	//function_4_Transcription_two
{return  param_1*(1-modif_0/modif_1-param_0/modif_1+pow((pow((1-modif_0/modif_1-param_0/modif_1),2)+4*param_0/modif_1),0.5))/2;} 
double function_4_Translation_two(double param_0, double modif_0) 	//function_4_Translation_two
{return  param_0/modif_0;} 
#endif FUNCTIONS

#ifdef ODEs
dx[0] = function_4_Transcription(p[1], p[7], x_c[2], x_c[3])*p[0]-(p[4] * x_c[0]) *p[0];	// 
dx[1] = function_4_Translation(p[2], x_c[0])*p[0]-(p[5] * x_c[1]) *p[0];	// 
dx[2] = function_4_Activation(p[3], x_c[1])*p[0]-(p[6] * x_c[2]) *p[0];	// 
dx[3] = function_4_Translation_two(p[9], x_c[4])*p[0]-(p[11] * x_c[3]) *p[0];	// 
dx[4] = function_4_Transcription_two(p[7], p[8], x_c[2], x_c[3])*p[0]-(p[10] * x_c[4]) *p[0];	// 
#endif ODEs
