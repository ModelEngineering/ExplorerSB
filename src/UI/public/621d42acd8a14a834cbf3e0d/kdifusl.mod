: modified by Jay Coggan for K diffusion

TITLE Calcium ion accumulation with longitudinal and radial diffusion

: The internal coordinate system is set up in PROCEDURE coord_cadifus()
: The scale factors set up in this procedure do not have to be recomputed
: when diam or DFree are changed.
: The amount of calcium in an annulus is ca[i]*diam^2*vol[i] with
: ca[0] being the second order correct concentration at the exact edge
: and ca[NANN-1] being the concentration at the exact center
: modified by j coggan


NEURON {
	SUFFIX kdifus
	:USEION k READ ko, ki, ik WRITE ki, ik
	USEION k READ ko, ki, ik WRITE ki
	RANGE ikbar
	GLOBAL vol :, Buffer0
}

DEFINE NANN  4

UNITS {
	(molar) = (1/liter)
	(mM)	= (millimolar)
	(um)	= (micron)
	(mA)	= (milliamp)
	FARADAY = (faraday)	 (10000 coulomb)
	PI	= (pi) (1)
}

PARAMETER {
	DFree = .6	(um2/ms)
	diam		(um)
	ko		(mM)
	ik		(mA/cm2)
	k1buf		(/mM-ms)
	k2buf		(/ms)
	ikbar		(mA/cm2)
	ki0 = 150 	(mM)		
}

ASSIGNED {
	ki		(mM)
	vol[NANN]	(1)	: gets extra cm2 when multiplied by diam^2
}

STATE {
	k[NANN]	(mM) 	: k[0] is equivalent to cai
	KBuffer[NANN]  (mM)
	Buffer[NANN]    (mM)
}

BREAKPOINT {
	SOLVE state METHOD sparse
	ik = ikbar
}

LOCAL coord_done

INITIAL {
	if (coord_done == 0) {
		coord_done = 1
		coord()
	}
	: note Buffer gets set to Buffer0 automatically
	: and KBuffer gets set to 0 (Default value of KBuffer0) as well
	FROM i=0 TO NANN-1 {
		k[i] = ki0
	}
}

LOCAL frat[NANN] 	: gets extra cm when multiplied by diam

PROCEDURE coord() {
	LOCAL r, dr2
	: cylindrical coordinate system  with constant annuli thickness to
	: center of cell. Note however that the first annulus is half thickness
	: so that the concentration is second order correct spatially at
	: the membrane or exact edge of the cell.
	: note k[0] is at edge of cell
	:      k[NANN-1] is at center of cell
	
	r = 1/2
						:starts at edge (half diam)
	dr2 = r/(NANN-1)/2			:half thickness of annulus
	vol[0] = 0
	frat[0] = 2*r
	FROM i=0 TO NANN-2 {
		vol[i] = vol[i] + PI*(r-dr2/2)*2*dr2	:interior half
		r = r - dr2
		frat[i+1] = 2*PI*r/(2*dr2)	:exterior edge of annulus
					: divided by distance between centers
		r = r - dr2
		vol[i+1] = PI*(r+dr2/2)*2*dr2	:outer half of annulus
	}
}

LOCAL dsq, dsqvol : can't define local variable in KINETIC block or use
		:  in COMPARTMENT
KINETIC state {
	COMPARTMENT i, diam*diam*vol[i] {k KBuffer Buffer}
	LONGITUDINAL_DIFFUSION j, DFree*diam*diam*vol[j] {k}
	~ k[0] << (-ik*PI*diam*frat[0]/(FARADAY))
	FROM i=0 TO NANN-2 {
		~ k[i] <-> k[i+1] (DFree*frat[i+1], DFree*frat[i+1])
	}
	dsq = diam*diam
	FROM i=0 TO NANN-1 {
		dsqvol = dsq*vol[i]
		~ k[i] + Buffer[i] <-> KBuffer[i] (k1buf*dsqvol,k2buf*dsqvol)
	}
	:ki = k[3]
	ki = (k[0] + k[1] + k[2] + k[3])/4
}
