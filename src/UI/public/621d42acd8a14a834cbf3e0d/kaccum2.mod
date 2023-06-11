TITLE potassium ion accumulation
: potassium ion accumulation inside and outside
: modified by j coggan

NEURON {
	SUFFIX kaccum2
	:USEION k READ ik, ki, ko WRITE ki, ko
	USEION k READ ik, ko WRITE  ko
	RANGE fhspace, kk
}

UNITS {
	(molar) = (1/liter)
	(mV) = (millivolt)
	(um) = (micron)
	(mM) = (millimolar)
	(mA) = (milliamp)
	FARADAY = 96520 (coul)
	R = 8.3134	(joule/degC)
}

PARAMETER {
	kbath = 4	(mM)		
	diam		(um)
	ik		(mA/cm2)
	fhspace	= 20000	(angstrom)	
	kk = 0.9			
	:kk = 0.1175	(ms)
					: bath to
					: FH space
	:ki0 = 155	(mM)
	ko0 = 4		(mM)    
}

STATE {
	:ki 	(mM)
	ko 	(mM)
}


INITIAL {
	
	:ki = ki0
	ko = ko0
	
}

BREAKPOINT {
	SOLVE state METHOD euler
}

DERIVATIVE state {
	:ki' = -ik * 4/(diam*FARADAY) * (1e4)
	:ki' = 0
	:ko' = ik/fhspace/FARADAY*(1e8) + kk*(kbath - ko)*(1e-3)
	ko' = ik/fhspace/FARADAY*(1e8) + (kbath - ko)/kk
	:ko' = 0 + kk*(kbath - ko)*(1e-3)
}
	
COMMENT
This model uses ina but does not WRITE it; thus this model does
not add anything to the total ionic current.

The initial block works around a difficulty that arises from a STATE in
this model having the same name as an ion.  (Note: in the cabpump model
there is no name conflict between the ca[] states and the cai ion
concentration.) The sequence of events when finitialize is called is
that the na_ion's nai,nao are initialized to the global variables
nai0_na_ion and nao0_na_ion respectively. Then this model's INITIAL block
is called. By default, nai/nao would be set to the initial state values
nai0/nao0 implicitly declared in this model and on exit from the intitial
block, the na_ion values would be assigned these local values. We therefore
directly set the local state values to the na_ion values. See the
"nocmodl nacum" generated nacum.c file to see the precise sequence on
the nrn_init() call.

diam is a special range variable in NEURON and refers to the diameter in
microns.  Under scop and hocmodl its default value is specified in the
PARAMETER block. In NEURON, however, its value is taken from the
"morphology" mechanism.
ENDCOMMENT
