import os
import time
from models.StateMachine import StateMachine
from models.Packet import Packet

SENDER_PORT = os.environ['SENDER_PORT']
PACKET_SIZE = int(os.environ['PACKET_SIZE'])


class Receiver(StateMachine):
    def __init__(self, sock, file):
        super().__init__('end')
        self.socket = sock
        self.data = b''
        self.file = file
        self.add("wait_from_below", self.wait_from_below)
        self.add("end", lambda: 0)
        self.socket.settimeout(5)

    def run(self, file):
        time.sleep(0.2)

        print('receiver running')
        self.socket.sendobj(Packet(data=file.encode('utf-8')).encode())
        super().run(0)

    def rdt_recv(self):
        try:
            data = self.socket.recvobj()
            return Packet(**data)
        except TimeoutError:
            return Packet()

    def wait_from_below(self, seq):
        rcvpkt = self.rdt_recv()
        print()
        print("RECV")
        print("DATA ", len(rcvpkt.data))
        print("FIN ", rcvpkt.fin)
        print()

        if rcvpkt.fin:
            with open(
                f"{os.path.dirname(__file__)}/files/{self.file}", 'wb'
            ) as f:
                f.write(self.data)
            return ("end", None)

        if not rcvpkt.data or rcvpkt.seq == -1:
            print("Timeout rcvpkt")
            return ("wait_from_below", seq)

        if rcvpkt.seq != seq:
            print("Invalid sequence in rcvpkt")
            sndpkt = Packet(ack=rcvpkt.seq)
            self.socket.sendobj(sndpkt.encode())
            return ("wait_from_below", seq)

        self.data += rcvpkt.data
        sndpkt = Packet(ack=seq)
        self.socket.sendobj(sndpkt.encode())

        return ("wait_from_below", int(not seq))
