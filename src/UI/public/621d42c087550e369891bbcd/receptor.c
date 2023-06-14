#include <stdio.h>
#include <stdlib.h>
#include "receptor.h"


receptor *create_receptor(int x, int y, int size) {
    // an IP3R is defined by its position in x and y and by its size
    receptor *r = (receptor *) malloc(sizeof(receptor));
    r->x = x;
    r->y = y;
    r->size = size;
    // IP3R First Ca, IP3 and second Ca binding sites are initialized at 0 = unbound state
    r->ca1 = 0;
    r->ip3 = 0;
    r->ca2 = 0;

    return r;

}
