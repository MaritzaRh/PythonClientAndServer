import socket as s
import sys

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
server_address = ('localhost', 10000)
print("Starting up on {} port {}".format(*server_address))
sock.bind(server_address)

sock.listen(1)

while True:
    print("Waiting for connection")
    connection, client_address = sock.accept()
    try:
        print("Connection from ", client_address)
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print("sending data back to client")
                connection.sendall(data)
            else:
                print("no data from ", client_address)
                break
    finally:
        connection.close()