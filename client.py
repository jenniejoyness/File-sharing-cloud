#!/usr/bin/env python
import os
import socket, sys

BUFFER_SIZE = 1024


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def listen_as_server(listening_port):
    TCP_IP = '0.0.0.0'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, int(listening_port)))
    s.listen(1)
    while True:
        # client connects to us
        conn, addr = s.accept()
        # gets the name of the file
        file_name = conn.recv(BUFFER_SIZE)
        if not file_name: break
        with open(file_name, 'rb') as file:
            data = file.read(BUFFER_SIZE)
            while data:
                conn.send(data)
                data = file.read(BUFFER_SIZE)
        conn.close()



def get_files():
    files = []
    for file_name in os.listdir("."):
        if os.path.isfile(file_name):
            files.append(file_name)
    return ",".join(files)


def listening_mode(TCP_IP, TCP_PORT, listening_port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    files = get_files()
    s.send("1 " + str(listening_port) + " " + files)
    s.close()
    listen_as_server(listening_port)

def user_mode(TCP_IP, TCP_PORT):
    # make connection with server to ask for file
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((TCP_IP, TCP_PORT))
    # request = raw_input("Search:")
    # s.send("2 " + request)
    # file_list = s.recv(BUFFER_SIZE)
    # # todo - choose which file
    file_name = "a.txt"
    ip = "127.0.0.1"
    port = 6648
    download(file_name,ip, port)
    #s.close()

def download(file_name,ip, port):
    file = open(file_name, "wb")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(file_name)
    data = s.recv(BUFFER_SIZE)
    while data:
        file.write(data)
        data = s.recv(BUFFER_SIZE)
    s.close()


if __name__ == "__main__":
    Mode = int(sys.argv[1])
    TCP_IP = sys.argv[2]
    TCP_PORT = int(sys.argv[3])
    if Mode == 0:
        listening_port = int(sys.argv[4])
        #listening_mode(TCP_IP, TCP_PORT, listening_port)
        listen_as_server(listening_port)
    else:
        user_mode(TCP_IP,TCP_PORT)

