import os, io
from pathlib import Path
from models.StateMachine import StateMachine
from models.Packet import Packet

PORT = os.environ['SENDER_PORT']
REQUEST_TIMEOUT = 2


class Sender(StateMachine):
    def __init__(self, sock, conn):
        super().__init__()
        self.socket = sock
        self.conn = conn
        self.conn.settimeout(20)
        self.stream = None

        self.add("wait_from_above", self.wait_from_above)
        self.add("wait_for_ack", self.wait_for_ack)
        self.add("end", self.socket.close)

    def run(self):
        print('running server')
        pkt = self.rdt_recv()
        if not pkt:
            print("Client disconnected")
            return ("end", None)
        print(pkt)
        # self.stream = open(f"{os.path.dirname(__file__)}/files/{pkt.data.decode('utf-8')}", 'rb')
        self.stream = io.BytesIO(
            Path(f"{os.path.dirname(__file__)}/files/{pkt.data.decode('utf-8')}").read_bytes()
        )

        super().run(0)

    def rdt_send(self, data, seq):
        sndpkt = Packet(data=data, seq=seq)
        self.conn.sendobj(sndpkt.encode())
        return sndpkt

    def rdt_recv(self):
        try:
            data = self.conn.recv(1024)
            return Packet().load(data=data)
        except Exception as e:
            print(e)

    def wait_from_above(self, seq):
        data = self.stream.read(1024)
        pkt = self.rdt_send(data, seq)
        return ("wait_for_ack", pkt)

    def wait_for_ack(self, pkt: Packet):
        rcvpkt = self.rdt_recv()

        if rcvpkt.ack is None or rcvpkt.ack != pkt.ack:
            if rcvpkt.ack is None:
                self.rdt_send()
            return ('wait_for_ack', rcvpkt.seq)

        return ("wait_from_above", int(not rcvpkt.seq))
