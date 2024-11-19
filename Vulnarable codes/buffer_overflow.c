// buffer_overflow.c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];  // Buffer with space for 10 characters
    strcpy(buffer, "This is a test for buffer overflow!");  // Copy a longer string

    printf("Buffer content: %s\n", buffer);
    return 0;
}

