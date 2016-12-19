import socket

HOST, PORT = "192.168.1.16", 1337


def send(data):
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
    finally:
        sock.close()
    print("Sent:     {}".format(data))


def receive(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        received = str(sock.recv(1024), "utf-8")
    finally:
        sock.close()

    print("Received: {}".format(received))
