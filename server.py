import socket, sys

uploaders = {}

'''
register uploader into dictionary.
key: name of file
value : ip, port
'''
def register(data, client_addr):
    files = data[-1].split(",")
    ip = client_addr[0]
    port = data[0]
    for file_name in files:
        uploaders[file_name] = (ip, port)

'''
search in dictionary all the files that contain the client request.
return string of file info split by ','
'''
def search(client_request, client_addr):
    files = []
    for key in uploaders.keys():
        if client_request[0] in key:
            files.append(key + " " + uploaders[key][0] + " " + uploaders[key][1])
    send_to_client(",".join(files) + "\n")


def send_to_client(message):
    c_socket.send(message)


def illegal_request(data, client_addr):
    return 'blah'


switcher = {
    "1": register,
    "2": search
}

'''
send to the correct handler.
if an illegal request is made (not 1 or 2) will ignore.
'''
def request_handler(client_request, client_addr):
    client_request = client_request.split(" ")
    func = switcher.get(client_request[0], illegal_request)
    func(client_request[1:], client_addr)


if __name__ == "__main__":
    TCP_IP = '0.0.0.0'
    TCP_PORT = int(sys.argv[1])
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    # handling client requests
    while True:
        c_socket, addr = s.accept()
        while True:
            data = c_socket.recv(BUFFER_SIZE)
            request_handler(data, addr)
            if not data: break
        c_socket.close()
