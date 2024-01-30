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



def benchmark_camera_framerate(device, frames=5): # This function benchmarks a given camera to determine its framerate.
    global config

    resolution = [config["dashcam"]["capture"]["opencv"]["resolution"]["width"], config["dashcam"]["capture"]["opencv"]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
    capture = cv2.VideoCapture(config["dashcam"]["capture"]["opencv"]["devices"][device]); # Open the video capture device.

    capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.

    print("Running benchmark for '" + device + "'...")


    for i in range(0, 10): # Loop a few times to allow the camera to warm up before the benchmark starts.
        ret, frame = capture.read() # Capture a video frame.
    start_time = time.time() # Record the exact time that the benchmark started.
    for i in range(0, frames): # Run until the specified number of frames have been captured.
        ret, frame = capture.read() # Capture a video frame.
        stamp_test = str(round(time.time()*100)/100) + " PLACEHOLDER" + str(round(time.time()/2)) # Manipulate a few random values to simulate the generation of the overlay stamp.
        cv2.putText(frame, stamp_test, (10, 10), 2, 0.8, (255,255,255)) # Add the test stamp to the video frame.

    end_time = time.time() # Record the exact time that the benchmark ended.
    total_time = end_time - start_time # Calculate how many seconds the benchmark took to complete.
    fps = frames / total_time # Calculate the number of frames captured per second.
    return fps # Return the calculated FPS.

for device in config["dashcam"]["capture"]["opencv"]["devices"]:
    framerate = benchmark_camera_framerate(device) # Benchmark this capture device and record the calculated FPS.
    print("Calculated FPS: " + str(framerate)) # Display the calculated FPS.
