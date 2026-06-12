#!/usr/bin/env python
import socket, sys, argparse, select, json

SERVER_IP = "127.0.0.1"

class UDP:
    #Sets up socket connection
    def __init__(self, sp):
        self.sp = sp
        self.socket_server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket_server.bind((SERVER_IP, self.sp))
        self.users = {}
        print("Server Starting...")

    #Loop to receive and send messages
    def run(self):
        while True:
            #Recieves and decodes clients's message
            message, address = self.socket_server.recvfrom(65535)
            data = json.loads(message.decode('utf-8'))
            print("Message received from client: ", data)

            #Gets client information during sign-in
            if data["type"] == "sign-in":
                try:
                    username = data["username"]
                    self.users[username] = address
                    print(f"{username} signed in from {address}")

                except Exception as e:
                    response = "JSON Error, Message Not Sent"

            #Returns a list of signed-in users
            elif data["type"] == "list":
                try:
                    response = json.dumps({
                        "type": "list-reply",
                        "users": self.users})
                    self.socket_server.sendto(response.encode('utf-8'), address)
              
                except Exception as e:
                  response = "JSON Error, Message Not Sent"
          
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP')
    parser.add_argument('sp', type=int, help="server port")
    args = parser.parse_args()

    udp = UDP(args.sp)
    udp.run()


