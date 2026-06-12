#!/usr/bin/env python
import socket, argparse, json, sys, select

class UDP:

    #Sets up socket connection
    def __init__(self, u, sip, sp):
        self.sip = sip
        self.u = u
        self.sp = sp
        self.socket_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.users = {}

        #Converts sign-in message to JSON and sends
        self.send(json.dumps({
            "type": "sign-in",
            "username": self.u,
        }))

    #Encodes and sends a message to server
    def send(self, message):
        self.socket_client.sendto(message.encode('utf-8'), (self.sip,self.sp))
    
    #Encodes and sends a message to client
    def client_send(self, ip, port, message):
        self.socket_client.sendto(message.encode('utf-8'), (ip, port))    
    
   #Converts list command to JSON and sends
    def list(self):
         self.send(json.dumps({
              "type": "list",
              "username": self.u,
          })) 

    #Loop to receive and send messages
    def run(self):
         print("> ", end="", flush=True)

         while True:
             readable, _, _ = select.select(
                 [self.socket_client, sys.stdin],
                 [],
                 []
             )

             for r in readable:

                 #Receives message
                 if r == self.socket_client:
                     response, addr = self.socket_client.recvfrom(65535)
                     response = json.loads(response.decode())

                     if response["type"] == "list-reply":
                         self.users = response["users"]
                         print("\nSigned In Users:", ", ".join(self.users.keys()))

                     elif response["type"] == "message":
                         print("\n" + response["text"])

                     print("> ", end="", flush=True)

                 #User input
                 elif r == sys.stdin:
                     self.message = sys.stdin.readline().strip()
                     input_list = self.message.split()

                     if not input_list:
                         print("> ", end="", flush=True)
                         continue

                     if input_list[0] == "list":
                         self.list()

                     elif input_list[0] == "send":
                         if len(input_list) < 3:
                             print("Usage: send USERNAME MESSAGE")
                             print("> ", end="", flush=True)
                             continue

                         username = input_list[1]
                         message = " ".join(input_list[2:])

                         if username not in self.users:
                             print("Error: User not found")
                             print("> ", end="", flush=True)
                             continue

                         ip, port = self.users[username]

                         msg_json = json.dumps({
                             "type": "message",
                             "text": f"<From {self.u}>: {message}"
                         })

                         self.client_send(ip, port, msg_json)

                     print("> ", end="", flush=True)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP')
    parser.add_argument('u', type=str, help="username")
    parser.add_argument('sip', type=str, help="ip address")
    parser.add_argument('sp', type=int, help="port")
    args = parser.parse_args()

    udp = UDP(args.u, args.sip, args.sp)
    udp.run()
