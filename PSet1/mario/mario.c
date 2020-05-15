/*
Write a program to print a pyramid of hashes based on a number inputted by the user, similar to the pyramids that are in Mario.

*/

#include <stdio.h>
#include <cs50.h>


int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    for (int i = 1; i <= n; i++)
    {
        //printing spaces at the beginning of line
        for (int m = n - i; m > 0; m--)
        {
            printf(" ");
        }
        //printing # based on row number
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        //adding space between hashes
        printf("  ");
        //printing second set of hashes
        for (int k = 1; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
