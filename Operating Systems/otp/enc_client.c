#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>  // ssize_t
#include <sys/socket.h> // send(),recv()
#include <netdb.h>      // gethostbyname()
#include <ctype.h>

// Error function used for reporting issues
void error(const char *msg) { 
  perror(msg); 
  exit(0); 
} 

// Set up the address struct
void setupAddressStruct(struct sockaddr_in* address, 
                        int portNumber, 
                        char* hostname){
 
  // Clear out the address struct
  memset((char*) address, '\0', sizeof(*address)); 

  // The address should be network capable
  address->sin_family = AF_INET;
  // Store the port number
  address->sin_port = htons(portNumber);

  // Get the DNS entry for this host name ("localhost")
  struct hostent* hostInfo = gethostbyname(hostname); 
  if (hostInfo == NULL) { 
    fprintf(stderr, "CLIENT: ERROR, no such host\n"); 
    exit(0); 
  }
  // Copy the first IP address from the DNS entry to sin_addr.s_addr
  memcpy((char*) &address->sin_addr.s_addr, 
        hostInfo->h_addr_list[0],
        hostInfo->h_length);
}

// argv[1] = plaintext
// argv[2] = key
// argv[3] = portnumber
int main(int argc, char *argv[]) {
  int socketFD, charsWritten, charsRead;
  struct sockaddr_in serverAddress;
  char buffer[3]; // used to pass 1 plaintext char, 1 key char, and null-terminating char from client to server,
                  // and receive 1 ciphertext char back from server after encoding occurs
  char handshake[15]; // used to establish handshake between client and server

  // print to stderr if too little or too many arguments are given
  if (argc > 4) { 
    fprintf(stderr,"Too many arguments given for enc_client."); 
    exit(0); 
  }

  if (argc < 4) {
    fprintf(stderr, "Not enough arguments given for enc_client.");
  }

  // Create a socket
  socketFD = socket(AF_INET, SOCK_STREAM, 0); 
  if (socketFD < 0){
    error("CLIENT: ERROR opening socket");
  }

   // Set up the server address struct
  setupAddressStruct(&serverAddress, atoi(argv[3]), "localhost");

  // Connect to server
  if (connect(socketFD, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0){
    error("CLIENT: ERROR connecting");
  }

  // clear out handshake buffer
  memset(handshake, '\0', sizeof(handshake));
  // receive message from server
  charsRead = recv(socketFD, handshake, sizeof(handshake), 0);
  // if message received equals "enc_server", send back "continue" to let server know handshake successful
  if (strcmp(handshake, "enc_server") == 0) {
    memset(handshake, '\0', sizeof(handshake));
    strcpy(handshake, "continue");
    send(socketFD, handshake, strlen(handshake), 0);
  // if message received from server is anything other than "enc_server", print error and exit status 2
  } else {
    fprintf(stderr, "invalid server for enc_client\n");
    exit(2);
  }

  // initialize two file pointers, one for plaintext and one for key
  FILE *filestream_plaintext;
  FILE *filestream_key;

  // open the plaintext file with read mode, report error if unable to open file
  filestream_plaintext = fopen(argv[1], "r");
  if (filestream_plaintext == NULL) {
    error("ERROR opening plaintext file");
  }

  // open the key file with the read mode, report error if unable to open file
  filestream_key = fopen(argv[2], "r");
  if (filestream_key == NULL) {
    error("ERROR opening key file");
  }

  // infinite for loop where data will be read from plaintext and key, sent to the server, encoded, and sent back to client
  for (;;)
  {
   // Clear out the buffer array
    memset(buffer, '\0', sizeof(buffer));
    // obtain a char from the plaintext file
    char plaintext_char = fgetc(filestream_plaintext);

    //if (feof(filestream_plaintext)) break;

    // check if the char from plaintext is a newline char; this would mean we're at the end of the file
    // if so, add the char to the buffer and send it (so the buffer knows not to expect any more data) and break the loop.
    if (plaintext_char == '\n') {
      buffer[0] = plaintext_char;
      charsWritten = send(socketFD, buffer, strlen(buffer), 0);
      break;
    }

    // if the plaintext char is not an uppercase letter or a space, report error and exit status 1
    if (isupper(plaintext_char) == 0 && plaintext_char != ' ') {
      fprintf(stderr, "Invalid character received from plaintext");
      exit(1);
    }

    // place the plaintext char in the 0 index of buffer
    buffer[0] = plaintext_char;
    //printf("plaintext buffer[0] = %c\n", buffer[0]);

    // obtain a char from the key file
    char key_char = fgetc(filestream_key);

    /*if (feof(filestream_key) && !feof(filestream_plaintext)) {
      fprintf(stderr, "Key is shorter than plaintext");
      exit(1);
    }*/

    // check if the char from key is a newline char; this would mean we're at the end of the file
    // the end of plaintext should always be reached before this step
    // if this condition is met, the key is too short; send the char so the server knows not to expect any more data
    // report error and exit status 1
    if (key_char == '\n') {
      buffer[0] = key_char;
      charsWritten = send(socketFD, buffer, strlen(buffer), 0);
      fprintf(stderr, "Key is shorter than plaintext");
      exit(1);
    }

    // if the key char is not an uppercase letter or a space, report error and exit status 1
    if (isupper(key_char) == 0 && key_char != ' ') {
      fprintf(stderr, "Invalid character received from key");
      exit(1);
    }

    // place the key char in the 1 index of buffer
    buffer[1] = key_char;
    //printf("key buffer[1] = %c\n", buffer[1]);

    // send the buffer with the plaintext char and key char to the server
    charsWritten = send(socketFD, buffer, strlen(buffer), 0); 
    if (charsWritten < 0){
      error("CLIENT: ERROR writing to socket");
    }
    if (charsWritten < strlen(buffer)){
      printf("CLIENT: WARNING: Not all data written to socket!\n");
    }

    // clear out the buffer again to receive message back from the server
    memset(buffer, '\0', sizeof(buffer));

    // receive the encoded char back from the server
    charsRead = recv(socketFD, buffer, sizeof(buffer), 0);
    if (charsRead < 0){
      error("CLIENT: ERROR reading from socket");
    }

    // initialize a variable with the encoded char received from server and print it to stdout
    char ciphertext_char = buffer[0];
    printf("%c", ciphertext_char);

    // repeat loop until end of plaintext file is reached or error occurs
  }
  // finish by printing a newline char to stdout and closing the socket, plaintext file, and key file
  putchar('\n');
  close(socketFD);
  fclose(filestream_plaintext);
  fclose(filestream_key);
  return 0;
}
