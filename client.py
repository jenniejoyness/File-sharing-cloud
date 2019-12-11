import os
import socket, sys
from operator import itemgetter

BUFFER_SIZE = 1024

'''
create server socket and wait for users to connect and request a certain file.
open file and send all info back to client.
'''

def listener(listening_port):
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


'''
returns a string separated by ',' of all the current file names in the current folder.
'''


def get_files():
    files = []
    for file_name in os.listdir("."):
        if os.path.isfile(file_name):
            files.append(file_name)
    return ",".join(files)


'''
1. create client socket - connect to server to inform which port will be listening on
and which files can be dowloaded
2. open server socket for other client file requests
'''


def listening_mode(TCP_IP, TCP_PORT, listening_port):
    # client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # files in current folder
    files = get_files()
    # this way of writing to will notify the server to add this client as a uploader
    s.send("1 " + str(listening_port) + " " + files)
    s.close()
    listener(listening_port)


'''
connect to server as client and send file requests from the user.
collect info from server about uploader.
connect to uploader and download file to current folder.
'''


def user_mode(TCP_IP, TCP_PORT):
    # make connection with server to ask for file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # waiting for user input
    while True:
        request = raw_input("Search: ")
        s.send("2 " + request)
        # receive a string of all file names and info
        file_list = s.recv(BUFFER_SIZE)
        while file_list.find("\n") == -1:
            file_list += s.recv(BUFFER_SIZE)
        if file_list == "\n":
            continue
        # sorted the data from ([Name][Ip][Port],... ) to list
        files_info = organize_info(file_list[:-1])
        show_files(files_info)

        file_num = raw_input("Choose: ")
        if not file_num.isdigit():
            continue
        file_num = int(file_num) - 1
        if (file_num not in range(0, len(files_info))):
            continue
        # download the selected file to current folder
        file_name = files_info[file_num][0]
        ip = files_info[file_num][1]
        port = int(files_info[file_num][2])
        download(file_name, ip, port)
    s.close()


'''
returns list of tuples that contain ("name",("ip","port"))
sorted alphabetically
'''


def organize_info(file_string):
    list = []
    files = file_string.split(",")
    files.sort()
    for file in files:
        name, ip, port = file.split(" ")
        list.append((name,ip, port))
    return list


'''
print all the file names.
'''
def show_files(files):
    counter = 1
    for file_name, ip, port in files:
        print str(counter) + " " + file_name
        counter += 1


'''
create file in current folder.
connect as client to the client uploader and request the file.
receive the data from the file and write to new file in current folder.
'''
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
    file.close()


if __name__ == "__main__":
    mode = int(sys.argv[1])
    TCP_IP = sys.argv[2]
    TCP_PORT = int(sys.argv[3])
    # listening mode
    if mode == 0:
        listening_port = int(sys.argv[4])
        listening_mode(TCP_IP, TCP_PORT, listening_port)
    else:
        user_mode(TCP_IP, TCP_PORT)
