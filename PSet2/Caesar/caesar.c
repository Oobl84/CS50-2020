#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            //check if each digit in argv is a number
            if (isdigit(argv[1][i]) == false)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    /*
    converting k to int and then normalising it
    to a place in the alphabet
    */

    int key = atoi(argv[1]) % 26;


    string text = get_string("plaintext: ");

    //variable to adjust position of character
    int shift;
    
    //starting output print
    printf("ciphertext: ");

    for (int i = 0; i < strlen(text); i++)
    {
        char c;
        //checking if character is uppercase
        if (text[i] >= 65 && text[i] <= 90)
        {
            shift = 65;
            c = (text[i] - shift + key) % 26 + shift;
            printf("%c", c);
        }
        //if character is lowercase
        else if (text[i] >= 97 && text[i] <= 122)
        {
            shift = 97;
            c = (text[i] - shift + key) % 26 + shift;
            printf("%c", c);
        }
        //print character as is
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;
}

