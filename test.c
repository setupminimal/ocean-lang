#include <stdio.h>

// C-Alike Example

/*
 This program checks to see if the input number
 represents a leap year. */
int main(void)
{
    int year; // This stores the year

    /* We also need to test what happens
       when block comments exist */
    printf("Enter a year\n");
    /* Or when they do wierd indenty things */
    scanf("%d", &year);

    if (year % 400 == 0)
    {
        printf("%d is a leap year.\n", year);
    }
    else if (year % 100 == 0)
    {
        printf("%d is not a leap year.\n", year);
    }
    else if (year % 4 == 0)
    {
        printf("%d is a leap year.\n", year);
    }
    else
    {
        printf("%d is not a leap year.\n", year);
    }

    return 0;
}

// The End

