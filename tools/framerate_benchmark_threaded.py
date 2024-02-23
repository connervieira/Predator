import os # Required to interact with certain operating system functions
import json # Required to process JSON data

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

from threading import Thread
import cv2
import time

frames = 240 # This determines how many frames will be captured for the benchmark.
output_file = "./output.avi"
display = False


class video_stream:
    def __init__(self, src=0): # This initializes the video stream object.
        self.stream = cv2.VideoCapture(src)
        codec = list("MJPG")
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the codec to be MJPEG.
        self.stream.set(cv2.CAP_PROP_FPS, 120) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self): # This starts the video stream.
        Thread(target=self.update, args=()).start()
        return self

    def update(self): # This function endlessly captures new frames until stopped.
        while True:
            if (self.stopped == True):
                return
            else:
                self.old_frame = self.frame
                (self.grabbed, self.frame) = self.stream.read()

    def read(self): # This function returns the most recent frame.
        return self.frame

    def stop(self): # This function stops the video stream.
        self.stopped = True



resolution = [config["dashcam"]["capture"]["video"]["resolution"]["width"], config["dashcam"]["capture"]["video"]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
for device in config["dashcam"]["capture"]["video"]["devices"]:
    if (len(output_file) > 0):
        output = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), 50, (resolution[0], resolution[1]))
    stream = video_stream(src=config["dashcam"]["capture"]["video"]["devices"][device]["index"]).start()
    start_time = time.time()

    frame_number = 0
    while frame_number < frames:
        frame_number += 1
        frame = stream.read()

        if (display == True):
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
        if (len(output_file) > 0):
            output.write(frame) # Save this frame to the video.

    output = None
    end_time = time.time()
    fps = frames / (end_time-start_time)
    print("Calculated FPS:" + str(round(fps)))


# do a bit of cleanup
cv2.destroyAllWindows()
stream.stop()
