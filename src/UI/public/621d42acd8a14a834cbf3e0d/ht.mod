: modified by Jay Coggan

: 	High threshold potassium chanel from 
:	Contribution of the Kv3.1 potassium channel to high-frequency firing in mouse auditory neurones
:	Lu-Yang Wang, Li Gan, Ian D. Forsythe and Leonard K. Kaczmarek
:	J. Physiol (1998), 501.9, pp. 183-194

NEURON {
	SUFFIX HT
	USEION k READ ek WRITE ik
 	RANGE gbar, g, ik
	GLOBAL ninf, ntau, pinf, ptau, an, bn, ap, bp
}

: area in paper is 1000 (um2) so divide our density parameters by 10

UNITS {
	(mV) = (millivolt)
	(S) = (mho)
	(mA) = (milliamp)
}

PARAMETER {
	gbar = .15 (S/cm2) 
	gamma = .1
	kan = .2120 (/ms) 
	ean = .04 (/mV)		
	kbn = .1974 (/ms) 
	ebn = 0 (/mV)
	ek = -90 (mV)
	:e_k = -90 (mV)
	kap = .00713 (/ms)	
	eap = -.1942 (/mV)	
	kbp = .0935 (/ms)	
	ebp = .0058 (/mV)	
}

ASSIGNED {
	v (mV)
	:ek (mV)
	ik (mA/cm2)

	ninf
	ntau (ms)
	pinf
	ptau (ms)

	an (/ms)
	bn (/ms)
	ap (/ms)
	bp (/ms)
}

STATE {
	n p
}

INITIAL {
	rates(v)
	n = ninf
	p = pinf
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	:ik = gbar*n^3*(1 - gamma + gamma*p)*(v - e_k)
	ik = gbar*n^3*(1 - gamma + gamma*p)*(v - ek)

:	ik = gbar*n^3*(1 - gamma + gamma*p)*(v - (-90))
}

DERIVATIVE state {
	rates(v)
	n' = (ninf - n)/ntau
	p' = (pinf - p)/ptau
}

PROCEDURE rates(v(mV)) {

	an = kan*exp(ean*v)
	bn = kbn*exp(ebn*v)

	ap = kap*exp(eap*v)
	bp = kbp*exp(ebp*v)

	ninf = an/(an + bn)
	ntau = 1/(an + bn)
	pinf = ap/(ap + bp)
	ptau = 1/(ap + bp)
}

