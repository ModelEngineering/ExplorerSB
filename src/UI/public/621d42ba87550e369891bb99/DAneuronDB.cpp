#include <stdio.h>
#include <stdlib.h>
#include "mex.h"    
 #include "matrix.h"   
 #include <string.h> 
#include <math.h>
#include <time.h>
 #include <iostream>

//-------------parameters --------------------------
double gL=0.18, gbarK=1, gbarCa=2.5, gbarKCa=7.8, gSNa=0.13; // maximal conductances for pacemaking
double gbarDR=0, gbarNa=0, gNa; // maximal conductances for spike producing current
// set gbarDR=2 and gbarNa=50 to add spikeproducing currents
double gDR, gCa, gKCa, gK; //conductances
double gampa, gnmda, gbarnmda, ggaba; //synaptic conductances
double nmdasig, ampasig, allgaba; //synaptic activation functions
double k=160, buf=0.00023, zF=0.019298, tc=0.52, r=0.2; //for Ca equation
double Mg=0.5, me=0.062; //for gnmda 
double EL=-35, EK=-90, ECa=50, ENMDA=0, EAMPA=0, EGABA=-90, ENa=55; // reversal potentials
double VHK=-10, VSK=7; //K current
double th=0.05; //for Na curent
double Vcah=-52, Sca=3; // for Ca current
double vhna=-50, slna=5; // for subthreshold Na current
double aact=1., tades=6.1, adesrel=40, adeact=1.6, nact=7., ndeact=170.; //for AMPA 
double nmdathresh=0.2, nmdasl=0.03, ampathresh=0.2, ampasl=0.03; //for NMDA
double dt=0.02, TT, tgl; //step, total time, global time
int N, Neq=9; // number of steps, number of equations
double inp; // input
double caleak=0.1; // fraction of Ca current in a leak current
double Iapp; //applied current
double vhh=-95, slh=8, th0=625, vtauh=-112, Eh=-20, gh, gbarh; // for Ih current
double *y, *f;
//---------------------------------------------------------
void system (void)
{    
// Na current
double alpham=-0.32*(y[0]+39)/(exp(-(y[0]+39)/4)-1);
double betam=0.28*(y[0]+4)/(exp((y[0]+4)/5)-1);
double minf=alpham/(alpham+betam);
double alphah=0.2*th*exp(-((y[0]+47.)/18.));
double betah=25.*th/(1.+(exp(-(y[0]+24.)/5.)));
gNa=gbarNa*(pow(minf,3))*y[5];
// Delayed rectifier K current
double alphan=-0.0032*(y[0]+5.)/(exp(-(y[0]+5.)/10.) - 1.);
double betan=0.05*exp(-((y[0]+10.)/16.));
double nsqr=y[4]*y[4];
gDR=gbarDR*(nsqr*nsqr);
// for K current
gK=gbarK/(1. + exp(-(y[0]-VHK)/VSK));
// for Ca current
double alphac=((fabs(y[0]-Vcah))>0.00001)? (-0.0032*(y[0]-Vcah)/(exp(-(y[0]-Vcah)/Sca) - 1.)) : (-0.0032*0.00001/(exp(-0.00001/Sca)-1.));
double betac=0.05*exp(-(y[0]-Vcah+5)/40.);
double csinf=alphac/(alphac+betac);
double csqr=csinf*csinf;
gCa=gbarCa*(csqr*csqr);
// for Ca-dependent K current
double ksq=k*k;
double casq=y[3]*y[3];
gKCa=gbarKCa*(casq*casq)/((casq*casq) + (ksq*ksq));
// for NMDAR current
nmdasig=1/(1+exp(-(y[1]-nmdathresh)/nmdasl));
gnmda=gbarnmda/(1+0.28*Mg*exp(-me*y[0]));
// for AMPAR current
ampasig=1/(1+exp(-(y[2]*y[6]-ampathresh)/ampasl));
// for subthreshold Na current
double na=1/(1+exp(-(y[0]-vhna)/slna));
// for H-current
double hinf=1/(1+exp((y[0]-vhh)/slh));
double tauh=th0*exp(0.075*(y[0]-vtauh))/(1+exp(0.083*(y[0]-vtauh)));
gh=gbarh*y[7];

f[0]= gnmda*(ENMDA-y[0])+ gampa*(EAMPA-y[0])+ ggaba*(EGABA-y[0]) + gCa*(ECa-y[0])
+ (gKCa+gK+gDR)*(EK-y[0])+ gL*(EL-y[0])+ gNa*(ENa-y[0]) + gSNa*na*(ENa-y[0])
+ gh*(Eh-y[0])+Iapp;// Voltage
f[1]=inp*(1-y[1])/nact-(1-inp)*y[1]/ndeact; // NMDA
f[2]=inp*(1-y[2])/aact-(1-inp)*y[2]/adeact; // AMPA activtion
f[3]= 2.*buf*((gCa+caleak*gL)*(ECa - y[0])/zF - y[3]/tc)/r; //Ca
f[4]= alphan*(1.-y[4])-betan*y[4]; // DR
f[5]= alphah*(1.-y[5])-betah*y[5]; // Na
f[6]=(1-inp)*(1-y[6])/adesrel-inp*y[6]/tades; //AMPA desensitization
f[7]= (hinf-y[7])/tauh; //Ih
}
void euler(double ggaba_1, double gbarnmda_1, double gampa_1)
{
 int i=0;
 ggaba=ggaba_1;
 gbarnmda=gbarnmda_1;
 gampa=gampa_1;
 system();
  while (i<Neq){y[i]+=dt*f[i]; i++;}
} 

//nlhs - Number of expected output mxArrays
//plhs - Array of pointers to the expected output mxArrays
//nrhs - Number of input mxArrays
//prhs - Array of pointers to the input mxArrays. Do not modify any prhs values in your MEX-file. Changing the data in these read-only mxArrays can produce undesired side effects.

void mexFunction( int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[] )
{
mxArray *tempy = mxCreateDoubleMatrix(1,Neq,mxREAL);
y=mxGetPr(tempy);
mxArray *tempf = mxCreateDoubleMatrix(1,Neq,mxREAL);
f=mxGetPr(tempf);
// inputs
double *ggaba1, *gbarnmda1,*gampa1, *Iapp1;      
TT   = *(mxGetPr(prhs[0]));
ggaba1 = (mxGetPr(prhs[1]));
gbarnmda1 = (mxGetPr(prhs[2]));
gampa1 = (mxGetPr(prhs[3]));
gbarh = *(mxGetPr(prhs[4]));
Iapp1 = (mxGetPr(prhs[5]));

int kk;
tgl=0;
dt=0.02;
N=(int)(TT/dt);
// outputs    
double *Vm;  
double *Ca;
plhs[0] = mxCreateDoubleMatrix(1,N,mxREAL);
plhs[1] = mxCreateDoubleMatrix(1,N,mxREAL);
Vm = mxGetPr(plhs[0]);
Ca = mxGetPr(plhs[1]);

y[0]=-60; y[1]=0.; y[2]=0; y[3]=40; y[4]=0; y[5]=0; y[6]=1.; y[7]=0.06; // initial conditions
	
kk=0;
for(int i=0; i<N; i++)
{
tgl+=dt;
inp=0;
ggaba=ggaba1[i];
Iapp=Iapp1[i];
gbarnmda=gbarnmda1[i];
gampa=gampa1[i];
euler(ggaba,gbarnmda,gampa);
Vm[kk]=y[0];
Ca[kk]=y[3];

if(kk>N) break;
kk++;
   }
   return;
} // end mexFunction()
