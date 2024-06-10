#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = get_int("Height: ");
    while (n < 1)
    {
        n = get_int("Height: ");
    }

    for (int i = 1; i < n + 1; i++)
    {
        for (int j = 1; j < n - i + 1; j++)
        {
            printf(" ");
        }
        for (int k = 1; k < i + 1; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int l = 1; l < i + 1; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}
