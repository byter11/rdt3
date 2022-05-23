import os
from gevent import socket
from .receiver import Receiver

SENDER_PORT = os.environ['SENDER_PORT']


def connect():
    print("Receiver connect()")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            file = input("File: ")
            sock.connect(('0.0.0.0', int(SENDER_PORT)))
            r = Receiver(sock)
            r.run(file)
        except KeyboardInterrupt:
            sock.close()
            break
