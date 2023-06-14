#include <stdio.h>

void readTrace(FILE* trace, FILE* spikes, FILE* metrics)
{

  double t,V,w,Vprev,freq = 0.0,lastSpike = -99.0;
  int count = 0;
  int status;

  status = fscanf(trace,"%le %le %le\n",&t,&V,&w);
  Vprev = V;

  while (status != EOF)
  {
    if(Vprev < 0.0 && V > 0.0)
    {
      if (lastSpike != -99.0)
        freq += 1.0/(t - lastSpike)*1000;
      fprintf(spikes,"%le\n",t);
      lastSpike = t;
      count++;
    }
    Vprev = V;
    status = fscanf(trace,"%le %le %le\n",&t,&V,&w);
  }

  if (count > 1)
    freq = freq/(count-1);
  else
    freq = 0;

  fprintf(metrics,"%le %lf\n",freq, 0.023);
}
