device = 2 # This determines the video capture device that will be used for the benchmark.
resolution = [1280, 720] # This determines the resolution that will be used for the video capture device.
frames = 240 # This determines how many frames will be captured for the benchmark.


import cv2
import time

capture = cv2.VideoCapture(device); # Open the video capture device.

capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.

time.sleep(2) # Wait for a few seconds before starting the benchmark to allow the camera to wake up.
print("Running benchmark...")

start_time = time.time() # Record the exact time that the benchmark started.

for i in range(0, frames): # Run until the specified number of frames have been captured.
    ret, frame = capture.read() # Capture a video frame.
    stamp_test = str(round(time.time()*100)/100) + " PLACEHOLDER" + str(round(time.time()/2)) # Manipulate a few random values to simulate the generation of the overlay stamp.
    cv2.putText(frame, stamp_test, (10, 10), 2, 0.8, (255,255,255)) # Add the test stamp to the video frame.

end_time = time.time() # Record the exact time that the benchmark ended.
total_time = end_time - start_time # Calculate how many seconds the benchmark took to complete.
fps = frames / total_time # Calculate the number of frames captured per second.
print("Calculated FPS: ", fps) # Display the calculated FPS.

capture.release() # Release the video capture device.
