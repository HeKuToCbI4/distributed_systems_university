import os
import pickle
import socket

import imread

filename = 'images/hello_there.jpg'
if __name__ == '__main__':
    try:
        os.remove(filename)
    except OSError:
        pass
    client_socket = socket.socket()
    client_socket.connect(('localhost', 1337))
    serialized = bytearray()
    while True:
        data = client_socket.recv(1024)
        serialized += data
        if not data:
            break
    hello_there = pickle.loads(serialized)
    imread.imsave(filename, hello_there)
