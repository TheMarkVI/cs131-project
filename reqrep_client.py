import zmq
import sys

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

#  Do 5 requests, waiting each time for a response
for request in range (5):
    print("Sending request ", request,"...")
    socket.send_string("Hello")
    #  Get the reply.
    message = socket.recv()
    print("\tReceived reply ", request, "[", message, "]")

socket.send_string("Bye")