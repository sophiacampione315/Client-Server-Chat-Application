# Client-Server-Chat-Application
This is a simple Chat Application created for my CY4740 Networking class that allows multiple clients to connect
to a server via UDP sockets. The application is written in Python. It uses
arg parse when accepting commands, and sends data back and forth in the form
of JSON strings. 

How It Works:

-The server is started by running the script along with the chosen 
port number. 

-The client connects to the server by running its script. The command requires
the client to sign in to the server using a username, as well as specify the 
IP address and port number of the server.

-The server receives this message, decodes it, and stores the dictionary in
another dictionary to save each client's sign-in information. The server lets
the client know it is ready to receive messages.

-The client has the option to send two commands:
    -list: returns the usernames of all clients currently signed in
    -send USERNAME MESSAGE: sends the specified client a message

-The client sends its command, and the proper JSON string is sent to the server.

-The server decodes the message and responds with the requested information.
