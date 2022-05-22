import os
import time
from models.StateMachine import StateMachine
from models.Packet import Packet

SENDER_PORT = os.environ['SENDER_PORT']


class Receiver(StateMachine):
    def __init__(self, sock):
        super().__init__()
        self.socket = sock
        self.data = b''
        self.add("wait_from_below", self.wait_from_below)
        self.add("end", self.socket.close)

    def run(self, file):
        time.sleep(0.2)

        print('receiver running')
        self.socket.sendobj(Packet(data=file.encode('utf-8')).encode())

        super().run(0)

    def rdt_recv(self):
        try:
            return Packet().load(self.socket.recv(1024))
        except TimeoutError:
            return Packet()

    def wait_from_below(self, seq):
        rcvpkt = self.rdt_recv()

        if rcvpkt.seq != seq:
            sndpkt = Packet(ack=rcvpkt.seq)
            self.socket.sendobj(sndpkt.encode())
            return ("wait_from_below", seq)

        self.data += rcvpkt.data
        sndpkt = Packet(ack=seq)
        self.socket.sendobj(sndpkt.encode())

        return ("wait_from_below", int(not seq))
