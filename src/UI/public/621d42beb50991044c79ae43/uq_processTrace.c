#include <stdlib.h>
#include <float.h>
#include <math.h>
#include "uq_ETCell.h"

#define SPIKE_POINT 0
#define PI 3.1415926535897932384626433832795028841971693993751

#define min(a,b) \
  ({ __typeof__ (a) _a = (a); \
      __typeof__ (b) _b = (b); \
    _a < _b ? _a : _b; })

void uq_processTrace(FILE* fp, FILE* op)
{
  //input metrics
  double t, V, nK, hNaP, mH, mLVA, hLVA, wBK, Ca, nMystery, tau;

  //output metrics
  double burstDuration = 0;
  double burstFrequency = 0;
  double spikesPerBurst = 0;
  double mmp = DBL_MAX;
  double amp = 0;
  double average_peak_firing_rate = 0;
  double average_firing_rate = 0;

  //flags
  int scan_status;
  int burst_status;
  int bursting_has_begun = 0;
  int burst_start_count = 0;
  int burst_end_count = 0;

  //auxiliary quantities
  double prev_V, prev_nK;
  double burstStartTimes[1000];
  double burstEndTimes[1000];
  double spikeTimes[1000];
  double peak_firing_rate = 0;
  int spike_count = 0;
  int valid_spikes = 0;
  int data_point_count = 0;
  int buffer = 3;
  double BURST_POINT = 0.25; // this is ok because the injected current is always zero for this case

  scan_status = fscanf (fp," %le %le %le %le %le %le %le %le %le %le %le\n", &t, &V, &nK, &hNaP, &mH, &mLVA, &hLVA, &wBK, &Ca, &nMystery, &tau);

  if(nK > BURST_POINT)
    burst_status = 2;
  else
    burst_status = 0;

  prev_V = V;
  prev_nK = nK;

  while(scan_status != EOF)
  {
    scan_status = fscanf (fp," %le %le %le %le %le %le %le %le %le %le %le\n", &t, &V, &nK, &hNaP, &mH, &mLVA, &hLVA, &wBK, &Ca, &nMystery, &tau);

    // burst begins
    if( (prev_nK <= BURST_POINT && nK > BURST_POINT && burst_status == 0) ||
        (prev_V < SPIKE_POINT && V > SPIKE_POINT && burst_status == 0) )
    {
      burst_status = 1;
      if(buffer <= 0)
      {
        bursting_has_begun = 1;
        burstStartTimes[burst_start_count] = t;
        burst_start_count++;
      }
    }
    // burst ends
    if(prev_nK > BURST_POINT && nK <= BURST_POINT && burst_status == 1)
    {
      burst_status = 0;
      buffer--;
      if(bursting_has_begun)
      {
        burstEndTimes[burst_end_count] = t;
        burst_end_count++;
        valid_spikes += spike_count;

        int i;
        for(i = 0;i < spike_count - 1; i++)
        {
          double inst_rate = 1.0/(spikeTimes[i+1] - spikeTimes[i]);
          inst_rate = inst_rate*1000;
          if(inst_rate > peak_firing_rate)
            peak_firing_rate = inst_rate;
          average_firing_rate += inst_rate;
        }
        average_peak_firing_rate += peak_firing_rate;
        spike_count = 0;
      }
    }

    //bursting
    if(burst_status && bursting_has_begun)
    {
      //spike occurs
      if(prev_V < SPIKE_POINT && V > SPIKE_POINT)
      {
        spikeTimes[spike_count] = t;
        spike_count++;
      }
    }

    if(V < mmp)
      mmp = V;

    amp += V;
    data_point_count++;



    prev_V = V;
    prev_nK = nK;
  } // while(scan_status != EOF)


  int num_bursts = min(burst_start_count, burst_end_count);

  average_firing_rate = average_firing_rate/(valid_spikes - 1);
  average_peak_firing_rate = average_peak_firing_rate/num_bursts;

  int i;

  for(i = 0; i < num_bursts; i ++)
  {
    burstDuration += burstEndTimes[i] - burstStartTimes[i];
  }

  burstDuration = burstDuration/num_bursts;

  double totalPeriod = 0;

  for(i = 0; i < num_bursts - 1; i ++)
  {
    totalPeriod += (burstStartTimes[i+1] - burstStartTimes[i]);
  }

  burstFrequency = ((num_bursts - 1)/totalPeriod)*1000;

  spikesPerBurst = (double)valid_spikes/(double)num_bursts;

  amp = amp/data_point_count;

  fprintf(op,"%.17e %.17e %.17e %.17e %.17e %.17e %.17e\n", burstDuration, burstFrequency, spikesPerBurst, mmp, amp, average_peak_firing_rate, average_firing_rate);


} // processTrace()
