import socket as s
import sys

socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_address = ('127.0.0.1', 10000)
print(f'connecting to {server_address[0]} port {server_address[1]}')
socket.connect(server_address)

try:
    message = b'This is the message. It will be repeated.'
    print(f'sending {message}')
    socket.sendall(message)

    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = socket.recv(16)
        amount_received += len(data)
        print(f'received {data}')
finally:
    print('closing socket')
    socket.close()
