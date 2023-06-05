import zmq
import time
import sys

port = "5679"

def bind_to_server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5679")
    print("Connected on port", port)
    return socket

def handle_client_request(socket):
    while True:
        try:
            #  Wait for next request from client
            print("Waiting for message...")
            message = socket.recv()
            # close connection
            if message == b"Bye":
                print("Closing connection!")
                break
            print("\tReceived request: ", message)
            time.sleep(1)  
            socket.send_string("World from %s" % port)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    socket = bind_to_server()
    handle_client_request()
