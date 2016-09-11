#!/usr/bin/env python

import socket, threading, os, platform

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))

while True:
        os.chdir(platform.system())
        socket.listen(5)
        client, address = socket.accept()
        print "{} connected".format( address )
        response = client.recv(255)
        if response != "":
                print response

print "Close"
client.close()
stock.close()
