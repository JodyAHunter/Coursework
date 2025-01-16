#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

// Error function used for reporting issues
void error(const char *msg) {
  perror(msg);
  exit(1);
} 

// this function takes a connected socket as an argument;
// it establishes a handshake with the dec_client, receives ciphertext and key data,
// decodes the data, and sends the decrypted plaintext back to the dec_client 
void receive_and_decrypt(int connectionSocket) {
  int charsRead; // records how many chars were sent to the dec_client
  char buffer[3]; // buffer used to send and receive data between the client and the server
                  // upon recv, buffer[0] = ciphertext, buffer[1] = key, buffer[2] = null-terminator
                  //upon send, buffer[0] = plaintext, buffer[1-2] = null-terminator
  int ciphertext_ascii; // int variable for ciphertext used to convert from ascii value for one-time-pad implementation
  int key_ascii; // int variable for key used to convert from ascii value for one-time-pad implementation
  int message_and_key; // int variable that holds the value of the key subtracted from the message for the one-time-pad algorithm
  char decrypted_char; // char variable to hold the final decrypted char after implementing one-time-pad 
                       // this is what will be sent back to the dec_client
  char handshake[] = "dec_server"; // handshake message to be sent to the dec_client; used to confirm the correct server has connected

  // send handshake message to client and clear out the handshake buffer to receive back confirmation
  send(connectionSocket, handshake, strlen(handshake), 0);
  memset(handshake, '\0', sizeof(handshake));
  // receive handshake message back from client
  recv(connectionSocket, handshake, sizeof(handshake), 0);
  // if client connected is dec_client, should receive back "continue"
  // otherwise, close the socket connection and exit status 2 
  if (strcmp(handshake, "continue") != 0) {
    close(connectionSocket);
    exit(2);
  }
 
  // begin infinite for loop to receive one ciphertext and one key char at a time,
  // implement one-time-pad algorithm, and send back decoded plaintext to the client
  for (;;) {

    // clear out the buffer array
    memset(buffer, '\0', sizeof(buffer));
    // receive one ciphertext char and one key char from the dec_client 
    charsRead = recv(connectionSocket, buffer, sizeof(buffer)-1, 0); 
    if (charsRead < 0){
      error("ERROR reading from socket");
    }
    // if the ciphertext char received is a newline char, we can expect no more data to come through; break loop
    if (buffer[0] == '\n') break;
    //printf("SERVER: buffer[0] = %c; buffer[1] = %c\n", buffer[0], buffer[1]);

    // place the ciphertext char and the key char each into their own int variable
    ciphertext_ascii = buffer[0];
    key_ascii = buffer[1];

    // subtract 65 from both values to convert them from ascii to one-time-pad values
    // 0-26 (0 = A, 1 = B, ... 25 = Z, 26 = space)
    ciphertext_ascii = ciphertext_ascii - 65;
    key_ascii = key_ascii - 65;

    // checks for ciphertext space, should be the only value that is negative after subtracting 65
    // changes the value to 26 if so
    if (ciphertext_ascii < 0) {
      ciphertext_ascii = 26;
    }

    // same space checks for key
    if (key_ascii < 0) {
      key_ascii = 26;
    }

    // obtain the numerical value of the key char subtracted from the ciphertext char
    message_and_key = ciphertext_ascii - key_ascii;

    // if value is negative, add 27 to it
    if (message_and_key < 0) {
      message_and_key = message_and_key + 27;
    }

    // modulo 27 to obtain numerical value for plaintext
    message_and_key = message_and_key % 27;

    // if the plaintext value is 26, this represents the space character
    // set the variable for the decrypted char to 32, the ascii value for space
    // otherwise, simply add 65 to convert the letter's numerical value to ascii
    if (message_and_key == 26) {
      decrypted_char = 32;
    } else {
      message_and_key = message_and_key + 65;
      decrypted_char = message_and_key;
    }

    // clear out buffer and put the new plaintext char into it
    memset(buffer, '\0', sizeof(buffer));
    buffer[0] = decrypted_char;


    // send plaintext char back to dec_client
    charsRead = send(connectionSocket, buffer, strlen(buffer), 0);

    if (charsRead < 0){
      error("ERROR writing to socket");
    }
  }
    // close the connection socket for this client and exit status 0
  close(connectionSocket);
  exit(0);
  }

// Set up the address struct for the server socket
void setupAddressStruct(struct sockaddr_in* address, 
                        int portNumber){
 
  // Clear out the address struct
  memset((char*) address, '\0', sizeof(*address)); 

  // The address should be network capable
  address->sin_family = AF_INET;
  // Store the port number
  address->sin_port = htons(portNumber);
  // Allow a client at any address to connect to this server
  address->sin_addr.s_addr = INADDR_ANY;
}

int main(int argc, char *argv[]){
  int connectionSocket;
  struct sockaddr_in serverAddress, clientAddress;
  socklen_t sizeOfClientInfo = sizeof(clientAddress);

  // Check usage & args
  if (argc < 2) { 
    fprintf(stderr,"USAGE: %s port\n", argv[0]); 
    exit(1);
  } 
  
  // Create the socket that will listen for connections
  int listenSocket = socket(AF_INET, SOCK_STREAM, 0);
  if (listenSocket < 0) {
    error("ERROR opening socket");
  }

  // Set up the address struct for the server socket
  setupAddressStruct(&serverAddress, atoi(argv[1]));

  // Associate the socket to the port
  if (bind(listenSocket, 
          (struct sockaddr *)&serverAddress, 
          sizeof(serverAddress)) < 0){
    error("ERROR on binding");
  }

  // Start listening for connetions. Allow up to 5 connections to queue up
  listen(listenSocket, 5); 
  
  // Accept a connection, blocking if one is not available until one connects
  while(1){
    // Accept the connection request which creates a connection socket
    connectionSocket = accept(listenSocket, 
                (struct sockaddr *)&clientAddress, 
                &sizeOfClientInfo); 
    if (connectionSocket < 0){
      error("ERROR on accept");
    }

    // when a connection is made, create a child process that calls the receive_and_decrypt function passing the connectionSocket as an argument
    pid_t spawnpid = -5;
    spawnpid = fork();
    switch (spawnpid){
      case -1:
        fprintf(stderr, "SERVER: fork() failed!");
        exit(1);
        break;

      case 0:
        receive_and_decrypt(connectionSocket);
        exit(1);
        break;

      default:
        break;
    }
  }
  // close the listening socket
  close(listenSocket); 
  return 0;
}
