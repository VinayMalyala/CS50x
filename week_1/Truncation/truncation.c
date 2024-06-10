#include <stdio.h>
#include <cs50.h>

int main(){
    int x = get_int("x: ");
    int y = get_int("y: ");

    printf("%i\n",x/y);
    // printf("%f\n",x/y);

    float z = x/y;
    printf("%f\n",z); //truncation

    float a = (float)x/(float)y; //type casting
    printf("%f\n",a);
}
