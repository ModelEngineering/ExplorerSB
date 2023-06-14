#ifndef PARAMETERS_H_INCLUDED
#define PARAMETERS_H_INCLUDED

// Reversal potentials (mV)
#define vL -62.5
#define vH -35.0
#define vNa 45.0
#define vK -105.0
#define vCa 120.0

// Conductances (mS/cm^2)
// commented out conductances are provided by a parameter determined by the location on the grid in parameter space
#define gL 2.5
// #define gH 20.0
// #define gNaP 8.3244
// #define gLVA 15.0213
#define gNa 29.17
#define gK 12.96
#define gHVA 2.0
// #define gBK 5.0
#define gHVK 10.0

// Na
#define theta_mNa -25.0
#define sigma_mNa -6.5

// K
#define theta_nK -26.0
#define sigma_nK -9.0
#define tau_nK 10.0

// LVA
#define theta_mLVA -37.1
#define sigma_mLVA -4.8916
#define tau_mLVA 40.0
#define theta_hLVA -59.2
#define sigma_hLVA 11.2326
#define tau_hLVA 350.0

// HVA
#define theta_mHVA -10.0
#define sigma_mHVA -6.5

// NaP
#define theta_mNaP -40.0
#define sigma_mNaP -4.0
#define theta_hNaP -54.0
#define sigma_hNaP 5.0
#define tau_hNaP 500.0

// H
#define theta_hH -61.32
#define sigma_hH 5.855
#define tau_hH_T 100.0
#define delta_hH_T 0.205
#define theta_hH_T -65.95
#define sigma_hH_T 4.44

// HVK
#define theta_mHVK -40.0
#define sigma_mHVK -2.0
#define theta_nHVK -30.0
#define sigma_nHVK -2.0

// BK
#define wBK_base 170 //base time constant (ms)
#define sigma_wBK -15.6

// Ca
#define Ca0 0.00002 // concentration of calcium (mM)
#define tau_Ca 8.0 //calcium concentration time constant (ms)
#define Ca_buffer 0.5 //accounts for quick calcium buffering
#define Ca_z 2.0 //unitless number
#define d 1.0 //depth where calcuim concentration is relevent (microns)

// other parameters
#define C 21.0 // capacitance (microF/cm^2)
#define F 96485.0 //Faraday's constant (C/mol)

#endif
