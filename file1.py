import zmq
import sys

port = "5679"

def connect_to_server():
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://97.94.97.230:5679")
    return socket

def send_and_receive(socket, request):
    print("Sending request ", request,"...")
    socket.send_string("Hello")
    #  Get the reply.
    message = socket.recv()
    print("\tReceived reply ", request, "[", message, "]")

if __name__ == "__main__":
    socket = connect_to_server()
    #  Do 5 requests, waiting each time for a response
    for request in range(5):
        send_and_receive(socket, request)
    socket.send_string("Bye")
