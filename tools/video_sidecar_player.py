# This script plays back a video file, and overlays information from its corresponding side-car file.


import cv2
import os
import json
import time


file_path_video = input("Video file-path: ")

overlay_color = {
    "plate": (0, 0, 255)
}

delay = 1/60
playback_offset = 0
pause = False

if (os.path.exists(file_path_video)):
    capture = cv2.VideoCapture(file_path_video)
    file_path_sidecar = os.path.splitext(file_path_video)[0] + ".json"
    if (os.path.exists(file_path_sidecar)):
        file = open(file_path_sidecar)
        sidecar_data = json.load(file)
        file.close()

        frame_number = 0
        while True:
            if (str(frame_number-playback_offset) in sidecar_data):
                frame_data = sidecar_data[str(frame_number-playback_offset)]
            else:
                frame_data = {}
            if (pause == False):
                ret, frame = capture.read()
            cv2.putText(frame, "Offset: " + str(playback_offset), (0, 40), 2, 1.2, (0,0,0), 4)
            for plate in frame_data:
                x = frame_data[plate]["coordinates"]["x"]
                y = frame_data[plate]["coordinates"]["y"]
                w = frame_data[plate]["coordinates"]["w"]
                h = frame_data[plate]["coordinates"]["h"]
                bounding_box = [x, y, w, h]
                cv2.putText(frame, plate, (x, y), 4, 1.2, overlay_color["plate"], 4)
                cv2.rectangle(frame, bounding_box, color=overlay_color["plate"], thickness=2)
            cv2.imshow("Video", frame)
            pressed_key = cv2.waitKey(1)
            if (pressed_key == ord("q")):
                break
            elif (pressed_key == ord(",")):
                frame_number -= 30
                frame_number = max([frame_number, 0]) # Cap the frame position from going below 0.
                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number) # Jump to the new position.
            elif (pressed_key == ord(".")):
                frame_number += 30
                frame_number = max([frame_number, 0]) # Cap the frame position from going below 0.
                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number) # Jump to the new position.
            elif (pressed_key == ord("]")):
                delay = delay/2 # Speed up the video playback.
            elif (pressed_key == ord("[")):
                delay = delay*2 # Slow down the video playback.
            elif (pressed_key == ord("'")):
                playback_offset += 1 # Push the overlay forward.
            elif (pressed_key == ord(";")):
                playback_offset -= 1 # Push the overlay backward.
            elif (pressed_key == 32): # Check to see if the space bar was pressed.
                pause = not pause # Toggle the paused status.

            frame_number += 1 # Increment the frame count.
            time.sleep(delay)

    else:
        print("There is no side-car file associated with this video.")
else:
    print("The specified file does not exist.")
