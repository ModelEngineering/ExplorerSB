#ifndef CLIST_H
#define CLIST_H

#include "part.h"

struct pnode {
    struct pnode *next;
    struct pnode *prev;
    part *p;
};


typedef struct pnode node;
typedef struct {
    node *start;
    int size;
} clist;


void add(clist *, part *);

void rem(clist *, part *);

void clear(clist *);

#endif

