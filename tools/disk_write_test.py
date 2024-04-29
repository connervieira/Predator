# This script captures video using each configured dash-cam video device, using both a queued and direct saving method, and compares how long each method takes to complete.
# The queued method captures all the frames into a queue, then saves the entire queue at once.
# The direct method captures frames and immediately saves them individually.


import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import cv2
import time

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



def dump_video(device, frames=100): # This function benchmarks a given camera to determine its framerate.
    global config


    resolution = [config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
    capture = cv2.VideoCapture(config["dashcam"]["capture"]["video"]["devices"][device]["index"]); # Open the video capture device.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the codec to be MJPEG.
    capture.set(cv2.CAP_PROP_FPS, 120) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.

    print("Testing " + str(device))

    for i in range(0, 10): # Loop a few times to allow the camera to warm up before the benchmark starts.
        ret, frame = capture.read() # Capture a video frame.

    print("Capturing Via Queue")
    frame_buffer = []
    start_time = time.time()
    for i in range(0, frames): # Run until the specified number of frames have been captured.
        ret, frame = capture.read() # Capture a video frame.
        stamp_test = str(round(time.time()*100)/100) + " PLACEHOLDER" + str(round(time.time()/2)) # Manipulate a few random values to simulate the generation of the overlay stamp.
        cv2.putText(frame, stamp_test, (10, 10), 2, 0.8, (255,255,255)) # Add the test stamp to the video frame.
        frame_buffer.append(frame)
    print("    Capture Time: " + str(time.time() - start_time))


    output = cv2.VideoWriter("./out-queue.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, (resolution[0],  resolution[1]))
    start_time = time.time()
    for frame in frame_buffer:
        output.write(frame)
    print("    Save Time: " + str(time.time() - start_time))


    output = None
    time.sleep(1)


    print("Capturing Directly")
    total_capture_time = 0
    total_save_time = 0
    output = cv2.VideoWriter("./out-direct.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, (resolution[0],  resolution[1]))
    for i in range(0, frames): # Run until the specified number of frames have been captured.
        start_time = time.time()
        ret, frame = capture.read() # Capture a video frame.
        stamp_test = str(round(time.time()*100)/100) + " PLACEHOLDER" + str(round(time.time()/2)) # Manipulate a few random values to simulate the generation of the overlay stamp.
        cv2.putText(frame, stamp_test, (10, 10), 2, 0.8, (255,255,255)) # Add the test stamp to the video frame.
        frame_buffer.append(frame)
        total_capture_time = total_capture_time + (time.time() - start_time)
        start_time = time.time()
        output.write(frame)
        total_save_time = total_save_time + (time.time() - start_time)

    print("    Capture Time: " + str(total_capture_time))
    print("    Save Time: " + str(total_save_time))


for device in config["dashcam"]["capture"]["video"]["devices"]:
    dump_video(device)
