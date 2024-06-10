#include <stdio.h>
#include <cs50.h>

int main(void){

    string name = get_string("Enter name: ");
    /*
    int i;
    for (i=0; name[i] != '\0'; i++);
    printf("Length of input is: %i\n", i);
    */

    int n=0;
    while (name[n] != '\0'){
        n++;
    }
    printf("%i\n", n);
}
