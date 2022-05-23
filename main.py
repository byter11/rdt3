# Load configuration variables
from dotenv import load_dotenv
load_dotenv()

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
