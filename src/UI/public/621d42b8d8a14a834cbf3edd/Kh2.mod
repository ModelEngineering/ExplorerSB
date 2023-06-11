TITLE Anomalous rectifier
 
COMMENT
  from "An Active Membrane Model of the Cerebellar Purkinje Cell
        1. Simulation of Current Clamp in Slice"
  
  "Anomalous Rectification in Neurons from Cat Sensorimotor Cortex
    In Vitro" W.J.SPAIN, P.C.SCHWINDT, and W.E.CRILL
           JOURNAL OF NEUROPHYSIOLOGY Vol 57, No.5
ENDCOMMENT
 
UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
}
 
NEURON {
        SUFFIX Kh2
        USEION k WRITE ik
        RANGE  gkbar, gk, minf, nexp, ik
} 
 
INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}
 
PARAMETER {
        v (mV)
        celsius = 37 (degC)
        dt (ms)
        gkbar   = .0003 (mho/cm2)
        ek      = -30 (mV)

}
 
STATE {
        m 
}
 
ASSIGNED {
        ik (mA/cm2)
        gk minf nexp
}
 
BREAKPOINT {
        SOLVE states
        gk = gkbar *m
        ik = gk* (v-ek)
}
 
UNITSOFF
 
INITIAL {
        rates(v)
        m = minf
}

PROCEDURE states() {  :Computes state variables m, 
        rates(v)      :             at the current v and dt.
        m = m + nexp*(minf-m)
}

PROCEDURE rates(v) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.
        LOCAL  q10, tinc
        TABLE minf,nexp DEPEND dt, celsius FROM -100 TO 100 WITH 200
        q10 = 3^((celsius - 37)/10)
        tinc = -dt * q10
                :"m" potassium activation system
        minf = 0.2/(1+exp((v+82)/7))
        nexp = 1 - exp(tinc/36.8)
}

 
UNITSON
