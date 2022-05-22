import os, socket
from .sender import Sender

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))

    sock.listen()

    while True:
        try:
            conn, addr = sock.accept()
            s = Sender(socket, conn)
            s.run(0)
            
        except KeyboardInterrupt:
            break
