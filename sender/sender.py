import os, time, socket, threading
from util.StateMachine import StateMachine

PORT = os.environ['SENDER_PORT']
REQUEST_TIMEOUT = 2

class Sender(StateMachine):
    def __init__(self, socket, conn):
        super().__init__()
        self.socket = socket
        self.conn = conn
        self.conn.settimeout(2)

        self.add("wait_from_above", self.wait_from_above)
        self.add("wait_for_ack", self.wait_for_ack)
    
    def run(self, cargo):
        print('yo')
        request = self.conn.recv(1024)
        if not request:
            print("Client disconnected")
            return ("end", None)
        super().run(cargo)
        
    def wait_from_above(self, pkt):

        self.conn.send(b'a')

        return ("wait_for_ack", pkt)
        
    def wait_for_ack(self, pkt):
        return ("wait_from_above", int(not pkt))
