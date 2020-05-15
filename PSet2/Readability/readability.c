#include <stdio.h>
#include <cs50.h>
#include <math.h> //for round
#include <ctype.h> //for lowercase
#include <string.h> //for strlen


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // save output from count functions
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    //calculate letters per hundred words and sentences per hundred words
    float let_per_hundw = (letters / (float) words) * 100;
    float sen_per_hundw = (sentences / (float) words) * 100;

    //calculate score
    float index = round(0.0588 * let_per_hundw - 0.296 * sen_per_hundw - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %0.0f\n", index);
    }


}

//counting letters in text
int count_letters(string text)
{
    int l_count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (tolower(text[i]) >= 97 && tolower(text[i]) <= 122) // looking only at lowercase letters.
        {
            l_count++;
        }
    }
    return l_count;
}

//counting words in text
int count_words(string text)
{
    int w_count = 1;
    int flag = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 32) //ascii code for spaces
        {   
            flag = 1; //flag for whether a space has been seen
        }
        if (isalpha(text[i]) && flag == 1) // check if next character is a letter
        {
            w_count++;
            flag = 0;
        }
    }
    return w_count;
}

//counting sentences in text
int count_sentences(string text)
{
    int s_count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        //checking for "!","." and "?" respectively
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            s_count++;
        }
    }
    return s_count;
}