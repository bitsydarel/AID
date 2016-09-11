#!/usr/bin/env python

import socket

hote = "5.58.57.50"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(port))
count = 6
socket.send("\nHey my name is Darel!\n".encode())

socket.send("\nTesting the client \n".encode())

print("Close")
socket.close()
