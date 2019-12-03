import socket, sys
from collections import namedtuple

uploader = namedtuple('uploader', ['ip', 'port', 'fileList'])
uploaders = {}


def register(data, client_addr):
    files = data[-1].split(",")
    print (client_addr[0], data[1], files)
    file_name = ""
    for file_name in files:
        uploaders[file_name] = (client_addr[0], data[1])
    print uploaders

def search()

def illegal_request(data, client_addr):
    return 'blah'


switcher = {
    "1": register
}


def request_handler(data, client_addr):
    data = data.split(" ")
    func = switcher.get(data[0], illegal_request)
    func(data, client_addr)


if __name__ == "__main__":
    TCP_IP = '0.0.0.0'
    TCP_PORT = int(sys.argv[1])
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # handling client requests f
    while True:
        c_socket, addr = s.accept()
        while True:
            data = c_socket.recv(BUFFER_SIZE)
            request_handler(data, addr)
            if not data: break
        c_socket.close()
