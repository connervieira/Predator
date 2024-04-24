# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os # Required to interact with certain operating system functions
import json # Required to process JSON data

predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

try:
    if (os.path.exists(predator_root_directory + "/config.json")):
        config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database from config.json
    else:
        print("The configuration file doesn't appear to exist at " + predator_root_directory + "/config.json.")
        exit()
except:
    print("The configuration database couldn't be loaded. It may be corrupted.")
    exit()

import utils
display_message = utils.display_message
debug_message = utils.debug_message
process_timing = utils.process_timing
get_gps_location = utils.get_gps_location
heartbeat = utils.heartbeat
update_state = utils.update_state
convert_speed = utils.convert_speed

import threading
import time
import cv2
import subprocess # Required for starting some shell commands
import sys
import datetime # Required for converting between timestamps and human readable date/time information
if (config["general"]["gps"]["enabled"] == True): # Only import the GPS libraries if GPS settings are enabled.
    from gps import * # Required to access GPS information.
    import gpsd
if (config["dashcam"]["saving"]["looped_recording"]["mode"] == "automatic"): # Only import the disk usage library if it is enabled in the configuration.
    import psutil # Required to get disk usage information

if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True): # Check to see if Reticulum notifications are enabled.
    import reticulum

import lighting # Import the lighting.py script.
update_status_lighting = lighting.update_status_lighting # Load the status lighting update function from the lighting script.



if (config["dashcam"]["saving"]["looped_recording"]["mode"] == "manual"): # Only validate the manual history length if manual looped recording mode is enabled.
    if (int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"]) != float(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])): # Check to see if the dashcam unsaved history length is not a whole number.
        display_message("The 'dashcam>saving>looped_recording>manual>history_length' setting doesn't appear to be an integer. This value has been rounded to the nearest whole number.", 3)
        config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"] = round(float(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])) # Found the dashcam history length off to a whole number.
    elif (type(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"]) != int): # Check to see if the dashcam history length is not an integer.
        display_message("The 'dashcam>saving>looped_recording>manual>history_length' setting doesn't appear to be an integer, but it is a whole number. Make sure this configuration value does not have a decimal point.", 2)
    if (int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"]) < 0): # Check to see if the dashcam history length is a negative number.
        display_message("The 'dashcam>saving>looped_recording>manual>history_length' setting appears to be a negative number. This value has been defaulted to 0, which is likely to cause unexpected behavior.", 3)
        config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"] = 0 # Default the dashcam history length to 0, even though this is likely to cause unexpected behavior.
    elif (int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"]) < 2): # Check to see if the dashcam history length is less than 2.
        display_message("The 'dashcam>saving>looped_recording>manual>history_length' setting appears to be a number that is less than 2. This is likely to cause unexpected behavior.", 2)
elif (config["dashcam"]["saving"]["looped_recording"]["mode"] == "automatic"): # Only validate the automatic looped recording configuration values if automatic looped recording mode is enabled.
    if (type(config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"]) != float):
        display_message("The 'dashcam>saving>looped_recording>automatic>minimum_free_percentage' setting is not a floating point number.", 2)
    if (config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"] < 0):
        display_message("The 'dashcam>saving>looped_recording>automatic>minimum_free_percentage' value is a negative number.", 3)
    elif (config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"] > 1):
        display_message("The 'dashcam>saving>looped_recording>automatic>minimum_free_percentage' value is greater than 1 (or 100%).", 3)
    elif (config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"] >= 0.99):
        display_message("The 'dashcam>saving>looped_recording>automatic>minimum_free_percentage' value is greater than or equal to 0.99 (or 99%). This is exceedingly high, and may cause Predator to run out of disk space in between segments.", 2)
    elif (config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"] <= 0.05):
        display_message("The 'dashcam>saving>looped_recording>automatic>minimum_free_percentage' value is less than or equal to 0.05 (or 5%). This is exceedingly low, and may cause issues if Predator is unable to reach the minimum free disk space threshold by only erasing dashcam segments.", 2)

    if (type(config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"]) != int):
        config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"] = int(round(config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"]))
        display_message("The 'dashcam>saving>looped_recording>automatic>max_deletions_per_round' setting is not an integer number. This value has been temporarily rounded to the nearest whole number.", 2)
    if (config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"] < 0):
        display_message("The 'dashcam>saving>looped_recording>automatic>max_deletions_per_round' setting is a negative number. This will prevent Predator from ever erasing old dash-cam segments.", 3)
    elif (config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"] < 2):
        display_message("The 'dashcam>saving>looped_recording>automatic>max_deletions_per_round' setting is less than 2. This is likely to cause unexpected behavior.", 2)

if (config["dashcam"]["parked"]["enabled"] == True): # Only validate the parking mode configuration values if parking mode is enabled.
    if (config["general"]["gps"]["enabled"] == False):
        display_message("Dash-cam parking mode is enabled, but GPS functionality is disabled. Parking mode needs GPS information to determine when the vehicle is stopped. Without it, Predator will enter parking mode as soon as the threshold time is reached, and it will never return to normal recording mode.", 2)
    if (config["dashcam"]["parked"]["conditions"]["speed"] < 0):
        display_message("The 'dashcam>parked>conditions>speed' setting is a negative number. This will prevent Predator from ever entering parked mode. To prevent unexpected behavior, you should set 'dashcam>parked>enabled' to 'false'.", 2)

    if (config["dashcam"]["parked"]["recording"]["sensitivity"] < 0):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is a negative number. This will cause unexpected behavior.", 3)
    elif (config["dashcam"]["parked"]["recording"]["sensitivity"] > 0.9):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is an exceedingly high value (above 90%). This will likely cause unexpected behavior.", 2)
    elif (config["dashcam"]["parked"]["recording"]["sensitivity"] > 1):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is above 100%. This will effectively prevent Predator from ever detecting motion.", 2)







# Define global variables
parked = False # Start with parked mode disabled.
recording_active = False # This value is set to true whenever Predator is actively recording (not dormant/waiting for motion).
current_segment_name = {} # This stores the name of each capture device thread's segment.
for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
    if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
        current_segment_name[device] = ""

frames_to_write = {}
for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
    if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
        frames_to_write[device] = [] # Add this device to the frame buffer.

segments_saved_time = {} # This is a dictionary that holds a list of the dashcam segments that have been saved, and the time that they were saved.
instant_framerate = {} # This will hold the instantaneous frame-rate of each device, which is calculated based on the time between the two most recent frames. This value is expected to flucuate significantly.
calculated_framerate = {} # This will hold the calculated frame-rate of each device, which is calculated based on the number of frames captured in the previous segment.
shortterm_framerate = {} # This will hold the short-term frame-rate of each device, which is calculated based on number of frames captured over the previous few seconds.
for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
    if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
        shortterm_framerate[device] = {}
        shortterm_framerate[device]["start"] = 0
        shortterm_framerate[device]["frames"] = 0
        shortterm_framerate[device]["framerate"] = 0

audio_recorders = {} # This will hold each audio recorder process.
first_segment_started_time = 0

audio_record_command = "arecord --format=cd"
if (config["dashcam"]["capture"]["audio"]["device"] != ""): # Check to see if a custom device has been set.
    audio_record_command += " --device=\"" + str(config["dashcam"]["capture"]["audio"]["device"]) + "\""
print(audio_record_command)





def merge_audio_video(video_file, audio_file, output_file, audio_offset=0):
    debug_message("Merging audio and video files")

    merge_command = "ffmpeg -i " + audio_file + " -itsoffset -" + str(audio_offset) + " -i " + video_file + " -c copy " + output_file
    erase_command = "timeout 1 rm " + video_file + " " + audio_file

    merge_process = subprocess.run(merge_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    first_attempt = utils.get_time()
    while (merge_process.returncode != 0): # If the merge process exited with an error, keep trying until it is successful. This might happen if one of the files hasn't fully saved to disk.
        merge_process = subprocess.run(merge_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if (utils.get_time() - first_attempt > 5): # Check to see if FFMPEG has been trying for at least 5 seconds.
            display_message("The audio and video segments could not be merged. It is possible one or both of the files is damaged.", 2)
            process_timing("end", "Dashcam/File Merging")
            return False # Time out, and exit with a success value False.
    subprocess.run(erase_command.split())

    debug_message("Merged audio and video files")
    return True



def benchmark_camera_framerate(device, frames=5): # This function benchmarks a given camera to determine its framerate.
    global config

    resolution = [config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
    capture = cv2.VideoCapture(config["dashcam"]["capture"]["video"]["devices"][device]["index"]); # Open the video capture device.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
    capture.set(cv2.CAP_PROP_FPS, 240) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.

    capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0]) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1]) # Set the video stream height.
    if (capture is None or capture.isOpened() == False): # Check to see if the capture failed to open.
        display_message("Failed to open video capture on device '" + str(device) + "' for frame-rate benchmarking.", 3)

    debug_message("Running benchmark for '" + device + "'...")

    for i in range(0, 10): # Loop a few times to allow the camera to warm up before the benchmark starts.
        ret, frame = capture.read() # Capture a video frame.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is convered to flip this capture device's output.
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
    start_time = utils.get_time() # Record the exact time that the benchmark started.
    for i in range(0, frames): # Run until the specified number of frames have been captured.
        ret, frame = capture.read() # Capture a video frame.
        frame = apply_dashcam_stamps(frame, device) # Apply dashcam overlay stamps to the frame.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is convered to flip this capture device's output.
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.

    end_time = utils.get_time() # Record the exact time that the benchmark ended.
    total_time = end_time - start_time # Calculate how many seconds the benchmark took to complete.
    fps = frames / total_time # Calculate the number of frames captured per second.
    debug_message("Capture device '" + device + "' runs at " + str(round(fps*10)/10) + "fps")

    return fps # Return the calculated FPS.






# This function is called when the lock trigger file is created, usually to save the current and last segments.
def save_dashcam_segments(file1, file2=""):
    global config
    global segments_saved_time
    process_timing("start", "Dashcam/File Maintenance")
    cooldown = 0.5 # This is how long Predator will wait to allow other threads to detect the lock trigger file. This also determines how long the user has to wait before saving the same file again.

    anything_saved = False # This will be changed to 'True' is one or more files is saved.
    if (os.path.isdir(config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"]) == False): # Check to see if the saved dashcam video folder needs to be created.
        os.system("mkdir -p '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Create the saved dashcam video directory.
    if (os.path.isdir(config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"])): # Check to see if the dashcam saving directory exists.
        if (file1 in segments_saved_time): # Check to see if file 1 has been saved previously.
            if (utils.get_time() - segments_saved_time[file1] > cooldown): # Check to see if a certain amount of time has passed since this segment was last saved before saving it again.
                os.system("cp '" + file1 + "' '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Copy the current dashcam video segment to the saved folder.
                segments_saved_time[file1] = utils.get_time()
                anything_saved = True # Indicate that at least one file was saved.
        else: # If file 1 hasn't been saved previously, then save it.
            os.system("cp '" + file1 + "' '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Copy the current dashcam video segment to the saved folder.
            segments_saved_time[file1] = utils.get_time()
            anything_saved = True # Indicate that at least one file was saved.
        if (file2 != ""): # Check to see if there is a second file to copy.
            if (file2 in segments_saved_time): # Check to see if file 2 has been saved previously.
                if (utils.get_time() - segments_saved_time[file2] > cooldown): # Check to see if a certain amount of time has passed since this segment was last saved before saving it again.
                    os.system("cp '" + file2 + "' '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Copy the last dashcam video segment to the saved folder.
                    segments_saved_time[file2] = utils.get_time()
                    anything_saved = True # Indicate that at least one file was saved.
            else: # If file 2 hasn't been saved previously, then save it.
                os.system("cp '" + file2 + "' '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Copy the last dashcam video segment to the saved folder.
                segments_saved_time[file2] = utils.get_time()
                anything_saved = True # Indicate that at least one file was saved.
    else:
        display_message("The dashcam saving directory does not exist, and could not be created. The dashcam video could not be locked.", 3)

    if (anything_saved == True): # Check to see if anything was saved before displaying the dashcam save notice.
        display_message("Saved the current dashcam segment.", 1)

    time.sleep(0.3) # Wait for a short period of time so that other dashcam recording threads have time to detect the trigger file.
    os.system("rm -rf '" + config["general"]["interface_directory"] + "/" + config["dashcam"]["saving"]["trigger"] + "'") # Remove the dashcam lock trigger file.
    if (os.path.exists(config["general"]["interface_directory"] + "/" + config["dashcam"]["saving"]["trigger"])): # Check to see if the trigger file exists even after it should have been removed.
        display_message("Unable to remove dashcam lock trigger file.", 3)

    process_timing("end", "Dashcam/File Maintenance")




def apply_dashcam_stamps(frame, device=""):
    global instant_framerate
    global calculated_framerate
    global shortterm_framerate

    process_timing("start", "Dashcam/Apply Stamps")
    try:
        height, width, channels = frame.shape
    except:
        display_message("Failed to determine frame size while applying overlay stamps. It is likely something has gone wrong with video capture.", 3)
        width = 1280
        height = 720

    main_stamp_position = [10, height - 10] # Determine where the main overlay stamp should be positioned in the video stream.
    main_stamp = ""
    if (config["dashcam"]["stamps"]["main"]["unix_time"]["enabled"] == True): # Check to see if the Unix epoch time stamp is enabled.
        main_stamp = main_stamp + str(round(utils.get_time())) + " " # Add the current Unix epoch time to the main stamp.
    if (config["dashcam"]["stamps"]["main"]["date"]["enabled"] == True): # Check to see if the date stamp is enabled.
        main_stamp = main_stamp + str(datetime.datetime.fromtimestamp(utils.get_time()).strftime("%Y-%m-%d")) + " "  # Add the date to the main stamp.
    if (config["dashcam"]["stamps"]["main"]["time"]["enabled"] == True): # Check to see if the time stamp is enabled.
        main_stamp = main_stamp + str(datetime.datetime.fromtimestamp(utils.get_time()).strftime("%H:%M:%S")) + " "  # Add the time to the main stamp.
    main_stamp = main_stamp  + "  " + config["dashcam"]["stamps"]["main"]["message_1"] + "  " + config["dashcam"]["stamps"]["main"]["message_2"] # Add the customizable messages to the overlay stamp.

    diagnostic_stamp_position = [10, height - 10 - round(30 * config["dashcam"]["stamps"]["size"])] # Determine where the diagnostic overlay stamp should be positioned in the video stream.
    diagnostic_stamp = ""
    if (config["dashcam"]["stamps"]["diagnostic"]["framerate"]["enabled"] == True): # Check to see if the frame-rate stamp is enabled.
        if (config["dashcam"]["stamps"]["diagnostic"]["framerate"]["mode"] == "instant" and device in instant_framerate): # Only add the frame-rate stamp if there is frame-rate information for this device.
            diagnostic_stamp = diagnostic_stamp + (str("%." + str(config["dashcam"]["stamps"]["diagnostic"]["framerate"]["precision"]) + "f") % instant_framerate[device]) + "FPS " # Add the current frame-rate to the main stamp.
        elif (config["dashcam"]["stamps"]["diagnostic"]["framerate"]["mode"] == "average" and device in calculated_framerate): # Only add the frame-rate stamp if there is frame-rate information for this device.
            diagnostic_stamp = diagnostic_stamp + (str("%." + str(config["dashcam"]["stamps"]["diagnostic"]["framerate"]["precision"]) + "f") % calculated_framerate[device]) + "FPS " # Add the current frame-rate to the main stamp.
        elif (config["dashcam"]["stamps"]["diagnostic"]["framerate"]["mode"] == "hybrid" and device in shortterm_framerate): # Only add the frame-rate stamp if there is frame-rate information for this device.
            diagnostic_stamp = diagnostic_stamp + (str("%." + str(config["dashcam"]["stamps"]["diagnostic"]["framerate"]["precision"]) + "f") % shortterm_framerate[device]["framerate"]) + "FPS " # Add the current frame-rate to the main stamp.


    gps_stamp_position = [10, 30] # Determine where the GPS overlay stamp should be positioned in the video stream.
    gps_stamp = "" # Set the GPS to a blank placeholder. Elements will be added to this in the next steps.
    if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS features are enabled before processing the GPS stamp.
        current_location = get_gps_location() # Get the current location.
        
        if (config["dashcam"]["stamps"]["gps"]["location"]["enabled"] == True): # Check to see if the GPS location stamp is enabled.
            gps_stamp = gps_stamp + "(" + str(f'{current_location[0]:.5f}') + ", " + str(f'{current_location[1]:.5f}') + ")  " # Add the current coordinates to the GPS stamp.
        if (config["dashcam"]["stamps"]["gps"]["altitude"]["enabled"] == True): # Check to see if the GPS altitude stamp is enabled.
            gps_stamp = gps_stamp + str(round(current_location[3])) + "m  " # Add the current altitude to the GPS stamp.
        if (config["dashcam"]["stamps"]["gps"]["speed"]["enabled"] == True): # Check to see if the GPS speed stamp is enabled.
            gps_stamp = gps_stamp + str(round(convert_speed(current_location[2],config["dashcam"]["stamps"]["gps"]["speed"]["unit"])*10)/10) + config["dashcam"]["stamps"]["gps"]["speed"]["unit"] + "  " # Add the current speed to the GPS stamp.

    # Determine the font color of the stamps from the configuration.
    main_stamp_color = config["dashcam"]["stamps"]["main"]["color"]
    diagnostic_stamp_color = config["dashcam"]["stamps"]["diagnostic"]["color"]
    gps_stamp_color = config["dashcam"]["stamps"]["gps"]["color"]

    # Add the stamps to the video stream.
    cv2.putText(frame, main_stamp, (main_stamp_position[0], main_stamp_position[1]), 2, config["dashcam"]["stamps"]["size"], (main_stamp_color[2], main_stamp_color[1], main_stamp_color[0])) # Add the main overlay stamp to the video stream.
    cv2.putText(frame, diagnostic_stamp, (diagnostic_stamp_position[0], diagnostic_stamp_position[1]), 2, config["dashcam"]["stamps"]["size"], (diagnostic_stamp_color[2], diagnostic_stamp_color[1], diagnostic_stamp_color[0])) # Add the main overlay stamp to the video stream.
    cv2.putText(frame, gps_stamp, (gps_stamp_position[0], gps_stamp_position[1]), 2, config["dashcam"]["stamps"]["size"], (gps_stamp_color[2], gps_stamp_color[1], gps_stamp_color[0])) # Add the GPS overlay stamp to the video stream.

    process_timing("end", "Dashcam/Apply Stamps")
    return frame





def detect_motion(frame, background_subtractor):
    process_timing("start", "Dashcam/Detection Motion")
    frame_height, frame_width, channels = frame.shape
    total_image_area = frame_height * frame_width

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = background_subtractor.apply(gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = [] # This is a placeholder that will hold the list of filtered motion detection contours.

    moving_area = 0 # This value will hold the number of pixels in the image that are moving.
    for contour in contours: # Iterate through each contour.
        x, y, w, h = cv2.boundingRect(contour) # Define the edges of the contour.
        width_percentage = (w / frame_width)
        height_percentage = (h / frame_height)

        if (width_percentage < 0.95 and height_percentage < 0.95): # Check to make sure this movement contour doesn't cover the entire screen.
            moving_area += cv2.contourArea(contour) # Increment the moving_area counter by the number of pixels in the contour.
            filtered_contours.append(contour)



    moving_percentage = moving_area / total_image_area # Calculate the percentage of the frame that is in motion.
    moving_percentage_human = "{:.5f}%".format(moving_percentage*100) # Convert the moving percentage to a human-readable string.

    process_timing("end", "Dashcam/Detection Motion")
    return filtered_contours, moving_percentage





# This function is called as a subprocess of the normal dashcam recording, and is triggered when motion is detected. This function exits when motion is no longer detected (after the motion detection timeout).
def record_parked_motion(capture, framerate, width, height, device, directory, frame_history):
    global instant_framerate
    global calculated_framerate
    global parked
    global recording_active
    global config
    global audio_recorders

    recording_active = True # Indicate the Predator is not actively capturing frames.

    last_motion_detected = utils.get_time() # Initialize the last time that motion was detected to now. We can assume motion was just detected because this function is only called after motion is detected.

    process_timing("start", "Dashcam/Detection Motion")
    background_subtractor = cv2.createBackgroundSubtractorMOG2() # Initialize the background subtractor for motion detection.
    process_timing("end", "Dashcam/Detection Motion")

    process_timing("start", "Dashcam/Writing")
    for frame in frame_history: # Iterate through each frame in the frame history.
        write_frame(frame, device)
    process_timing("end", "Dashcam/Writing")


    current_segment_name[device] = directory + "/predator_dashcam_" + str(round(utils.get_time())) + "_" + str(device) + "_0_P"

    process_timing("start", "Dashcam/Audio Processing")
    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        audio_filepath = current_segment_name[device] + "." + str(config["dashcam"]["capture"]["audio"]["extension"])
        audio_recorders[device] = subprocess.Popen((audio_record_command + " " + audio_filepath).split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
    process_timing("end", "Dashcam/Audio Processing")

    frames_captured = 0 # This is a placeholder that will keep track of how many frames are captured in this parked recording.
    capture_start_time = utils.get_time() # This stores the time that this parked recording started.
    last_frame_captured = time.time() # This will hold the exact time that the last frame was captured. Here, the value is initialized to the current time before any frames have been captured.
    shortterm_framerate[device]["start"] = time.time()

    process_timing("start", "Dashcam/Calculations")
    last_alert_minimum_framerate_time = 0 # This value holds the last time a minimum frame-rate alert was displayed. Here the value is initialized.
    if (float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) == 0): # Check to see if the minimum frame-rate is 0.
        expected_time_since_last_frame_slowest = 100 # Default to an arbitrarily high expected slowest frame-rate.
    else:
        expected_time_since_last_frame_slowest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) # Calculate the longest expected time between two frames.
    expected_time_since_last_frame_fastest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Calculate the shortest expected time between two frames.
    process_timing("end", "Dashcam/Calculations")

    while (utils.get_time() - last_motion_detected < config["dashcam"]["parked"]["recording"]["timeout"] and parked == True): # Run until motion is not detected for a certain period of time.
        heartbeat() # Issue a status heartbeat.
        update_state("dashcam/parked_active", instant_framerate)

        if (capture is None or capture.isOpened() == False): # Check to see if the capture failed to open.
            display_message("The video capture on device '" + str(device) + "' was dropped during parked recording", 3)

        if (time.time() - shortterm_framerate[device]["start"] > float(config["developer"]["dashcam_shortterm_framerate_interval"])):
            shortterm_framerate[device]["framerate"] = shortterm_framerate[device]["frames"] / (time.time() - shortterm_framerate[device]["start"])
            shortterm_framerate[device]["start"] = time.time()
            shortterm_framerate[device]["frames"] = 0
        shortterm_framerate[device]["frames"] += 1

        time_since_last_frame = time.time()-last_frame_captured # Calculate the time (in seconds) since the last frame was captured.
        instant_framerate[device] = 1/time_since_last_frame
        if (time_since_last_frame > expected_time_since_last_frame_slowest): # Check see if the current frame-rate is below the minimum expected frame-rate.
            if (frames_captured > 1): # Check to make sure we aren't at the very beginning of recording, where frame-rate might be inconsistent.
                if (time.time() - last_alert_minimum_framerate_time > 1): # Check to see if at least 1 second has passed since the last minimum frame-rate alert.
                    display_message("The framerate on '" + device + "' (" + str(round((1/time_since_last_frame)*100)/100) + "fps) has fallen below the minimum frame-rate.", 2)
                last_alert_minimum_framerate_time = time.time() # Record the current time as the time that the last minimum frame-rate alert was shown.
        elif (time_since_last_frame < expected_time_since_last_frame_fastest): # Check see if the current frame-rate is above the maximum expected frame-rate.
            time.sleep(expected_time_since_last_frame_fastest - time_since_last_frame) # Wait to force the frame-rate to stay below the maximum limit.
        last_frame_captured = time.time() # Update the time that the last frame was captured immediately before capturing the next frame.
        ret, frame = capture.read() # Capture a frame.
        last_frame_captured = time.time() # Update the time that the last frame was captured.
        frames_captured+=1 # Increment the frame counter.

        process_timing("start", "Dashcam/Image Manipulation")
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is convered to flip this capture device's output.
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
        process_timing("end", "Dashcam/Image Manipulation")

        process_timing("start", "Dashcam/Motion Detection")
        contours, moving_percentage = detect_motion(frame, background_subtractor) # Run motion analysis on this frame.

        if (moving_percentage > float(config["dashcam"]["parked"]["recording"]["sensitivity"]) * 0.8): # Check to see if there is movement that exceeds 80% of the sensitivity threshold. This ensures that motion that is just barely over the threshold doesn't cause Predator to repeatedly start and stop recording.
            last_motion_detected = utils.get_time()
            if (utils.get_time() - last_motion_detected > 2): # Check to see if it has been more than 2 seconds since motion was last detected so that the message is only displayed after there hasn't been motion for some time.
                display_message("Detected motion.", 1)

        if (config["dashcam"]["parked"]["recording"]["highlight_motion"]["enabled"] == True):
            for contour in contours: # Iterate through each contour.
                if cv2.contourArea(contour) > 1: # Check to see if this contour is big enough to be worth highlighting.
                    color = config["dashcam"]["parked"]["recording"]["highlight_motion"]["color"]
                    x, y, w, h = cv2.boundingRect(contour) # Define the edges of the contour.
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (color[2], color[1], color[0]), 2) # Draw a box around the contour in the frame.

        process_timing("end", "Dashcam/Motion Detection")

        frame = apply_dashcam_stamps(frame, device) # Apply dashcam overlay stamps to the frame.

        process_timing("start", "Dashcam/Writing")
        write_frame(frame, device)
        process_timing("end", "Dashcam/Writing")

    recording_active = False

    display_message("Stopped motion recording.", 1)


    return frames_captured / (utils.get_time() - capture_start_time)


def delete_old_segments():
    global config

    process_timing("start", "Dashcam/File Maintenance")

    dashcam_files_list_command = "ls " + config["general"]["working_directory"] + " | grep predator_dashcam" # Set up the command to get a list of all unsaved dashcam videos in the working directory.
    dashcam_files = str(os.popen(dashcam_files_list_command).read())[:-1].splitlines() # Run the command, and record the raw output string.
    dashcam_files = sorted(dashcam_files) # Sort the dashcam files alphabetically to get them in chronological order (oldest first).

    if (config["dashcam"]["saving"]["looped_recording"]["mode"] == "manual"): # Check to see if looped recording is in manual mode.
        if (len(dashcam_files) > int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])): # Check to see if the current number of dashcam segments in the working directory is higher than the configured history length.
            videos_to_delete = dashcam_files[0:len(dashcam_files) - int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])] # Create a list of all of the videos that need to be deleted.
            for video in videos_to_delete: # Iterate through each video that needs to be deleted.
                os.system("timeout 5 rm '" + config["general"]["working_directory"] + "/" + video + "'") # Delete the dashcam segment.
    elif (config["dashcam"]["saving"]["looped_recording"]["mode"] == "automatic"): # Check to see if looped recording is in automatic mode.
        free_disk_percentage = psutil.disk_usage(path=config["general"]["working_directory"]).free / psutil.disk_usage(path=config["general"]["working_directory"]).total # Calculate the initial free disk percentage.
        videos_deleted_this_round = 0 # This is a placeholder that will be incremented for each video deleted in the following step.
        while free_disk_percentage < float(config["dashcam"]["saving"]["looped_recording"]["automatic"]["minimum_free_percentage"]): # Run until the free disk percentage is lower than the configured minimum.
            if (len(dashcam_files) - videos_deleted_this_round <= 1): # Check to see if there is one or fewer total dashcam videos.
                display_message("The minimum free disk space hasn't been reached, but there are no more dashcam segments that can be deleted. You should try to free up space on the storage device, or decrease the minimum free disk space percentage in the configuration.", 2)
                break
            if (videos_deleted_this_round > config["dashcam"]["saving"]["looped_recording"]["automatic"]["max_deletions_per_round"]): # Check to see if the maximum allowed deletions per round have been reached.
                display_message("The maximum number of segments that can be deleted per round have been erased by looped recording. It is possible something has gone wrong with the disk usage analysis, or you recently increased the maximum free disk space percentage.", 2)
                break # Exit the loop
            os.system("timeout 5 rm '" + config["general"]["working_directory"] + "/" + dashcam_files[videos_deleted_this_round] + "'") # Delete the oldest remaining segment.
            free_disk_percentage = psutil.disk_usage(path=config["general"]["working_directory"]).free / psutil.disk_usage(path=config["general"]["working_directory"]).total # Recalculate the free disk percentage.
            videos_deleted_this_round += 1
    elif (config["dashcam"]["saving"]["looped_recording"]["mode"] == "disabled"): # Check to see if looped recording is disabled.
        pass
    else:
        display_message("The 'dashcam>saving>looped_recording>mode' configuration value is invalid. Looped recording is disabled.", 3)

    process_timing("end", "Dashcam/File Maintenance")






dashcam_recording_active = False
frames_since_last_segment = {}
def capture_dashcam_video(directory, device="main", width=1280, height=720):
    global frames_since_last_segment
    global dashcam_recording_active
    global instant_framerate
    global calculated_framerate
    global shortterm_framerate
    global audio_recorders
    global first_segment_started_time 
    global audio_record_command
    global recording_active

    device_id = config["dashcam"]["capture"]["video"]["devices"][device]["index"]



    debug_message("Opening video stream on '" + device + "'")


    calculated_framerate[device] = benchmark_camera_framerate(device) # Benchmark this capture device to determine its initial operating framerate.
    if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
        calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.

    output_process = threading.Thread(target=dashcam_output_handler, args=[directory, device, width, height, calculated_framerate[device]], name="OutputHandler" + str(device))
    output_process.start()

    process_timing("start", "Dashcam/Capture Management")
    capture = cv2.VideoCapture(device_id) # Open the video stream.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
    capture.set(cv2.CAP_PROP_FPS, 120) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.

    capture.set(cv2.CAP_PROP_FRAME_WIDTH,width) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height) # Set the video stream height.
    process_timing("end", "Dashcam/Capture Management")

    process_timing("start", "Dashcam/Motion Detection")
    background_subtractor = cv2.createBackgroundSubtractorMOG2() # Initialize the background subtractor for motion detection.
    process_timing("end", "Dashcam/Motion Detection")


    frame_history = [] # This will hold the last several frames in a buffer.


    if (capture is None or not capture.isOpened()):
        display_message("Failed to start dashcam video capture using '" + device  + "' device. Verify that this device is associated with a valid identifier.", 3)
        exit()

    
    process_timing("start", "Dashcam/Calculations")
    last_alert_minimum_framerate_time = 0 # This value holds the last time a minimum frame-rate alert was displayed. Here the value is initialized.

    if (float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) == 0): # Check to see if the minimum frame-rate is 0.
        expected_time_since_last_frame_slowest = 100
    else:
        expected_time_since_last_frame_slowest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) # Calculate the longest expected time between two frames.
    expected_time_since_last_frame_fastest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Calculate the shortest expected time between two frames.
    process_timing("end", "Dashcam/Calculations")

    if (first_segment_started_time == 0): # Check to see if the first segment start time hasn't yet been updated. Since this is a global variable, another dashcam thread may have already set it.
        first_segment_started_time = utils.get_time() # This variable keeps track of when the first segment was started.
    frames_captured = 0
    last_frame_captured = time.time() # This will hold the exact time that the last frame was captured. Here, the value is initialized to the current time before any frames have been captured.

    # Initialize the first segment.
    force_create_segment = False
    segment_number = 0
    segment_started_time = time.time() # This value holds the exact time the segment started for sake of frame-rate calculations.
    shortterm_framerate[device]["start"] = time.time()
    shortterm_framerate[device]["frames"] = 0
    frames_since_last_segment[device] = 0
    current_segment_name[device] = directory + "/predator_dashcam_" + str(round(first_segment_started_time)) + "_" + str(device) + "_" + str(segment_number) + "_N"
    process_timing("start", "Dashcam/Audio Processing")
    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        audio_filepath = current_segment_name[device] + "." + str(config["dashcam"]["capture"]["audio"]["extension"])
        audio_recorders[device] = subprocess.Popen((audio_record_command + " " + audio_filepath).split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
    process_timing("end", "Dashcam/Audio Processing")


    while dashcam_recording_active: # Only run while the dashcam recording flag is set to 'True'. While this flag changes to 'False' this recording process should exit entirely.
        heartbeat() # Issue a status heartbeat.

        if (first_segment_started_time == 0): # Check to see if the first segment started time has been reset to 0.
            first_segment_started_time = utils.get_time() # Here the first segment start time is re-initialized after it was reset by parked mode.

        if (parked == False): # Only update the segment if Predator is not in parked mode.
            recording_active = True # Indicate the Predator is not actively capturing frames.
            if (force_create_segment == True or utils.get_time() > first_segment_started_time + (segment_number+1)*config["dashcam"]["saving"]["segment_length"]): # Check to see if it is time to start a new segment.
                force_create_segment = False # Reset the segment creation force variable.
                calculated_framerate[device] = frames_since_last_segment[device]/(time.time()-segment_started_time) # Calculate the frame-rate of the previous segment.
                if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
                    calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.
                while (utils.get_time() > first_segment_started_time + (segment_number+1)*config["dashcam"]["saving"]["segment_length"]): # Run until the segment number is correct. This prevents a bunch of empty video files from being created when the system time suddenly jumps into the future.
                    frames_since_last_segment[device] = 0 # Reset the global "frames_since_last_segment" variable for this device so the main recording thread knows a new segment has been started.
                    segment_started_time = time.time() # This value holds the exact time the segment started for sake of frame-rate calculations.
                    if (force_create_segment == False): # Only increment the segment counter if this segment was not forced to be created.
                        segment_number+=1
                current_segment_name[device] = directory + "/predator_dashcam_" + str(round(first_segment_started_time + (segment_number*config["dashcam"]["saving"]["segment_length"]))) + "_" + str(device) + "_" + str(segment_number) + "_N" # Update the current segment name.

                process_timing("start", "Dashcam/Audio Processing")
                if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
                    if (audio_recorders[device].poll() is None): # Check to see if there is an active audio recorder.
                        audio_recorders[device].terminate() # Kill the previous segment's audio recorder.
                    audio_filepath = current_segment_name[device] + "." + str(config["dashcam"]["capture"]["audio"]["extension"])
                    audio_recorders[device] = subprocess.Popen((audio_record_command + " " + audio_filepath).split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
                process_timing("end", "Dashcam/Audio Processing")


        process_timing("start", "Dashcam/Calculations")
        if (time.time() - shortterm_framerate[device]["start"] > float(config["developer"]["dashcam_shortterm_framerate_interval"])):
            shortterm_framerate[device]["framerate"] = shortterm_framerate[device]["frames"] / (time.time() - shortterm_framerate[device]["start"])
            shortterm_framerate[device]["start"] = time.time()
            shortterm_framerate[device]["frames"] = 0
        shortterm_framerate[device]["frames"] += 1

        time_since_last_frame = time.time()-last_frame_captured # Calculate the time (in seconds) since the last frame was captured.
        instant_framerate[device] = 1/time_since_last_frame
        if (time_since_last_frame > expected_time_since_last_frame_slowest): # Check see if the current frame-rate is below the minimum expected frame-rate.
            if (frames_since_last_segment[device] > 1 and previously_parked_dormant == False): # Check to make sure we aren't at the very beginning of recording, where frame-rate might be inconsistent.
                if (time.time() - last_alert_minimum_framerate_time > 1): # Check to see if at least 1 second has passed since the last minimum frame-rate alert.
                    display_message("The framerate on '" + device + "' (" + str(round((1/time_since_last_frame)*100)/100) + "fps) has fallen below the minimum frame-rate.", 2)
            last_alert_minimum_framerate_time = time.time() # Record the current time as the time that the last minimum frame-rate alert was shown.
        elif (time_since_last_frame < expected_time_since_last_frame_fastest): # Check see if the current frame-rate is above the maximum expected frame-rate.
            time.sleep(expected_time_since_last_frame_fastest - time_since_last_frame) # Wait to force the frame-rate to stay below the maximum limit.
        process_timing("end", "Dashcam/Calculations")

        last_frame_captured = time.time() # Update the time that the last frame was captured immediately before capturing the next frame.
        process_timing("start", "Dashcam/Video Capture")
        ret, frame = capture.read() # Capture a frame.
        process_timing("end", "Dashcam/Video Capture")
        frames_since_last_segment[device] += 1 # Increment the number of frames captured since the last segment.
        if not ret: # Check to see if the frame failed to be read.
            display_message("Failed to receive video frame from the '" + device  + "' device. It is possible this device has been disconnected.", 2)
            for i in range(1, 12): # Attempt to re-open the capture device several times.
                time.sleep(5*i) # Wait before re-attempting to open the capture device. The length of time between attempts increases with each attempt.
                display_message("Attempting to re-open capture on '" + device  + "' device.", 1)
                process_timing("start", "Dashcam/Capture Management")
                capture = cv2.VideoCapture(device_id) # Open the video stream.
                codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
                capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
                capture.set(cv2.CAP_PROP_FPS, 120) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.
                capture.set(cv2.CAP_PROP_FRAME_WIDTH,width) # Set the video stream width.
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT,height) # Set the video stream height.
                process_timing("end", "Dashcam/Capture Management")
                process_timing("start", "Dashcam/Video Capture")
                ret, frame = capture.read() # Capture a frame.
                process_timing("end", "Dashcam/Video Capture")
                if ret: # Check to see if the frame was successfully read.
                    display_message("Successfully re-opened capture on the '" + device  + "' capture device.", 1)
                    break # Exit the loop, now that the capture device has been re-established.
            if not ret: # Check to see if the frame failed to be read.
                display_message("Video recording on the '" + device  + "' device has been stopped.", 3)
                break # If the capture device can't be re-opened, then stop recording on this device.

        frames_captured+=1
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is convered to flip this capture device's output.
            process_timing("start", "Dashcam/Image Manipulation")
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
            process_timing("end", "Dashcam/Image Manipulation")

        process_timing("start", "Dashcam/Frame Buffer")
        if (config["dashcam"]["parked"]["recording"]["buffer"] > 0): # Check to see if the frame buffer is greater than 0 before adding frames to the buffer.
            frame_history.append(apply_dashcam_stamps(frame, device)) # Add the frame that was just captured to the frame buffer.
            if (len(frame_history) > config["dashcam"]["parked"]["recording"]["buffer"]): # Check to see if the frame buffer has exceeded the maximum length.
                frame_history = frame_history[-config["dashcam"]["parked"]["recording"]["buffer"]:] # Trim the frame buffer to the appropriate length.
        process_timing("end", "Dashcam/Frame Buffer")




        if (parked == True): # Check to see if the vehicle is parked.
            update_state("dashcam/parked_dormant")
            segment_number = 0 # Reset the segment number.
            first_segment_started_time = 0 # Reset the first segment start time.
            force_create_segment = True # Force the segment manager to start a new segment the next time it is called (when Predator exits parked mode)
            recording_active = False

            previously_parked_dormant  = True # Indicate that Predator was parked so that we know that the next loop isn't the first loop of Predator being in parked mode.

            process_timing("start", "Dashcam/Audio Processing")
            if (config["dashcam"]["capture"]["audio"]["enabled"] == True):
                if (audio_recorders[device].poll() is None): # Check to see if there is an active audio recorder.
                    audio_recorders[device].terminate() # Kill the active audio recorder.
            process_timing("end", "Dashcam/Audio Processing")
            process_timing("start", "Dashcam/Motion Detection")
            contours, moving_percentage = detect_motion(frame, background_subtractor) # Run motion analysis on this frame.
            process_timing("end", "Dashcam/Motion Detection")


            if (moving_percentage > float(config["dashcam"]["parked"]["recording"]["sensitivity"])): # Check to see if there is movement that exceeds the sensitivity threshold.
                display_message("Detected motion.", 1)
                if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["motion_detected"]["enabled"] == True): # Check to see if Predator is configured to send motion detection notifications over Reticulum.
                    for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
                        reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has detected motion while parked", destination) # Send a Reticulum LXMF message to this destination.
                calculated_framerate[device] = record_parked_motion(capture, calculated_framerate[device], width, height, device, directory, frame_history) # Run parked motion recording, and update the framerate to the newly calculated framerate.
                if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
                    calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.
                process_timing("start", "Dashcam/Motion Detection")
                background_subtractor = cv2.createBackgroundSubtractorMOG2() # Reset the background subtractor after motion is detected.
                process_timing("end", "Dashcam/Motion Detection")


        else: # If the vehicle is not parked, then run normal video processing.
            update_state("dashcam/normal", instant_framerate)
            previously_parked_dormant = False

            frame = apply_dashcam_stamps(frame, device)
            write_frame(frame, device)

            if (config["developer"]["print_timings"] == True):
                utils.clear(True)
                print(json.dumps(process_timing("dump", ""), indent=4))


    capture.release()
    cv2.destroyAllWindows()



def start_dashcam_recording(dashcam_devices, directory, background=False): # This function starts dashcam recording on a given list of dashcam devices.
    at_least_one_enabled_device = False
    for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True): # Check to see if this device is enabled.
            at_least_one_enabled_device = True
    if (at_least_one_enabled_device == False):
        display_message("There are no dashcam capture devices enabled. Dashcam recording will not start.", 3)
    del at_least_one_enabled_device

    update_status_lighting("normal") # Initialize the status lighting to normal.

    dashcam_process = [] # Create a placeholder list to store the dashcam processes.
    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
    global parked
    global recording_active
    global dashcam_recording_active
    dashcam_recording_active = True
    
    for device in dashcam_devices: # Run through each camera device specified in the configuration, and launch an OpenCV recording instance for it.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
            dashcam_process.append(threading.Thread(target=capture_dashcam_video, args=[directory, device, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]], name="Dashcam" + str(dashcam_devices[device]["index"])))
            dashcam_process[iteration_counter].start()


            iteration_counter += 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.
            print("Started dashcam recording on " + str(dashcam_devices[device]["index"])) # Inform the user that recording was initiation for this camera device.

    try:
        if (background == False): # If background recording is disabled, then prompt the user to press enter to halt recording.
            print("Press Ctrl+C to stop dashcam recording...") # Wait for the user to press enter before continuing, since continuing will terminate recording.
        if (config["dashcam"]["parked"]["enabled"] == True): # Check to see if parked mode functionality is enabled.
            last_moved_time = utils.get_time() # This value holds the Unix timestamp of the last time the vehicle exceeded the parking speed threshold.
            while True: # The user can break this loop with Ctrl+C to terminate dashcam recording.
                if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled.
                    current_location = get_gps_location() # Get the current GPS location.
                else:
                    current_location = [0, 0, 0, 0, 0, 0]
                if (current_location[2] > config["dashcam"]["parked"]["conditions"]["speed"]): # Check to see if the current speed exceeds the parked speed threshold.
                    last_moved_time = utils.get_time()
                if (utils.get_time() - last_moved_time > config["dashcam"]["parked"]["conditions"]["time"]): # Check to see if the amount of time the vehicle has been stopped exceeds the time threshold to enable parked mode.
                    if (parked == False): # Check to see if Predator wasn't already in parked mode.
                        display_message("Entered parked mode.", 1)
                        if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["parking_mode_enabled"]["enabled"] == True): # Check to see if Predator is configured to parking mode activation notifications over Reticulum.
                            for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
                                reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has entered parked mode.", destination) # Send a Reticulum LXMF message to this destination.
                        recording_active = True # Indicate the Predator is not actively capturing frames.
                    parked = True # Enter parked mode.
                else:
                    if (parked == True): # Check to see if Predator wasn't already out of parked mode.
                        display_message("Exited parked mode.", 1)
                        if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["parking_mode_disabled"]["enabled"] == True): # Check to see if Predator is configured to parking mode deactivation notifications over Reticulum.
                            for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
                                reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has exited parked mode.", destination) # Send a Reticulum LXMF message to this destination.
                    parked = False # Exit parked mode.
                    recording_active = True # Indicate the Predator is actively capturing frames.
                
                time.sleep(1)
    except Exception as exception:
        dashcam_recording_active = False # All dashcam threads are watching this variable globally, and will terminate when it is changed to 'False'.
        display_message("Dashcam recording halted.", 1)
        print(exception)



def dashcam_output_handler(directory, device, width, height, framerate):
    global calculated_framerate
    global frames_since_last_segment
    global frames_to_write
    global audio_recorders
    global recording_active

    if (os.path.isdir(config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"]) == False): # Check to see if the saved dashcam video folder needs to be created.
        os.system("mkdir -p '" + config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "'") # Create the saved dashcam video directory.

    segment_number = 0 # This variable keeps track of the segment number, and will be incremented each time a new segment is started.

    last_video_file = "" # Initialize the path of the last video file to just be a blank string.
    last_audio_file = "" # Initialize the path of the last audio file to just be a blank string.
    last_segment_name = "" # Initialize the path of the last base filename to just be a blank string.
    previous_loop_segment_name = "" # This value is used to keep track of what the segment name was during the last processing loop. This allows us to detect when the segment name is changed.

    save_this_segment = False # This will be set to True when the saving trigger is created. The current and previous dashcam segments are saved immediately when the trigger is created, but this allows the completed segment to be saved once the next segment is started, such that the saved segment doesn't cut off at the moment the user triggered a save.

    process_timing("start", "Dashcam/Calculations")
    if (framerate > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the frame-rate benchmark results exceed the maximum allowed frame-rate.
        framerate = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.
    process_timing("end", "Dashcam/Calculations")

    while (current_segment_name[device] == ""): # Wait until the first segment name is initialized by the main recording thread.
        time.sleep(0.01)

    previous_loop_segment_name = current_segment_name[device] # Initialize to be the same.
    output = cv2.VideoWriter(current_segment_name[device] + ".avi", cv2.VideoWriter_fourcc(*'XVID'), float(framerate), (width,  height)) # Initialize the first video output.

    while True:
        time.sleep(0.001)

        video_filepath = current_segment_name[device] + ".avi"
        if (last_segment_name != ""):
            last_video_file = last_segment_name + ".avi"
        else:
            last_video_file = ""
        

        # ===== Check to see if any dash-cam segments need to be saved. =====
        process_timing("start", "Dashcam/Interface Interactions")
        if (os.path.exists(config["general"]["interface_directory"] + "/" + config["dashcam"]["saving"]["trigger"])): # Check to see if the trigger file exists.
            if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if Predator is configured to merge audio and video files.
                dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[video_filepath], name="DashcamSegmentSave") # Create the thread to save this dashcam segment.
                dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled.
                    dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[audio_filepath], name="DashcamSegmentSave") # Create the thread to save the current audio segment as a separate file, even though merging is enabled, since the merge won't have been executed yet.
                    dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                if (last_segment_name != ""): # Check to see if a last filename is set before attempting to copy the last merged video file.
                    dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[str(last_segment_name + ".mkv")], name="DashcamSegmentSave") # Create the thread to save the last video segment.
                    dashcam_segment_saving.start() # Start the dashcam segment saving thread.
            else: # Otherwise, save the last segment as separate audio/video files.
                dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[video_filepath, last_video_file], name="DashcamSegmentSave") # Create the thread to save the current and last video segments.
                dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled.
                    dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[audio_filepath, last_audio_file], name="DashcamSegmentSave") # Create the thread to save the current and last audio segments.
                    dashcam_segment_saving.start() # Start the dashcam segment saving thread.
            save_this_segment = True # This flag causes Predator to save this entire segment again when the next segment is started.
            update_status_lighting("dashcam_save") # Run the function to update the status lighting.

        process_timing("end", "Dashcam/Interface Interactions")



        for frame in frames_to_write[device]: # Iterate through each frame that needs to be written.
            output.write(frame)
        frames_to_write[device] = [] # Clear the frame buffer.


        if (recording_active == True): # Check to see if recording is active before updating the output.
            if (previous_loop_segment_name != current_segment_name[device]): # Check to see if the current segment name has changed since the last loop (meaning a new segment has started).
                last_segment_name = previous_loop_segment_name

                output = None # Release the previous video output file.
                output = cv2.VideoWriter(current_segment_name[device] + ".avi", cv2.VideoWriter_fourcc(*'XVID'), float(calculated_framerate[device]), (width,  height)) # Start the new video output file.

                process_timing("start", "Dashcam/Calculations")
                if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
                    calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.
                process_timing("end", "Dashcam/Calculations")
                process_timing("start", "Dashcam/Writing")
                output = cv2.VideoWriter(current_segment_name[device] + ".avi", cv2.VideoWriter_fourcc(*'XVID'), float(calculated_framerate[device]), (width,  height)) # Update the video output.
                process_timing("end", "Dashcam/Writing")


                last_video_path = last_segment_name + ".avi"
                last_audio_path = last_segment_name + "." + str(config["dashcam"]["capture"]["audio"]["extension"])


                # Merge the video/audio segment that was just completed.
                process_timing("start", "Dashcam/File Merging")
                if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if Predator is configured to merge audio and video files.
                    last_filename_merged = last_segment_name + ".mkv"
                    if (os.path.exists(last_audio_path) == False):
                        display_message("The audio file was missing during audio/video merging. It is possible something has gone wrong with recording.", 2)
                    else:
                        if (last_segment_name[-1].upper() == "P"): # Check to see if the previous file was recorded while parked.
                            audio_offset = -(config["dashcam"]["parked"]["recording"]["buffer"] / calculated_framerate[device]) # Calculate the audio offset based on the size of the frame-buffer
                            print("Applying offset of " + str(audio_offset))
                        else: # Otherwise, the video was recorded during normal operating.
                            audio_offset = 0 # Don't apply an offset, because the audio and video file should start at the same time.
                        merge_audio_video(last_video_path, last_audio_path, last_filename_merged, audio_offset) # Run the audio/video merge.
                process_timing("end", "Dashcam/File Merging")
                


                if (save_this_segment == True): # Now that the new segment has been started, check to see if the segment that was just completed should be saved.
                    if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if Predator is configured to merge audio and video files.
                        if (os.path.exists(last_filename_merged)): # Check to make sure the merged video file actually exists before saving.
                            dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[last_filename_merged], name="DashcamSegmentSave") # Create the thread to save the dashcam segment. At this point, "last_video_file" is actually the completed previous video segment, since we just started a new segment.
                            dashcam_segment_saving.start() # Start the dashcam segment saving thread.

                            # Now that the merged file has been saved, go back and delete the separate files that were saved to the locked folder previously.
                            base_file = config["general"]["working_directory"] + "/" + config["dashcam"]["saving"]["directory"] + "/" + os.path.splitext(os.path.basename(last_filename_merged))[0]
                            os.system("rm '" + base_file + ".avi'")
                            os.system("rm '" + base_file + "." + str(config["dashcam"]["capture"]["audio"]["extension"]) + "'")
                        else: # If the merged video file doesn't exist, it is likely something went wrong with the merging process.
                            display_message("The merged video/audio file did exist when Predator tried to save it. It is likely the merge process has failed unexpectedly. The separate files are being saved as a fallback.", 3)
                            dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[last_video_file, last_audio_path], name="DashcamSegmentSave") # Create the thread to save the dashcam segment. At this point, "last_video_file" is actually the completed previous video segment, since we just started a new segment.
                            dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                    else: # If audio/video merging is disabled, then save the separate video and audio files.
                        dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[last_video_path], name="DashcamSegmentSave") # Create the thread to save the dashcam segment. At this point, "last_video_file" is actually the completed previous video segment, since we just started a new segment.
                        dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                        if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled.
                            dashcam_segment_saving = threading.Thread(target=save_dashcam_segments, args=[last_audio_path], name="DashcamSegmentSave") # Create the thread to save the dashcam segment. At this point, "last_audio_path" is actually the completed previous video segment, since we just started a new segment.
                            dashcam_segment_saving.start() # Start the dashcam segment saving thread.
                    save_this_segment = False # Reset the segment saving flag.
                    update_status_lighting("normal") # Return status lighting to normal.


                delete_old_segments() # Handle the erasing of any old dash-cam segments that need to be deleted.
            previous_loop_segment_name = current_segment_name[device] # Updated the previous segment name to be the current name, since we are about to restart the loop.





def write_frame(frame, device):
    global frames_to_write
    frames_to_write[device].append(frame) # Add the frame to the queue of frames to write.
    if (len(frames_to_write) > int(config["developer"]["dashcam_saving_queue_overflow"])):
        display_message("The queue of dash-cam frames to save to disk has overflowed on '" + str(device) + "'! It is likely that the capture device is outrunning the storage medium. Consider decreasing the maximum frame-rate.", 2)


