#include <stdio.h>
#include <cs50.h>

int main(void){
    int x = get_int("What's x? \n"); //doesnot raise an error even the input is string
    int y = get_int("What's y? \n");

    if(x<y){
        printf("%d is less than %d\n",x,y);
    }else if(x>y){
        printf("%i is greater than %i\n",x,y);
    }else{
        printf("%d is equal to %i\n",x,y);
    }


    int a,b;
    printf("What's a?\n");
    scanf("%d",&a);
    printf("What's b?\n");
    scanf("%d",&b);

    if(a>b){
        printf("a is greater than b\n");
    }else{
        printf("a is not greater than b\n");
    }
}
