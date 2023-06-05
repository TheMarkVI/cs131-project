# CS131 Project: Fridge object detection
'''
Author(s): CS131 Project Group 2

Github inspiration: "Coding Your Own Object Detection Program"
https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md

Also inspired from the detectnet.py program in jetson-inference/python/examples

Sidenote:
- GitHub CoPilot seemed to have come alive... (it's a bit scary)
    - (It even generated the above comment for me...)
'''
import numpy as np
#import zmq
import time
import sys
# import argparse # for parsing arguments from command line (if need be)

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

# from detectnet.py example:
# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

PORT = 5679

SYS_CAMERA = "/dev/video0"
SYS_DISPLAY = "display://0"
MODELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/ssd-mobilenet.onnx"
LABELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/labels.txt"

camera = videoSource(SYS_CAMERA)  # 'csi://0' for MIPI CSI camera
display = videoOutput(SYS_DISPLAY) # 'my_video.mp4' for file

# load objection detection model 
# net = detectNet("ssd-mobilenet-v2", threshold=0.5) # Uses the default ssd-mobilenet-v2 model
net = detectNet(model=MODELPATH, labels=LABELPATH, \
               input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)
                		     # Uses retrained model with fridge objects
				     # Might be able to move the model and label paths
                                     # in the same directory. Just .onnx and .txt files

itemsNeeded = [] # list of items needed
itemsFound = [] # list of items found

# Load labels from labels.txt file
fridgeList = []
with open(LABELPATH, "r") as f:
    for line in f:
        fridgeList.append(line.strip())

print("Labels:", fridgeList)

# print(fridgeList) # verify: print labels from labels.txt file

# driver code for object detection
input("Press Enter to Continue... (Press Ctrl+C to exit)")

while display.IsStreaming():
    img = camera.Capture()

    if img is None:
        # print("render image...")
        #print("itemsNeeded:", itemsNeeded)
        #print("itemsFound:", itemsFound)
        continue

    detections = net.Detect(img)
    print(detections)

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

    # not sure if we need this...
    # print("detected {:d} objects in image".format(len(detections))) # print detections

    # for detection in detections:
    #    print(detection) # print object name, confidence, bounding box coordinates

    # To do:
    # Implement a way to check if the object is in the fridge
    # if it is not, then add it to the list of items needed
    # if it is, then add it to the list of items found
    # print("Items needed: ", itemsNeeded)
    # print("Items found: ", itemsFound)

    # To do: send itemsNeeded to a server
    # via MQTT or something similar

# Print lists of items at the end of the program
print("fridgeList:", fridgeList)
print("itemsNeeded:", itemsNeeded)
print("itemsFound:", itemsFound)
