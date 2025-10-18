import socket

ip = "127.0.0.1"
port = 33941 # must be the port number from above

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
    finally:
        sock.close()

client(ip, port, b"print ('Hello World')")