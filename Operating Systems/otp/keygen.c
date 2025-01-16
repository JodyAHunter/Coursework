#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#define MAX_CHAR 27

int
main(int argc, char *argv[])
{
  if (argc > 2) {
    errx(1, "Too many arguments given for keygen.");
  }

  if (argc < 2) {
    errx(1, "Not enough arguments given for keygen.");
  }

  // obtain length of key given as argument
  int key_length = atoi(argv[1]);
  //printf("key length = %d\n", key_length);

  // loop over the range of the key length, generating a random digit for each iteration
  int i;
  for (i = 0; i < key_length; i++) {
    int rand_num = rand() % MAX_CHAR;
    rand_num = rand_num + 65;
    // handle spaces
    if (rand_num == 91) {
      rand_num = 32;
    }
    printf("%c", rand_num);
  }

  putchar('\n');

  return 0;
}
