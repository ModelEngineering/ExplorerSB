#include <stdio.h>
#include <stdlib.h>
#include "mex.h"         
#include "matrix.h"      
#include <string.h> 
#include <math.h>
#include <time.h>
#include <iostream>

//---------- parameters ----------------------
double dt=0.02, TT, tgl; //step, total time, global time
int N, NG=30, Neq=8+NG*4;// # of steps,  # of GABA neurons, # of equations
double gL=0.18, gbarK=1, gbarCa=2.5, gbarKCa=7.8, gSNa=0.13; //maximal conductances
double gCa, gKCa, gK; //conductances
double gampa=0, gnmda, gbarnmda, ggaba; //synaptic conductances
double nmdasig, ampasig, allgaba; //synaptic activation functions
double EL=-35, EK=-90, ENa=55, ECa=50, ENMDA=0, EAMPA=0, EGABA=-90; // reversal potentials
double k=160, buf=0.00023, zF=0.019298, tc=0.52, r=0.2; //for Ca  balance equation
double caleak=0.1; // fraction of Ca current in a leak current
double Vcah=-52, Sca=3; // for Ca current
double VHK=-10, VSK=7; //for K current
double vhna=-50, slna=5; // for subthreshold Na current
double aact=1., tades=6.1, adesrel=40, adeact=1.6, nact=7., ndeact=170.; //for AMPA current
double nmdathresh=0.2, nmdasl=0.03, ampathresh=0.2, ampasl=0.03; //for NMDA current
double Mg=0.5, me=0.062; //for gnmda 
double amg, bmg, minfgg, ang, bng, ahg, bhg, gnmdagg, gspikeg, vgnz; // for GABA population
double glg=0.1, gna=22, gdrg=7, tng=1, thg=5, tbn=0.7, as=12, bs=0.1; // for GABA population
double gampag=0, gnmdabarg=0; //GABA synaptic conductances
double inp, Iapp; // synaptic input, input current

double *y, *f;
double *glg1=new double[NG];

void system (void)
{
// for K current    
gK=gbarK/(1. + exp(-(y[0]-VHK)/VSK)); 
// for subthreshold Na current
double na=1/(1+exp(-(y[0]-vhna)/slna));
// for Ca current
double alphac=((fabs(y[0]-Vcah))>0.00001)? (-0.0032*(y[0]-Vcah)/(exp(-(y[0]-Vcah)/Sca) - 1.)) : (-0.0032*0.00001/(exp(-0.00001/Sca)-1.));
double betac=0.05*exp(-(y[0]-Vcah+5)/40.);
double csinf=alphac/(alphac+betac);
double csqr=csinf*csinf;
gCa=gbarCa*(csqr*csqr); // Ca conductance
// for Ca-dependent K current
double ksq=k*k; // K^2
double casq=y[1]*y[1]; // Ca^2
gKCa=gbarKCa*(casq*casq)/((casq*casq) + (ksq*ksq)); //SK conductance
// for NMDAR current
double nmdasig=1/(1+exp(-(y[4]-nmdathresh)/nmdasl));
gnmda=gbarnmda/(1+0.28*Mg*exp(-me*y[0])); //NMDA conductance
//for AMPAR current
double ampasig=1/(1+exp(-(y[2]*y[3]-ampathresh)/ampasl));

// Cumulative activation of GABAR by all GABA neurons in a population
allgaba=0;
for (int ig=0; ig<NG; ig++){
	allgaba+=y[8+ig*4];
}
allgaba/=NG;

f[0]= gnmda*nmdasig*(ENMDA-y[0])+ gampa*ampasig*(EAMPA-y[0])+ ggaba*allgaba*(EGABA-y[0]) + gCa*(ECa-y[0])
+ (gKCa+gK)*(EK-y[0])+ gL*(EL-y[0])+ gSNa*na*(ENa-y[0])+Iapp;// Voltage
f[1]= 2.*buf*((gCa+caleak*gL)*(ECa - y[0])/zF - y[1]/(1*tc))/r; //Ca
f[2]=inp*(1-y[2])/aact-(1-inp)*y[2]/adeact; // AMPA activation
f[3]=(1-inp)*(1-y[3])/adesrel-inp*y[3]/tades; //AMPA desensitization
f[4]=inp*(1-y[4])/nact-(1-inp)*y[4]/ndeact; // NMDA

// model of GABA neurons
for (int ig=0; ig<NG; ig++)
{
// for Na current	
double amg=0.1*(y[5+ig*4]+30.0)/(1.0-exp(-(y[5+ig*4]+30.0)/10.0));
double bmg=4.0*exp(-(y[5+ig*4]+55.0)/18.0);
double minfgg=amg/(amg+bmg);
double ahg=0.07*exp(-(y[5+ig*4]+53.0)/20.0);
double bhg=1.0/(1.0+exp(-(y[5+ig*4]+23.0)/10.0));
// for K current
double ang=0.01*(y[5+ig*4]+29.0)/(1.0-exp(-(y[5+ig*4]+29.0)/10.0));
double bng=tbn*0.125*exp(-(y[5+ig*4]+39.0)/80.0);
// NMDA conductance on GABA neuron
double gnmdagg=gnmdabarg/(1+0.28*Mg*exp(-me*y[5+ig*4]));
// GABA "release" depending on GABA voltage
double gspikeg=1/(1+exp(-y[5+ig*4]/2));

f[5+ig*4]=gnmdagg*nmdasig*(ENMDA-y[5+ig*4]) + gampag*ampasig*(EAMPA-y[5+ig*4])
	-glg1[ig]*(y[5+ig*4]+51)-gna*pow(minfgg,3)*y[7+ig*4]*(y[5+ig*4]-55)
    -gdrg*pow(y[6+ig*4],4)*(y[5+ig*4]+90)+Iapp;
f[6+ig*4]=tng*(ang*(1-y[6+ig*4])-bng*y[6+ig*4]); // K receptor activation 
f[7+ig*4]=thg*(ahg*(1-y[7+ig*4])-bhg*y[7+ig*4]); //Na receptor activation
f[8+ig*4]=as*gspikeg*(1-y[8+ig*4])-bs*(1-gspikeg)*y[8+ig*4]; // GABA receptor activation on the DA neuron
}

}
void euler(double ggaba_1, double gbarnmda_1)
{
ggaba=ggaba_1;
gbarnmda=gbarnmda_1;
 int i=0;
 system();
  while (i<Neq){y[i]+=dt*f[i]; i++;}
} 

//nlhs - Number of expected output mxArrays
//plhs - Array of pointers to the expected output mxArrays
//nrhs - Number of input mxArrays
//prhs - Array of pointers to the input mxArrays 

void mexFunction( int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[] )
{	
mxArray *tempy = mxCreateDoubleMatrix(1,Neq,mxREAL);
y=mxGetPr(tempy);    
mxArray *tempf = mxCreateDoubleMatrix(1,Neq,mxREAL);
f=mxGetPr(tempf);

TT   = *(mxGetPr(prhs[0]));
double *input, *ggaba1, *gbarnmda1;
input = mxGetPr(prhs[1]);
ggaba1 = (mxGetPr(prhs[2]));
gbarnmda1 = (mxGetPr(prhs[3]));
Iapp = *(mxGetPr(prhs[4]));

int kk;
tgl=0; dt=0.02; N=(int)(TT/dt);
    
double *Vm, *allgaba1, *Ca, *nmdasig1, *mas_Vgaba;  

plhs[0] = mxCreateDoubleMatrix(1,N,mxREAL);
plhs[1] = mxCreateDoubleMatrix(1,N,mxREAL);
plhs[2] = mxCreateDoubleMatrix(1,N,mxREAL);
plhs[3] = mxCreateDoubleMatrix(1,N,mxREAL);
plhs[4] = mxCreateDoubleMatrix(1,NG*N,mxREAL);
    
Vm = mxGetPr(plhs[0]);     
allgaba1 = mxGetPr(plhs[1]);
Ca = mxGetPr(plhs[2]);
nmdasig1 = mxGetPr(plhs[3]);
mas_Vgaba = mxGetPr(plhs[4]);   

 for(int i=0; i<NG;i++)
{ for(int j=0;j<N;j++) mas_Vgaba[i*N+j] = 0; } 

double glg_m[30];

 glg_m[0]=0.0555; glg_m[1]=0.0675; glg_m[2]=0.0250; glg_m[3]=0.0698; glg_m[4]=0.0322;
 glg_m[5]=0.0701; glg_m[6]=0.037; glg_m[7]=0.0647; glg_m[8]=0.0264; glg_m[9]=0.0743; 
 glg_m[10]=0.0592; glg_m[11]=0.0417; glg_m[12]=0.0308; glg_m[13]=0.0480; glg_m[14]=0.0353;
 glg_m[15]=0.0745; glg_m[16]=0.0698; glg_m[17]=0.0706; glg_m[18]=0.0517; glg_m[19]=0.0316;
 glg_m[20]=0.0671; glg_m[21]=0.0462; glg_m[22]=0.0648; glg_m[23]=0.0273; glg_m[24]=0.0325;
 glg_m[25]=0.0692; glg_m[26]=0.073; glg_m[27]=0.054; glg_m[28]=0.0383; glg_m[29]=0.0539;


// initial conditions  
 y[0]=-60.; y[1]=50.; y[2]=0; y[3]=1; y[4]=0;
 for (int ig=0; ig<NG; ig++){y[5+ig*4]=-40; y[6+ig*4]=0; y[7+ig*4]=0; y[8+ig*4]=0.;}
	
   kk=0;
    for(int i=0; i<N; i++)
    {
	for(int ii=0; ii<NG; ii++) glg1[ii]=glg_m[ii];
	tgl+=dt;
	inp = input[i];
	ggaba=ggaba1[i];
	gbarnmda=gbarnmda1[i];
	euler (ggaba, gbarnmda);
	Vm[kk]=y[0];
	Ca[kk]=y[1];
	nmdasig1[i]=y[4];
	allgaba1[i]=allgaba;
	
    for(int ig=0;ig<NG;ig++)
		{		
			mas_Vgaba[ig*N+kk]=y[5+ig*4];	
		}
		
	if(kk>N) break;
kk++;
   }
   return;
} // end mexFunction()
