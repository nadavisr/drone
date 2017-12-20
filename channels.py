import socket
class Channels():
    def __init__(self):
        self.udpSocket = socket.socket
        self.tcpSocketControl = socket.socket
        self.tcpSocketVideo1 = socket.socket
        self.tcpSocketVideo2 = socket.socket
        self.stopListen = False