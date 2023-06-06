from datetime import datetime
from google.cloud import firestore
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:2000")
print("Connected on port 2000")

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.
db = firestore.Client(project='mercurial-shape-387021')

while True:
    try:
        #  Wait for next request from client
        print("Waiting for message...")
        message = socket.recv_json()
        db.collection("Groceries").add(message)
        print("\tReceived request: ", message)
        time.sleep(1)  
    except Exception as e:
        print(e)