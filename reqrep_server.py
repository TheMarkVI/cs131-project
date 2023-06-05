import zmq
import time
import sys

port = "5679"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
# socket.bind("tcp://themarkvi.asuscomm.com:5679")
# socket.bind("tcp://127.0.0.1:%s" % port)
# socket.bind("tcp://10.13.240.1:%s" % port)
socket.bind("tcp://0.0.0.0:2000")
print("Connected on port", port)

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


# import requests

# try:
#     x = requests.get("https://97.94.97.230", timeout=10)
#     print(x.status_code)
# except requests.exceptions.ConnectionError as e:
#     raise ValueError("Firewall is blocking the connection")


# have siraaj on ucr wifi
# ip should be 10.13.240.1
# bind? and connect to that ip
# client connects and should be able to send messages like that