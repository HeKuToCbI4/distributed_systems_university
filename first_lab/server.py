import socket
import imread
import pickle
if __name__ == '__main__':
    server_socket = socket.socket()
    server_socket.bind(('', 1337))
    hello_there = imread.imload('images/general_kenobi.jpg')
    serialized = pickle.dumps(hello_there, protocol=0)
    server_socket.listen(1)
    connection, address = server_socket.accept()
    print(f'client {connection} {address} connected')

    connection.send(serialized)
    print('Data sent.')
