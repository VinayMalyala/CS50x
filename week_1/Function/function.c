#include <stdio.h>
#include <cs50.h>

void meow(){
    printf("meow\n");
}

int main(void){
    for(int i=0;i<3;i++){
        meow();
    }
}
