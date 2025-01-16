#define _POSIX_C_SOURCE 200809L
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <err.h>
#include <errno.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdint.h>

#ifndef MAX_WORDS
#define MAX_WORDS 512
#endif

// Skeleton code provided functions (expand modified by me)
char *words[MAX_WORDS];
size_t wordsplit(char const *line);
char * expand(char const *word);

int last_foreground_exit;  // global variable for the exit status of the last foreground command
pid_t recent_background_process;  // global variable for the process ID of the last background process

void sigint_handler(int sig) {}  // provided in assignment instructions; reprints the prompt for input when SIGINT is sent during get_line

int main(int argc, char *argv[])
{
  // sigaction struct that will store original dispositions for SIGTSTP, used for child process
  struct sigaction original_sigtstp = {0};
  // sigaction struct that will store original dispositions for SIGINT, used for child process
  struct sigaction original_sigint = {0};

  // establish sigaction struct with sa_handler set to SIG_IGN; used for ignoring the signal that it is assigned to
  // In this case, it will be used to ignore SIGTSTP at all times and SIGINT when not reading input
  struct sigaction ignore_action = {0};
  ignore_action.sa_handler = SIG_IGN;
  sigfillset(&ignore_action.sa_mask);
  ignore_action.sa_flags = 0;

  // call sigaction with the ignore struct for SIGTSTP
  sigaction(SIGTSTP, &ignore_action, &original_sigtstp);

  // establish sigaction struct with sa_handler set to the sigint_handler function provided
  // This will be used only when reading input 
  struct sigaction sigint_sigaction = {0};
  sigint_sigaction.sa_handler = sigint_handler;
  sigfillset(&sigint_sigaction.sa_mask);
  sigint_sigaction.sa_flags = 0;

  // call sigaction with the ignore struct for SIGINT
  sigaction(SIGINT, &ignore_action, &original_sigint);

  // Receive input, stdin if no file is provided
  FILE *input = stdin;
  char *input_fn = "(stdin)";
  if (argc == 2) {
    input_fn = argv[1];
    input = fopen(input_fn, "re");
    if (!input) err(1, "%s", input_fn);
  } else if (argc > 2) {
    errx(1, "too many arguments");
  }

  char *line = NULL;
  size_t n = 0;

  for (;;) {
prompt:;
       // background process management
       pid_t spawnpid = -5;
       int child_status;

       // check if background process was exited or signaled using non-blocking wait
       // child process id and exit status provided if exited
       // child process id and signal causing termination provided if signaled
       if ((spawnpid = waitpid(recent_background_process, &child_status, WNOHANG | WUNTRACED)) > 0) {
         if (WIFEXITED(child_status)) {
           fprintf(stderr, "Child process %d done. Exit status %d.\n", spawnpid, WEXITSTATUS(child_status));
            } else if (WIFSIGNALED(child_status)) {
                fprintf(stderr, "Child process %d done. Signaled %d.\n", spawnpid, WTERMSIG(child_status));
            }

         // if process was stopped, continue the process by sending SIGCONT signal
         if (WIFSTOPPED(child_status)) {
              if (kill(spawnpid, SIGCONT) == -1) {
                errx(1, "Error occurred sending SIGCONT.");
            } else {
              fprintf(stderr, "Child process %d stopped. Continuing.\n", spawnpid);
            }
         }
       }

    // Displays PS1 prompt using getenv if input is stdin
    if (input == stdin) {
      char* prompt;
      if ((prompt = getenv("PS1")) == NULL) {
        fprintf(stderr, "Error displaying prompt");
      } else {
        fprintf(stderr, "%s", prompt);
      }
    }

    // call sigaction with sigint_sigaction handler prior to reading input with get_line function
    sigaction(SIGINT, &sigint_sigaction, NULL);

    // read input
    ssize_t line_len = getline(&line, &n, input);

    // after reading input, change SIGINT sa_handler back to ignore
    sigaction(SIGINT, &ignore_action, NULL);
      
    // exit if at the end of given input; if reading input was interrupted, clear errno and jump back to prompt
    if (line_len < 0) {
      if (feof(input)) {
        exit(0);
      } else if (errno == EINTR) {
        errno = 0;
        clearerr(input);
        fprintf(stderr, "\n");
        goto prompt;
      } else {
        errx(errno, "Error reading from input.");
      }
    }
    
    // skeleton code - calls wordsplit and expand functions, parses words received and builds strings
    size_t nwords = wordsplit(line);
    for (size_t i = 0; i < nwords; ++i) {
      //fprintf(stderr, "Word %zu: %s\n", i, words[i]);
      char *exp_word = expand(words[i]);
      free(words[i]);
      words[i] = exp_word;
      //fprintf(stderr, "Expanded Word %zu: %s\n", i, words[i]);
    }
    
    // jump back to prompt if no words were given with input
    if (nwords == 0) goto prompt;

    // first word of the parsed words array is checked for built-in "exit" command
    // if more than 2 words are provided, error occurs for too many arguments given
    // if only the command is given with no argument, program exits with exit status of last foreground command
    // otherwise, the argument is checked for a digit at each char; program exits with the status of the given integer
    if (strcmp(words[0], "exit") == 0) {
      if (nwords > 2) {
        errx(1, "Too many arguments given for exit command.");
      } else if (nwords == 1) {
        exit(last_foreground_exit);
      } else {
        int digit_checker;
        for (digit_checker = 0; digit_checker < strlen(words[1]); digit_checker++) {
          if (isdigit(words[1][digit_checker]) == 0) {
            errx(1, "argument given for exit is not an integer.");
          }
        }
        // Update last_foreground_exit variable before exiting program
        last_foreground_exit = atoi(words[1]);
        exit(atoi(words[1]));
      }

    // first word of the parsed array is checked for built-in "cd" command
    // if more than 2 words are provided, error occurs for too many arguments given
    // if only the command is given with no argument, program changes to the home directory of the user
    // otherwise, program changes directories to the directory provided, or produces an error if directory does not exist
    } else if (strcmp(words[0], "cd") == 0) {
      if (nwords > 2) {
        errx(1, "Too many arguments given for cd command.");
      } else if (nwords == 1) {
        char *expanded_home = expand("${HOME}");
        if (chdir(expanded_home) == -1) {
          errx(1, "Error occurred while trying to cd to home directory.");
        }
      } else {
        if (chdir(words[1]) == -1) {
           errx(1, "Error occurred while trying to cd to directory: %s", words[1]);
        }
      }

    // if "exit" or "cd" is not given, a child process is forked to carry out any other commands given
    } else {

      // initialize an array for passing arguments to the execvp command in the child process
      char *exec_args[nwords + 1];
      // index counter used to build execution arguments array
      int exec_args_index = 0;

      // fork process
      spawnpid = fork();
      switch (spawnpid) {
        
        // fork error
        case -1:
          errx(1, "Error with forking.");
          break;

        // child process  
        case 0:

          // reset child process to the original signal dispositions when smallsh was invoked
          sigaction(SIGINT, &original_sigint, NULL);
          sigaction(SIGTSTP, &original_sigtstp, NULL);

          // Parse through words array to create a new array that will be passed on to execvp
          // checks for and handles redirection operators
          for (int i = 0; i < nwords; i++) {

            // redirect stdout to stdin by opening the file following the operator and calling dup2 function
            if (strcmp(words[i], ">") == 0) {
              if (words[i + 1]) {
                int targetFD = open(words[i + 1], O_WRONLY | O_CREAT | O_TRUNC, 0777);
                if (targetFD == -1) {
                  errx(1, "Error opening '>' argument.");
                }
                int newfd = dup2(targetFD, 1);
                if (newfd == -1) {
                  errx(2, "Error using dup2 for '>'.");
                }
              } else {
                errx(1, "No argument after '>' operator.");
              }
              // increment i to avoid adding operator to the new execvp arguments array
              i++;

              // redirect stdin to come from a file instead of the keyboard by opening the file following the operator and calling dup2 function
            } else if (strcmp(words[i], "<") == 0) {
              if (words[i + 1]) {
                int sourceFD = open(words[i + 1], O_RDONLY);
	              if (sourceFD == -1) { 
		              errx(1, "Error opening '<' argument."); 
                }
	              int result = dup2(sourceFD, 0);
	              if (result == -1) { 
		              errx(2, "Error using dup2 for '<'."); 
                }
              } else {
                errx(1, "No argument after the '<' operator.");
              }
              // increment i to avoid adding operator to the new execvp arguments array
              i++;

              // redirect stdout to stdin but open the file with the append flag instead of the trunc flag
            } else if (strcmp(words[i], ">>") == 0) {
              if (words[i + 1]) {
                int targetFD = open(words[i + 1], O_WRONLY | O_CREAT | O_APPEND, 0777);
                if (targetFD == -1) {
                  errx(1, "Error opening '>>' argument.");
                }
                int newfd = dup2(targetFD, 1);
                if (newfd == -1) {
                  errx(2, "Error using dup2 for '>>'.");
                }
              } else {
                errx(1, "No argument after the '>>' operator.");
              }
              // increment i to avoid adding operator to the new execvp arguments array
              i++;

              // if no redirection operators are present, add the currnt index of words to the current index of the new execvp arguments array
              // increment the index of the execvp arguments array before starting loop over
            } else {
              exec_args[exec_args_index] = words[i];
              exec_args_index++;
            }
          }

          // set null terminator for execvp arguments array
          exec_args[exec_args_index] = NULL;

          // call execvp function with the newly parsed exec args array
          if (execvp(exec_args[0], exec_args) == -1) {
              errx(1, "execvp failed :(");
          }
          break;

        // parent process
        default:

          // checks the last token for the background process operator
          // if operator is not present, performs a non-blocking wait of the child process
          if (strcmp(words[nwords-1], "&") != 0) {
            spawnpid = waitpid(spawnpid, &child_status, WUNTRACED);

            // if the child process is exited, the last_foreground_exit variable is updated with child process id
            if (WIFEXITED(child_status)) {
              last_foreground_exit = WEXITSTATUS(child_status);
            // if the child process was terminated by a signal, last_foreground_exit variable is updated with the signal number
            } else if (WIFSIGNALED(child_status)) {
              last_foreground_exit = (WTERMSIG(child_status)) + 128;

            // if the child process is stopped, it is continued with the SIGCONT signal
            // recent_background_process variable is updated with child process id and it continues as a background process
            } else if (WIFSTOPPED(child_status)) {
                if (kill(spawnpid, SIGCONT) == -1) {
                  errx(1, "Error occurred sending SIGCONT to foreground process.");
              } else {
                fprintf(stderr, "Child process %d stopped. Continuing.\n", spawnpid);
                recent_background_process = spawnpid;
              }
          }

          // treat child as background process
          // update recent_background_process variable and start over infinite loop
          } else {
            recent_background_process = spawnpid;
          }
          break;
      }
    }
  }
}

char *words[MAX_WORDS] = {0};


/* Splits a string into words delimited by whitespace. Recognizes
 * comments as '#' at the beginning of a word, and backslash escapes.
 *
 * Returns number of words parsed, and updates the words[] array
 * with pointers to the words, each as an allocated string.
 */
size_t wordsplit(char const *line) {
  size_t wlen = 0;
  size_t wind = 0;

  char const *c = line;
  for (;*c && isspace(*c); ++c); /* discard leading space */

  for (; *c;) {
    if (wind == MAX_WORDS) break;
    /* read a word */
    if (*c == '#') break;
    for (;*c && !isspace(*c); ++c) {
      if (*c == '\\') ++c;
      void *tmp = realloc(words[wind], sizeof **words * (wlen + 2));
      if (!tmp) err(1, "realloc");
      words[wind] = tmp;
      words[wind][wlen++] = *c; 
      words[wind][wlen] = '\0';
    }
    ++wind;
    wlen = 0;
    for (;*c && isspace(*c); ++c);
  }
  return wind;
}


/* Find next instance of a parameter within a word. Sets
 * start and end pointers to the start and end of the parameter
 * token.
 */
char
param_scan(char const *word, char const **start, char const **end)
{
  static char const *prev;
  if (!word) word = prev;
  
  char ret = 0;
  *start = 0;
  *end = 0;
  for (char const *s = word; *s && !ret; ++s) {
    s = strchr(s, '$');
    if (!s) break;
    switch (s[1]) {
    case '$':
    case '!':
    case '?':
      ret = s[1];
      *start = s;
      *end = s + 2;
      break;
    case '{':;
      char *e = strchr(s + 2, '}');
      if (e) {
        ret = s[1];
        *start = s;
        *end = e + 1;
      }
      break;
    }
  }
  prev = *end;
  return ret;
}

/* Simple string-builder function. Builds up a base
 * string by appending supplied strings/character ranges
 * to it.
 */
char *
build_str(char const *start, char const *end)
{
  static size_t base_len = 0;
  static char *base = 0;

  if (!start) {
    /* Reset; new base string, return old one */
    char *ret = base;
    base = NULL;
    base_len = 0;
    return ret;
  }
  /* Append [start, end) to base string 
   * If end is NULL, append whole start string to base string.
   * Returns a newly allocated string that the caller must free.
   */
  size_t n = end ? end - start : strlen(start);
  size_t newsize = sizeof *base *(base_len + n + 1);
  void *tmp = realloc(base, newsize);
  if (!tmp) err(1, "realloc");
  base = tmp;
  memcpy(base + base_len, start, n);
  base_len += n;
  base[base_len] = '\0';

  return base;
}

/* Expands all instances of $! $$ $? and ${param} in a string 
 * Returns a newly allocated string that the caller must free
 */
char *
expand(char const *word)
{
  char const *pos = word;
  char const *start, *end;
  char c = param_scan(pos, &start, &end);
  build_str(NULL, NULL);
  build_str(pos, start);
  while (c) {
    if (c == '!') {
      
      // expands the recent_background_process variable
      // if no background process is available yet, an empty string is built
      if (recent_background_process != 0) {
          char *recent_background_process_string;
          asprintf(&recent_background_process_string, "%d", recent_background_process);
          build_str(recent_background_process_string, NULL);
          free(recent_background_process_string);
      } else {
        build_str("", NULL);
      }
    }  // expands the process id of the current process
    else if (c == '$') {
      pid_t pid = getpid();
      char *pid_str;
      asprintf(&pid_str, "%d", pid);
      build_str(pid_str, NULL);
      free(pid_str);
    }  // expands the last_foreground_exit variable
       // if there is no last_foreground_exit, a string is built with the value of "0"
    else if (c == '?') {
      if (last_foreground_exit == 0) {
        build_str("0", NULL);
      } else {
        char *last_foreground_exit_string;
        asprintf(&last_foreground_exit_string, "%d", last_foreground_exit);
        build_str(last_foreground_exit_string, NULL);
        free(last_foreground_exit_string);
      }
    }
    //  expands environment variables using getenv function
    else if (c == '{') {
      // obtain the length of the variable string by ignoring the "${}" characters and leaving an extra index for null termination
      size_t stripped_var_len = (end - 1) - (start + 2) + 1;
      // create new string with obtained length
      char stripped_var[stripped_var_len];
      // variable for number of bytes to copy in strncpy, leave last index for null terminator
      int bytes_copied = stripped_var_len - 1;
      // call strncpy starting at first char after '{' in environment variable
      strncpy(stripped_var, start + 2, bytes_copied);
      // add null terminator
      stripped_var[bytes_copied] = '\0';
      // call getenv and build str with result, if getenv returns null, build empty string
      if (getenv(stripped_var) == NULL) {
          build_str("", NULL);
      } else {
        build_str(getenv(stripped_var), NULL);
      }
    }
    
    pos = end;
    c = param_scan(pos, &start, &end);
    build_str(pos, start);
  }
  return build_str(start, NULL);
}
