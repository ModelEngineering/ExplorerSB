#include <math.h>
#include <omp.h>
#include "gsl/gsl_errno.h"
#include "gsl/gsl_matrix.h"
#include "gsl/gsl_odeiv2.h"
#include "uq_ETCell.h"
#include "uq_parameters.h"

#define TIME 7000
#define NUM_EQ 9

int vfield (double t, const double y[], double dy[], void *params);
double squarewave(double t, double freq, double amp, double duty_cycle);

/*Definition of squarewave function*/

double squarewave(double t, double freq, double amp, double duty_cycle)
{
  double t_sec = t/1000;
  double period = 1.0/freq;
  double phase = fmod(t_sec,period)/period;

  if(phase*100 < duty_cycle)
    return amp;
  else
    return 0;
}



/*Definition of ODE model ET cell*/

int vfield (double t, const double y[], double dy[], void *params)
{
  double V = y[0];
  double nK = y[1];
  double hNaP = y[2];
  double hH = y[3];
  double mLVA = y[4];
  double hLVA = y[5];
  double mBK = y[6];
  double Ca = y[7];
  double nHVK = y[8];

  double* conductances = (double*)params;

  double gH = conductances[0];
  double gLVA = conductances[1];
  double gNaP = conductances[2];
  double gBK = conductances[3];


  // auxiliary quantities for BK channel
  double theta_mBK = -20.0 + 59.2*exp(-90.0*Ca) + 96.7*exp(-470.0*Ca);
  double p = 2.9 + 6.3*exp(-360*Ca);
  double s = -25.3 + 107.5*exp(-120.0*Ca);
  double f = 1.0/(10.0*(exp(-(V+100.0-s)/63.6)+exp((-150.0+(V+100.0-s))/63.6))) - 5.2;


  // infinity curves
  double mNa_inf = 1.0/(1.0+exp((V-theta_mNa)/sigma_mNa));
  double nK_inf = 1.0/(1.0+exp((V-theta_nK)/sigma_nK));
  double mNaP_inf = 1.0/(1.0+exp((V-theta_mNaP)/sigma_mNaP));
  double hNaP_inf = 1.0/(1.0+exp((V-theta_hNaP)/sigma_hNaP));
  double hH_inf = 1.0/(1.0+exp((V-theta_hH)/sigma_hH));
  double mLVA_inf = 1.0/(1.0+exp((V-theta_mLVA)/sigma_mLVA));
  double hLVA_inf = 1.0/(1.0+exp((V-theta_hLVA)/sigma_hLVA));
  double mHVA_inf = 1.0/(1.0+exp((V-theta_mHVA)/sigma_mHVA));
  double mBK_inf = 1.0/(1.0+exp((V-theta_mBK)/sigma_mBK));
  double mHVK_inf = 1.0/(1.0+exp((V-theta_mHVK)/sigma_mHVK));
  double nHVK_inf = 1.0/(1.0+exp((V-theta_nHVK)/sigma_nHVK));

  //time constants
  double nHVK_tau = 1000/(1.0+exp(-(V+35))) + 1000;
  double nK_tau = tau_nK/cosh((V-theta_nK)/(2.0*sigma_nK));
  double hNaP_tau = tau_hNaP/cosh((V-theta_hNaP)/(2.0*sigma_hNaP));
  double hH_tau = tau_hH_T*exp(delta_hH_T*(V-theta_hH_T)/sigma_hH_T)
                            / (1+exp((V-theta_hH_T)/sigma_hH_T));
  double mLVA_tau = tau_mLVA/cosh((V-theta_mLVA)/(2.0*sigma_mLVA));
  double hLVA_tau = tau_hLVA/cosh((V-theta_hLVA)/(2.0*sigma_hLVA));
  double mBK_tau = -(p - 1.0)*(f - 0.2)/0.8 + mBK_base;


  // compute values for the currents
  double INa = gNa*(1.0-nK)*mNa_inf*mNa_inf*mNa_inf*(V-vNa);
  double IHVK = gHVK*mHVK_inf*nHVK*(V - vK);
  double IK = gK*nK*nK*nK*nK*(V-vK);
  double IL = gL*(V-vL);
  double IH = gH*hH*(V-vH);
  double INaP = gNaP*mNaP_inf*hNaP*(V-vNa);
  double ILVA = gLVA*mLVA*mLVA*hLVA*(V-vCa);
  double IHVA = gHVA*mHVA_inf*(V-vCa);
  double IBK = gBK*mBK*(V-vK);


  dy[0] = -(INa + IK + ILVA + IH + INaP + IL + IHVA + IBK + IHVK)/C;
  dy[1] = (nK_inf-nK)/nK_tau;
  dy[2] = (hNaP_inf-hNaP)/hNaP_tau;
  dy[3] = (hH_inf-hH)/hH_tau;
  dy[4] = (mLVA_inf-mLVA)/mLVA_tau;
  dy[5] = (hLVA_inf-hLVA)/hLVA_tau;
  dy[6] = (mBK_inf - mBK)/mBK_tau;
  dy[7] = -Ca_buffer*10.0*(ILVA + IHVA)/(Ca_z*F*d) + (Ca0 - Ca)/tau_Ca;
  dy[8] = (nHVK_inf - nHVK)/nHVK_tau;

  return GSL_SUCCESS;
}



/*GSL solver*/

void uq_ET(double* parameters,int num_pars, FILE* fp) {

  // double begin = omp_get_wtime();

  gsl_odeiv2_system sys = {vfield, NULL, NUM_EQ, parameters};

  gsl_odeiv2_driver * driver =
    gsl_odeiv2_driver_alloc_y_new (&sys, gsl_odeiv2_step_rk2,
          1e-6, 1e-6, 0.0);
  int i;
  double t = 0.0, t1 = TIME; //time in ms
   double y[NUM_EQ] = {-51.7045, 0.0531, 0.0604, 0.1720, 0.0460, 0.2084, 0.1292, 0.0005, 0};

  for (i = 0; i <= (4*TIME); i++)
    {
      double ti = i * t1 / (4*TIME);

      int status = gsl_odeiv2_driver_apply (driver, &t, ti, y);

      if (status != GSL_SUCCESS) {
          fprintf (stderr,"error, return value=%d\n", status);
          break;
        }

      //compute currents
      double V = y[0];
      double nK = y[1];
      double hNaP = y[2];
      double hH = y[3];
      double mLVA = y[4];
      double hLVA = y[5];
      double mBK = y[6];
      double Ca = y[7];
      double nHVK = y[8];
      double tau = 1000/(1.0+exp(-(V+35))) + 200;

      // output to file. 17 significant digits for full double precision
      fprintf (fp," %.17e %.17e %.17e %.17e %.17e %.17e %.17e %.17e %.17e %.17e %.17e\n",
                  t, V, nK, hNaP, hH, mLVA, hLVA, mBK, Ca, nHVK, tau);


    }

  gsl_odeiv2_driver_free (driver);

  // double end = omp_get_wtime();
  //
  // fprintf(stdout, "%f\n", end-begin);
}
