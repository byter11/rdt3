import sender
from gevent import socket, monkey
import bson
import receiver
import threading

monkey.patch_all()

bson.patch_socket()

threading.Thread(target=sender.listen).start()

receiver.connect()
