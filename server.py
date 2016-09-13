import socket
from _thread import start_new_thread

count = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 7125))
sock.listen(1000)
#Printing that the server started
print("\nServer starded \n")

#Creating a function for each client
def new_client(conn):
    
    while 1:
        x = input("\n{0}: ".format(addr[0]))
        conn.send(x.encode())
        respond = conn.recv(1024)
        print("\nFrom {0}\n".format(addr[0]))
        print(str(respond.decode()))
        if respond.decode() == "":
            conn.close()
            print("\nClonnection closed\nwaiting for a connection\n")
            break
        continue

while 1:
    try:
        conn, addr = sock.accept()
        print('\nconnected:', addr)
        start_new_thread(new_client, (conn,))
        count += 1
        print("number of client connected: {0}".format(count))
    except KeyboardInterrupt:
        print("\nClosing the Server \nExiting...")
        conn.close()
        exit()