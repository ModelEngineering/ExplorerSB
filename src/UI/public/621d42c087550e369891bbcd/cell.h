#ifndef __CELLH__
#define __CELLH__

#include "clist.h"
#include "receptor.h"
#include "params.h"

// main structure for the simulation : cell
typedef struct {
    // list of Ca particles 
    clist *ca;

    // number of free Ca
    int free_ca;

    // list of IP3 particles 
    clist *ip3;

    // IP3R
    // table of receptors, storing each receptor
    receptor **recs; 
    // receptor map, to check easily the presence of an IP3R at a given position in space
    int *rmap;

    // plc position map
    int *pmap; 

    // simulation parameters
    params *param;

} cell;

// Cell constructor function
cell *create_cell(int ip0, int ca0, int free_ca, params *param);

// utilities functions 
void remove_calcium(cell *c, part *p);

void remove_ip3(cell *c, part *p);

void add_ip3(int ip0, cell *c, params *param);

// output functions 
void print_calcium_data(cell *c, char *name);

void print_ip3_data(cell *c, char *name);

void print_receptor_data(cell *c, char *name);

void print_plc_data(cell *c, char *name);

// main loop 
void cycle(cell *c);

// main loop functions
void produce(cell *c);

void degrade(cell *c);

void diffuse_and_bind(cell *c);

// binding/unbinding functions
int check_rmap(cell *c, int x, int y);

int check_pmap(cell *c, int x, int y);

void check_calcium_binding(cell *c, part *p);

void check_calcium_unbinding(cell *c, part *p);

void check_ip3_binding(cell *c, part *p);

void check_ip3_unbinding(cell *c, part *p);

int get_bindings(cell *c);

int get_xca1(cell *c);

int get_xca2(cell *c);

int get_xip3(cell *c);


#endif

