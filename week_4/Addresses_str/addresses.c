#include <cs50.h>
#include <stdio.h>

int main(void){

    // string s = "HI!";
    char *s = "HI!";

    printf("%p\n", s);
    // printf("%p\n", s[0]); invalid
    printf("%p\n", &s[0]);

    printf("%c", *s);
    printf("%c\n", *(s+1));
}
