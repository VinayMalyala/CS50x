#include <stdio.h>
#include <cs50.h>
#include <string.h> //strlen
#include <ctype.h> //toupper

int main(void){
    string s = get_string("Before: ");

    printf("After: ");
    for (int i=0, n=strlen(s); i < n; i++){
        if (s[i] >= 'a' && s[i] <= 'z'){
            printf("%c",toupper(s[i]));
        }
        else{
            printf("%c",s[i]);
        }
    }
    printf("\n");
}
