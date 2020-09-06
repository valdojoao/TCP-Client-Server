# Python TCP Client and Server

The goal of this project is to build a tcp client and a tcp server


## Requirements
- Python  > 3.5.x. <br />
- The server should listen on port 3443 <br />
- The server should accept a maximum of 100 connected clients <br />
- The server should send the current date to each client every 10 seconds <br />
- The client should be a command line application and  should connect to the server with a TLS connection <br />
- Once started the client should receive the current date from the server every 10 seconds <br />
- The client should listen on the standard input and send a text message to the server every time the return key is pressed, the server should respond to the client with the same string but reversed <br />
- All the implementation must be covered  with automated tests.
<br />
<br />


## Execute

Use the following command to execute the code.

 1 - Open the terminal and run the Server Program first: python threadServer.py <br />
 2 - Open new terminal tab then  start the Client program: python threadClient.py <br />
 in order to connect n clients, repeat step 2 n times<br />
 
 ## Automated tests
 In order to run the automated tests run the script: python tests.py 

