# This script allows you to test your object recognition settings with a real-time video stream.

import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import cv2 # Required to capture video.
from ultralytics import YOLO
import numpy

predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

try:
    if (os.path.exists(predator_root_directory + "/../config.json")):
        config = json.load(open(predator_root_directory + "/../config.json")) # Load the configuration database from config.json
    else:
        print("The configuration file doesn't appear to exist at " + predator_root_directory + "/../config.json.")
        exit()
except:
    print("The configuration database couldn't be loaded. It may be corrupted.")
    exit()


model = YOLO("../assets/models/dashcam_model.pt")
def predict(frame):
    global model
    results = model(frame)
    class_names = results[0].names

    detected_objects = [] # This is a placeholder that will hold all of the detected objects.
    for result in results:
        boxes = result.boxes
        for i in range(0, len(boxes)):
            obj = {}
            box = result.boxes[i].xyxy.numpy().tolist()[0]
            obj["bbox"] = {}
            obj["bbox"]["x1"] = round(box[0])
            obj["bbox"]["y1"] = round(box[1])
            obj["bbox"]["x2"] = round(box[2])
            obj["bbox"]["y2"] = round(box[3])
            obj["name"] = class_names[int(result.boxes[i].cls.numpy().tolist()[0])]
            obj["conf"] = result.boxes[i].conf.numpy().tolist()[0]
            detected_objects.append(obj)
    return detected_objects

device = "main"

if (device not in config["dashcam"]["capture"]["video"]["devices"]):
    print("The specified device does not exist in the configuration. Be sure to change the 'device' variable in the motion_detect_test.py file to the device you want to test.")
    exit()

resolution = [config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
#capture = cv2.VideoCapture(config["dashcam"]["capture"]["video"]["devices"][device]["index"]); # Open the video capture device.
capture = cv2.VideoCapture("/home/cvieira/Downloads/ParkingEventDemo.mp4"); # Open the video capture device.
codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the codec to be MJPEG.
capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.

background_subtractor = cv2.createBackgroundSubtractorMOG2()

total_area = resolution[0] * resolution[1] # Calculate the total area of the frame.

output = cv2.VideoWriter("./predator_object_recognition_test.avi", cv2.VideoWriter_fourcc(*'XVID'), 16, (resolution[0], resolution[1])) # Update the video output.


while True:
    ret, frame = capture.read()

    detected_objects = predict(frame)
    for element in detected_objects:
        print(element["name"], element["conf"])
        if (element["conf"] >= config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["minimum_confidence"] and element["name"] in config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["objects"]): # Check to see if this object is in the list of target objects.
            print("Detected event.")
            color = config["dashcam"]["parked"]["event"]["label"]["color"]
            cv2.rectangle(frame, (element["bbox"]["x1"], element["bbox"]["y1"]), (element["bbox"]["x2"], element["bbox"]["y2"]), (color[2], color[1], color[0]), 2) # Draw a box around the contour in the frame.

    cv2.imshow('Object Detection', frame)

    output.write(frame) # Save this frame to the video file.
    if cv2.waitKey(1) == ord('q'):
        break
        
capture.release()
cv2.destroyAllWindows()
