import socket
import threading
import errno

class Client():
    def __init__(self, username, password):
        self.HEADER = 16
        self.PORT = 9000
        self.IP = "192.168.73.1"
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.msg = ""
        self.messageQueue = []

        self.my_username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.username = self.my_username.encode(self.FORMAT)
        print(self.username)
        self.username_header = f"{len(self.username):<{self.HEADER}}".encode(self.FORMAT)
        print(self.username_header)
        self.client_socket.send(self.username_header+self.username)
        print(self.username_header+self.username)

    def send_message(self, msg):
        while True:
            if self.messageQueue != []:
                print(self.messageQueue)
                msg = self.messageQueue[0]
                del(self.messageQueue[0])
            else:
                msg = 0
            if msg != 0:
                message = msg.encode(self.FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b' ' * (self.HEADER - len(send_length))
                self.client_socket.send(send_length)
                self.client_socket.send(message)
    
    def recieve_message(self):
            try:
                username_header = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
                username_length = int(username_header.strip())
                username = self.client_socket.recv(username_length).decode(self.FORMAT)
                message_header = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
                message_length = int(message_header.strip())
                message = self.client_socket.recv(message_length).decode(self.FORMAT)
                return f'{username}:{message}'
            except:
                return 0
        