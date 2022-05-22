import os
from gevent import socket
from .receiver import Receiver

SENDER_PORT = os.environ['SENDER_PORT']


def connect():
    print("Receiver connect()")
    while True:
        try:
            file = input("File: ")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', int(SENDER_PORT)+1))
            sock.connect(('0.0.0.0', int(SENDER_PORT)))
            r = Receiver(sock)
            r.run(file)
        except KeyboardInterrupt:
            sock.close()
            break
