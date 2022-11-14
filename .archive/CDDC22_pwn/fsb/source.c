#include <stdio.h>

int main() 
{
    long buf[6]; 
    initialize(); 
    buf[4] = buf+9;  // gift 
    read(0, buf, sizeof buf); 
    printf(buf); 
}

