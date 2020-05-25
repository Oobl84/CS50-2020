// Implements a dictionary's functionality
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100;

// Hash table
node *table[N];

//word count in dictionary
int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int n = hash(word);

    node *tmp = table[n];

    while (tmp != NULL)
    {
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
        else
        {
            tmp = tmp->next;
        }
    }
    return false;
}

// Hashes word to a number - from http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{

    unsigned long hash_val = 5381;
    int c;

    while ((c = *word++))
    {
        hash_val = ((hash_val << 5) + hash_val) + tolower(c);
    }

    return (unsigned int)(hash_val % N);

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        return false;
    }

    char item[LENGTH + 1];

    while (fscanf(dict, "%s", item) != EOF)
    {
        node *w = malloc(sizeof(node));

        if (w == NULL)
        {
            return false;
        }
        strcpy(w->word, item);
        w->next = NULL;

        int h = hash(w->word);
        w->next = table[h];
        table[h] = w;

        word_count++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

        word_count = 0;
    }
    return true;
}
