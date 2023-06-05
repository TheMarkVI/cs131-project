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

# Use these paths if the model is in the cs131-project folder
MODELPATH = "./models/fruit/ssd-mobilenet.onnx"
LABELPATH = "./models/fruit/labels.txt"

# Use these paths if the model is in the jetson-inference ssd folder
# MODELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/ssd-mobilenet.onnx"
# LABELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/labels.txt"

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
found_id = [] # list of ids of items found

# Load labels from labels.txt file
fridgeList = []
with open(LABELPATH, "r") as f:
    for line in f:
        fridgeList.append(line.strip())

itemsNeeded = fridgeList # initially, all items are needed
print("Labels (from fridgeList):", fridgeList)
print("Items needed:", itemsNeeded)

# driver code for object detection
input("Press Enter to Continue... (Press Ctrl+C to exit)")

while display.IsStreaming():
    # clear lists
    found_id = found_id.clear()
    itemsNeeded = itemsNeeded.clear()
    itemsFound = itemsFound.clear()

    # Capture image from camera
    img = camera.Capture()

    if img is None:
        continue

    detections = net.Detect(img)

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))


    # print detections in console 
    print("detected {:d} objects in image".format(len(detections)))

    # Find ID of detected objects and add to list
    for detection in detections:
        found_id = found_id.append(detections[detection].ClassID)
        itemsFound = itemsFound.append(fridgeList[found_id])
        print(detection) # print object name, confidence, bounding box coordinates

    for i in itemsNeeded:
        for j in fridgeList:
            itemsNeeded.append(fridgeList[j])
        
    for i in itemsNeeded:
        for j in itemsFound:
            if itemsFound[j] == itemsNeeded[i]:
                itemsNeeded.remove(itemsNeeded[i])

    print("Items needed:", itemsNeeded)

    # To do: send itemsNeeded to a server
    # Basic client/server type connection

# Print lists of items at the end of the program
print("fridgeList:", fridgeList)
print("itemsFound:", itemsFound)
print("itemsNeeded:", itemsNeeded)
