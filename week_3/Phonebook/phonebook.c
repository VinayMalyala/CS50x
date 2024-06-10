#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void){
    string names[] = {"Carter", "David", "John"};
    string numbers[] = {"+1-617-495-1000", "+1-617-495-1045", "+1-617-495-1060"};

    string name = get_string("Name: ");
    for (int  i=0; i<3; i++){
        if (strcmp(names[i], name) == 0){
            printf("Found %s\n", numbers[i]);
            return 0;
        }
    }
    printf("Not Found\n");
    return 1;
}
