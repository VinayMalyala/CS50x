#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[]){
    if (argc != 2){
        printf("Missing command-line argument\n"); //./greet Vinay Malyala
        return 1;
    }
    printf("hello, %s\n", argv[1]); //./greet Vinay
    return 0;  //echo $?
}
