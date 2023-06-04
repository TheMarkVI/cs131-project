import zmq
import time
import sys

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
print("Connected on port", port)

num_iters = 0

while True:
    #  Wait for next request from client
    print("Waiting for message...")
    message = socket.recv()
    # close connection
    if message == b"Bye":
        print("Closing connection!")
        break
    print("\tReceived request: ", message)
    time.sleep (1)  
    socket.send_string("World from %s" % port)
    num_iters += 1