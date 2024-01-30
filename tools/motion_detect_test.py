# This script allows you to test your motion detection settings with a real-time video stream.

import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import cv2 # Required to capture video.

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

capture = cv2.VideoCapture(0) # TODO: Replace with a capture device from the configuration.

resolution = [config["dashcam"]["capture"]["resolution"]["width"], config["dashcam"]["capture"]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.

background_subtractor = cv2.createBackgroundSubtractorMOG2()

total_area = resolution[0] * resolution[1] # Calculate the total area of the frame.

#output = cv2.VideoWriter("/home/pi/Downloads/predator_motion_detect_test.avi", cv2.VideoWriter_fourcc(*'XVID'), 16), (resolution[0], resolution[1])) # Update the video output.

while True:
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = background_subtractor.apply(gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    moving_area = 0
    for contour in contours:
        moving_area += cv2.contourArea(contour)
        if cv2.contourArea(contour) > 10:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    moving_percentage = moving_area / total_area # Calculate the percentage of the frame that is in motion.
    moving_percentage_human = "{:.5f}%".format(moving_percentage*100) # Convert the moving percentage to a human-readable string.
    if (moving_area > 0): # Check to see if there is any movement at all.
        if (moving_percentage > float(config["dashcam"]["parked"]["recording"]["sensitivity"])): # Check to see if there is movement that exceeds the sensitivity threshold.
            print(str(moving_area) + "\t(" + str(format(moving_percentage_human)) + ")\tTriggered") # Display the movement as both a number and a percentage.
        else:
            print(str(moving_area) + "\t(" + str(format(moving_percentage_human)) + ")") # Display the movement as both a number and a percentage.
    
    cv2.putText(frame, moving_percentage_human, (10, 30), 2, 0.8, (0, 0, 0)) # Add the main overlay stamp to the video stream.
    cv2.imshow('Motion Detection', frame)

    #output.write(frame) # Save this frame to the video file.
    if cv2.waitKey(1) == ord('q'):
        break
        
capture.release()
cv2.destroyAllWindows()
