#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check if they've provided the right number of arguments
    if (argc != 2)
    {
        printf("Please enter one input for the program.\n");
        return 1;
    }
    //open file in read mode.
    FILE *pics = fopen(argv[1], "r");

    //check that file has been stored correctly
    if (pics == NULL)
    {
        printf("file %s cannot be opened for reading.\n", argv[1]);
        return 1;
    }
    //pointer to hold each block
    BYTE buffer[512];

    //holding filename
    char filename[8];

    //to hold file count
    int n = 0;
    int chunks;
    int flag = 0;

    //create first file name
    sprintf(filename, "%03i.jpg", n);
    printf("%s\n", filename);

    //creates write file
    FILE *img = fopen(filename, "a");

    while ((chunks = fread(buffer, 512, 1, pics)) > 0)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            flag = 1;

            if (n == 0)
            {
                //write bytes to file
                fwrite(buffer, 512, 1, img);
                n++;
            }
            else
            {
                //close old file
                fclose(img);

                //print new filename
                sprintf(filename, "%03i.jpg", n);

                //create new file to write
                img = fopen(filename, "a");

                fwrite(buffer, 512, 1, img);
                n++;
            }
        }
        else
        {
            if (flag == 1)
            {
                fwrite(buffer, 512, 1, img);
            }
        }
    }
    fclose(img);
    fclose(pics);
    printf("end of file\n");
    printf("num pics: %i\n", n);
}
