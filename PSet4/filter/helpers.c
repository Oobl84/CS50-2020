#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int px = round((image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen)/ (float) 3);
            image[i][j].rgbtBlue = px;
            image[i][j].rgbtRed = px;
            image[i][j].rgbtGreen = px;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float o_rd = image[i][j].rgbtRed;
            float o_gn = image[i][j].rgbtGreen;
            float o_bu = image[i][j].rgbtBlue;

            int sep_rd = round(0.393 * o_rd + 0.769 * o_gn + 0.189 * o_bu);
            int sep_gn = round(0.349 * o_rd + 0.686 * o_gn + 0.168 * o_bu);
            int sep_bu = round(0.272 * o_rd + 0.534 * o_gn + 0.131 * o_bu);

            if (sep_rd > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sep_rd;
            }

            if (sep_gn > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sep_gn;
            }

            if (sep_bu > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sep_bu;
            }

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE holder;
    int n = round(width / (float) 2);

    for (int i = 0; i < height; i++)
    {
        //only need to go halfway
        for (int j = 0; j < n ; j ++)
        {
            //setting holder pixel values to initial pixel
            holder.rgbtRed = image[i][j].rgbtRed;
            holder.rgbtGreen = image[i][j].rgbtGreen;
            holder.rgbtBlue = image[i][j].rgbtBlue;

            //setting initial pixel to opposite pixel
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;

            //setting opposite pixel to initial pixels original values
            image[i][width - j - 1].rgbtRed = holder.rgbtRed;
            image[i][width - j - 1].rgbtGreen = holder.rgbtGreen;
            image[i][width - j - 1].rgbtBlue = holder.rgbtBlue;

        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //temp array to hold transformed pixels
    RGBTRIPLE arr[height][width];

    int px_red = 0, px_green = 0, px_blue = 0;
    float counter = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            counter = 0;
            px_red = 0;
            px_green = 0;
            px_blue = 0;

            //checking neighbouring rows
            for (int r = -1; r < 2; r++)
            {
                if (i + r >= 0 && i + r < height)
                {
                    //checking neighbouring columns
                    for (int c = -1; c < 2; c++)
                    {
                        if (j + c >= 0 && j + c < width)
                        {
                            px_red += image[i + r][j + c].rgbtRed;
                            px_green += image[i + r][j + c].rgbtGreen;
                            px_blue += image[i + r][j + c].rgbtBlue;
                            counter++;
                        }
                    }

                }
            }
            //changing pixel colour
            arr[i][j].rgbtRed = round(px_red / counter);
            arr[i][j].rgbtGreen = round(px_green / counter);
            arr[i][j].rgbtBlue = round(px_blue / counter);
        }
    }

    //copying image back to original file.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = arr[i][j].rgbtRed;
            image[i][j].rgbtGreen = arr[i][j].rgbtGreen;
            image[i][j].rgbtBlue = arr[i][j].rgbtBlue;
        }
    }
    return;
}
