# CS131 Project: Fridge object detection
'''
Github inspiration: "Coding Your Own Object Detection Program"
https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md

'''

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

# load objection detection model 
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("/dev/video0")  # 'csi://0' for MIPI CSI camera
display = videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
    img = camera.Capture()

    if img is not None:
        continue

    detections = net.Detect(img)

    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)
