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

  // Get the DNS entry for this host name
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

// argv[1] = ciphertext
// argv[2] = key
// argv[3] = portnumber
int main(int argc, char *argv[]) {
  int socketFD, charsWritten, charsRead;
  struct sockaddr_in serverAddress;
  char buffer[3]; // used to pass 1 ciphertext char, 1 key char, and 1 null-terminating char to server,
                  // and receive back 1 plaintext char from server after decoding occurs
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
  // if message received is "dec_server", send back "continue" to let the server know the handshake was successful
  if (strcmp(handshake, "dec_server") == 0) {
    memset(handshake, '\0', sizeof(handshake));
    strcpy(handshake, "continue");
    send(socketFD, handshake, strlen(handshake), 0);
  // if message received from server is anything other than "dec_server", print error and exit status 2
  } else {
    fprintf(stderr, "invalid server for dec_client\n");
    exit(2);
  }

  // initialize two file pointers, one for ciphertext and one for key
  FILE *filestream_ciphertext;
  FILE *filestream_key;

  // open the ciphertext file with read mode, report error if unable to open file
  filestream_ciphertext = fopen(argv[1], "r");
  if (filestream_ciphertext == NULL) {
    error("ERROR opening ciphertext file");
  }

  // open the key file with read mode, report error if unable to open file
  filestream_key = fopen(argv[2], "r");
  if (filestream_key == NULL) {
    error("ERROR opening key file");
  }

  // infinite for loop where data will be read from ciphertext and key, sent to the server, decoded, and sent back to client
  for (;;)
  {
   // Clear out the buffer array
    memset(buffer, '\0', sizeof(buffer));
    // obtain a char from the ciphertext file
    char ciphertext_char = fgetc(filestream_ciphertext);

    //if (feof(filestream_ciphertext)) break;

    // check if the char from ciphertext is a newline char; this would mean we're at the end of the file
    // if so, add the char to the buffer and send it (so the server knows not to expect any more data) and break the loop.
    if (ciphertext_char == '\n') {
      buffer[0] = ciphertext_char;
      charsWritten = send(socketFD, buffer, strlen(buffer), 0);
      break;
    }

    // if the ciphertext char is not an uppercase letter or a space, report error and exit status 1
    if (isupper(ciphertext_char) == 0 && ciphertext_char != ' ') {
      fprintf(stderr, "Invalid character received from ciphertext");
      exit(1);
    }

    // place the ciphertext char in the 0 index of the buffer
    buffer[0] = ciphertext_char;

    // obtain a char from the key file
    char key_char = fgetc(filestream_key);

    /*if (feof(filestream_key) && !feof(filestream_ciphertext)) {
      fprintf(stderr, "Key is shorter than ciphertext");
      exit(1);
    }*/

    // check if the char from key is a newline char; this would mean we're at the end of the file
    // the end of ciphertext should always be reached before this step
    // if this condition is met, the key is too short; send the char so the server knows not to expect any more data
    // report error and exit status 1
    if (key_char == '\n') {
      buffer[0] = key_char;
      charsWritten = send(socketFD, buffer, strlen(buffer), 0);
      fprintf(stderr, "Key is shorter than ciphertext");
      exit(1);
    }

    // if the key char is not an uppercase letter or a space, report error and exit status 1
    if (isupper(key_char) == 0 && key_char != ' ') {
      fprintf(stderr, "Invalid character received from key");
      exit(1);
    }

    // place the key char in the 1 index of buffer
    buffer[1] = key_char;

    // send the buffer with the ciphertext char and the key char to the server
    charsWritten = send(socketFD, buffer, strlen(buffer), 0); 
    if (charsWritten < 0){
      error("CLIENT: ERROR writing to socket");
    }
    if (charsWritten < strlen(buffer)){
      printf("CLIENT: WARNING: Not all data written to socket!\n");
    }

    // clear out the buffer again to receive message back from server
    memset(buffer, '\0', sizeof(buffer));

    // receive the decoded char back from the server
    charsRead = recv(socketFD, buffer, sizeof(buffer), 0);
    if (charsRead < 0){
      error("CLIENT: ERROR reading from socket");
    }

    // initialize a variable with the decoded char received from server and print it to stdout
    char plaintext_char = buffer[0];
    printf("%c", plaintext_char);

    // repeat loop until the end of ciphertext file is reached or error occurs
  }
  // finish by printing a newline char to stdout and closing the socket, ciphertext file, and key file
  putchar('\n');
  close(socketFD);
  fclose(filestream_ciphertext);
  fclose(filestream_key);
  return 0;
}
