import zmq
import sys

port = "5679"

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
# socket.connect("tcp://97.94.97.230:5679")
socket.connect("tcp://10.13.43.167:2000")

#  Do 5 requests, waiting each time for a response
for request in range(5):
    print("Sending request ", request,"...")
    socket.send_string("Hello")
    #  Get the reply.
    message = socket.recv()
    print("\tReceived reply ", request, "[", message, "]")

    socket.send_string("Bye")