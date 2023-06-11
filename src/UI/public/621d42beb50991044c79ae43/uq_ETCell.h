#ifndef UQ_ETCELL_H_INCLUDED
#define UQ_ETCELL_H_INCLUDED

#include <stdio.h>

void uq_ET(double* pars, int num_pars, FILE* fp);
void uq_processTrace(FILE* fp, FILE* op);

#endif
