#ifndef __REC__
#define __REC__


typedef struct {
    unsigned char ca1;
    unsigned char ip3;
    unsigned char ca2;
    int x, y;
    int size;
} receptor;


receptor *create_receptor(int x, int y, int size);

#endif
