#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);

    int coins = 0;

    while (change >= 25)
    {
        change -= 25;
        coins++;
    }

    while (change >= 10)
    {
        change -= 10;
        coins++;
    }

    while (change >= 5)
    {
        change -= 5;
        coins++;
    }

    while (change >= 1)
    {
        change -= 1;
        coins++;
    }

    printf("%i\n", coins);
}
