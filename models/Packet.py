import bson


class Packet:
    def __init__(self, ack=-1, seq=-1, fin=0, checksum=b'', data=b''):
        self.ack = int(ack)
        self.seq = int(seq)
        self.fin = int(fin)
        self.checksum = checksum
        self.data = data

    def load(self, data):
        decoded = bson.loads(data)
        self.ack = decoded.get('ack', -1)
        self.seq = decoded.get('seq', -1)
        self.fin = decoded.get('fin', 0)
        self.checksum = decoded.get('checksum', '')
        self.data = decoded.get('data', '')
        return self

    def encode(self):
        return {
          'ack': self.ack,
          'seq': self.seq,
          'fin': self.fin,
          'checksum': self.checksum,
          'data': self.data
        }
        # return self._dump()

    def _dump(self, indent=0):
        return bson.dumps({
          'ack': self.ack,
          'seq': self.seq,
          'fin': self.fin,
          'checksum': self.checksum,
          'data': self.data
          })

    def __str__(self):
        return f"""
        ack: {self.ack}
        seq: {self.seq}
        fin: {self.fin}
        checksum: {self.checksum}
        data: {self.data}"""
