import os
from gevent import socket
from .sender import Sender

SENDER_PORT = os.environ['SENDER_PORT']


def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', int(SENDER_PORT)))

    sock.listen()
    print("Sender listen()")

    while True:
        try:
            conn, addr = sock.accept()
            print("Client Connected")
            s = Sender(sock, conn)
            s.run()
            conn.close()

        except KeyboardInterrupt:
            break
