#include <stdio.h>
#include <cs50.h>

int main(void)
{

    long n; // input number
    long iter; // copy of long number to manipulate
    int counter = 0; //var to count digits
    int doubles = 0; //to store doubles of number
    int holder = 0; // to store inbetween step for doubles
    int remainders = 0; //to store other numbers
    int checksum; // to check value
    long divider = 1;  // for calculating digits
    int digits;

    n = get_long("Number:");
    iter = n;



    while (iter > 0)
    {

        //summing remainder numbers
        remainders += iter % 10;

        //remove final digit from iter and incrementing counter
        iter = (iter - (iter % 10)) / 10;
        counter += 1;
        
        //check that it needs to run next stage( for correct count)
        if (iter > 0)
        {
                
            //double and then add digits
            holder = (iter % 10) * 2;
    
            //removing doubled-digit from n and increment counter
            iter = (iter - (iter % 10)) / 10;
            counter += 1;
    
            //checking if it needs to add digits together
            if (holder >= 10)
            {
                doubles += 1 + (holder % 10);
            }
            else
            {
                doubles += holder;
            }
        }
    }
    checksum = doubles + remainders;

    if (checksum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        for (int i = 1; i <= (counter - 2); i++)
        {
            divider *= 10;

        }
        digits = (n - (n % divider)) / divider;

        if (counter == 15)
        {

            if (digits == 34 || digits == 37)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (counter == 16)
        {
            if (digits > 39 && digits < 50)
            {
                printf("VISA\n");
            }
            else if (digits > 50 && digits < 56)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (counter == 13)
        {
            if (digits > 39 && digits < 50)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
}