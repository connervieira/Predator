# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import global_variables
import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import fnmatch # Required to use wildcards to check strings.

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
save_to_file = utils.save_to_file

# Determine if the object recognition library needs to be imported.
if ("object_recognition" not in config["dashcam"]): # Check to see if the object recognition field is missing. This will be the case if this instance of Predator has been updated from a version that previously didn't support this feature.
    config["dashcam"]["object_recognition"] = {}
object_recognition_needed = False
if (config["dashcam"]["parked"]["event"]["trigger"] == "object_recognition"):
    object_recognition_needed = True
for device in config["dashcam"]["object_recognition"]:
    if (config["dashcam"]["object_recognition"][device]["enabled"] == True):
        object_recognition_needed = True
if (object_recognition_needed == True):
    import object_recognition # object_recognition.py
del object_recognition_needed

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

if (config["dashcam"]["alpr"]["enabled"] == True): # Check to see if background ALPR processing is enabled.
    import alpr

import lighting # Import the lighting.py script.
update_status_lighting = lighting.update_status_lighting # Load the status lighting update function from the lighting script.

must_import_gpiozero = False
if ("physical_controls" in config["dashcam"] and len(config["dashcam"]["physical_controls"]["dashcam_saving"]) > 0):
    must_import_gpiozero = True
for stamp in config["dashcam"]["stamps"]["relay"]["triggers"]: # Check to see if there are any GPIO relay stamps active.
    if (must_import_gpiozero == True):
        break # Exit the loop, since GPIOZero has already been imported.
    if (config["dashcam"]["stamps"]["relay"]["triggers"][stamp]["enabled"] == True): # Check to see if at least one relay stamp is enabled.
        must_import_gpiozero = True
if (must_import_gpiozero == True):
    from gpiozero import Button # Import GPIOZero



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

    if (config["dashcam"]["parked"]["event"]["trigger_motion"]["sensitivity"] < 0):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is a negative number. This will cause unexpected behavior.", 3)
    elif (config["dashcam"]["parked"]["event"]["trigger_motion"]["sensitivity"] > 0.9):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is an exceedingly high value (above 90%). This will likely cause unexpected behavior.", 2)
    elif (config["dashcam"]["parked"]["event"]["trigger_motion"]["sensitivity"] > 1):
        display_message("The 'dashcam>parked>recording>sensitivity' setting is above 100%. This will effectively prevent Predator from ever detecting motion.", 2)







# Define global variables
parked = False # Start with parked mode disabled.
first_segment_start_time = 0 # This keeps track of the timestamp of when the first dash-cam segment started.

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

audio_record_command = "sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " arecord --quiet --format=" + str(config["dashcam"]["capture"]["audio"]["format"])
if (config["dashcam"]["capture"]["audio"]["device"] != ""): # Check to see if a custom device has been set.
    audio_record_command += " --device=" + str(config["dashcam"]["capture"]["audio"]["device"]) + ""
if (str(config["dashcam"]["capture"]["audio"]["rate"]) != ""): # Check to see if a custom rate has been set.
    audio_record_command += " --rate=" + str(config["dashcam"]["capture"]["audio"]["rate"]) + ""






last_trigger_file_created = 0
def create_trigger_file():
    update_status_lighting("dashcam_save") # Since the current dashcam segment is being saved, return to the corresponding status lighting value.

    global last_trigger_file_created
    if (time.time() - last_trigger_file_created > 1): # Check to see if the time that has passed since the last trigger file is more than 1 second.
        if (os.path.isdir(config["general"]["interface_directory"]) == False): # Check to see if the interface directory has not yet been created.
            os.system("mkdir -p '" + str(config["general"]["interface_directory"]) + "'")
            os.system("chmod -R 777 '" + str(config["general"]["interface_directory"]) + "'")
        if (os.path.exists(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"])) == False): # Check to see if the trigger file hasn't already been created.
            os.system("echo " + str(time.time()) + " > \"" + os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"]) + "\"") # Save the trigger file with the current time as the timestamp.
    last_trigger_file_created = time.time()

# This function calls the function "event" when the button on "pin" is held for "hold_time" seconds.
def watch_button(pin, hold_time, event):
    debug_message("Watching pin " + str(pin))
    button = Button(pin)
    time_pressed = 0
    last_stuck_warning = 0
    while global_variables.predator_running:
        if (button.is_pressed and time_pressed == 0): # Check to see if the button was just pressed.
            debug_message("Pressed" + str(pin))
            time_pressed = time.time()
        elif (button.is_pressed and time.time() - time_pressed >= 10): # Check to see if the button has been held for an excessively long time (it may be stuck).
            if (time.time() - last_stuck_warning > 10): # Check to see if it has been at least 30 seconds since the last time a stuck warning was displayed.
                display_message("The button on pin " + str(pin) + " appears to be stuck.", 3)
            last_stuck_warning = time.time()
        elif (button.is_pressed and time.time() - time_pressed >= hold_time): # Check to see if the button is being held, and the time threshold has been reached.
            debug_message("Triggered " + str(pin))
            event()
        elif (button.is_pressed == False): # If the button is not pressed, reset the timer.
            time_pressed = 0

        time.sleep(hold_time/10) # Wait briefly before checking the pin again.


def run_command_delayed(command, delay=5):
    time.sleep(delay)
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



def merge_audio_video(video_file, audio_file, output_file, audio_offset=0):
    debug_message("Merging audio and video files")

    merge_command = ["ffmpeg", "-i", audio_file, "-itsoffset", "-" + str(audio_offset), "-i", video_file, "-c", "copy", output_file]
    erase_command = ["timeout", "1", "rm", video_file, audio_file]

    merge_process = subprocess.run(merge_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    first_attempt = utils.get_time()
    while (merge_process.returncode != 0): # If the merge process exited with an error, keep trying until it is successful. This might happen if one of the files hasn't fully saved to disk.
        merge_process = subprocess.run(merge_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if (utils.get_time() - first_attempt > 5): # Check to see if FFMPEG has been trying for at least 5 seconds.
            display_message("The audio and video segments could not be merged. It is possible one or both of the files is damaged.", 2)
            process_timing("end", "Dashcam/File Merging")
            return False # Time out, and exit with a success value False.
    delayed_erase_command = threading.Thread(target=run_command_delayed, args=[erase_command, 2]) # Create a thread to erase the old files with a delay (so other threads can finish)
    delayed_erase_command.start()

    debug_message("Merged audio and video files")
    return True



# This function runs in a seperate thread from the main dashcam capture, and will intermittently grab the most recent frame, and run ALPR on it.
if (config["dashcam"]["alpr"]["enabled"] == True): # Check to see if background ALPR processing is enabled.
    if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if the license plate logging file name is not empty. If the file name is empty, then license plate logging will be disabled.
        plate_log = alpr.load_alpr_log()
def background_alpr(device):
    global current_frame_data
    if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if the license plate logging file name is not empty. If the file name is empty, then license plate logging will be disabled.
        global plate_log

    while global_variables.predator_running: # Run until dashcam capture finishes.
        if (device in current_frame_data):
            debug_message("Running ALPR")
            process_timing("start", "Dashcam/ALPR Processing")
            temporary_image_filepath = config["general"]["interface_directory"] + "/DashcamALPR_" + str(device) + ".jpg" # Determine where this frame will be temporarily saved for processing.
            cv2.imwrite(temporary_image_filepath, current_frame_data[device]) # Write this frame to the interface directory.
            alpr_results = alpr.run_alpr(temporary_image_filepath) # Run ALPR on the frame.
            process_timing("end", "Dashcam/ALPR Processing")

            debug_message("Validating plates")
            process_timing("start", "Dashcam/ALPR Validation")
            detected_plates_valid = [] # This will hold all of the plates that pass the validation sequence.
            detected_plates_all = [] # This will hold all plates detected, regardless of validation.
            if (len(alpr_results["results"]) > 0): # Check to see if at least one plate was detected.
                for result in alpr_results["results"]:
                    guesses_valid = {} # This is a temporary dictionary that will hold the valid guesses before they are added to the complete list of detected plates.
                    guesses_all = {} # This is a temporary dictionary that will hold all guesses before they are added to the complete list of detected plates.
                    for candidate in result["candidates"]:
                        if (candidate["confidence"] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate exceeds the minimum confidence threshold.
                            if any(alpr.validate_plate(candidate["plate"], format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]) or len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0: # Check to see if this plate passes validation.
                                guesses_valid[candidate["plate"]] = candidate["confidence"] # Add this plate to the list of valid guesses.
                        guesses_all[candidate["plate"]] = candidate["confidence"] # Add this plate to the list of valid guesses.

                    if (len(guesses_valid) == 0): # If there are no valid guesses, then check to see if "best_effort" mode is enabled.
                        if (config["general"]["alpr"]["validation"]["best_effort"] == True): # Check to see if "best_effort" is enabled.
                            guesses_valid[result["candidates"][0]["plate"]] = result["candidates"][0]["confidence"] # Add the most likely plate to the valid guesses.

                    if (len(guesses_valid) > 0): # Check to see if there is at least one valid guess.
                        detected_plates_valid.append(guesses_valid) # Add the valid guesses as a new plate.
                    if (len(guesses_all) > 0): # Check to see if there is at least one guess.
                        detected_plates_all.append(guesses_all) # Add the guesses as a new plate.
                    del guesses_valid
                    del guesses_all
            process_timing("end", "Dashcam/ALPR Validation")


            debug_message("Checking for alerts")
            process_timing("start", "Dashcam/ALPR Alerts")
            if (config["general"]["alerts"]["alerts_ignore_validation"]):
                plates_to_check_alerts = detected_plates_all
            else:
                plates_to_check_alerts = detected_plates_valid
            alert_database = alpr.load_alert_database(config["general"]["alerts"]["databases"], config["general"]["working_directory"]) # Load the license plate alert database.
            active_alerts = {} # This is an empty placeholder that will hold all of the active alerts. 
            if (len(alert_database) > 0): # Only run alert processing if the alert database isn't empty.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user.
                    for plate in plates_to_check_alerts: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                        for guess in plate: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                            if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                active_alerts[guess] = {}
                                active_alerts[guess]["rule"] = rule # Add this plate to the active alerts dictionary with the rule that triggered it.
                                if ("name" in alert_database[rule]):
                                    active_alerts[guess]["name"] = alert_database[rule]["name"]
                                if ("description" in alert_database[rule]):
                                    active_alerts[guess]["description"] = alert_database[rule]["description"]
                                if (config["general"]["alerts"]["allow_duplicate_alerts"] == False):
                                    break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.
            process_timing("end", "Dashcam/ALPR Alerts")


            # Save detected license plates to file.
            debug_message("Logging ALPR results")
            process_timing("start", "Dashcam/ALPR Logging")
            if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if license plate history saving is enabled.
                debug_message("Saving license plate history")

                if (len(detected_plates_all) > 0): # Only save the license plate history for this round if 1 or more plates were detected.
                    current_time = time.time() # Get the current timestamp.

                    plate_log[current_time] = {} # Initialize an entry in the plate history log using the current time.

                    if (config["realtime"]["gps"]["alpr_location_tagging"] == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                        if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS functionality is enabled.
                            current_location = get_gps_location() # Get the current location.
                        else:
                            current_location = [0.0, 0.0] # Grab a placeholder for the current location, since GPS functionality is disabled.

                        plate_log[current_time]["location"] = {"lat": current_location[0],"lon": current_location[1]} # Add the current location to the plate history log entry.

                    plate_log[current_time]["plates"] = {}

                    for plate in detected_plates_all: # Iterate though each plate detected this round.
                        top_plate = list(plate.keys())[0]
                        if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Only initialize the plate's guesses to the log if Predator is configured to do so.
                            plate_log[current_time]["plates"][top_plate] = {"alerts": [], "guesses": {}} # Initialize this plate in the plate log.
                        else:
                            plate_log[current_time]["plates"][top_plate] = {"alerts": []} # Initialize this plate in the plate log.
                        for guess in plate: # Iterate through each guess in this plate.
                            if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                plate_log[current_time]["plates"][top_plate]["alerts"].append(active_alerts[guess]) # Add the rule that triggered the alert to a separate list.
                            if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Only add this guess to the log if Predator is configured to do so.
                                plate_log[current_time]["plates"][top_plate]["guesses"][guess] = plate[guess] # Add this guess to the log, with its confidence level.

                    save_to_file(config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"], json.dumps(plate_log)) # Save the modified plate log to the disk as JSON data.
            process_timing("end", "Dashcam/ALPR Logging")


            # Issue interface directory updates.
            if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
                process_timing("start", "Dashcam/ALPR Interface")
                debug_message("Issuing interface updates")
                heartbeat() # Issue a status heartbeat.

                # Reformat the plates to the format expected by the interface directory.
                plates_to_save_to_interface = {}
                for plate in detected_plates_valid:
                    top_plate = list(plate.keys())[0]
                    plates_to_save_to_interface[top_plate] = {}
                    for guess in plate:
                        plates_to_save_to_interface[top_plate][guess] = plate[guess]

                utils.log_plates(plates_to_save_to_interface) # Update the list of recently detected license plates.
                utils.log_alerts(active_alerts) # Update the list of active alerts.
                process_timing("end", "Dashcam/ALPR Interface")


            # Display alerts.
            process_timing("start", "Dashcam/ALPR Display")
            alpr.display_alerts(active_alerts) # Display active alerts.
            if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                if (len(active_alerts) > 0): # Check to see if there are active alerts.
                    update_status_lighting("alpr_alert") # Run the function to update the status lighting.
                elif (len(detected_plates_valid) > 0):
                    update_status_lighting("alpr_detection") # Run the function to update the status lighting.
                else:
                    update_status_lighting("dashcam_save") # Since the current dashcam segment is being saved, return to the corresponding status lighting value.
            for plate in detected_plates_valid: # Run once for each detected plate.
                utils.play_sound("alpr_notification") # Play the "new plate detected" sound.
            for alert in active_alerts: # Run once for each active alert.
                if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications enabled.
                    debug_message("Issuing alert push notification")
                    os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=A license plate in an alert database has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.

                if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                    utils.display_shape("triangle") # Display an ASCII triangle in the output.

                utils.play_sound("alpr_alert") # Play the alert sound, if configured to do so.
            process_timing("end", "Dashcam/ALPR Display")


            time.sleep(float(config["dashcam"]["alpr"]["interval"])) # Sleep (if configured to do so) before starting the next processing loop.


if (config["realtime"]["saving"]["object_recognition"]["enabled"] == True):
    debug_message("Loading object_recognition history")
    object_recognition_file_location = config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["object_recognition"]["file"]
    if (os.path.exists(object_recognition_file_location) == False): # If the log file doesn't exist, create it.
        save_to_file(object_recognition_file_location, "{}") # Save a blank placeholder dictionary to the log file.
    object_recognition_file = open(object_recognition_file_location, "r") # Open the log file for reading.
    object_recognition_file_contents = object_recognition_file.read() # Read the raw contents of the file as a string.
    object_recognition_file.close() # Close the log file.

    if (utils.is_json(object_recognition_file_contents) == True): # If the file contains valid JSON data, then load it.
        object_recognition_log = json.loads(object_recognition_file_contents) # Read and load the log from the file contents.
    else: # If the log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        object_recognition_log = json.loads("{}") # Load a blank placeholder dictionary.

def background_object_recognition(device):
    global object_recognition_file_location
    global object_recognition_log
    global current_frame_data

    while device not in current_frame_data: # Wait until the first frame is captured on this device.
        time.sleep(1)

    last_object_alert = 0 # This is a placeholder that will hold the timestamp of the last object alert.
    while global_variables.predator_running:
        # Detect objects:
        detected_objects = object_recognition.predict(current_frame_data[device], "dashcam")
        considered_objects = []
        for detected_object in detected_objects:
            if (detected_object["name"] in config["dashcam"]["object_recognition"][device]["objects_considered"]):
                if (detected_object["conf"] >= config["dashcam"]["object_recognition"][device]["minimum_confidence"]):
                    considered_objects.append(detected_object)
        del detected_objects

        # Find object alerts:
        alert_objects = []
        for detected_object in considered_objects:
            if (detected_object["name"] in config["dashcam"]["object_recognition"][device]["objects_alert"]):
                alert_objects.append(detected_object)

        # Handle object logging:
        if (device not in object_recognition_log):
            object_recognition_log[device] = {}
        if (len(considered_objects) > 0):
            object_recognition_log[device][utils.get_time()] = considered_objects
            utils.save_to_file(object_recognition_file_location, json.dumps(object_recognition_log, indent=4))

        # Handle alerts:
        if (len(alert_objects) > 0):
            if (time.time() - last_object_alert > 3):
                print(utils.style.red + "Detected alert object" + utils.style.end)
                utils.play_sound("dashcam_object_alert")
                update_status_lighting("dashcam_object") # Return the status lighting to normal.
            last_object_alert = time.time()


        time.sleep(float(config["dashcam"]["object_recognition"][device]["delay"]))



def benchmark_camera_framerate(device, frames=5): # This function benchmarks a given camera to determine its framerate.
    global config

    resolution = [config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]] # This determines the resolution that will be used for the video capture device.
    capture = cv2.VideoCapture(config["dashcam"]["capture"]["video"]["devices"][device]["index"]); # Open the video capture device.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
    capture.set(cv2.CAP_PROP_FPS, 240) # Set the frame-rate to an arbitrarily high value so OpenCV will use the highest frame-rate the capture supports.

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

    if (fps > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
        fps = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.

    if (fps + config["dashcam"]["saving"]["framerate_snap"] >= float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the frame-rate benchmark is within a certain threshold of the maximum allowed framerate.
        fps = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.

    return fps # Return the calculated FPS.






# This function is called when the lock trigger file is created, usually to save the current and last segments.
last_played_dashcam_saved_sound = 0 # This holds the timestamp of the last time the dashcam video was saved so we don't play the saved sound repeatedly in short succession.
def lock_dashcam_segment(file):
    global config
    global last_played_dashcam_saved_sound

    process_timing("start", "Dashcam/File Maintenance")

    if (time.time()-last_played_dashcam_saved_sound > 5):
        utils.play_sound("dashcam_saved")
    last_played_dashcam_saved_sound = time.time()
    utils.display_message("Locked dash-cam segment file")

    if (os.path.isdir(os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"])) == False): # Check to see if the saved dashcam video folder needs to be created.
        os.system("mkdir -p '" + os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"] + "'")) # Create the saved dashcam video directory.

    if (os.path.isdir(os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"]))): # Check to see if the dashcam saving directory exists.
        os.system("cp \"" + file + "\" \"" + os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"]) + "\"") # Copy the current dashcam video segment to the saved folder.
        anything_saved = True # Indicate that at least one file was saved.
    else:
        display_message("The dashcam saving directory does not exist, and could not be created. The dashcam video could not be locked.", 3)

    time.sleep(0.5) # Wait for a short period of time so that other dashcam recording threads have time to detect the trigger file.
    os.system("rm -f '" + os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"]) + "'") # Remove the dashcam lock trigger file.
    if (os.path.exists(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"]))): # Check to see if the trigger file exists even after it should have been removed.
        display_message("Unable to remove dashcam lock trigger file.", 3)

    process_timing("end", "Dashcam/File Maintenance")


relay_triggers = {}
for stamp in config["dashcam"]["stamps"]["relay"]["triggers"]: # Iterate over reach configured relay trigger.
    if (config["dashcam"]["stamps"]["relay"]["triggers"][stamp]["enabled"] == True): # Check to see if this relay stamp is enabled.
        relay_triggers[stamp] = Button(int(config["dashcam"]["stamps"]["relay"]["triggers"][stamp]["pin"])) # Add this button to the list of relays being monitored.


def apply_dashcam_stamps(frame, device=""):
    global instant_framerate
    global calculated_framerate
    global shortterm_framerate
    global parked

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
    if (config["dashcam"]["stamps"]["diagnostic"]["state"]["enabled"] == True): # Check to see if the state overlay stamp is enabled.
        current_state = utils.get_current_state()
        if (parked == False):
            if (os.path.exists(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"])) == True): # Check to see if the trigger file exists.
                diagnostic_stamp = diagnostic_stamp + "NS"
            else:
                diagnostic_stamp = diagnostic_stamp + "NN"
        elif (parked == True):
            if (current_state["mode"] == "dashcam/parked_dormant"):
                diagnostic_stamp = diagnostic_stamp + "PD"
            elif (current_state["mode"] == "dashcam/parked_active"):
                diagnostic_stamp = diagnostic_stamp + "PA"


    if (config["dashcam"]["stamps"]["relay"]["enabled"] == True): # Check to see if relay stamp features are enabled before processing the relay stamp.
        stamp_number = 0
        for stamp in config["dashcam"]["stamps"]["relay"]["triggers"]:
            if (config["dashcam"]["stamps"]["relay"]["triggers"][stamp]["enabled"] == True): # Check to see if this relay stamp is enabled.
                if (relay_triggers[stamp].is_pressed): # Check to see if the relay is triggered.
                    relay_stamp_color = config["dashcam"]["stamps"]["relay"]["colors"]["on"]
                else:
                    relay_stamp_color = config["dashcam"]["stamps"]["relay"]["colors"]["off"]
                relay_stamp = config["dashcam"]["stamps"]["relay"]["triggers"][stamp]["text"] # Set the relay stamp text to a blank placeholder. Elements will be added to this in the next steps.
                (label_width, label_height), baseline = cv2.getTextSize(relay_stamp, 2, config["dashcam"]["stamps"]["size"], 1)
                relay_stamp_position = [width - 10 - label_width, (30 * stamp_number) + round(30 * config["dashcam"]["stamps"]["size"])] # Determine where the diagnostic overlay stamp should be positioned in the video stream.
                cv2.putText(frame, relay_stamp, (relay_stamp_position[0], relay_stamp_position[1]), 2, config["dashcam"]["stamps"]["size"], (relay_stamp_color[2], relay_stamp_color[1], relay_stamp_color[0])) # Add the relay overlay stamp to the video stream.
                stamp_number += 1


    gps_stamp_position = [10, 30] # Determine where the GPS overlay stamp should be positioned in the video stream.
    gps_stamp = "" # Set the GPS to a blank placeholder. Elements will be added to this in the next steps.
    if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS features are enabled before processing the GPS stamp.
        if (config["dashcam"]["stamps"]["gps"]["location"]["enabled"] == True or config["dashcam"]["stamps"]["gps"]["altitude"]["enabled"] == True or config["dashcam"]["stamps"]["gps"]["speed"]["enabled"] == True): # Check to see if at least one of the GPS stamps is enabled.
            current_location = utils.get_gps_location_lazy() # Get the most recent location.
            
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




def dashcam_parked_dormant(device):
    global parked
    update_state("dashcam/parked_dormant", instant_framerate)

    device_index = config["dashcam"]["capture"]["video"]["devices"][device]["index"]

    # Initialize motion detection:
    if (config["dashcam"]["parked"]["event"]["trigger"] == "motion"):
        process_timing("start", "Dashcam/Detection Motion")
        background_subtractor = cv2.createBackgroundSubtractorMOG2() # Initialize the background subtractor for motion detection.
        process_timing("end", "Dashcam/Detection Motion")

    capture = cv2.VideoCapture(device_index) # Open the video stream.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
    capture.set(cv2.CAP_PROP_FPS, config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"]) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]) # Set the video stream height.
    process_timing("end", "Dashcam/Capture Management")

    if (capture is None or not capture.isOpened()):
        display_message("Failed to start dashcam video capture using '" + device  + "' device. Verify that this device is associated with a valid identifier.", 3)
        exit()

    frame_buffer = [] # This is a buffer that will hold the last N frames.
    while global_variables.predator_running and parked == True:
        ret, frame = capture.read() # Capture a frame.

        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is configured to flip this capture device's output.
            process_timing("start", "Dashcam/Image Manipulation")
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
            process_timing("end", "Dashcam/Image Manipulation")

        process_timing("start", "Dashcam/Capture Management")
        current_frame_data[device] = frame # Set the current frame for this device as the frame after rotation has been applied, but before overlay stamps.
        process_timing("end", "Dashcam/Capture Management")

        frame_buffer.append(apply_dashcam_stamps(frame, device))
        if (len(frame_buffer) > config["dashcam"]["parked"]["event"]["buffer"]): # Check to see if the frame buffer has exceeded the maximum length.
            frame_buffer = frame_buffer[-config["dashcam"]["parked"]["event"]["buffer"]:] # Trim the frame buffer to the appropriate length.


        # ==========================================
        # Run event detection on the captured frame:
        if (config["dashcam"]["parked"]["event"]["trigger"] == "motion"):
            process_timing("start", "Dashcam/Motion Detection")
            contours, moving_percentage = detect_motion(frame, background_subtractor) # Run motion analysis on this frame.
            if (moving_percentage > float(config["dashcam"]["parked"]["event"]["trigger_motion"]["sensitivity"])): # Check to see if there is movement that exceeds the sensitivity threshold.
                display_message("Detected event.", 1)
                dashcam_parked_event(capture, device, frame_buffer)
                delete_old_segments()
            process_timing("end", "Dashcam/Motion Detection")
        elif (config["dashcam"]["parked"]["event"]["trigger"] == "object_recognition"):
            process_timing("start", "Dashcam/Object Recognition")
            detected_objects = object_recognition.predict(frame, "dashcam")
            for element in detected_objects:
                if (element["conf"] >= config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["minimum_confidence"] and element["name"] in config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["objects"]): # Check to see if this object is in the list of target objects.
                    display_message("Detected event.", 1)
                    dashcam_parked_event(capture, frame_buffer)
                    delete_old_segments()
            process_timing("end", "Dashcam/Object Recognition")
        else:
            utils.display_message("Unknown event detection method", 3)
        # ==========================================




# This function is called as a subprocess of the parked dashcam recording, and is triggered when motion is detected. This function exits when motion is no longer detected (after the motion detection timeout), and returns to dormant parked mode.
def dashcam_parked_event(capture, device, frame_buffer):
    global parked
    global instant_framerate
    global calculated_framerate
    global audio_recorders
    global audio_record_command



    directory = config["general"]["working_directory"]

    last_event_detected = utils.get_time() # Initialize the last time that an event was detected to now. We can assume an event was just detected because this function is only called after an event is triggered.


    # Initialize motion detection:
    if (config["dashcam"]["parked"]["event"]["trigger"] == "motion"):
        process_timing("start", "Dashcam/Detection Motion")
        background_subtractor = cv2.createBackgroundSubtractorMOG2() # Initialize the background subtractor for motion detection.
        process_timing("end", "Dashcam/Detection Motion")



    # Initialize the output for this segment:
    start_time = utils.get_time()
    segment_base_name = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H%M%S') + " Predator"
    segment_name = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H%M%S') + " Predator " + str(device) + " P"
    del start_time
    output_codec = list(config["dashcam"]["saving"]["file"]["codec"])
    output = cv2.VideoWriter(os.path.join(directory, segment_name + "." + config["dashcam"]["saving"]["file"]["extension"]), cv2.VideoWriter_fourcc(output_codec[0], output_codec[1], output_codec[2], output_codec[3]), calculated_framerate[device], (config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"])) # Initialize the first video output.

    # Handle audio recording for this segment:
    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        process_timing("start", "Dashcam/Audio Processing")
        audio_filepath = os.path.join(directory, segment_base_name + "." + str(config["dashcam"]["capture"]["audio"]["extension"]))
        if (segment_base_name not in audio_recorders or audio_recorders[segment_base_name].poll() is not None): # Check to see if the audio recorder hasn't yet been started by another thread.
            subprocess.Popen(("sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " killall arecord").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Kill the previous arecord instance (if one exists)
            command = "sleep " + str(float(config["dashcam"]["capture"]["audio"]["start_delay"])) + "; " + audio_record_command + " \"" + str(audio_filepath) + "\""
            if (config["dashcam"]["capture"]["audio"]["display_output"] == True):
                print("Executing:", audio_record_command)
                audio_recorders[segment_base_name] = subprocess.Popen(command, shell=True) # Start the next segment's audio recorder.
            else:
                audio_recorders[segment_base_name] = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
            del command
        process_timing("end", "Dashcam/Audio Processing")


    process_timing("start", "Dashcam/Writing")
    original_buffer_size = len(frame_buffer)
    for frame in frame_buffer: # Iterate through each frame in the frame history.
        output.write(frame)
    del frame_buffer

    process_timing("end", "Dashcam/Writing")

    frames_captured = 0 # This is a placeholder that will keep track of how many frames are captured in this parked recording.
    capture_start_time = time.time() # This stores the time that this parked recording started.
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


    while global_variables.predator_running and parked == True and utils.get_time() - last_event_detected < config["dashcam"]["parked"]["event"]["timeout"]: # Run until the criteria for event recording are no longer met.
        heartbeat() # Issue a status heartbeat.
        update_state("dashcam/parked_active", instant_framerate)

        if (capture is None or capture.isOpened() == False): # Check to see if the capture failed to open.
            display_message("The video capture on device '" + str(device) + "' was dropped during parked recording", 3)

        process_timing("start", "Dashcam/Calculations")
        if (time.time() - shortterm_framerate[device]["start"] > float(config["developer"]["dashcam_shortterm_framerate_interval"])): # Check to see if enough time has passed since the last short-term framerate update was made.
            shortterm_framerate[device]["framerate"] = shortterm_framerate[device]["frames"] / (time.time() - shortterm_framerate[device]["start"]) # Calculate the short-term frame-rate.
            shortterm_framerate[device]["start"] = time.time() # Reset the timer.
            shortterm_framerate[device]["frames"] = 0 # Reset the number of frames.
        shortterm_framerate[device]["frames"] += 1 # Increment the number of frames since the last reading.
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
        process_timing("end", "Dashcam/Calculations")

        process_timing("start", "Dashcam/Image Manipulation")
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is convered to flip this capture device's output.
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
        process_timing("end", "Dashcam/Image Manipulation")


        # ==========================================
        # Run event detection on the captured frame:
        if (config["dashcam"]["parked"]["event"]["trigger"] == "motion"):
            process_timing("start", "Dashcam/Motion Detection")
            contours, moving_percentage = detect_motion(frame, background_subtractor) # Run motion analysis on this frame.

            if (moving_percentage > float(config["dashcam"]["parked"]["event"]["trigger_motion"]["sensitivity"])): # Check to see if there is movement that exceeds the sensitivity threshold. This ensures that motion that is just barely over the threshold doesn't cause Predator to repeatedly start and stop recording.
                if (utils.get_time() - last_event_detected > 2): # Check to see if it has been more than 2 seconds since motion was last detected so that the message is only displayed after there hasn't been motion for some time.
                    display_message("Detected event.", 1)
                last_event_detected = utils.get_time()

            if (config["dashcam"]["parked"]["event"]["label"]["enabled"] == True):
                for contour in contours: # Iterate through each contour.
                    if cv2.contourArea(contour) > 1: # Check to see if this contour is big enough to be worth highlighting.
                        color = config["dashcam"]["parked"]["event"]["label"]["color"]
                        x, y, w, h = cv2.boundingRect(contour) # Define the edges of the contour.
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (color[2], color[1], color[0]), 2) # Draw a box around the contour in the frame.
            process_timing("end", "Dashcam/Motion Detection")
        elif (config["dashcam"]["parked"]["event"]["trigger"] == "object_recognition"):
            process_timing("start", "Dashcam/Object Recognition")
            detected_objects = object_recognition.predict(frame, "dashcam")
            for element in detected_objects:
                if (element["conf"] >= config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["minimum_confidence"] and element["name"] in config["dashcam"]["parked"]["event"]["trigger_object_recognition"]["objects"]): # Check to see if this object is in the list of target objects.
                    if (utils.get_time() - last_event_detected > 2): # Check to see if it has been more than 2 seconds since motion was last detected so that the message is only displayed after there hasn't been motion for some time.
                        display_message("Detected event.", 1)
                    last_event_detected = utils.get_time()
                    if (config["dashcam"]["parked"]["event"]["label"]["enabled"] == True):
                        color = config["dashcam"]["parked"]["event"]["label"]["color"]
                        cv2.rectangle(frame, (element["bbox"]["x1"], element["bbox"]["y1"]), (element["bbox"]["x2"], element["bbox"]["y2"]), (color[2], color[1], color[0]), 2) # Draw a box around the contour in the frame.
            process_timing("end", "Dashcam/Object Recognition")
        # ==========================================


        frame = apply_dashcam_stamps(frame, device) # Apply dashcam overlay stamps to the frame.

        process_timing("start", "Dashcam/Writing")
        output.write(frame)
        process_timing("end", "Dashcam/Writing")

    display_message("Stopped parked event recording.", 1)

    # Stop audio/video recording:
    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        process_timing("start", "Dashcam/Audio Processing")
        if (segment_base_names[-1] in audio_recorders and audio_recorders[segment_base_names[-1]].poll() is None): # Check to see if there is an active audio recorder.
            audio_recorders[segment_base_names[-1]].terminate() # Kill the previous segment's audio recorder.
        time.sleep(config["dashcam"]["capture"]["audio"]["start_delay"]) # Wait briefly for the audio recorder to terminate.
        subprocess.Popen(("sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " killall arecord").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Force kill all audio recording processes.
        process_timing("end", "Dashcam/Audio Processing")
    output = None # Release the output.

    process_timing("start", "Dashcam/Calculations")
    calculated_framerate[device] = frames_captured / (time.time() - capture_start_time)
    if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
        calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.
    process_timing("end", "Dashcam/Calculations")



def delete_old_segments():
    global config

    process_timing("start", "Dashcam/File Maintenance")

    dashcam_files_list_command = "ls " + config["general"]["working_directory"] + " | grep \" Predator \"" # Set up the command to get a list of all unsaved dashcam videos in the working directory.
    dashcam_files = str(os.popen(dashcam_files_list_command).read())[:-1].splitlines() # Run the command, and record the raw output string.
    dashcam_files = sorted(dashcam_files) # Sort the dashcam files alphabetically to get them in chronological order (oldest first).

    if (config["dashcam"]["saving"]["looped_recording"]["mode"] == "manual"): # Check to see if looped recording is in manual mode.
        if (len(dashcam_files) > int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])): # Check to see if the current number of dashcam segments in the working directory is higher than the configured history length.
            videos_to_delete = dashcam_files[0:len(dashcam_files) - int(config["dashcam"]["saving"]["looped_recording"]["manual"]["history_length"])] # Create a list of all of the videos that need to be deleted.
            for video in videos_to_delete: # Iterate through each video that needs to be deleted.
                video_file = config["general"]["working_directory"] + "/" + video
                sidecar_file = os.path.splitext(video_file)[0] + ".json" # This file will only exists if it has been generated by the user with pre-recorded mode.
                audio_file = os.path.splitext(video_file)[0] + "." + config["dashcam"]["capture"]["audio"]["extension"]
                if (os.path.exists(video_file)): # Check to see if this video file still exists (it hasn't been deleted by another thread).
                    os.system("timeout 5 rm '" + video_file + "'") # Delete the dashcam segment.
                if (os.path.exists(sidecar_file)): # Check to see if there is a side-car file associated with this video.
                    os.system("timeout 5 rm '" + sidecar_file + "'") # Delete the dashcam segment side-car file.
                if (os.path.exists(audio_file)): # Check to see if there is an audio file associated with this video. This is generally unnecessary, since audio files should be included in the query to get all dashcam files.
                    os.system("timeout 5 rm '" + audio_file + "'") # Delete the dashcam segment audio file.
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
            video_file = dashcam_files[videos_deleted_this_round]
            sidecar_file = os.path.splitext(video_file)[0] + ".json" # This file will only exists if it has been generated by the user with pre-recorded mode.
            if (os.path.exists(video_file)): # Check to see if this video file still exists (it hasn't been deleted by another thread).
                os.system("timeout 5 rm '" + config["general"]["working_directory"] + "/" + video_file + "'") # Delete the oldest remaining segment.
            if (os.path.exists(sidecar_file)): # Check to see if this video file still exists (it hasn't been deleted by another thread).
                os.system("timeout 5 rm '" + config["general"]["working_directory"] + "/" + sidecar_file + "'") # Delete the side-car file associated with this segment.
            free_disk_percentage = psutil.disk_usage(path=config["general"]["working_directory"]).free / psutil.disk_usage(path=config["general"]["working_directory"]).total # Recalculate the free disk percentage.
            videos_deleted_this_round += 1 # Increment the number of videos deleted this round.
    elif (config["dashcam"]["saving"]["looped_recording"]["mode"] == "disabled"): # Check to see if looped recording is disabled.
        pass
    else:
        display_message("The 'dashcam>saving>looped_recording>mode' configuration value is invalid. Looped recording is disabled.", 3)

    process_timing("end", "Dashcam/File Maintenance")






# This is the actual dashcam recording function. This function captures video.
current_frame_data = {} # This will hold the most recent frame captured by each camera.

def dashcam_normal(device):
    global config
    global first_segment_start_time # This is a global variable that allows all dash-cam threads to determine the timestamp that their segments should be recorded relative to.
    global shortterm_framerate # This holds the short-term frame-rate calculations.

    directory = config["general"]["working_directory"]

    device_index = config["dashcam"]["capture"]["video"]["devices"][device]["index"]


    process_timing("start", "Dashcam/Calculations")
    calculated_framerate[device] = benchmark_camera_framerate(device) # Benchmark this capture device to determine its initial operating framerate.
    process_timing("end", "Dashcam/Calculations")


    process_timing("start", "Dashcam/Capture Management")
    debug_message("Opening video stream on '" + device + "'")

    capture = cv2.VideoCapture(device_index) # Open the video stream.
    codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
    capture.set(cv2.CAP_PROP_FPS, config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to a high value so OpenCV will use the highest frame-rate the capture supports.

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"]) # Set the video stream width.
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]) # Set the video stream height.
    process_timing("end", "Dashcam/Capture Management")


    if (capture is None or not capture.isOpened()):
        display_message("Failed to start dashcam video capture using '" + device  + "' device. Verify that this device is associated with a valid identifier.", 3)
        exit()

    
    process_timing("start", "Dashcam/Calculations")
    last_alert_minimum_framerate_time = 0 # This value holds the last time a minimum frame-rate alert was displayed. Here the value is initialized.

    if (float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) == 0): # Check to see if the minimum frame-rate is 0.
        expected_time_since_last_frame_slowest = 100 # Set the slowest expected frame time to an arbitrarily high value.
    else:
        expected_time_since_last_frame_slowest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["min"]) # Calculate the longest expected time between two frames.
    expected_time_since_last_frame_fastest = 1/float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Calculate the shortest expected time between two frames.
    process_timing("end", "Dashcam/Calculations")


    if (first_segment_start_time == 0): # Check to see if the first segment start time hasn't yet been updated. Since this is a global variable, another dashcam thread may have already set it.
        first_segment_start_time = utils.get_time() # This variable keeps track of when the first segment was started. It is shared between threads.
    last_frame_captured = time.time() # This will hold the exact time that the last frame was captured. Here, the value is initialized to the current time before any frames have been captured.

    # Initialize the first segment:
    segment_number = 0
    segment_started_time = time.time() # This value holds the exact time the segment started for sake of frame-rate calculations.
    shortterm_framerate[device]["start"] = time.time()
    shortterm_framerate[device]["frames"] = 0
    frames_since_last_segment = 0

    segment_base_names = [datetime.datetime.fromtimestamp(first_segment_start_time).strftime('%Y-%m-%d %H%M%S') + " Predator"] # Initialize the first segment name for this device.
    segment_names = [datetime.datetime.fromtimestamp(first_segment_start_time).strftime('%Y-%m-%d %H%M%S') + " Predator " + str(device) + " N"] # Initialize the first segment name for this device.

    output_codec = list(config["dashcam"]["saving"]["file"]["codec"])
    output = cv2.VideoWriter(os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["saving"]["file"]["extension"]), cv2.VideoWriter_fourcc(output_codec[0], output_codec[1], output_codec[2], output_codec[3]), calculated_framerate[device], (config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"])) # Initialize the first video output.


    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        process_timing("start", "Dashcam/Audio Processing")
        audio_filepath = os.path.join(directory, segment_base_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"]))
        if (segment_base_names[-1] not in audio_recorders or audio_recorders[segment_base_names[-1]].poll() is not None): # Check to see if the audio recorder hasn't yet been started by another thread.
            subprocess.Popen(("sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " killall arecord").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Kill the previous arecord instance (if one exists)
            command = "sleep " + str(float(config["dashcam"]["capture"]["audio"]["start_delay"])) + "; " + audio_record_command + " \"" + str(audio_filepath) + "\""
            if (config["dashcam"]["capture"]["audio"]["display_output"] == True):
                print("Executing:", audio_record_command)
                audio_recorders[segment_base_names[-1]] = subprocess.Popen(command, shell=True) # Start the next segment's audio recorder.
            else:
                audio_recorders[segment_base_names[-1]] = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
            del command
        process_timing("end", "Dashcam/Audio Processing")





    while global_variables.predator_running and parked == False: # Only run while the dashcam recording flag is set to 'True' and Predator is not parked. While this flag changes to 'False' this recording process should exit.
        heartbeat() # Issue a status heartbeat.

        # =======================================
        # ===== Start of segment management =====
        # =======================================
        if (utils.get_time() > first_segment_start_time + (segment_number+1)*config["dashcam"]["saving"]["segment_length"]): # Check to see if a new segment needs to be created.
            # End the current segment:
            output = None # Release the output writer.
            if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
                process_timing("start", "Dashcam/Audio Processing")
                if (segment_base_names[-1] in audio_recorders and audio_recorders[segment_base_names[-1]].poll() is None): # Check to see if there is an active audio recorder.
                    audio_recorders[segment_base_names[-1]].terminate() # Kill the previous segment's audio recorder.
                process_timing("end", "Dashcam/Audio Processing")

            # Merge the video/audio segment that was just completed:
            process_timing("start", "Dashcam/File Merging")
            if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if Predator is configured to merge audio and video files.
                if (os.path.exists(os.path.join(directory, segment_base_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"]))) == True): # Check to make sure the audio file exists before attemping to merge.
                    merge_audio_video(
                        os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["saving"]["file"]["extension"]), # video file path
                        os.path.join(directory, segment_base_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"])), # audio file path
                        os.path.join(directory, segment_names[-1] + ".mkv"), # output file path
                        float(config["dashcam"]["capture"]["audio"]["start_delay"]) # audio offset
                    )
                else: # The audio file does not exist.
                    display_message("The audio file was missing during audio/video merging.", 2)
            process_timing("end", "Dashcam/File Merging")

            # Handle segment locking:
            if (os.path.exists(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"])) == True): # Check to see if the trigger file exists.
                # == Save the most recent segment: ==
                if (os.path.exists(os.path.join(directory, segment_names[-1] + ".mkv"))): # Check to see if the merge file exists.
                    threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-1] + ".mkv")], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam segment.
                else: # Otherwise, merging is disabled, or the merge process failed.
                    threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["saving"]["file"]["extension"])], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam video segment.
                    if (config["dashcam"]["capture"]["audio"]["enabled"] == True):
                        threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["capture"]["audio"]["extension"])], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam audio segment.
                # == Save the segment before the most recent (if applicable): ==
                if (len(segment_names) > 1): # Check to see if there is a segment before the current.
                    with open(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"])) as file:
                        last_trigger_timestamp = utils.to_int(file.read())
                    if (last_trigger_timestamp - (first_segment_start_time + (segment_number * config["dashcam"]["saving"]["segment_length"])) <= 15): # Check to see if the save was initiated within the first 15 seconds of the segment.
                        if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True):
                            threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-2] + ".mkv")], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam segment.
                        else:
                            threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-2] + "." + config["dashcam"]["saving"]["file"]["extension"])], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam segment.
                            if (config["dashcam"]["capture"]["audio"]["enabled"] == True):
                                threading.Thread(target=lock_dashcam_segment, args=[os.path.join(directory, segment_names[-2] + "." + config["dashcam"]["capture"]["audio"]["extension"])], name="DashcamSegmentSave").start() # Create the thread to save this dash-cam segment.


            # Calculate the frame-rate of the last segment:
            calculated_framerate[device] = frames_since_last_segment/(time.time()-segment_started_time) # Calculate the frame-rate of the previous segment.
            if (calculated_framerate[device] > float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"])): # Check to see if the calculated frame-rate exceeds the maximum allowed frame-rate.
                calculated_framerate[device] = float(config["dashcam"]["capture"]["video"]["devices"][device]["framerate"]["max"]) # Set the frame-rate to the maximum allowed frame-rate.


            delete_old_segments() # Handle the erasing of any old dash-cam segments that need to be deleted.
            update_status_lighting("normal") # Return the status lighting to normal.


            # Initialize the next segment name:
            while (utils.get_time() > first_segment_start_time + (segment_number+1)*config["dashcam"]["saving"]["segment_length"]): # Run until the segment number is correct. This prevents a bunch of empty video files from being created when the system time suddenly jumps into the future.
                frames_since_last_segment = 0 # Reset the global "frames_since_last_segment" variable for this device.
                segment_started_time = time.time() # This value holds the exact time the segment started for sake of frame-rate calculations.
                segment_number += 1
            segment_base_names.append(datetime.datetime.fromtimestamp(first_segment_start_time + (segment_number*config["dashcam"]["saving"]["segment_length"])).strftime('%Y-%m-%d %H%M%S') + " Predator")
            segment_names.append(datetime.datetime.fromtimestamp(first_segment_start_time + (segment_number*config["dashcam"]["saving"]["segment_length"])).strftime('%Y-%m-%d %H%M%S') + " Predator " + str(device) + " N")

            # Initialize the output for the next segment:
            output_codec = list(config["dashcam"]["saving"]["file"]["codec"])
            output = cv2.VideoWriter(os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["saving"]["file"]["extension"]), cv2.VideoWriter_fourcc(output_codec[0], output_codec[1], output_codec[2], output_codec[3]), calculated_framerate[device], (config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"], config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"])) # Initialize the first video output.

            # Handle audio recording for the next segment:
            if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
                process_timing("start", "Dashcam/Audio Processing")
                audio_filepath = os.path.join(directory, segment_base_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"]))
                if (segment_base_names[-1] not in audio_recorders or audio_recorders[segment_base_names[-1]].poll() is not None): # Check to see if the audio recorder hasn't yet been started by another thread.
                    subprocess.Popen(("sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " killall arecord").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Kill the previous arecord instance (if one exists)
                    command = "sleep " + str(float(config["dashcam"]["capture"]["audio"]["start_delay"])) + "; " + audio_record_command + " \"" + str(audio_filepath) + "\""
                    if (config["dashcam"]["capture"]["audio"]["display_output"] == True):
                        print("Executing:", audio_record_command)
                        audio_recorders[segment_base_names[-1]] = subprocess.Popen(command, shell=True) # Start the next segment's audio recorder.
                    else:
                        audio_recorders[segment_base_names[-1]] = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Start the next segment's audio recorder.
                    del command
                process_timing("end", "Dashcam/Audio Processing")
        # =====================================
        # ===== End of segment management =====
        # =====================================



        # ==========================================================
        # Manage the video capture frame-rate statistics and alerts:
        process_timing("start", "Dashcam/Calculations")
        if (time.time() - shortterm_framerate[device]["start"] > float(config["developer"]["dashcam_shortterm_framerate_interval"])):
            shortterm_framerate[device]["framerate"] = shortterm_framerate[device]["frames"] / (time.time() - shortterm_framerate[device]["start"])
            shortterm_framerate[device]["start"] = time.time()
            shortterm_framerate[device]["frames"] = 0
        shortterm_framerate[device]["frames"] += 1

        time_since_last_frame = time.time()-last_frame_captured # Calculate the time (in seconds) since the last frame was captured.
        last_frame_captured = time.time() # Update the time that the last frame was captured.
        instant_framerate[device] = 1/time_since_last_frame
        if (time_since_last_frame > expected_time_since_last_frame_slowest): # Check see if the current frame-rate is below the minimum expected frame-rate.
            if (frames_since_last_segment > 1): # Check to make sure we aren't at the very beginning of recording, where frame-rate might be inconsistent.
                if (time.time() - last_alert_minimum_framerate_time > 1): # Check to see if at least 1 second has passed since the last minimum frame-rate alert.
                    display_message("The framerate on '" + device + "' (" + str(round((1/time_since_last_frame)*100)/100) + "fps) has fallen below the minimum frame-rate.", 2)
            last_alert_minimum_framerate_time = time.time() # Record the current time as the time that the last minimum frame-rate alert was shown.
        elif (time_since_last_frame < expected_time_since_last_frame_fastest): # Check see if the current frame-rate is above the maximum expected frame-rate.
            time.sleep(expected_time_since_last_frame_fastest - time_since_last_frame) # Wait to force the frame-rate to stay below the maximum limit.
        process_timing("end", "Dashcam/Calculations")



        # =======================================
        # Read the frame from the capture device:
        process_timing("start", "Dashcam/Video Capture")
        ret, frame = capture.read() # Capture a frame.
        frames_since_last_segment += 1 # Increment the number of frames captured since the last segment.
        process_timing("end", "Dashcam/Video Capture")

        if not ret: # Check to see if the frame failed to be read.
            display_message("Failed to receive video frame from the '" + device  + "' device. It is possible this device has been disconnected.", 2)
            for i in range(1, 12): # Attempt to re-open the capture device several times.
                time.sleep(5*i) # Wait before re-attempting to open the capture device. The length of time between attempts increases with each attempt.
                display_message("Attempting to re-open capture on '" + device  + "' device.", 1)
                process_timing("start", "Dashcam/Capture Management")
                capture = cv2.VideoCapture(device_index) # Open the video stream.
                codec = list(config["dashcam"]["capture"]["video"]["devices"][device]["codec"])
                capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(codec[0], codec[1], codec[2], codec[3])) # Set the video codec.
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["width"]) # Set the video stream width.
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config["dashcam"]["capture"]["video"]["devices"][device]["resolution"]["height"]) # Set the video stream height.
                process_timing("end", "Dashcam/Capture Management")
                process_timing("start", "Dashcam/Video Capture")
                ret, frame = capture.read() # Capture a frame.
                process_timing("end", "Dashcam/Video Capture")
                if ret: # Check to see if the frame was successfully read.
                    display_message("Successfully re-opened capture on the '" + device  + "' capture device.", 1)
                    break # Exit the loop, now that the capture device has been re-established.
            if not ret: # Check to see if the frame failed to be read.
                display_message("Video recording on the '" + device  + "' device could not be restarted.", 3)
                break # If the capture device can't be re-opened, then stop recording on this device.


        # ======================================
        # Apply image manipulation to the frame:
        if (config["dashcam"]["capture"]["video"]["devices"][device]["flip"]): # Check to see if Predator is configured to flip this capture device's output.
            process_timing("start", "Dashcam/Image Manipulation")
            frame = cv2.rotate(frame, cv2.ROTATE_180) # Flip the frame by 180 degrees.
            process_timing("end", "Dashcam/Image Manipulation")

        process_timing("start", "Dashcam/Capture Management")
        current_frame_data[device] = frame # Set the current frame for this device as the frame after rotation has been applied, but before overlay stamps.
        process_timing("end", "Dashcam/Capture Management")

        frame = apply_dashcam_stamps(frame, device)


        # ===================================
        # Write the frame to the output file:
        output.write(frame)


        # ===============
        # Send telemetry:
        telemetry_data = {}
        telemetry_data["image"] = dict(current_frame_data)
        current_location = utils.get_gps_location_lazy() # Get the most recent location.
        telemetry_data["location"] = {
            "time": utils.get_time(),
            "lat": current_location[0],
            "lon": current_location[1],
            "alt": current_location[3],
            "spd": current_location[2],
            "head": current_location[4]
        }
        #utils.send_telemetry(telemetry_data)
        telemetry_thread = threading.Thread(target=utils.send_telemetry, args=[dict(telemetry_data)]) # Create a separate thread to process and upload telemetry.
        telemetry_thread.start()


        # ===================
        # Handle diagnostics:
        update_state("dashcam/normal", instant_framerate)
        if (config["developer"]["print_timings"] == True):
            utils.clear(True)
            print(json.dumps(process_timing("dump", ""), indent=4))



    # ===============================================
    # The main recording loop has exited, so wrap up:
    if (config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if audio recording is enabled in the configuration.
        process_timing("start", "Dashcam/Audio Processing")
        if (segment_base_names[-1] in audio_recorders and audio_recorders[segment_base_names[-1]].poll() is None): # Check to see if there is an active audio recorder.
            audio_recorders[segment_base_names[-1]].terminate() # Kill the previous segment's audio recorder.
        time.sleep(config["dashcam"]["capture"]["audio"]["start_delay"]) # Wait briefly for the audio recorder to terminate.
        subprocess.Popen(("sudo -u " + str(config["dashcam"]["capture"]["audio"]["record_as_user"]) + " killall arecord").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) # Force kill all audio recording processes.
        process_timing("end", "Dashcam/Audio Processing")
    output = None # Release the output file.
    capture.release() # Release the capture device.
    first_segment_start_time = 0 # Reset the segment start time.

    process_timing("start", "Dashcam/File Merging")
    if (config["dashcam"]["capture"]["audio"]["merge"] == True and config["dashcam"]["capture"]["audio"]["enabled"] == True): # Check to see if Predator is configured to merge audio and video files.
        if (os.path.exists(os.path.join(directory, segment_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"]))) == True): # Check to make sure the audio file exists before attemping to merge.
            merge_audio_video(
                os.path.join(directory, segment_names[-1] + "." + config["dashcam"]["saving"]["file"]["extension"]), # video file path
                os.path.join(directory, segment_base_names[-1] + "." + str(config["dashcam"]["capture"]["audio"]["extension"])), # audio file path
                os.path.join(directory, segment_names[-1] + ".mkv"), # output file path
                float(config["dashcam"]["capture"]["audio"]["start_delay"]) # audio offset
            )
        else: # The audio file does not exist.
            display_message("The audio file was missing during audio/video merging.", 2)
    process_timing("end", "Dashcam/File Merging")
    # ===============================================






# This function is responsible for starting the dashcam recording process. It calls the relevant recording functions as subprocesses.
def dashcam():
    global parked

    # =================================================================================
    # Check to see if there is at least one capture device enabled (as a sanity check):
    at_least_one_enabled_device = False
    for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True): # Check to see if this device is enabled.
            at_least_one_enabled_device = True
    if (at_least_one_enabled_device == False):
        display_message("There are no dashcam capture devices enabled. Dashcam recording will not start.", 3)
    del at_least_one_enabled_device
    # =================================================================================



    update_status_lighting("normal") # Initialize the status lighting to normal.
    os.system("rm -f '" + os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"]) + "'") # Remove the dashcam lock trigger file, in case it exists at start-up.

    # =================================
    # Initialize the physical controls:
    button_watch_threads = {} # This will hold the processes watching each GPIO that will trigger a dashcam save.

    for pin in config["dashcam"]["physical_controls"]["dashcam_saving"]: # Iterate through each dashcam save GPIO trigger.
        hold_time = float(config["dashcam"]["physical_controls"]["dashcam_saving"][pin]["hold_time"])
        if (hold_time < 0):
            utils.display_message("The 'hold time' for pin '" + str(pin) + "' is negative. This will likely cause unexpected behavior.", 2)
        button_watch_threads[int(pin)] = threading.Thread(target=watch_button, args=[int(pin), hold_time, create_trigger_file], name="ButtonWatch" + str(pin)) # Create a thread to monitor this pin.
        button_watch_threads[int(pin)].start() # Start the thread to monitor the pin.

    for pin in config["dashcam"]["physical_controls"]["stop_predator"]: # Iterate through each Predator termination GPIO trigger.
        hold_time = float(config["dashcam"]["physical_controls"]["stop_predator"][pin]["hold_time"])
        if (hold_time < 0):
            utils.display_message("The 'hold time' for pin '" + str(pin) + "' is negative. This will likely cause unexpected behavior.", 2)
        button_watch_threads[int(pin)] = threading.Thread(target=watch_button, args=[int(pin), hold_time, utils.stop_predator], name="ButtonWatch" + str(pin)) # Create a thread to monitor this pin.
        button_watch_threads[int(pin)].start() # Start the thread to monitor the pin.
    # =================================



    dashcam_normal_processes = [] # Create a placeholder to store the normal dashcam recording processes.
    dashcam_parked_processes = [] # Create a placeholder to store the parked dashcam recording processes.
    dashcam_alpr_process = {} # Create a placeholder to store the dashcam ALPR processes.
    dashcam_objectrecognition_process = {} # Create a placeholder to store the dashcam object recognition processes for standard recording.

    utils.play_sound("recording_started")
    if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["start_up"]["enabled"] == True): # Check to see if Predator is configured to send start-up notifications over Reticulum.
        for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
            reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has been started", destination) # Send a Reticulum LXMF message to this destination.
    
    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
    for device in config["dashcam"]["capture"]["video"]["devices"]: # Iterate through each device in the configuration.
        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
            dashcam_normal_processes.append(threading.Thread(target=dashcam_normal, args=[device], name="DashcamCapture" + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"])))
            dashcam_normal_processes[iteration_counter].start()
            if (config["dashcam"]["alpr"]["enabled"] == True): # Check to see if background ALPR processing is enabled.
                if (device in config["dashcam"]["alpr"]["devices"]): # Check to see if this device is in the list of devices to run ALPR on.
                    dashcam_alpr_process[iteration_counter] = threading.Thread(target=background_alpr, args=[device], name="DashcamALPR" + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"]))
                    dashcam_alpr_process[iteration_counter].start()

            iteration_counter += 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.
            print("Started dashcam recording on " + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"])) # Inform the user that recording was initiation for this camera device.

    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
    for device in config["dashcam"]["object_recognition"]: # Iterate over each device configured to run object recognition during recording.
        if (config["dashcam"]["object_recognition"][device]["enabled"] == True): # Check to make sure object recognition is enabled for this device.
            dashcam_objectrecognition_process[iteration_counter] = threading.Thread(target=background_object_recognition, args=[device], name="DashcamObjectRecognition" + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"]))
            dashcam_objectrecognition_process[iteration_counter].start()
            iteration_counter += 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.



    last_moved_time = utils.get_time() # This value holds the Unix timestamp of the last time the vehicle exceeded the parking speed threshold. Here it is initialized to the current time.
    while global_variables.predator_running: # Run until Predator is terminated.
        if (config["dashcam"]["parked"]["enabled"] == True): # Check to see if parking mode is enabled before checking for movement.
            if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled.
                current_location = get_gps_location() # Get the current GPS location.
            else:
                current_location = [0, 0, 0, 0, 0, 0]
            if (current_location[2] > config["dashcam"]["parked"]["conditions"]["speed"]): # Check to see if the current speed exceeds the parked speed threshold.
                last_moved_time = utils.get_time()

            if (utils.get_time() - last_moved_time > config["dashcam"]["parked"]["conditions"]["time"]): # Check to see if the amount of time the vehicle has been stopped exceeds the time threshold to enable parked mode.
                if (parked == False): # Check to see if Predator wasn't already in parked mode.
                    parked = True # Enter parked mode.
                    display_message("Entered parked mode.", 1)
                    if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["parking_mode_enabled"]["enabled"] == True): # Check to see if Predator is configured to parking mode activation notifications over Reticulum.
                        for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
                            reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has entered parked mode.", destination) # Send a Reticulum LXMF message to this destination.
                    time.sleep(2) # Wait briefly to allow the other threads to finish.
                    # Start parked dormant dash-cam monitoring:
                    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
                    for device in config["dashcam"]["capture"]["video"]["devices"]: # Run through each camera device specified in the configuration, and launch an OpenCV recording instance for it.
                        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
                            dashcam_parked_processes.append(threading.Thread(target=dashcam_parked_dormant, args=[device], name="ParkedDormant" + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"])))
                            dashcam_parked_processes[iteration_counter].start()
                            iteration_counter += 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.

            else: # The vehicle has not been stopped for the minimum time to activate parking mode.
                if (parked == True): # Check to see if Predator wasn't already out of parked mode.
                    parked = False # Exit parked mode.
                    display_message("Exited parked mode.", 1)
                    if (config["dashcam"]["notifications"]["reticulum"]["enabled"] == True and config["dashcam"]["notifications"]["reticulum"]["events"]["parking_mode_disabled"]["enabled"] == True): # Check to see if Predator is configured to parking mode deactivation notifications over Reticulum.
                        for destination in config["dashcam"]["notifications"]["reticulum"]["destinations"]: # Iterate over each configured destination.
                            reticulum.lxmf_send_message(str(config["dashcam"]["notifications"]["reticulum"]["instance_name"]) + " has exited parked mode.", destination) # Send a Reticulum LXMF message to this destination.
                    time.sleep(2) # Wait briefly to allow the other threads to finish.
                    # Restart normal dash-cam recording:
                    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
                    for device in config["dashcam"]["capture"]["video"]["devices"]: # Run through each camera device specified in the configuration, and launch an OpenCV recording instance for it.
                        if (config["dashcam"]["capture"]["video"]["devices"][device]["enabled"] == True):
                            dashcam_normal_processes.append(threading.Thread(target=dashcam_normal, args=[device], name="DashcamCapture" + str(config["dashcam"]["capture"]["video"]["devices"][device]["index"])))
                            dashcam_normal_processes[iteration_counter].start()
                            iteration_counter += 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.
        time.sleep(1)
    display_message("Dashcam recording exited.", 1)
