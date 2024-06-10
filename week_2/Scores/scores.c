#include <stdio.h>
#include <cs50.h>

int main(){
    const int N = 3;
    int scores[N];
    for(int i=0;i<N;i++){
        scores[i] = get_int("Score :");
    }
    int sum = 0;

    for(int i=0;i<N;i++){
        sum += scores[i];
    }

    printf("Average = %f\n",sum/(float)N);
}
