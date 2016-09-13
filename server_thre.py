#!/usr/bin/env python

import threading, socket
from queue import Queue

class ClientThread(threading.Thread):
    
    def __init__(self, ip, port, client_conn, id):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.client_conn = client_conn
        self.id = id
        super()
        print("[+] New Thread For {0} On Port {1}".format(self.ip, self.port))


    def run(self):
        while 1:
            x = input("\nClient {0} ip {1}: ".format(self.id,self.ip))
            self.client_conn.send(x.encode())
            respond = self.client_conn.recv(1024)
            print("\nFrom client {0} ip {1}\n".format(self.id,self.ip))
            print(str(respond.decode()))
            if respond.decode() == "":
                self.client_conn.close()
                print("\nClonnection closed\nwaiting for a connection\n")
                break
            continue
        

count = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 7125))
sock.listen(1000)
client_id = 0

#Printing that the server started
print("\nAID Server starded\n")

while 1:
    try:
        conn, (client_ip, client_port) = sock.accept()
        client_id += 1
        client_thread = ClientThread(client_ip, client_port, conn, client_id)
        client_thread.daemon = True
        client_thread.start()
        count += 1
        print("number of client connected: {0}".format(count))
    except KeyboardInterrupt:
        print("\nClosing the Server \nExiting...")
        conn.close()
        exit()