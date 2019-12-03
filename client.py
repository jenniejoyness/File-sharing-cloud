#!/usr/bin/env python
import os
import socket, sys
from operator import itemgetter

from collections import namedtuple

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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    while True:
        request = raw_input("Search: ")
        s.send("2 " + request)
        file_list = s.recv(BUFFER_SIZE)
        while file_list.find("\n") == -1:
            file_list += s.recv(BUFFER_SIZE)
        if file_list == "\n":
            continue
        files_info = make_dict(file_list[:-1])
        show_files(files_info)

        file_num = raw_input("Choose: ")
        if not file_num.isdigit():
            continue
        file_num = int(file_num) - 1
        if (file_num not in range(0,len(files_info))):
            continue
        file_name = files_info[file_num][0]
        ip = files_info[file_num][1][0]
        port = int(files_info[file_num][1][1])
        download(file_name, ip, port)
# s.close()


def make_dict(file_string):
    dict = {}
    files = file_string.split(",")
    files.sort()
    for file in files:
        name, ip, port = file.split(" ")
        dict[name] = (ip, port)
    return sorted(dict.items(), key=itemgetter(0))


def show_files(files):
    counter = 1
    for file_name, address in files:
        print str(counter) + " " + file_name
        counter += 1


def download(file_name, ip, port):
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
        listening_mode(TCP_IP, TCP_PORT, listening_port)
    else:
        user_mode(TCP_IP, TCP_PORT)
