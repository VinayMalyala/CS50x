#include <stdio.h>
#include <cs50.h>

int calc(int a, char opr, int b) {
    switch (opr) {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b != 0) {
                return a / b;
            } else {
                printf("Error: Division by zero!\n");
                return 0;
            }
        default:
            printf("Error: Invalid operator. Supported operators are '+', '-', '*', and '/'.\n");
            return 0;
    }
}

int main() {
    int x = get_int("Enter x: ");
    char opr = get_char("Enter operator (+, -, *, /): ");
    int y = get_int("Enter y: ");

    printf("%i %c %i = %i\n", x, opr, y, calc(x, opr, y));
}
