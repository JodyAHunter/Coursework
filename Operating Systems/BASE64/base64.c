#include <stdio.h>
#include <errno.h>
#include <stdint.h>
#include <string.h>
#include <err.h>

static char const b64_alphabet[] = 
  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  "abcdefghijklmnopqrstuvwxyz"
  "0123456789"
  "+/";

int main(int argc, char *argv[])
{
    FILE *filestream = stdin;

    // Error handling for too many arguments given
    if (argc > 2) {
        fprintf(stderr, "Usage: %s [FILE]\n", argv[0]);
        errx(1, "Too many arguments");
    // File given to read from instead of stdin
    } else if (argc == 2 && strcmp(argv[1], "-")) {
        filestream = fopen(argv[1], "r");
        if (filestream == NULL) {
            errx(1, "An error opening the file has occurred");
        }
    }
    // Loop counter for placing newline character
    int loop_counter = 0;

    for (;;) {
        uint8_t input_bytes[3] = {0};
        size_t n_read = fread(input_bytes, 1, 3, filestream);
        // Error handling for reading from the filestream
        if (ferror(filestream) != 0) {
            errx(1, "Error occurred while reading from filestream\n");
        }
        // Conditional for 0 bytes of input given, close file if not stdin and exit 0
        if (n_read == 0 && loop_counter == 0) {
            if (filestream != stdin) {
                fclose(filestream);
            }
            return 0;
        }
        // Data successfully read from filestream
        if (n_read != 0) {

            int alph_ind[4];
            alph_ind[0] = input_bytes[0] >> 2;
            alph_ind[1] = (input_bytes[0] << 4 | input_bytes[1] >> 4) & 0x3Fu;
            alph_ind[2] = (input_bytes[1] << 2 | input_bytes[2] >> 6) & 0x3Fu;
            alph_ind[3] = input_bytes[2] & 0x3Fu;

            char output[4];
            output[0] = b64_alphabet[alph_ind[0]];
            output[1] = b64_alphabet[alph_ind[1]];
            output[2] = b64_alphabet[alph_ind[2]];
            output[3] = b64_alphabet[alph_ind[3]];
          
            // 1 byte received, two '=' required for padding
            if (n_read == 1) {
                fwrite(output, 1, 2, stdout);
                putchar('=');
                putchar('=');
            // 2 bytes received, one '=' required for padding
            } else if (n_read == 2) {
                fwrite(output, 1, 3, stdout);
                putchar('=');
            // 3 bytes received, no padding neccessary
            } else {
            fwrite(output, 1, 4, stdout);
            // Error handling for writing to stdout
            if (ferror(stdout)) {
                errx(1, "An error occurred while writing to stdout\n");
            }
            }
            // Increment loop counter and check if newline character is needed
            loop_counter += 1;
            if (loop_counter % 19 == 0) {
                putchar('\n');

            }
        }
        // Check if at the end of filestream and place newline character if one was not just placed for wrapping
        if (n_read < 3) {
            if (feof(filestream)) {
                if (loop_counter % 19 == 0) {
                    break;
                } else {
                  putchar('\n');
                  break;
                }
            }
        }
    }
    // If receiving input from an opened file and not stdin, close the file
    if (filestream != stdin) {
      fclose(filestream);
    }
    return 0;
    }
