#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <err.h>
#include <errno.h>
#include <pthread.h>

#define SIZE 1000 // number of characters per line of input

#define NUM_ITEMS 50 // number of lines of input

// Buffer 1, shared resource between Input Thread and Line Separator Thread
char buffer_1[NUM_ITEMS*SIZE];
// Number of items in the buffer
int count_1 = 0;
// Index where the Input Thread will put the next item
int prod_idx_1 = 0;
// Index where the Line Separator Thread will pick up the next item
int con_idx_1 = 0;
// Initialize the mutex for buffer 1
pthread_mutex_t mutex_1 = PTHREAD_MUTEX_INITIALIZER;
// Initialize the condition variables for buffer 1
pthread_cond_t full_1 = PTHREAD_COND_INITIALIZER;
pthread_cond_t empty_1 = PTHREAD_COND_INITIALIZER;

// Buffer 2, shared resource between Line Separator Thread and Plus Sign Thread
char buffer_2[NUM_ITEMS*SIZE];
// Number of items in the buffer
int count_2 = 0;
// Index where the Line Separator Thread will put the next item
int prod_idx_2 = 0;
// Index where the Plus Sign Thread will pick up the next item
int con_idx_2 = 0;
// Initialize the mutex for buffer 2
pthread_mutex_t mutex_2 = PTHREAD_MUTEX_INITIALIZER;
// Initialize the condition variables for buffer 2
pthread_cond_t full_2 = PTHREAD_COND_INITIALIZER;
pthread_cond_t empty_2 = PTHREAD_COND_INITIALIZER;

// Buffer 3, shared resource between Plus Sign Thread and Output Thread
char buffer_3[NUM_ITEMS*SIZE];
// Number of items in the buffer
int count_3 = 0;
// Index where the Plus Sign Thread will put the next item
int prod_idx_3 = 0;
// Index where the Output Thread will pick up the next item
int con_idx_3 = 0;
// Initialize the mutex for buffer 3
pthread_mutex_t mutex_3 = PTHREAD_MUTEX_INITIALIZER;
// Initialize the condition variables for buffer 3
pthread_cond_t full_3 = PTHREAD_COND_INITIALIZER;
pthread_cond_t empty_3 = PTHREAD_COND_INITIALIZER;

// function that puts a char from the input line into buffer_1 from the get_input function;
// called within a for loop, n represents current index of iteration, increments producer index
// and count of items in buffer_1 with each iteration;
char* put_buffer1(char *line, size_t n)
{
  buffer_1[prod_idx_1] = line[n];
  prod_idx_1++;
  count_1++;
  return line;
}

// function that gets a line from buffer_1;
// initializes a pointer 'line' to the start of buffer_1 at the consumer index;
// iterates over the line from buffer with a for loop and adds each character 'i' to the initialized 'line' pointer;
// consumer index is incremented and count of items in buffer_1 is decremented with each iteration;
char* get_buffer1()
{
    char* line = &buffer_1[con_idx_1];
    for (int i = 0; i < strlen(line); i++) {
      line[i] = buffer_1[con_idx_1];
      con_idx_1++;
      count_1--;
    }
    return line;
}

// function that puts a char into buffer_2 from the line in the line_separator function after converting newlines to spaces;
// called within a for loop, i represents current index of iteration, increments producer index
// and count of items in buffer_2 with each iteration;
char* put_buffer2(char *line2, int i)
{
  buffer_2[prod_idx_2] = line2[i];
  prod_idx_2++;
  count_2++;
  return line2;
}

// function that gets a line from buffer_2;
// initializes a pointer 'line' to the start of buffer_2 at the consumer index;
// iterates over the line from buffer with a for loop and adds each character 'i' to the initialized 'line' pointer;
// consumer index is incremented and count of items in buffer_2 is decremented with each iteration;
char* get_buffer2()
{
    char* line = &buffer_2[con_idx_2];
    for (int i = 0; i < strlen(line); i++) {
      line[i] = buffer_2[con_idx_2];
      con_idx_2++;
      count_2--;
    }
    return line;
}

// function that puts a char into buffer_3 from the modified line in the plus_sign function after converting '++' to '^';
// called within a for loop, i represents current index of iteration, increments producer index
// and count of items in buffer_3 with each iteration;
char* put_buffer3(char *modified_line3, int i)
{
  buffer_3[prod_idx_3] = modified_line3[i];
  prod_idx_3++;
  count_3++;
  return modified_line3;
}

// function that gets a line from buffer_3;
// initializes a pointer 'line' to the start of buffer_3 at the consumer index;
// iterates over the line from buffer with a for loop and adds each character 'i' to the initialized 'line' pointer;
// consumer index is incremented and count of items in buffer_3 is decremented with each iteration;
char* get_buffer3()
{
    char* line = &buffer_3[con_idx_3];
    for (int i = 0; i < strlen(line); i++) {
      line[i] = buffer_3[con_idx_3];
      con_idx_3++;
      count_3--;
    }
    return line;
}

// this function is the first thread;
// function that receives input from stdin in an infinite loop and puts the input into buffer_1;
// this is a modified version of the mtp_single_thread skeleton code on os1;
void *get_input(void *args)
{
  // initialize char pointer and allocated size to use in getline
  char *line = NULL;
  size_t n = 0;
  // begin infinite loop
  for (;;) {
    // read from stdin to line
    ssize_t len = getline(&line, &n, stdin);
    // error handling/break if STOP\n is passed from stdin
    if (len == -1) {
      if (feof(stdin)) break; // EOF is not defined by the spec. I treat it as "STOP\n"
      else err(1, "stdin");
    }
    if (strcmp(line, "STOP\n") == 0) break;

    // lock mutex_1; when count of buffer_1 is at max capacity, wait for signal that buffer has space available
    pthread_mutex_lock(&mutex_1);
    while (count_1 == SIZE*NUM_ITEMS)
      pthread_cond_wait(&empty_1, &mutex_1);

    // for loop that iterates over the length of the line read from stdin, placing each char into buffer_1;
    for (size_t n = 0; n < len; ++n) {
      put_buffer1(line, n);
    }

    // send signal that buffer_1 now has data and unlock mutex_1; 
    pthread_cond_signal(&full_1);
    pthread_mutex_unlock(&mutex_1);
  }
  free(line);
  return NULL;
}

// this function is the second thread;
// function that receives data from buffer_1 and changes all newline characters into spaces ('\n' -> ' ');
// after modifying the data, new data is placed into buffer_2;
void *line_separator(void *args)
{
  // lock mutex_1; when buffer_1 is empty, wait for signal that data has been added to the buffer
  pthread_mutex_lock(&mutex_1);
  while (count_1 == 0)
    pthread_cond_wait(&full_1, &mutex_1);

  // initialize a char pointer and call get_buffer1 to receive a line of data from buffer_1
  char *line2 = get_buffer1();

  // send signal that buffer_1 now has space for data and unlock mutex_1
  pthread_cond_signal(&empty_1);
  pthread_mutex_unlock(&mutex_1);

  // iterate over the line received from buffer_1 in a for loop;
  // check each char, if char is a newline character '\n', then replace it with a space ' '
  for (int i = 0; i < strlen(line2); i++) {
    if (line2[i] == '\n' ) {
      line2[i] = ' ';
    }
  }
  // lock mutex_2; when count of buffer_2 is at max capacity, wait for signal that space is available
  pthread_mutex_lock(&mutex_2);
  while (count_2 == SIZE*NUM_ITEMS)
    pthread_cond_wait(&empty_2, &mutex_2);

  // iterate over the length of the line placing each character into buffer_2
  for (int i = 0; i < strlen(line2); i++ ) {
    put_buffer2(line2, i);
  }
  // send signal that buffer_2 now has data and unlock mutex_2
  pthread_cond_signal(&full_2);
  pthread_mutex_unlock(&mutex_2);

  return NULL;
}

// this function is the third thread;
// function that receives data from buffer_2 and changes any occurrence of "++" in the line to '^';
// after line is modified, the new data is added to buffer_3
void *plus_sign(void *args)
{
  // lock mutex 2; when buffer_2 is empty, wait for the signal that data has been added to the buffer
  pthread_mutex_lock(&mutex_2);
  while (count_2 == 0)
    pthread_cond_wait(&full_2, &mutex_2);

  // initialize a char pointer and call get_buffer2 to receive a line of data from buffer_2
  char *line3 = get_buffer2();
  // signal that buffer_2 now has space for data and unlock mutex_2
  pthread_cond_signal(&empty_2);
  pthread_mutex_unlock(&mutex_2);

  // initialize a char array with the length of line3 received from buffer_2 and an index counter
  char modified_line3[strlen(line3)];
  int modified_line_index = 0;
  // iterate over the length of the line checking each char and its following char for two consecutive plus signs;
  // if found, the two plus signs are replaced with a single '^' character in the modified line
  for (int i = 0; i < strlen(line3); i++) {
    if (line3[i] == '+' && line3[i+1] == '+') {
      i++;
      modified_line3[modified_line_index] = '^';
    } else {
      modified_line3[modified_line_index] = line3[i];
    }
    modified_line_index++;
  }
  // lock mutex_2; when count of buffer_3 is at max capacity, wait for signal that space is available  
  pthread_mutex_lock(&mutex_3);
  while (count_3 == SIZE*NUM_ITEMS)
    pthread_cond_wait(&empty_3, &mutex_3);

  // iterate over the length of the modified line placing each char into buffer_3
  for (int i = 0; i < strlen(modified_line3); i++ ) {
    put_buffer3(modified_line3, i);
    }

  // send signal that buffer_3 now has data and unlock mutex_3
  pthread_cond_signal(&full_3);
  pthread_mutex_unlock(&mutex_3);

  return NULL;
}

// this function is the fourth thread;
// function that receives data from buffer_3 and prints the data to stdout, 80 chars at a time followed by newline '\n';
// the logic for displaying the output comes from the os1 mtp_single_thread skeleton code
void *output(void *args)
{
  // initialize 80 character array to be used for displaying to stdout, along with an character counter
  char output[80];
  size_t output_counter = 0;
  // lock mutex_3; when buffer_3 is empty, wait for the signal that data has been added to the buffer
  pthread_mutex_lock(&mutex_3);
  while (count_3 == 0)
    pthread_cond_wait(&full_3, &mutex_3);

  // initialize a char pointer and call get_buffer3 to receive a line of data from buffer_3 
  char *line4 = get_buffer3();
  // signal that buffer_3 now has space for data and unlock mutex_3
  pthread_cond_signal(&empty_3);
  pthread_mutex_unlock(&mutex_3);

  // iterate over the length of the line received from buffer_3 adding each char to the matching index of the output array
  for (size_t n = 0; n < strlen(line4); ++n) {
    output[output_counter] = line4[n];
    // check if the counter is at 80 chars with each iteration; if so, write output to stdout, place newline, and flush stdout
    if (++output_counter == 80) {
      fwrite(output, 1, 80, stdout);
      putchar('\n');
      fflush(stdout);
      // reset the output character counter to 0
      output_counter = 0;
    }
  }
  return NULL;
}

int main()
{
    // initialize IDs of the four threads
    pthread_t input_t, line_separator_t, plus_sign_t, output_t;
    // Start threads
    pthread_create(&input_t, NULL, get_input, NULL);
    pthread_create(&line_separator_t, NULL, line_separator, NULL);
    pthread_create(&plus_sign_t, NULL, plus_sign, NULL);
    pthread_create(&output_t, NULL, output, NULL);
    // wait for threads to exit
    pthread_join(input_t, NULL);
    pthread_join(line_separator_t, NULL);
    pthread_join(plus_sign_t, NULL);
    pthread_join(output_t, NULL);
    exit(0);
}
