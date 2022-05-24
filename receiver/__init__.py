import os
from gevent import socket
from .receiver import Receiver

SENDER_PORT = os.environ['SENDER_PORT']


def connect():
    print("Receiver connect()")
    sock = None
    while True:
        try:
            file = input("File: ")
            if file.lower() == 'q':
                if sock is not None:
                    sock.close()
                return
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('0.0.0.0', int(SENDER_PORT)))
            r = Receiver(sock, file)
            r.run(file)
        except KeyboardInterrupt:
            sock.close()
            break
