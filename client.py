import socket
import threading
import errno

class Client():
    def __init__(self, username, password):
        self.HEADER = 16
        self.PORT = 9000
        self.IP = "3.222.3.116"
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.msg = ""

        self.my_username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.client_socket.setblocking(False)

        self.username = self.my_username.encode(self.FORMAT)
        self.username_header = f"{len(self.username):<{self.HEADER}}".encode(self.FORMAT)

    def send_message(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client_socket.send(self.username_header)
        self.client_socket.send(self.username)
        self.client_socket.send(send_length)
        self.client_socket.send(message)
        try:
            username_header = self.client_socket.recv(self.HEADER)
            username_length = int(username_header.decode(self.FORMAT).strip())
            username = self.client_socket.recv(username_length).decode(self.FORMAT)
            message_header = self.client_socket.recv(self.HEADER)
            message_length = int(message_header.decode(self.FORMAT).strip())
            message = self.client_socket.recv(message_length).decode(self.FORMAT)
        except:
            return 0
        return f'{username}:{message}'