#include <stdio.h>
#include <stdlib.h>
#include "clist.h"

void add(clist *li, part *pro) {
    // add particle pro to clist li
    node *no = malloc(sizeof(node));
    no->p = pro;
    no->next = 0x0;

    if (li->start) {
        node *cur = li->start;
        while (cur->next) {
            cur = cur->next;
        }
        cur->next = no;
        no->prev = cur;
    }
    else {
        li->start = no;
        no->prev = 0x0;
    }
    li->size += 1;
}

void rem(clist *li, part *p) {
    // remove particle p from clist li
    node *cur = li->start;

    while ((cur->p != p) && (cur->next != 0x0)) {
        cur = cur->next;
    }
    if (cur->p == p) {
        if (cur->prev) {
            cur->prev->next = cur->next;
        }
        else {
            li->start = cur->next;
	    if (li->start)
	      li->start->prev = 0x0;
        }
	if (cur->next)
	  cur->next->prev = cur->prev;
        free(cur);
        li->size += -1;
        if (li->size == 0)
            li->start = 0x0;
        return;
    }

}

void clear(clist *li) {
    // clear clist li
    if (li->start != 0x0) {
        node *tmp = li->start;
        li->start = tmp->next;
        li->size += -1;
        free(tmp);
        clear(li);
    }
}


