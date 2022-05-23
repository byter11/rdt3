import os
import io
from pathlib import Path
from models.StateMachine import StateMachine
from models.Packet import Packet

PORT = os.environ['SENDER_PORT']
REQUEST_TIMEOUT = 2


class Sender(StateMachine):
    def __init__(self, sock, conn):
        super().__init__('end')
        self.socket = sock
        self.conn = conn
        self.conn.settimeout(20)
        self.stream = None

        self.add("wait_from_above", self.wait_from_above)
        self.add("wait_for_ack", self.wait_for_ack)
        self.add("end", self.end)

    def run(self):
        print('running server')
        pkt = self.rdt_recv()
        if not pkt:
            print("Client disconnected")
            return ("end", None)

        print("Requested: ", pkt.data.decode('utf-8'))
        self.stream = io.BytesIO(
            Path(
                f"{os.path.dirname(__file__)}/files/{pkt.data.decode('utf-8')}"
            ).read_bytes()
        )

        super().run(0)

    def rdt_send(self, data, seq):
        sndpkt = Packet(data=data, seq=seq)
        self.conn.sendobj(sndpkt.encode())
        return sndpkt

    def rdt_recv(self):
        try:
            data = self.conn.recvobj()
            return Packet(**data)
        except TimeoutError as e:
            print("timeout ", e)

        return Packet()

    def end(self):
        print('ending')
        sndpkt = Packet(fin=1)
        print('fin ', sndpkt)
        self.conn.sendobj(sndpkt.encode())

    def wait_from_above(self, seq):
        print("wait_from_above", seq)
        data = self.stream.read(1024)
        print(len(data))
        if len(data) <= 0:
            return ("end", 0)
        pkt = self.rdt_send(data, seq)
        return ("wait_for_ack", pkt)

    def wait_for_ack(self, pkt: Packet):
        print("wait_for_ack", pkt.seq)
        rcvpkt = self.rdt_recv()

        if rcvpkt.ack is None or rcvpkt.ack != pkt.seq:
            print("Invalid ACK")
            if rcvpkt.ack is None:
                print("NO ACK Received. Re sending")
                self.rdt_send(pkt.data, pkt.seq)
            return ('wait_for_ack', rcvpkt.seq)

        print('ACK: ', rcvpkt)
        return ("wait_from_above", int(not int(rcvpkt.ack)))
