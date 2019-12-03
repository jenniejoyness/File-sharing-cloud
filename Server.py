import socket, sys
from collections import namedtuple

uploader = namedtuple('uploader', ['ip', 'port', 'fileList'])

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

uploaders = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    c_socket, addr = s.accept()

    print 'New connection from:', addr
    while True:
        data = c_socket.recv(BUFFER_SIZE)
		uploaders.append(uploader(addr.ip, addr.port, data))
        if not data: break
        print "received:", data
        c_socket.send(data.upper())
    c_socket.close()