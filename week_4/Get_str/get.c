#include <stdio.h>

int main(void){
    // char *s;
    char s[5];
    printf("s: ");
    scanf("%s", s);
    printf("s: %s\n", s); //run --> clang -o get -Wno-uninitialized get.c
}
