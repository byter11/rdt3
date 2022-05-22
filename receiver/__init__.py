import os, socket
from .receiver import Receiver

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8081))

    sock.connect(('0.0.0.0', 8080))
    sock.send(b'hello')
    s = sock.recv(1024)
    print(s)
