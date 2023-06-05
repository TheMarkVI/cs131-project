# CS131 Project: Fridge object detection
'''
Github inspiration: "Coding Your Own Object Detection Program"
https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md

'''
import numpy as np
#import zmq
import time
import sys

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# from detectnet.py example:
# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

PORT = 5679

MODELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/ssd-mobilenet.onnx"
LABELPATH = "../jetson-inference/python/training/detection/ssd/models/fruit/labels.txt"

# load objection detection model 
net = detectNet("ssd-mobilenet-v2", threshold=0.5) # Uses the default ssd-mobilenet-v2 model
# net = detectNet(model=MODELPATH, labels=LABELPATH, \
#                input_blob="input_0", output_cvg="scores", output_bbox="boxes", threshold=0.5)
                		     # Uses retrained model with fridge objects
				     # Might be able to move the model and label paths
                                     # in the same directory. Just .onnx and .txt files

camera = videoSource("/dev/video0")  # 'csi://0' for MIPI CSI camera
display = videoOutput("display://0") # 'my_video.mp4' for file

# load list of objects in fridge; this should be the list of labels from the model
# fridgeList = ['Apple','Artichoke','Bagel','Banana','Beer','Bell pepper','Bread','Broccoli',\
#     'Cabbage','Cake','Candy','Cantaloupe','Carrot','Cheese','Coffee','Cookie','Croissant',\
#         'Cucumber','Egg','Food','Fruit','Grape','Grapefruit','Guacamole','Juice','Lemon','Mango',\
#             'Milk','Muffin','Mushroom','Orange','Pancake','Pasta','Peach','Pear','Pineapple','Pizza',\
#                 'Pomegranate','Popcorn','Potato','Pumpkin','Salad','Seafood','Snack',\
#                     'Submarine sandwich','Tomato','Turkey','Vegetable','Waffle','Watermelon','Wine','Zucchini']

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
input("Press Enter to Continue...")

while display.IsStreaming():
    img = camera.Capture()

    if img is not None:
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

print("fridgeList:", fridgeList)
print("itemsNeeded:", itemsNeeded)
print("itemsFound:", itemsFound)
