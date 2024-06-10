#include <stdio.h>
#include <cs50.h>

int main(void){
    int numbers[] = {20, 500, 100, 10, 1, 50};

    int n = get_int("Number: ");

    for (int i=0; i<7; i++){
        if(numbers[i] == n){
            printf("Number Found\n");
            return 0;
        }
    }
    printf("Number not Found\n");
    return 1;
}
