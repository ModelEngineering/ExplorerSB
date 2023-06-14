/* Copyright: Marta Varela, atrial dog electrophysiology model
See Varela et al, PLoS Comp Bio, 2016 (http://dx.doi.org/10.1371/journal.pcbi.1005245)
Email: marta.varela@kcl.ac.uk */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

 // constants (single-cell model)
#define vcell  20100.0      // cell volume, um3 */
#define vi  (vcell*0.68)      // intracellular volume, 13668 um3 */
#define vup  (0.0552*vcell)   // volume of sarcoplasmic uptake compartment, 1109.52 um3 */
#define vrel (0.0048*vcell)  // volume of sarcoplasmic uptake compartment, 96.48 um3 */
#define T (310.0)              // (baseline) temperature, 37 deg Celsius = 310 K */
#define Cm 100.0          // membrane capacitance, pF
#define F 96.4867          // Faraday constant (charge per mol), coul/mmol */
#define R 8.3143           // universal gas constant, J K-1 mol-1 */
#define FRT (F/(R*T))
#define Fvi (F*vi)

double trpnbar = 0.35;   
double cmdnbar = 0.045;			
double csqnbar = 10.0;  
double kmnai = 10.0;				// mM
double kmko = 1.5;				// mM         
double kmcap = 0.0005;			// mM */	
double kmnalr = 87.5;			// mM */               
double kmcalr = 1.38;			// mM */
double ksatlr = 0.1;
double gammalr = 0.35;
double kmup = 6e-4;
double iupbar = 0.0035;
double caupmax = 27.0;
double tautr = 180.0;
double grelbar = 8.0;			// ms-1, max release rate*/ 

double kc = 5.4;             // K+ baseline concentration ?, mM (numerator in Nernst)
double nac = 140.0;            // Na+ baseline concentration ?, mM 
double cac = 1.8;            // Ca2+ baseline concentration ?, mM ?? used 2 for( wilders ? 
double clc = 132;



int main(int argc, char **argv) {

  /* computed quantities */
  double Ek,Ena,Eca,ina,icaL,ibna,ibca,Ecl;
  double inak,ik1,ito,ikur,ikr,iks,inaca,icap,ikach,ibcl;
  double naidot,kidot,caidot,cmdndot,trpndot,csqndot,clidot,caupdot,careldot;
  double irel,itr,iup,iupleak,fnak,caflux,rect,expnaca;
  double a,b,inff,tau;
  double gna, gcaL, gk1, gto, gkr, gks, gbna, gbca, gkach, gkur,gbcl;
  double icapbar, knacalr, inakbar, fkur, recta, ichange;
  double sigma, nac3, CNaCa2, Tend;
  int celltype, nbeats, drug, remod;
  double dt = 0.005, V, BCL, extrams, t=0.0;
  double stimdur = 2.0, stiminten = -20.0, istim;
  double m, hh, jj, d, f, fca, xr, xs, xa, oa, oi, ua, ui, uu, vv, w, cmdn, trpn, csqn; 
  double ki, nai, cai, cli, caup, carel;
  int cnt, cntout;

  cntout = 1.0/dt; // to output V at every 1.0 ms

  // default values for simulation parameters
  BCL = 500; // in ms, roughly corresponding to sinus rhythm in a healthy dog
  nbeats =3;
  celltype=1; //RA
  drug =0; //no drug
  remod =0; //no remodelling
  extrams=0;

  printf("argc: %d\n", argc);
  switch (argc) {
	  case 7:
		  extrams = atof(argv[6]);
	  case 6:
		  remod = atoi(argv[5]);
	  case 5:
		  drug = atoi(argv[4]);
	  case 4:
		  celltype = atoi(argv[3]);
	  case 3:
		  nbeats = atoi(argv[2]);
	  case 2:
		  BCL = atof(argv[1]);
		  break;
	  }

  Tend=BCL*nbeats+extrams; // time at which the simulation ends

  sigma = (exp(nac/67.3)-1.0)/7.0;   
  nac3=pow(nac,3.0);
  CNaCa2=1/((pow(kmnalr,3.0)+pow(nac,3.0))*(kmcalr+cac));

  // non-cell-type-dependent currents
  gna = 7.8;
  gbna = 1.0e-5;
  gbca = 1.0e-5;
  gkur = 0.0115;

  icapbar = 0.275;
  knacalr = 1600.0;
  inakbar = 0.6;
  
  // LA currents 
  gcaL=0.34;
  gk1=0.1;
  gto=0.096;
  gbcl=8.0e-4;
  gkr=0.0145;
  gks=0.052;
  gkach=0.0045;
  
  // CARDIAC REGION
  switch (celltype) {
  case 1: // RA
  case 5: // PM
	  gkr=0.00899;
	  break;
  case 3: // BB
	  gcaL=0.58;
	  gkr=0.00899;
	  break;
  case 4: //PV
	  gcaL=0.255;
	  gk1=0.036;
	  gto=0.07104;
	  gbcl=0.0055;
	  gkr=0.022475;
	  gks=0.0832;
	  gkach=0.0065;
	  break;
	  }

  // DEGREE OF REMODELLING
  if (remod==1) { // moderate remodelling
	  gna=gna*0.90; // new value
	  gcaL=gcaL*0.47;
	  gk1=gk1*1.80;
	  gto=gto*0.54;
	  knacalr=knacalr*1.64;
	  gkach=gkach*1.8;
	  }
  else if (remod==2) { //advanced remodelling
	  gna=gna*0.80;  // new value
	  gcaL=gcaL*0.31;
	  gk1=gk1*2.57;
	  gto=gto*0.38;
	  knacalr=knacalr*2.34;
	  gkach=gkach*2.57;
	  }

  //DRUG IN USE
  if (drug==1) { // Vernakalant 10
	  gkur=gkur*0.55;
	  gto=gto*0.56;
	  gkr=gkr*0.68;
	  //gna=gna*0.90; //new
	  gkach=gkach*0.54;
	  }
  if (drug==2) { // Vernakalant 30
	  gkur=gkur*0.30;
	  gto=gto*0.30;
	  gkr=gkr*0.41;
	  gna=gna*0.90; //gna=gna*0.70;
	  gkach=gkach*0.22;
	  } 
  if (drug==7) {//  Amiodarone 5
	  gks=gks*0.80;
	  gkr=gkr*0.50;
	  gna=gna*0.90;
	  //gna=gna*0.60;
	  gkach=gkach*0.22;
	  gcaL=gcaL*0.50;
	  gk1=gk1*0.70;
  }
  if (drug==9) {// Amiodarone 10
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gcaL=gcaL*0.50*0.7;
          gk1=gk1*0.70*0.7;
  }
  if (drug==12) { // Amiodarone 10 with ICaL off
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gk1=gk1*0.70*0.7;
  }
  if (drug==13) { // Amiodarone 10 with IK1 off
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gcaL=gcaL*0.50*0.7;
  }
  if (drug==14) { // Vernakalant 30 - with ICaL
          gkur=gkur*0.30;
          gto=gto*0.30;
          gkr=gkr*0.41;
          gna=gna*0.70;
          gkach=gkach*0.22;
          gcaL=gcaL*0.60;
  }
  if (drug==15) { // Vernakalant 30 - with IK1
          gkur=gkur*0.30;
          gto=gto*0.30;
          gkr=gkr*0.41;
          gna=gna*0.70;
          gkach=gkach*0.22;
          gk1=gk1*0.60;
  }

  V=-85.53;				// resting potential, mV from table 2 of paper
  m=0.001972;			// INa activation variable
  hh=0.9791;		  // INa fast inactivation variable
  jj=0.9869;				// INa slow inactivation variable
  d=4.757e-6;			// ICa activation variable
  f=0.9999;				// ICa V-dependent inactivation variable
  fca=0.7484;			// ICa Ca2+-dependent inactivation variable
  xr=7.433e-7;			// IKr activation variable
  xs=0.01791;			// IKs activation variable
  xa=1e-5;              // IKAch activation variable
    
  oa=0.07164;			// Ito activation variable
  oi=0.9980;			// Ito inactivation variable
  ua=0.05869;			// IKurd activation variable
  ui=0.9987;			// Ikurd inactivation variable
  uu=0.0;				// activation gating variable for Irel
  vv=1.0;				// Ca2+ flux-dependent inactivation variable for Irel
  w=0.9993;				// V-dependent inactivation variable for Irel
  cmdn=1.856e-3;		// calmodulin concentration in myoplasm, mM
  trpn=7.022e-3;		// troponin concentration in myoplasm, mM
  csqn=6.432;			// sequestrin concentration in myoplasm, mM

  nai=11.75;			// initial Na+ concentration, mM from table 2 of paper (denominator in Nernst)
  cai=1.024e-4;			// initial Ca2+ concentration, mM from table 2 of paper
  ki=138.4;				// initial K+ concentration, mM from table 2 of paper
  cli=29.26;			// initial Cl- concentration, mM from table 2 of paper
  caup=1.502;			// initial Ca2+ in uptake SR concentration, mM from table 2 of paper
  carel=1.502;			// initial Ca2+ in release SR, mM from table 2 of paper

  printf("Running simulation for BCL = %lf ms, nbeats = %d, cell type = %d, remod = %d, drug = %d, extrams = %lf.\n", BCL, nbeats, celltype, remod, drug, extrams);

   // time loop
   for(cnt=0;cnt<(int)(Tend/dt);cnt++) {
	   t=dt*cnt;
	   // stimulus current
	  if ((int)t%(int)(BCL)>=0&&(int)t%(int)(BCL)<stimdur&&t<BCL*nbeats)
		  istim = stiminten;
	  else
		  istim = 0;

     // compute equilibrium u using Nernst
		Ek = 26.71*log(kc/ki );
		Ena = 26.71*log(nac/nai );
		Eca = 13.35*log(cac/cai );    
        Ecl = 26.71*log(cli /clc);

        // compute currents 
		ina = gna*pow(m ,3.0)*hh *jj *(V-Ena);   
		ito = gto*pow(oa ,3.0)*oi *(V-Ek);   
        
        fkur = 1.0+3.0/(1.0+exp((V-14.0)/-6.0));
		ikur = gkur*fkur*pow(ua ,3.0)*ui *(V-Ek);
        
        if (celltype==2||celltype==4) { // LA or PV
            rect = 0.6+1.0/(0.5+0.5*exp((V+8.0)/24.4)); 
			}
        else { // RA or BB
            rect =  0.6+1.0/(0.5+exp((V-26.0)/20.4));
			}
            
		ikr = gkr*rect*xr *(V-Ek);         
		iks = gks*xs *xs *(V-Ek);
		icaL = gcaL*d *f *fca *(V-60.0);  
        
        if (celltype==4) { // PV
            ik1 = gk1*(V-Ek)/(0.66+exp(0.078*(V-Ek-18.0)));
			}
        else {
            ik1 = gk1*(V-Ek)/(1.0+exp(0.072*(V-Ek)));
			}
        
        recta=1.0/(0.1+exp(0.078*(V-Ek-65.0)));
        ikach= gkach*xa *(V-Ek)*recta;

        ibna = gbna*(V-Ena);
        ibca = gbca*(V-Eca); 

        fnak = 1.0/(1.0+0.1245*exp(-0.1*V*FRT)+0.0365*sigma*exp(-V*FRT));  
        inak = inakbar*fnak*kc/(kc+kmko)/(1+pow((kmnai/nai ),1.5));     

        icap = icapbar*cai /(cai +kmcap); 

        expnaca=exp((gammalr-1)*V*FRT);
		inaca = knacalr*CNaCa2/(1+ksatlr*expnaca)*(nai *nai *nai *cac*exp(V*gammalr*FRT)-nac3*cai *expnaca); 
        
        ibcl = gbcl*(V-Ecl);  
              
        // update concentrations of each ion
		naidot = Cm*(-3*inak-3*inaca-ibna-ina)/(Fvi);
        kidot = Cm*(2*inak-ik1-ito-ikur-ikr-iks-ikach)/(Fvi);
        clidot = Cm*ibcl/(Fvi);

		//dynamic buffers  
		cmdndot = 200.0*cai *(1.0-cmdn /cmdnbar) - 0.476*cmdn /cmdnbar;
		trpndot =  78.4*cai *(1.0-trpn /trpnbar) - 0.392*trpn /trpnbar;
		csqndot = 0.48*carel *(1.0-csqn /csqnbar) - 0.4*csqn /csqnbar;
		// above buffer derivatives in units: per milliseconds */

		cmdn  = cmdn  + dt*cmdndot*cmdnbar;      
		trpn  = trpn  + dt*trpndot*trpnbar;
		csqn  = csqn  + dt*csqndot*csqnbar;
		// above bound buffer units: mM */

		irel = grelbar*uu *uu *vv *w *(carel -cai );          

		iup = iupbar/(1.0+kmup/cai );
		iupleak = iupbar*caup /caupmax;     
		itr = (caup -carel )/tautr;      
          
		caidot = Cm*(2.0*inaca-icap-icaL-ibca)/(2.0*Fvi) + (iupleak-iup)*vup/vi+irel*vrel/vi
		 - trpnbar*trpndot - cmdnbar*cmdndot;
		caupdot = iup-itr*vrel/vup-iupleak;
		caup  = caup  + dt*caupdot;
		careldot = itr-irel-31.0*csqndot;
		carel  = carel  + dt*careldot;

        // update all concentrations */
        nai  = nai  + dt*naidot;
        ki  = ki  + dt*kidot;
        cai  = cai  + dt*caidot;
        cli  = cli  + dt*clidot;

        // update ina m gate */
        a = 0.32*(V+47.13)/(1-exp(-0.1*(V+47.13)));
        if (fabs(V+47.13) < 1e-10) {
            a = 3.2;
			}
        b = 0.08*exp(-V/11);
        tau = 1.0/(a+b);
		inff = a*tau;
        m  = inff + (m -inff)*exp(-dt/tau);
          
        // update ina hh and jj gates */
        if (V >= -40.0) {     
			a  = 0.0;
            b = 1.0/(0.13*(1.0+exp((V+10.66)/-11.1)));
			}
        else { 
			a = 0.135*exp((V+80.0)/-6.8);
            b = 3.56*exp(0.079*V)+3.1e5*exp(0.35*V);
			}
        tau = 1.0/(a+b);
		inff = a*tau;
        hh  = inff + (hh -inff)*exp(-dt/tau);
        if (V >= -40.0) { 
            a  = 0.0;
            b = 0.3*exp(-2.535e-7*V)/(1.0+exp(-0.1*(V+32.0)));
			}
        else  {
            a = (-1.2714e5*exp(0.2444*V)-3.474e-5*exp(-0.04391*V))*(V+37.78)/(1.0+exp(0.311*(V+79.23)));
            b = 0.1212*exp(-0.01052*V)/(1+exp(-0.1378*(V+40.14)));
			}
        tau = 1.0/(a+b);
		inff = a*tau;
        jj  = inff + (jj -inff)*exp(-dt/tau);
          
        // update oa ito gate */
        inff = pow((1.0+exp((V-12.0)/-11.5)),(-1.0/3.0));
        tau = 0.4/(exp((V-15.0)/20.0));
        oa  = inff + (oa -inff)*exp(-dt/tau);

        // update oi ito gate */
        inff = 1.0/(1.0+exp((V+31.0)/6.45));    
        a = 1.0/(1.2+exp((V +95.2)/5.85));      
        b = 1.0/(9.54+exp((V -48.0)/-20.0));  
        tau = 1.0/(a+b); 
        oi  = inff + (oi -inff)*exp(-dt/tau);

        // update ua ikur gate */
        a = 1.47/(exp((V +33.20)/-30.63)+exp((V -27.6)/-30.65));
        b = 0.42/(exp((V +26.64)/2.49)+exp((V +44.41)/20.36));
        tau = 1.0/(a+b); 
        inff = pow((1+exp((V +2.81)/-9.49)),(-1.0/3.0));
        ua  = inff + (ua -inff)*exp(-dt/tau);

        // update ui ikur gate */
        a = 1.0/(21.0+exp((V -185.0)/-28.0));
        b = exp((V -158.0)/16.0);
        tau = 1.0/(a+b); 
        inff = 1.0/(1.0+exp((V -99.45)/27.48));
        ui  = inff + (ui -inff)*exp(-dt/tau);

        // update the xr ikr gate */
        a = 0.04*(V -248.0)/(1.0-exp((V -248.0)/-28.0));
        b = 0.028*(V +163.0)/(exp((V +163.0)/21.0)-1.0);
        tau = 1.0/(a+b);
        inff = 1.0/(1.0+exp((V +7.654)/-5.377));  
        xr  = inff + (xr -inff)*exp(-dt/tau);

        // update the xs iks gate */
        a = 0.00001*(V+28.5)/(1.0-exp((V+28.5)/-115.0));
        b = 0.00023*(V+28.5)/(exp((V+28.5)/3.3)-1.0);
        if (fabs(V+28.5) < 1e-10) {
            a = 0.00115; 
            b = 0.000759;
			}
        tau = 1.0/(a+b);
        inff = sqrt(1.0/(1.0+exp((V-13.0)/-12.0)));
	    xs  = inff + (xs -inff)*exp(-dt/tau);

        // update icaL d gate */
        inff =  1.0/(1.0+exp((-V-2.0)/5.0));
        tau = (1.0/(1.0+exp((V+10.0)/-6.24)))*(1.0-exp((V+10.0)/-6.24))/(0.035*(V+10.0));
        if (fabs(V-10)<1e-10) {
            tau = 0.763;
			}
        d  = inff + (d -inff)*exp(-dt/tau);

        // update icaL f gate */
        tau = 400.0/(1+4.5*exp(-0.0007*pow(V-9,2.0)));
        inff = 1.0/(1.0+exp((-V-34.0)/-6.3));      
        f  = inff + (f -inff)*exp(-dt/tau);

        // update icaL fca gate 
        inff = 0.29+0.8/(1.0+exp((cai -1.2e-4)/0.00006));                           
        tau = 2.0;
        fca  = inff + (fca -inff)*exp(-dt/tau);   
        
        // update the SR gating variables */
        // caflux is expected in umoles/ms, hence the factor of 1000 */
        // 1e-15 is used to scale the volumes~ */ 
        
        // update irel uu gate
        caflux = 1e3*(1e-15*vrel*irel-1e-15*Cm*(0.5*icaL-0.2*inaca)/(2.0*F));
        inff = 1.0/(1.0+exp(-(caflux-3.4175e-13 )/13.67e-16));
        tau = 11.2;
        uu  = inff + (uu -inff)*exp(-dt/tau); 
        
        // update irel vv gate
        inff = 1.0-1.0/(1.0+exp(-(caflux-6.835e-14)/13.67e-16));
        tau = 1.91+2.09/(1.0+exp(-(caflux-3.4175e-13)/13.67e-16));  
        vv  = inff + (vv -inff)*exp(-dt/tau); 
        
        // update irel w gate
        inff = 1.0-1.0/(1.0+exp(-(V-40.0)/17.0));
        tau = 6.0*(1.0-exp(-(V-7.9)/5.0))/(1.0+0.3*exp(-(V-7.9)/5.0))/(V-7.9);
	    if (fabs(V-7.9) < 1e-10) {
            tau = 0.9231;
			}
        w  = inff + (w -inff)*exp(-dt/tau);
         
        // update the ikach xa gate
        inff=1.0/(1.0+exp((-93.0-V)/-15.2));
        tau=360.0+130.0*(1.0-exp(-(V+130.0)/50.0));
        xa  = inff + (xa -inff)*exp(-dt/tau);
        
		// update membrane voltage                                 
		ichange = -(ina+icaL+icap+ik1+ito+ikur+ikr+iks+ibna+ibca+inak+inaca+ikach+ibcl+istim); 		
		V = V + dt*ichange;
		if(cnt%cntout==0) {
			printf("t = %.1lf ms, V = %.1lf mV\n",t,V);
			}
		} // end of time loop
		return 0;
} // end of main
