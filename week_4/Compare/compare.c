#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void){

    char *s = get_string("s: ");
    char *t = get_string("t: ");

    if (strcmp(s, t) == 0){
        printf("Same\n");
    }
    else{
        printf("Different\n");
    }

    /*string s = get_string("s: ");
    string t = get_string("t: ");

    if (s == t){
        printf("Same\n");
    }
    else{
        printf("Different\n");
    }*/
}
