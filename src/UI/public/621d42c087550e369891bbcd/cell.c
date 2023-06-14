#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "clist.h"
#include "cell.h"


cell *
create_cell(int ip0, int ca0, int free_ca, params *param) {
    cell *c = (cell *) malloc(sizeof(cell));

    /*
     * main cell variables initialization
     *
     */
    c->param = param;
    c->free_ca = free_ca;

    double wx = param->wx;
    double wy = param->wy;
    int nr = param->nip3r;
    int size = param->size;

    /*
     * create calcium list
     */

    c->ca = (clist *) malloc(sizeof(clist));
    c->ca->start = 0x0;
    int i;
    for (i = 0; i < ca0; i++) {

        /*
         * create Ca particles at random position uniformly
         */
        double x = wx * box_noise();
        double y = wy * box_noise();
        part *p = create_part(x, y);
        /*
         * add it to the Ca list
         */
        add(c->ca, p);

    }

    /*
     * create ip3 list
     */

    c->ip3 = (clist *) malloc(sizeof(clist));
    c->ip3->start = 0x0;
    for (i = 0; i < ip0; i++) {

        /*
         * create IP3 particle at random position uniformly
         */
        double x = wx * box_noise();
        double y = wy * box_noise();
        part *p = create_part(x, y);

        // add it to IP3 list
        add(c->ip3, p);
    }

    /*
     * create (empty) receptors table
     * receptors are identified by their id (0<=i<nr) and are stored in the
     * rmap for easy access.
     */

    c->recs = (receptor **) malloc(nr * sizeof(receptor *));

    int iwx = (int) floor(wx / size) + 1;
    int iwy = (int) floor(wy / size) + 1;
    c->rmap = (int *) calloc((size_t) (iwx * iwy), sizeof(int));
    for (i = 0; i < iwx * iwy; i++)
        c->rmap[i] = -1;

    /*
     create plc position at random using param->nplc
     pmap = 1 if a plc molecule is at position (x, y) ; 0 otherwise 
     */

    c->pmap = (int *) calloc((size_t) (iwx * iwy), sizeof(int));
    for (i = 0; i < param->nplc; i++) {
        int x = (int) floor(iwx * box_noise());
        int y = (int) floor(iwy * box_noise());
        c->pmap[x + iwx * y] = 1;
    }
    return c;
}


void
add_ip3(int ip0, cell *c, params *param) {
    //function that adds an IP3 particle to the cell
    c->param = param;
    
    double wx = param->wx;
    double wy = param->wy;
    
    while (c->ip3->size < ip0) {
        /*
        * create IP3 at random position uniformly
        */
        double x = wx * box_noise();
        double y = wy * box_noise();
        part *p = create_part(x, y);
            
        /*
        * add it to the IP3 list
        */
        add(c->ip3, p);
    }
    
}


// functions for removal of particles from cell

void
remove_calcium(cell *c, part *p) {
    rem(c->ca, p);
    free(p);
    c->free_ca -= 1;
}

void
remove_ip3(cell *c, part *p) {
    rem(c->ip3, p);
    free(p);
}

// functions for diffusion of particles within the cell

void
diffuse_and_bind(cell *c) {
    // Ca diffusion
    node *no = c->ca->start;
    while (no != 0x0) {
        part *p = no->p;


        // check if particle Ca is bound to IP3R
        if (p->bound < 0) {
            // If Ca not bound, diffuse and check if binds to a plc molecule or to IP3R
            move_part(p,
                      c->param->wx,
                      c->param->wy,
                      c->param->Dca,
                      c->param->sdt);

            check_calcium_binding(c, p);


        } else {
            // Else (ie Ca is bound), check Ca unbinding
            check_calcium_unbinding(c, p);
        }
        no = no->next;
    }

    // IP3 diffusion
    no = c->ip3->start;
    while (no != 0x0) {
        part *p = no->p;
        // check if particle IP3 is bound to IP3R
        if (p->bound < 0) {
            // If IP3 not bound, diffuse and check if binds to IP3R
            move_part(p,
                      c->param->wx,
                      c->param->wy,
                      c->param->Dip3,
                      c->param->sdt);

            check_ip3_binding(c, p);
        } else {
            // If IP3 bound, check if unbinds
            check_ip3_unbinding(c, p);
        }
        no = no->next;
    }
}

int
check_rmap(cell *c, int x, int y) {
    /*
    	function that checks whether there is an IP3R molecule at position (x, y)
	-1: no IP3R at position (x, y)
	otherwise returns the indice of the given IP3R in c->recs
     */
    int s = c->param->size;
    double wx = c->param->wx;
    double wy = c->param->wy;
    int iwx = (int) floor(wx / s) + 1;
    int iwy = (int) floor(wy / s) + 1;
    if ((x < 0) || (x >= iwx) || (y < 0) || (y >= iwy))
        return -1;
    return c->rmap[x + iwx * y];

}

int check_pmap(cell *c, int x, int y) {
    /*
    	function that checks whether there is a PLC molecule at position (x, y)
	returns 1 if there is a PLC at position (x, y)
     */
    int s = c->param->size;
    double wx = c->param->wx;
    double wy = c->param->wy;
    int iwx = (int) floor(wx / s) + 1;
    int iwy = (int) floor(wy / s) + 1;
    if ((x < 0) || (x >= iwx) || (y < 0) || (y >= iwy))
        return 0;
    return c->pmap[x + iwx * y];
}

void
check_calcium_binding(cell *c, part *p) {
    // Function that checks Ca binding
    int s = c->param->size;
    int ix = (int) floor((p->x) / s);
    int iy = (int) floor((p->y) / s);


    // First, check Ca binding to PLC molecules
    int pl = check_pmap(c, ix, iy);
    if (pl == 1) {
        // If there is a PLC molecule at position (x, y), check Ca binding to PLC and IP3 synthesis
        double o = box_noise();
        if (o < c->param->delta) {
            part *ip = create_part(ix, iy);
            add(c->ip3, ip);
        }
    }

    // Then, check Ca binding to IP3R
    int rec = check_rmap(c, ix, iy);
    // Check if there is an IP3R at position (x, y)
    if (rec != -1) {
        receptor *r = c->recs[rec];

        if ((r->ca1 == 1) && (r->ca2 == 1))
	    // If both Ca sites are bound to Ca, do nothing
            return;

        // Check which Ca site is free, starting with the one that has higher probability to be bound: first Ca site
        if (r->ca1 == 0) {
	    // If first Ca site is free, check Ca binding
            double o = box_noise();
            if (o < c->param->a1) {
                r->ca1 = 1;
		c->free_ca -= 1;
                p->bound = 2 * rec;
                return;
            }
        }
        if (r->ca2 == 0) {
	    // If second Ca site is free, check Ca binding
            double o = box_noise();
            if (o < c->param->a3) {
                r->ca2 = 1;
		c->free_ca -= 1;
                p->bound = 2 * rec + 1;
                return;
            }
        }
    }
}


void
check_calcium_unbinding(cell *c, part *p) {
    // Function that checks Ca binding
    receptor *r = c->recs[(p->bound) / 2];
    int rtype = (p->bound) % 2;
    double unb = rtype == 0 ? c->param->b1 : c->param->b3;
    double o = box_noise();
    if (o < unb) {
        if (rtype == 0)
            r->ca1 = 0;
        else
            r->ca2 = 0;
        p->bound = -1;
	c->free_ca += 1;
    }
}


void
check_ip3_binding(cell *c, part *p) {
    // Function that checks IP3 binding to IP3R
    int s = c->param->size;
    int ix = (int) floor((p->x) / s);
    int iy = (int) floor((p->y) / s);
    int rec = check_rmap(c, ix, iy);
    if (rec != -1) {
        receptor *r = c->recs[rec];
        if (r->ip3 == 1)
            return;
        if (r->ip3 == 0) {
	    // IP3 can bind an IP3R only if no IP3 is already bound to it
            double o = box_noise();
            if (o < c->param->a2) {
                r->ip3 = 1;
                p->bound = rec;
                return;
            }
        }
    }
}

void
check_ip3_unbinding(cell *c, part *p) {
    // Function that checks IP3 unbinding from IP3R
    receptor *r = c->recs[p->bound];
    double unb = c->param->b2;
    double o = box_noise();
    if (o < unb) {
        r->ip3 = 0;
        p->bound = -1;
    }
}

void
degrade(cell *c) {
    // Decay of IP3 and Ca function


    // Ca decay

    node *np = c->ca->start;
    while (np != 0x0) {
        if (np->p->bound >= 0) {
            np = np->next;
        } else {
            // Only unbound Ca can decay, with probability alpha
            double o = box_noise();

            if (o < c->param->alpha) {

                part *p = np->p;
                np = np->next;
                rem(c->ca, p);
                free(p);
		c->free_ca -= 1;
            } else {
                np = np->next;
            }
        }
    }

    // IP3 decay
    np = c->ip3->start;
    while (np != 0x0) {
        if (np->p->bound >= 0) {
            np = np->next;
        } else {
            // Only unbound IP3 can decay, with probability beta
            double o = box_noise();

            if (o < c->param->beta) {

                part *p = np->p;
                np = np->next;
                rem(c->ip3, p);
                free(p);
            } else {
                np = np->next;
            }
        }
    }

}

void
produce(cell *c) {
    // Cytosolic influx of Calcium function

    // IP3R-dependent Ca influx
    int i;
    int nr = c->param->nip3r;
    for (i = 0; i < nr; i++) {
	// Check IP3R open state for each IP3R
        receptor *r = c->recs[i];
        int ca1 = r->ca1;
        int ip3 = r->ip3;
        int ca2 = r->ca2;
        int res = ca1 * ip3 * (1 - ca2);
        if (res > 0) {
	    // If IP3R open, Ca influx
            double o = box_noise();
            double mu = c->param->mu;
            while (o < mu) {
                part *p = create_part(r->x, r->y);
                add(c->ca, p);
		c->free_ca += 1;
                mu += -1;

            }

        } else {
	    // IP3R-independent Ca influx
            double var = box_noise();
    	    double le = c->param->gamma;
	    double rad = c->param->rgamma;
	    // 
	    if (c->param->rgamma == 100) {
		    // if rgamma == 100 => uniform distribution of this Ca influx
		    double var = box_noise();
	    	    double le = c->param->gamma;
	    	    if (var < le) {
			double x = c->param->wx * box_noise();
			double y = c->param->wy * box_noise();
			part *p = create_part(x, y);
			add(c->ca, p);
		    	c->free_ca += 1;
		    }
	    } else {
		    // else IP3R-independent Ca influx within rgamma radius from IP3R
		    if (var < le) {
			double t = 2 * 3.14159265358979323846 * box_noise();
			double ra = sqrt(box_noise()) * rad;
			double rx = (double)r->x;
			double ry = (double)r->y;
			double x = ra * cos(t) + rx;
			double y =  ra * sin(t) + ry;
		
			if (x < 0){
				x = 0;
			}
			if (y<0){
				y=0;
			}
			if (x > c->param->wx) {
				x = c->param->wx;
			}
			if (y > c->param->wy) {
				y = c->param->wy;
			}
			part *p = create_part(x, y);
			add(c->ca, p);
			c->free_ca += 1;
		    }
            }
        }
    }

}

void
cycle(cell *c) {
    // Cell main loop, called at each time step
    diffuse_and_bind(c);
    degrade(c);
    produce(c);
}

void
print_calcium_data(cell *c, char *name) {
    // function to print the positions of Ca ions at each time step
    node *no = c->ca->start;
    FILE *f = fopen(name, "w");
    if (f == NULL) {
        printf("Folder /movies to write Ca data doesn't exist");
        exit(EXIT_FAILURE);
    }
    while (no != 0x0) {
        fprintf(f, "%lg %lg\n", no->p->x, no->p->y);
        no = no->next;
    }
    fclose(f);
}

void
print_receptor_data(cell *c, char *name) {
    // function to print the positions of IP3R molecules at each time step
    int i;
    FILE *f = fopen(name, "w");
    if (f == NULL) {
        printf("Folder /movies to write IP3R data doesn't exist");
        exit(EXIT_FAILURE);
    }
    for (i = 0; i < c->param->nip3r; i++) {
        receptor *r = c->recs[i];
        fprintf(f, "%d %d\n", r->x, r->y);
    }
    fclose(f);
}


void
print_plc_data(cell *c, char *name) {
    // function to print the positions of PLC molecules at each time step
    int ix, iy;
    double wx = c->param->wx;
    double wy = c->param->wy;
    int size = c->param->size;
    FILE *f = fopen(name, "w");
    if (f == NULL) {
        printf("Folder /movies to write PLC data doesn't exist");
        exit(EXIT_FAILURE);
    }
    int iwx = (int) floor(wx / size) + 1;
    int iwy = (int) floor(wy / size) + 1;
    for (ix = 0; ix < iwx; ix++)
        for (iy = 0; iy < iwy; iy++) {
            if (c->pmap[ix + iwx * iy] == 1)
                fprintf(f, "%d %d\n", ix, iy);
        }
    fclose(f);
}


void
print_ip3_data(cell *c, char *name) {
    // function to print the positions of IP3 molecules at each time step
    node *no = c->ip3->start;
    FILE *f = fopen(name, "w");
    if (f == NULL) {
        printf("Folder /movies to write IP3 data doesn't exist");
        exit(EXIT_FAILURE);
    }
    while (no != 0x0) {
        fprintf(f, "%lg %lg\n", no->p->x, no->p->y);
        no = no->next;
    }
    fclose(f);
}

int
get_bindings(cell *c) {
    // function to get the number of open IP3R
    int i, s = 0;
    for (i = 0; i < c->param->nip3r; i++) {
        receptor *r = c->recs[i];
        int ca1 = r->ca1;
        int ip3 = r->ip3;
        int ca2 = r->ca2;
        int res = ca1 * ip3 * (1 - ca2);
        s += res;
    }
    return s;
}

int get_xca1(cell *c) {
    // function to get the number of first Ca sites bound
    int i, xca1 = 0;
    for (i = 0; i < c->param->nip3r; i++) {
	receptor *r = c->recs[i];
	xca1 += r->ca1;
    }
    return xca1;
}

int get_xca2(cell *c) {
    // function to get the number of second Ca sites bound
    int i, xca2 = 0;
    for (i = 0; i < c->param->nip3r; i++) {
	receptor *r = c->recs[i];
	xca2 += r->ca2;
    }
    return xca2;
}

int get_xip3(cell *c) {
    // function to get the number of IP3 sites bound
    int i, xip3 = 0;
    for (i = 0; i < c->param->nip3r; i++) {
	receptor *r = c->recs[i];
	xip3 += r->ip3;
    }
    return xip3;
}
