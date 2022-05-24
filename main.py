# Load configuration variables
import os
from dotenv import load_dotenv
load_dotenv()

pktsize = input("Packet size: ")
os.environ['PACKET_SIZE'] = str(int(pktsize)) or 1024

import sender
import bson
import receiver
import threading
from gevent import socket, monkey

# Patch socket module to send objects using BSON
monkey.patch_all()
bson.patch_socket()

# Start Sender and Receiver
threading.Thread(target=sender.listen).start()
receiver.connect()
