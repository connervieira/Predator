# Predator

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Predator...")


import os # Required to interact with certain operating system functions
import json # Required to process JSON data


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database from config.json



import time # Required to add delays and handle dates/times
import subprocess # Required for starting some shell commands
import sys
if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    if (config["realtime"]["status_lighting_enabled"] == True or config["realtime"]["push_notifications_enabled"] == True or config["realtime"]["webhook"] != ""):
        import urllib.request # Required to make network requests
        import validators # Required to validate URLs
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
import fnmatch # Required to use wildcards to check strings
import psutil # Required to get disk usage information
import lzma # Required to open and manipulate ExCam database.
import math # Required to run more complex math functions.
import random # Required to generate random numbers.



import utils # Import the utils.py scripts.
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
validate_plate = utils.validate_plate # Load the plate validation function from the utils script.
download_plate_database = utils.download_plate_database # Load the plate database downloading function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.


import ignore # Import the library to handle license plates in the ignore list.
ignore_list = ignore.fetch_ignore_list() # Fetch the ignore lists.




if (config["developer"]["offline"] == True): # If offline mode is enabled, then disable all network based features.
    config["realtime"]["webhook"] = ""
    config["realtime"]["push_notifications_enabled"] = False
    config["realtime"]["gotify_server"] = "" # This is redundant, since 'push_notifications_enabled' is disabled, but it serves as a backup.
    config["realtime"]["status_lighting_enabled"] = False
    config["realtime"]["status_lighting_base_url"] = "" # This is redundant, since 'status_lighting_enabled' is disabled, but it serves as a backup.
    config["developer"]["remote_sources"] = []



if (config["general"]["disable_object_recognition"] == False): # Check to see whether or not object recognition (Tensorflow/OpenCV) has been globally disabled.
    try: # "Try" to import Tensorflow and OpenCV; Don't quit the entire program if an error is encountered.
        import silence_tensorflow.auto # Silences tensorflow warnings
        import cv2 # Required for object recognition (not license plate recognition)
        import cvlib as cv # Required for object recognition (not license plate recognition)
        from cvlib.object_detection import draw_bbox # Required for object recognition (not license plate recognition)
    except Exception:
        print (Exception) # Display the exception that was encountered
        countdown(5) # Start a countdown to allow the user to see the error, then continue loading.


import lighting # Import the lighting.py script.
update_status_lighting = lighting.update_status_lighting # Load the status lighting update function from the lighting script.




# Load the configuration values from the config file.

# ----- General configuration -----
crop_script_path = predator_root_directory + "/crop_image" # Path to the cropping script in the Predator directory.
ascii_art_header = config["general"]["ascii_art_header"] # This setting determines whether or not the large ASCII art Predator title will show on start-up. When set to False, a small, normal text title will appear instead. This is useful when running Predator on a device with a small display to avoid weird formatting.
custom_startup_message = config["general"]["custom_startup_message"] # This setting determines whether or not the large ASCII art Predator title will show on start-up. When set to False, a small, normal text title will appear instead. This is useful when running Predator on a device with a small display to avoid weird formatting.
auto_start_mode = config["general"]["auto_start_mode"] # This variable determines whether or not automatically start in a particular mode. When empty, the user will be prompted whether to start in pre-recorded mode or in real-time mode. When set to "0", Predator will automatically start into management mode when launched. When set to "1", Predator will automatically select and start pre-recorded mode when launched. When set to "2", Predator will automatically select and start real-time mode when launched. When set to "3", Predator will start into dashcam-mode when launched.
default_root = config["general"]["default_root"] # If this variable isn't empty, the "root directory" prompt will be skipped when starting Predator. This variable will be used as the root directory. This variable only affects real-time mode and dash-cam mode.
silence_file_saving = config["general"]["silence_file_saving"] # This setting determines whether log messages about file saving will be printed to console. Set this to True to silence the messages indicating whether or not files were successfully saved or updated.
disable_object_recognition = config["general"]["disable_object_recognition"] # This setting is responsible for globally disabling object recognition (TensorFlow and OpenCV) in the event that it isn't supported on a particular platform. When set to true, any features involving object recognition, other than license plate recognition, will be disabled.
gps_enabled = config["general"]["gps_enabled"] # This setting determines whether or not Predator's GPS features are enabled.
speed_display_unit = config["general"]["speed_display_unit"] # This setting determines the units Predator will use to display the current speed.
management_mode_enabled = config["general"]["modes_enabled"]["management"] # This setting is used to prevent management mode from being loaded from the user menu or command line arguments of Predator.
prerecorded_mode_enabled = config["general"]["modes_enabled"]["prerecorded"] # This setting is used to prevent prerecorded mode from being loaded from the user menu or command line arguments of Predator.
realtime_mode_enabled = config["general"]["modes_enabled"]["realtime"] # This setting is used to prevent realtime mode from being loaded from the user menu or command line arguments of Predator.
dashcam_mode_enabled = config["general"]["modes_enabled"]["dashcam"] # This setting is used to prevent dashcam mode from being loaded from the user menu or command line arguments of Predator.
alert_database_license_plates = config["general"]["alert_databases"]["license_plates"] # This configuration value defines the file that Predator will load the alert list for license plates from.


# ----- Pre-recorded mode configuration -----
left_margin = config["prerecorded"]["left_margin"] # How many pixels will be cropped on the left side of the frame in pre-recorded mode.
right_margin = config["prerecorded"]["right_margin"] # How many pixels will be cropped on the right side of the frame in pre-recorded mode.
top_margin = config["prerecorded"]["top_margin"] # How many pixels will be cropped on the top of the frame in pre-recorded mode.
bottom_margin = config["prerecorded"]["bottom_margin"] # How many pixels will be cropped on the bottom of the frame in pre-recorded mode.



# ----- Real-time mode configuration -----
realtime_alpr_enabled = config["realtime"]["realtime_alpr_enabled"] # This setting determines whether or not Predator will run license plate recognition while operating in real-time mode.
realtime_output_level = int(config["realtime"]["realtime_output_level"]) # This setting determines how much information Predator shows the user while operating in real-time mode.
clear_between_rounds = config["realtime"]["clear_between_rounds"] # This setting determines whether or not Predator will clear the output screen between analysis rounds in real-time mode.
delay_between_rounds = config["realtime"]["delay_between_rounds"] # This setting defines how long Predator will wait in between analysis rounds in real-time mode.
print_invalid_plates = config["realtime"]["print_invalid_plates"] # In real-time mode, print all plates that get invalided by the formatting rules in red. When this is set to false, only valid plates are displayed.
print_detected_plate_count = config["realtime"]["print_detected_plate_count"] # This setting determines whether or not Predator will print how many license plates it detects in each frame while operating in real-time mode.
realtime_guesses = config["realtime"]["realtime_guesses"] # This setting determines how many guesses Predator will make per plate in real-time mode. The higher this number, the less accurate guesses will be, but the more likely it will be that a plate matching the formatting guidelines is found.
manual_trigger = config["realtime"]["manual_trigger"] # This setting determines whether or not Predator will wait to be manually triggered before taking an image.
alpr_location_tagging = config["realtime"]["alpr_location_tagging"] # This setting determines whether or not detected license plates will be tagged with the current GPS location.
alerts_ignore_validation = config["realtime"]["alerts_ignore_validation"] # This setting determines whether alerts will respect or ignore the license plate validation formatting template.
camera_resolution = config["realtime"]["camera_resolution"] # This is the resolution you want to use when taking images using the connected camera. Under normal circumstances, this should be the maximum resoultion supported by your camera.
real_time_cropping_enabled = config["realtime"]["real_time_cropping_enabled"] # This value determines whether or not each frame captured in real-time mode will be cropped.
real_time_left_margin = config["realtime"]["real_time_left_margin"] # How many pixels will be cropped from the left side of the frame in real-time mode.
real_time_right_margin = config["realtime"]["real_time_right_margin"] # How many pixels will be cropped from the right side of the frame in real-time mode.
real_time_top_margin = config["realtime"]["real_time_top_margin"] # How many pixels will be cropped from the bottom side of the frame in real-time mode.
real_time_bottom_margin = config["realtime"]["real_time_bottom_margin"] # How many pixels will be cropped from the top side of the frame in real-time mode.
real_time_image_rotation = config["realtime"]["real_time_image_rotation"] # How many degrees clockwise the image will be rotated in real-time mode.
fswebcam_device = config["realtime"]["fswebcam_device"] # This setting determines the video device that 'fswebcam' will use to take images in real-time mode.
fswebcam_flags = config["realtime"]["fswebcam_flags"] # These are command flags that will be added to the end of the FSWebcam command. You can use these to customize how FSWebcam takes images in real-time mode based on your camera set up.
audio_alerts = config["realtime"]["audio_alerts"] # This setting determines whether or not Predator will make use of sounds to inform the user of events.
webhook = config["realtime"]["webhook"] # This setting can be used to define a webhook that Predator will send a request to when it detects a license plate in real-time mode. See CONFIGURATION.md to learn more about how to use flags in this setting.
shape_alerts = config["realtime"]["shape_alerts"] # This setting determines whether or not prominent text-based shapes will be displayed for various actions. This is useful in vehicle installations where you may want to see whether or not Predator detected a plate at a glance.
save_real_time_object_recognition = config["realtime"]["save_real_time_object_recognition"] # This setting determines whether or not Predator will save the objects detected in real-time mode to a file. When this is turned off, object recognition data will only be printed to the console.
speed_display_enabled = config["realtime"]["speed_display_enabled"] # This setting determines whether or not Predator will display the current GPS speed each processing cycle in real-time mode.

# Default settings
default_save_license_plates_preference = config["realtime"]["default_save_license_plates_preference"] # If this variable isn't empty, the "save license plates" prompt will be skipped when starting in real-time mode. If this variable is set to "y", license plates will be saved.
default_save_images_preference = config["realtime"]["default_save_images_preference"] # If this variable isn't empty, the "save images" prompt will be skipped when starting in real-time mode. If this variable is set to "y", all images will be saved.
default_license_plate_format = config["realtime"]["default_license_plate_format"] # If this variable isn't empty, the "license plate format" prompt will be skipped when starting in real-time mode. This variable will be used as the license plate format.
default_realtime_object_recognition = config["realtime"]["default_realtime_object_recognition"] # If this variable isn't empty, then the "real-time object detection" prompt will be skipped when starting in real-time mode. If this variable is set to "y", object recognition will be turned on.

# Push notification settings
push_notifications_enabled = config["realtime"]["push_notifications_enabled"] # This setting determines whether or not Predator will attempt to use Gotify to broadcast notifications for certain events.
gotify_server = config["realtime"]["gotify_server"] # This setting specifies the server address of the desired Gotify server, and should include the protocol (Ex: http://) and port (Ex: 80).
gotify_application_token = config["realtime"]["gotify_application_token"] # This setting specifies the Gotify application token that Predator will use to broadcast notifications.

# Status lighting system settings
status_lighting_enabled = config["realtime"]["status_lighting_enabled"]
status_lighting_base_url = config["realtime"]["status_lighting_base_url"]
status_lighting_values = config["realtime"]["status_lighting_values"]

# Audio alert settings
alert_sounds_startup = config["realtime"]["startup_sound"]["path"]
alert_sounds_startup_repeat = config["realtime"]["startup_sound"]["repeat"]
alert_sounds_startup_delay = config["realtime"]["startup_sound"]["delay"]
alert_sounds_notice = config["realtime"]["notification_sound"]["path"]
alert_sounds_notice_repeat = config["realtime"]["notification_sound"]["repeat"]
alert_sounds_notice_delay = config["realtime"]["notification_sound"]["delay"]
alert_sounds_alert = config["realtime"]["alert_sound"]["path"]
alert_sounds_alert_repeat = config["realtime"]["alert_sound"]["repeat"]
alert_sounds_alert_delay = config["realtime"]["alert_sound"]["delay"]




# ----- Dash-cam mode configuration -----
dashcam_resolution = config["dashcam"]["dashcam_resolution"] # This setting determines what resolution Predator will attmpt to record at. Be sure that your camera is capable of recording at resolution specified here.
dashcam_frame_rate = config["dashcam"]["dashcam_frame_rate"] # This setting determines what frame rate Predator will attmpt to record at. Be sure that your camera is capable of recording at the frame rate specified here.
dashcam_device = config["dashcam"]["dashcam_device"] # This setting defines what camera device(s) Predator will attempt to use when recording video in dash-cam mode.
dashcam_background_mode_realtime = config["dashcam"]["dashcam_background_mode_realtime"] # This setting determines whether dash-cam recording will automatically start in background mode when user runs real-time mode. It should be noted that running dash-cam recording and real-time mode simutaneously is only possible with two cameras connected, since the same camera device can't be used for both processes.








# Display the start-up intro header.
clear()
if (ascii_art_header == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
    print(style.red + style.bold)
    print(" /$$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$ ")
    print("| $$__  $$| $$__  $$| $$_____/| $$__  $$ /$$__  $$|__  $$__//$$__  $$| $$__  $$")
    print("| $$  \ $$| $$  \ $$| $$      | $$  \ $$| $$  \ $$   | $$  | $$  \ $$| $$  \ $$")
    print("| $$$$$$$/| $$$$$$$/| $$$$$   | $$  | $$| $$$$$$$$   | $$  | $$  | $$| $$$$$$$/")
    print("| $$____/ | $$__  $$| $$__/   | $$  | $$| $$__  $$   | $$  | $$  | $$| $$__  $$")
    print("| $$      | $$  \ $$| $$      | $$  | $$| $$  | $$   | $$  | $$  | $$| $$  \ $$")
    print("| $$      | $$  | $$| $$$$$$$$| $$$$$$$/| $$  | $$   | $$  |  $$$$$$/| $$  | $$")
    print("|__/      |__/  |__/|________/|_______/ |__/  |__/   |__/   \______/ |__/  |__/" + style.end + style.bold)
    print("")
    print("                            COMPUTER VISION SYSTEM")
    if (custom_startup_message != ""): # Only display the line for the custom message if the user has defined one.
        print("")
        print(custom_startup_message) # Show the user's custom defined start-up message.
    print(style.end)
else: # If the user his disabled the large ASCII art header, then show a simple title header with minimal styling.
    print(style.red + style.bold + "PREDATOR" + style.end)
    print(style.bold + "Computer Vision System" + style.end + "\n")
    if (custom_startup_message != ""): # Only display the line for the custom message if the user has defined one.
        print(custom_startup_message) # Show the user's custom defined start-up message.

if (audio_alerts == True and int(alert_sounds_startup_repeat) > 0): # Check to see if the user has audio alerts enabled.
    for i in range(0, int(alert_sounds_startup_repeat)): # Repeat the sound several times, if the configuration says to.
        os.system("mpg321 " + alert_sounds_startup + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
        time.sleep(float(alert_sounds_startup_delay)) # Wait before playing the sound again.

if (push_notifications_enabled == True): # Check to see if the user has push notifications enabled.
    os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=Predator has been started.' > /dev/null 2>&1 &") # Send a push notification via Gotify indicating that Predator has started.



# Run some basic error checks to see if any of the data supplied in the configuration seems wrong.
if (os.path.exists(crop_script_path) == False): # Check to see that the cropping script exists at the path specified by the user in the configuration.
    print(style.yellow + "Warning: The 'crop_script_path' defined in the configuration section doesn't point to a valid file. Image cropping will be broken. Please make sure the 'crop_script_path' points to a valid file." + style.end)

if (int(left_margin) < 0 or int(right_margin) < 0 or int(bottom_margin) < 0 or int(top_margin) < 0): # Check to make sure that all of the pre-recorded mode cropping margins are positive numbers.
    print(style.yellow + "Warning: One or more of the cropping margins for pre-recorded mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping margins have all been set to 0." + style.end)
    left_margin = "0"
    right_margin = "0"
    bottom_margin = "0"
    top_margin = "0"

if (int(real_time_left_margin) < 0 or int(real_time_right_margin) < 0 or int(real_time_bottom_margin) < 0 or int(real_time_top_margin) < 0): # Check to make sure that all of the real-time mode cropping margins are positive numbers.
    print(style.yellow + "Warning: One or more of the cropping margins for real-time mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping margins have all been set to 0." + style.end)
    real_time_left_margin = "0"
    real_time_right_margin = "0"
    real_time_bottom_margin = "0"
    real_time_top_margin = "0"

if (re.fullmatch("(\d\d\dx\d\d\d)", dashcam_resolution) == None and re.fullmatch("(\d\d\d\dx\d\d\d)", dashcam_resolution) == None and re.fullmatch("(\d\d\d\dx\d\d\d\d)", dashcam_resolution) == None): # Verify that the dashcam_resolution setting matches the format 000x000, 0000x000, or 0000x0000.
    print(style.yellow + "Warning: The 'dashcam_resolution' specified in the real-time configuration section doesn't seem to align with the '0000x0000' format. It's possible there has been a typo. defaulting to '1280x720'" + style.end)
    dashcam_resolution = "1280x720"

if (fswebcam_device == ""): # Check to make sure that a camera device has been specified in the real-time configuration section.
    print(style.yellow + "Warning: The 'fswebcam_device' specified in the real-time configuration section is blank. It's possible there has been a typo. Defaulting to /dev/video0" + style.end)
    fswebcam_device = "/dev/video0"


shared_realtime_dashcam_device = False
for device in dashcam_device:
    if (dashcam_background_mode_realtime == True and dashcam_device[device] == fswebcam_device): # If Predator is configured to run background dashcam recording in real-time mode, then make sure the the dashcam camera device and real-time camera device are different.
        shared_realtime_dashcam_device = True
        dashcam_background_mode_realtime = False
if (shared_realtime_dashcam_device == True):
        print(style.yellow + "Warning: The 'dashcam_background_mode_realtime' setting is turned on, but the same recording device has been specified for 'dashcam_device' and 'fswebcam_device'. Predator can't use the same device for two different tasks. Background dash-cam recording in real-time mode has been temporarily disabled." + style.end)


if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications turned on in the configuration.
    if (gotify_server == "" or gotify_server == None): # Check to see if the gotify server has been left blank
        print(style.yellow + "Warning: The 'push_notifications_enabled' setting is turned on, but the 'gotify_server' hasn't been set. Push notifications have been disabled." + style.end)
        push_notifications_enabled = False
    if (gotify_application_token == "" or gotify_application_token == None): # Check to see if the Gotify application token has been left blank.
        print(style.yellow + "Warning: The 'push_notifications_enabled' setting is turned on, but the 'gotify_application_token' hasn't been set. Push notifications have been disabled." + style.end)
        push_notifications_enabled = False



# Figure out which mode to boot into.
print("Please select an operating mode.")
if (management_mode_enabled == True): # Only show the Management mode option if it's enabled in the Predator configuration.
    print("0. Management")
if (prerecorded_mode_enabled == True): # Only show the Pre-recorded mode option if it's enabled in the Predator configuration.
    print("1. Pre-recorded")
if (realtime_mode_enabled == True): # Only show the Real-time mode option if it's enabled in the Predator configuration.
    print("2. Real-time")
if (dashcam_mode_enabled == True): # Only show the Dash-cam mode option if it's enabled in the Predator configuration.
    print("3. Dash-cam")

# Check to see if the auto_start_mode configuration value is an expected value. If it isn't execution can continue, but the user will need to manually select what mode Predator should start in.
if (auto_start_mode != "" and auto_start_mode != "0" and auto_start_mode != "1" and auto_start_mode != "2" and auto_start_mode != "3"):
    print(style.yellow + "Warning: The 'auto_start_mode' configuration value isn't properly set. This value should be blank, '0', '1', '2', '3'. It's possible there's been a typo." + style.end)

if (len(sys.argv) > 1): # Check to see if there is at least 1 command line argument.
    if (sys.argv[1] == "0" or sys.argv[1] == "1" or sys.argv[1] == "2" or sys.argv[1] == "3"): # Check to see if a mode override was specified in the Predator command arguments.
        auto_start_mode = sys.argv[1] # Set the automatic start mode to the mode specified by the command line argument.

if (len(sys.argv) > 2): # Check to see if there are at least 2 command line arguments.
    default_root = str(sys.argv[2]) # Set the default root directory to the path specified by the command line argument.


if (auto_start_mode == "0" and management_mode_enabled == True): # Based on the configuration, Predator will automatically boot into management mode.
    print(style.bold + "Automatically starting into management mode." + style.end)
    mode_selection = "0"
elif (auto_start_mode == "1" and prerecorded_mode_enabled == True): # Based on the configuration, Predator will automatically boot into pre-recorded mode.
    print(style.bold + "Automatically starting into pre-recorded mode." + style.end)
    mode_selection = "1"
elif (auto_start_mode == "2" and realtime_mode_enabled == True): # Based on the configuration, Predator will automatically boot into real-time mode.
    print(style.bold + "Automatically starting into real-time mode." + style.end)
    mode_selection = "2"
elif (auto_start_mode == "3" and dashcam_mode_enabled == True): # Based on the configuration, Predator will automatically boot into dash-cam mode.
    print(style.bold + "Automatically starting into dash-cam mode." + style.end)
    mode_selection = "3"
else: # No 'auto start mode' has been configured, so ask the user to select manually.
    mode_selection = input("Selection: ")





# Intial setup has been completed, and Predator will now load into the specified mode.









if (mode_selection == "0" and management_mode_enabled == True): # The user has selected to boot into management mode.
    if (default_root != ""): # Check to see if the user has configured a default root directory path.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = input("Project root directory path: ")

    # Run some validation to make sure the information just entered by the user is correct.
    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        print(style.yellow + "Warning: The root project directory entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")


    while True:
        clear()
        print("Please select an option")
        print("0. Quit")
        print("1. File Management")
        print("2. Information")
        print("3. Configuration")

        selection = input("Selection: ")

        if (selection == "0"): # The user has selected to quit Predator.
            break # Break the 'while true' loop to terminate Predator.

        elif (selection == "1"): # The user has selected the "File Management" option.
            print("    Please select an option")
            print("    0. Back")
            print("    1. View")
            print("    2. Copy")
            print("    3. Delete")
            selection = input("    Selection: ")

            if (selection == "0"): # The user has selected to return back to the previous menu.
                pass # Do nothing, and just finish this loop.
            elif (selection == "1"): # The user has selected the "view files" option.
                os.system("ls -1 " + root) # Run the 'ls' command in the project root directory.
            elif (selection == "2"): # The user has selected the "copy files" option.

                # Reset all of the file selections to un-selected.
                copy_management_configuration = False
                copy_prerecorded_processed_frames = False
                copy_prerecorded_gpx_files = False
                copy_prerecorded_license_plate_analysis_data = False
                copy_prerecorded_object_recognition_data = False
                copy_prerecorded_license_plate_location_data = False
                copy_realtime_images = False
                copy_realtime_object_recognition_data  = False
                copy_realtime_license_plate_recognition_data = False
                copy_dashcam_video = False

                while True: # Run the "copy files" selection menu on a loop forever until the user is finished selecting files.
                    clear() # Clear the console output before each loop.
                    print("Please select which files to copy")
                    print("0. Continue")
                    print("")
                    print("===== Management Mode =====")
                    if (copy_management_configuration == True):
                        print("M1. [X] Configuration files")
                    else:
                        print("M1. [ ] Configuration files")
                    print("")
                    print("===== Pre-recorded Mode =====")
                    if (copy_prerecorded_processed_frames == True):
                        print("P1. [X] Processed video frames")
                    else:
                        print("P1. [ ] Processed video frames")
                    if (copy_prerecorded_gpx_files == True):
                        print("P2. [X] GPX files")
                    else:
                        print("P2. [ ] GPX files")
                    if (copy_prerecorded_license_plate_analysis_data == True):
                        print("P3. [X] License plate analysis data files")
                    else:
                        print("P3. [ ] License plate analysis data files")
                    if (copy_prerecorded_object_recognition_data == True):
                        print("P4. [X] Object recognition data files")
                    else:
                        print("P4. [ ] Object recognition data files")
                    if (copy_prerecorded_license_plate_location_data == True):
                        print("P5. [X] License plate location data files")
                    else:
                        print("P5. [ ] License plate location data files")
                    print("")
                    print("===== Real-time Mode =====")
                    if (copy_realtime_images == True):
                        print("R1. [X] Captured images")
                    else:
                        print("R1. [ ] Captured images")
                    if (copy_realtime_object_recognition_data == True):
                        print("R2. [X] Object recognition data files")
                    else:
                        print("R2. [ ] Object recognition data files")
                    if (copy_realtime_license_plate_recognition_data == True):
                        print("R3. [X] License plate recognition data files")
                    else:
                        print("R3. [ ] License plate recognition data files")
                    print("")
                    print("===== Dash-cam Mode =====")
                    if (copy_dashcam_video == True):
                        print("D1. [X] Dash-cam videos")
                    else:
                        print("D1. [ ] Dash-cam videos")
                    print("")

                    selection = input("Selection: ") # Prompt the user for a selection.


                    if (selection == "0"):
                        break

                    # Toggle the file indicated by the user.
                    elif (selection.lower() == "m1"):
                        copy_management_configuration = not copy_management_configuration
                    elif (selection.lower() == "p1"):
                        copy_prerecorded_processed_frames = not copy_prerecorded_processed_frames
                    elif (selection.lower() == "p2"):
                        copy_prerecorded_gpx_files = not copy_prerecorded_gpx_files
                    elif (selection.lower() == "p3"):
                        copy_prerecorded_license_plate_analysis_data = not copy_prerecorded_license_plate_analysis_data
                    elif (selection.lower() == "p4"):
                        copy_prerecorded_object_recognition_data = not copy_prerecorded_object_recognition_data
                    elif (selection.lower() == "p5"):
                        copy_prerecorded_license_plate_location_data = not copy_prerecorded_license_plate_location_data
                    elif (selection.lower() == "r1"):
                        copy_realtime_images = not copy_realtime_images
                    elif (selection.lower() == "r2"):
                        copy_realtime_object_recognition_data = not copy_realtime_object_recognition_data
                    elif (selection.lower() == "r3"):
                        copy_realtime_license_plate_recognition_data = not copy_realtime_license_plate_recognition_data
                    elif (selection.lower() == "d1"):
                        copy_dashcam_video = not copy_dashcam_video
                

                # Prompt the user for the copying destination.
                copy_destination = "" # Set the copy_destination as a blank placeholder.
                while os.path.exists(copy_destination) == False: # Repeatedly ask the user for a valid copy destination until they enter one that is valid.
                    copy_destination = input("Destination path: ") # Prompt the user for a destination path.


                # Copy the files as per the user's inputs.
                print("Copying files...")
                if (copy_management_configuration):
                    os.system("cp " + predator_root_directory + "/config.json " + copy_destination)
                if (copy_prerecorded_processed_frames):
                    os.system("cp -r " + root + "/frames " + copy_destination)
                if (copy_prerecorded_gpx_files):
                    os.system("cp " + root + "/*.gpx " + copy_destination)
                if (copy_prerecorded_license_plate_analysis_data):
                    os.system("cp " + root + "/pre_recorded_license_plate_export.* " + copy_destination)
                if (copy_prerecorded_object_recognition_data):
                    os.system("cp " + root + "/pre_recorded_object_detection_export.* " + copy_destination)
                if (copy_prerecorded_license_plate_location_data):
                    os.system("cp " + root + "/pre_recorded_license_plate_location_data_export.* " + copy_destination)
                if (copy_realtime_images):
                    os.system("cp " + root + "/realtime_image* " + copy_destination)
                if (copy_realtime_object_recognition_data):
                    os.system("cp " + root + "/real_time_object_detection* " + copy_destination)
                if (copy_realtime_license_plate_recognition_data):
                    os.system("cp " + root + "/real_time_plates* " + copy_destination)
                if (copy_dashcam_video):
                    os.system("cp " + root + "/predator_dashcam* " + copy_destination)

                clear()
                print("Files have finished copying.")


            elif (selection == "3"): # The user has selected the "delete files" option.
                # Reset all of the file selections to un-selected.
                delete_management_custom = False
                delete_prerecorded_processed_frames = False
                delete_prerecorded_gpx_files = False
                delete_prerecorded_license_plate_analysis_data = False
                delete_prerecorded_object_recognition_data = False
                delete_prerecorded_license_plate_location_data = False
                delete_realtime_images = False
                delete_realtime_object_recognition_data  = False
                delete_realtime_license_plate_recognition_data = False
                delete_dashcam_video = False

                while True: # Run the "delete files" selection menu on a loop forever until the user is finished selecting files.
                    clear() # Clear the console output before each loop.
                    print("Please select which files to delete")
                    print("0. Continue")
                    print("")
                    print("===== Management Mode =====")
                    if (delete_management_custom == True):
                        print("M1. [X] Custom file-name (Specified in next step)")
                    else:
                        print("M1. [ ] Custom file-name (Specified in next step)")
                    print("")
                    print("===== Pre-recorded Mode =====")
                    if (delete_prerecorded_processed_frames == True):
                        print("P1. [X] Processed video frames")
                    else:
                        print("P1. [ ] Processed video frames")
                    if (delete_prerecorded_gpx_files == True):
                        print("P2. [X] GPX files")
                    else:
                        print("P2. [ ] GPX files")
                    if (delete_prerecorded_license_plate_analysis_data == True):
                        print("P3. [X] License plate analysis data files")
                    else:
                        print("P3. [ ] License plate analysis data files")
                    if (delete_prerecorded_object_recognition_data == True):
                        print("P4. [X] Object recognition data files")
                    else:
                        print("P4. [ ] Object recognition data files")
                    if (delete_prerecorded_license_plate_location_data == True):
                        print("P5. [X] License plate location data files")
                    else:
                        print("P5. [ ] License plate location data files")
                    print("")
                    print("===== Real-time Mode =====")
                    if (delete_realtime_images == True):
                        print("R1. [X] Captured images")
                    else:
                        print("R1. [ ] Captured images")
                    if (delete_realtime_object_recognition_data == True):
                        print("R2. [X] Object recognition data files")
                    else:
                        print("R2. [ ] Object recognition data files")
                    if (delete_realtime_license_plate_recognition_data == True):
                        print("R3. [X] License plate recognition data files")
                    else:
                        print("R3. [ ] License plate recognition data files")
                    print("")
                    print("===== Dash-cam Mode =====")
                    if (delete_dashcam_video == True):
                        print("D1. [X] Dash-cam videos")
                    else:
                        print("D1. [ ] Dash-cam videos")
                    print("")

                    selection = input("Selection: ") # Prompt the user for a selection.

                    if (selection == "0"):
                        break

                    # Toggle the file indicated by the user.
                    elif (selection.lower() == "m1"):
                        delete_management_custom = not delete_management_custom
                    elif (selection.lower() == "p1"):
                        delete_prerecorded_processed_frames = not delete_prerecorded_processed_frames
                    elif (selection.lower() == "p2"):
                        delete_prerecorded_gpx_files = not delete_prerecorded_gpx_files
                    elif (selection.lower() == "p3"):
                        delete_prerecorded_license_plate_analysis_data = not delete_prerecorded_license_plate_analysis_data
                    elif (selection.lower() == "p4"):
                        delete_prerecorded_object_recognition_data = not delete_prerecorded_object_recognition_data
                    elif (selection.lower() == "p5"):
                        delete_prerecorded_license_plate_location_data = not delete_prerecorded_license_plate_location_data
                    elif (selection.lower() == "r1"):
                        delete_realtime_images = not delete_realtime_images
                    elif (selection.lower() == "r2"):
                        delete_realtime_object_recognition_data = not delete_realtime_object_recognition_data
                    elif (selection.lower() == "r3"):
                        delete_realtime_license_plate_recognition_data = not delete_realtime_license_plate_recognition_data
                    elif (selection.lower() == "d1"):
                        delete_dashcam_video = not delete_dashcam_video

                if (delete_management_custom):
                    delete_custom_file_name = input("Please specify the name of the additional file you'd like to delete from the current project folder: ")

                # Delete the files as per the user's inputs, after confirming the deletion process.
                if (input("Are you sure you want to delete the selected files permanently? (y/n): ").lower() == "y"):
                    print("Deleting files...")
                    if (delete_management_custom):
                        os.system("rm -r " + root + "/" + delete_custom_file_name)
                    if (delete_prerecorded_processed_frames):
                        os.system("rm -r " + root + "/frames")
                    if (delete_prerecorded_gpx_files):
                        os.system("rm " + root + "/*.gpx")
                    if (delete_prerecorded_license_plate_analysis_data):
                        os.system("rm " + root + "/pre_recorded_license_plate_export.*")
                    if (delete_prerecorded_object_recognition_data):
                        os.system("rm " + root + "/pre_recorded_object_detection_export.*")
                    if (delete_prerecorded_license_plate_location_data):
                        os.system("rm " + root + "/pre_recorded_license_plate_location_data_export.*")
                    if (delete_realtime_images):
                        os.system("rm " + root + "/realtime_image*")
                    if (delete_realtime_object_recognition_data):
                        os.system("rm " + root + "/real_time_object_detection*")
                    if (delete_realtime_license_plate_recognition_data):
                        os.system("rm " + root + "/real_time_plates*")
                    if (delete_dashcam_video):
                        os.system("rm " + root + "/predator_dashcam*")
                    clear()
                    print("Files have finished deleting.")
                else:
                    print("No files have been deleted.")


            else: # The user has selected an invalid option in the file management menu.
                print(style.yellow + "Warning: Invalid selection." + style.end)



        elif (selection == "2"): # The user has selected the "Information" option.
            print("    Please select an option")
            print("    0. Back")
            print("    1. About")
            print("    2. Neofetch")
            print("    3. Print Current Configuration")
            print("    4. Disk Usage")
            selection = input("    Selection: ")
            if (selection == "0"): # The user has selected to return back to the previous menu.
                pass # Do nothing, and just finish this loop.
            elif (selection == "1"): # The user has selected the "about" option.
                clear()
                print(style.bold + "============" + style.end)
                print(style.bold + "  Predator" + style.end)
                print(style.bold + "    V0LT" + style.end)
                print(style.bold + "    V6.0" + style.end)
                print(style.bold + "   GPL v3" + style.end)
                print(style.bold + "============" + style.end)
            elif (selection == "2"): # The user has selected the "neofetch" option.
                os.system("neofetch")
            elif (selection == "3"): # The user has selected the "print configuration" option.
                os.system("cat " + predator_root_directory + "/config.json")
            elif (selection == "4"): # The user has selected the "disk usage" option.
                print("Free space: " + str(round(((psutil.disk_usage(path=root).free)/1000000000)*100)/100) + "GB") # Display the free space on the storage device containing the current root project folder.
                print("Used space: " + str(round(((psutil.disk_usage(path=root).used)/1000000000)*100)/100) + "GB") # Display the used space on the storage device containing the current root project folder.
                print("Total space: " + str(round(((psutil.disk_usage(path=root).total)/1000000000)*100)/100) + "GB") # Display the total space on the storage device containing the current root project folder.
            else: # The user has selected an invalid option in the information menu.
                print(style.yellow + "Warning: Invalid selection." + style.end) # Inform the user that they have selected an invalid option.
            


        elif (selection == "3"): # The user has selected the "Configuration" option.
            print("    Please enter the name of a configuration section to edit")
            for section in config: # Iterate through each top-level section of the configuration database, and display them all to the user.
                if (type(config[section]) is list or type(config[section]) is dict): # Check to see if the current section we're iterating over is a list.
                    print("    '" + style.bold + str(section) + style.end + "'") # If the entry is a list, display it in bold.
                else:
                    print("    '" + style.italic + str(section) + style.end + "'") # If the entry is not a list (meaning it's an actual configuration value), display it in italics.
            selection1 = input("=== Selection (Tier 1): ")

            if (selection1 in config): # Check to make sure the section entered by the user actually exists in the configuration database.
                if (type(config[selection1]) is dict or type(config[selection1]) is list): # Check to make sure the current selection is a dictionary or list before trying to iterate through it.
                    print("        Please enter the name of a configuration section to edit")
                    for section in config[selection1]: # Iterate through each second-level section of the configuration database, and display them all to the user.
                        if (type(config[selection1][section]) is list or type(config[selection1][section]) is dict): # Check to see if the current section we're iterating over is a list.
                            print("        '" + style.bold + str(section) + style.end + "'") # If the entry is a list, display it in bold.
                        else:
                            print("        '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][section]) + "'") # If the entry is not a list (meaning it's an actual configuration value), display it in italics.
                    selection2 = input("======= Selection (Tier 2): ")
                    if selection2 in config[selection1]: # Check to make sure the section entered by the user actually exists in the configuration database.
                        if (type(config[selection1][selection2]) is dict or type(config[selection1][selection2]) is list): # Check to make sure the current selection is a dictionary or list before trying to iterate through it.
                            print("            Please enter the name of a configuration section to edit")
                            for section in config[selection1][selection2]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                if (type(config[selection1][selection2][section]) is list or type(config[selection1][selection2][section]) is dict): # Check to see if the current section we're iterating over is a list.
                                    print("            '" + style.bold + str(section) + style.end + "'") # If the entry is a list, display it in bold.
                                else:
                                    print("            '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][section]) + "'") # If the entry is not a list (meaning it's an actual configuration value), display it in italics.
                            selection3 = input("=========== Selection (Tier 3): ")
                            if selection3 in config[selection1][selection2]: # Check to make sure the section entered by the user actually exists in the configuration database.
                                if (type(config[selection1][selection2][selection3]) is dict or type(config[selection1][selection2][selection3]) is list): # Check to make sure the current selection is a dictionary or list before trying to iterate through it.
                                    print("                Please enter the name of a configuration section to edit")
                                    for section in config[selection1][selection2][selection3]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                        if (type(config[selection1][selection2][selection3][section]) is list or type(config[selection1][selection2][selection3][section]) is dict): # Check to see if the current section we're iterating over is a list.
                                            print("                '" + style.bold + str(section) + style.end + "'") # If the entry is a list, display it in bold.
                                        else:
                                            print("                '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][section]) + "'") # If the entry is not a list (meaning it's an actual configuration value), display it in italics.
                                    selection4 = input("=============== Selection (Tier 4): ")
                                else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 3)
                                    print("                Current Value: " + str(config[selection1][selection2][selection3]))
                                    if (type(config[selection1][selection2][selection3]) == str):
                                        config[selection1][selection2][selection3] = str(input("                New Value (String): "))
                                    elif (type(config[selection1][selection2][selection3]) == bool):
                                        new_value = input("                New Value (Boolean): ")
                                        if (new_value[0].lower() == "t" or new_value[0].lower() == "y"):
                                            config[selection1][selection2][selection3] = True
                                        elif (new_value[0].lower() == "f" or new_value[0].lower() == "n"):
                                            config[selection1][selection2][selection3] = False 
                                        else:
                                            config[selection1][selection2][selection3] = False 
                                            print(style.warning + "Warning: This configuration value is a boolean variable, but a non-boolean value was entered. Defaulting to 'false'.")
                                    elif (type(config[selection1][selection2][selection3]) == int):
                                        config[selection1][selection2][selection3] = int(input("                New Value (Integer): "))
                                    elif (type(config[selection1][selection2][selection3]) == float):
                                        config[selection1][selection2][selection3] = float(input("                New Value (Float): "))
                                    else:
                                        print(style.red + "Error: This configuration value didn't match any known variable type. This error should never occur and there's almost certainly a bug." + style.end)
                        else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 2)
                            print("            Current Value: " + str(config[selection1][selection2]))
                            if (type(config[selection1][selection2]) == str):
                                config[selection1][selection2] = str(input("            New Value (String): "))
                            elif (type(config[selection1][selection2]) == bool):
                                new_value = input("            New Value (Boolean): ")
                                if (new_value[0].lower() == "t" or new_value[0].lower() == "y"):
                                    config[selection1][selection2] = True
                                elif (new_value[0].lower() == "f" or new_value[0].lower() == "n"):
                                    config[selection1][selection2] = False 
                                else:
                                    config[selection1][selection2] = False 
                                    print(style.warning + "Warning: This configuration value is a boolean variable, but a non-boolean value was entered. Defaulting to 'false'.")
                            elif (type(config[selection1][selection2]) == int):
                                config[selection1][selection2] = int(input("            New Value (Integer): "))
                            elif (type(config[selection1][selection2]) == float):
                                config[selection1][selection2] = float(input("            New Value (Float): "))
                            else:
                                print(style.red + "Error: This configuration value didn't match any known variable type. This error should never occur and there's almost certainly a bug.." + style.end)

                else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 1)
                    print("        Current Value: " + str(config[selection1]))
                    if (type(config[selection1]) == str):
                        config[selection1] = str(input("            New Value (String): "))
                    elif (type(config[selection1]) == bool):
                        new_value = input("            New Value (Boolean): ")
                        if (new_value[0].lower() == "t" or new_value[0].lower() == "y"):
                            config[selection1] = True
                        elif (new_value[0].lower() == "f" or new_value[0].lower() == "n"):
                            config[selection1] = False 
                        else:
                            config[selection1] = False 
                            print(style.warning + "Warning: This configuration value is a boolean variable, but a non-boolean value was entered. Defaulting to 'false'.")
                    elif (type(config[selection1]) == int):
                        config[selection1] = int(input("            New Value (Integer): "))
                    elif (type(config[selection1]) == float):
                        config[selection1] = float(input("            New Value (Float): "))
                    else:
                        print(style.red + "Error: This configuration value didn't match any known variable type. This error should never occur and there's almost certainly a bug.." + style.end)
                    config[selection1] = input("        New Value: ")


            config_file = open(predator_root_directory + "/config.json", "w") # Open the configuration file.
            json.dump(config, config_file, indent=4) # Dump the JSON data into the configuration file on the disk.
            config_file.close() # Close the configuration file.
            config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database from config.json


        else: # The user has selected an invalid option in the main management menu.
            print(style.yellow + "Warning: Invalid selection." + style.end)

        input("\nPress enter to continue...") # Wait for the user to press enter before repeating the management menu loop.








# Pre-recorded mode

elif (mode_selection == "1" and prerecorded_mode_enabled == True): # The user has selected to boot into pre-recorded mode.
    # Get the required information from the user.
    if (default_root != ""): # Check to see if the user has configured a default root directory path.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = input("Project root directory path: ")
    video = input("Video file name: ")
    framerate = input("Optional: Frame analysis interval: ")
    if (framerate == None or framerate == "" or framerate == " "): # Check to see if the frame analysis interval prompt was left blank.
        framerate = 1.0 # If nothing was entered for the frame analysis interval prompt, default to 1.0
    else:
        framerate = float(framerate) # Convert the framerate string input into a floating point value.
    license_plate_format = input("Optional: License plate validation format: ")
    if (disable_object_recognition == True): # Check to see whether or not object recognition has been globally disabled in the Predator configuration.
        print(style.yellow + "Warning: Skipping object recognition prompt, since object recognition has been globally disabled in the Predator configuration. Adjust the `disable_object_recognition` configuration value to change this." + style.end)
        object_recognition_preference = "n"
    else:
        object_recognition_preference = input("Enable object recognition (y/n): ")
    video_start_time = input("Optional: Video starting time (YYYY-mm-dd HH:MM:SS): ") # Ask the user when the video recording started so we can correlate it's frames to a GPX file.
    if (video_start_time != ""):
        gpx_file = input("Optional: GPX file name: ")
    else:
        gpx_file = ""


    if (video_start_time == ""): # If the video_start_time preference was left blank, then default to 0.
        video_start_time = 0
    else:
        video_start_time = round(time.mktime(datetime.datetime.strptime(video_start_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the video_start_time human readable date and time into a Unix timestamp.

    if (object_recognition_preference.lower() == "y"): # Change the 'object_recognition_preference' to a boolean for easier manipulation.
        object_recognition_preference = True
    else:
        object_recognition_preference = False
        



    # Run some validation to make sure the information just entered by the user is correct.
    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        print(style.yellow + "Warning: The root project directory entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")

    if (video[0] == "*"): # Check to see if the first character is a wilcard.
        video_list_command = "ls " + root + "/" + video + " | tr '\n' ','";
        videos = str(os.popen(video_list_command).read())[:-1].split(",") # Run the command, and record the raw output string.
        for key, video in enumerate(videos):
            videos[key] = os.path.basename(video)
 
    else:
        videos = video.split(", ") # Split the video input into a list, based on the position of commas.
    for video in videos: # Iterate through each video specified by the user.
        if (os.path.exists(root + "/" + video) == False): # Check to see if each video file name supplied by the user actually exists in the root project folder.
            print(style.yellow + "Warning: The video file " + str(video) + " entered doesn't seem to exist in the root project directory. Predator will almost certainly fail." + style.end) # Inform the user that this video file couldn't be found.
            input("Press enter to continue...") # Wait for the user to press enter before continuing.

    if (gpx_file != "" and os.path.exists(root + "/" + gpx_file) == False): # Check to see if the GPX file name supplied by the user actually exists in the root project folder.
        print(style.yellow + "Warning: The GPX file name entered doesn't seem to exist. Predator will almost certainly encounter issues." + style.end)
        input("Press enter to continue...")

    if (len(license_plate_format) > 12): # Check to see if the license plate template supplied by the user abnormally long.
        print(style.yellow + "Warning: The license plate template supplied is abnormally long. Predator will still be able to operate as usual, but it's possible there's been a typo, since extremely few license plates are this long." + style.end)
        input("Press enter to continue...")



    clear() # Clear the console output

    
    # Split the supplied video(s) into individual frames based on the user's input.
    video_counter = 0 # Create a placeholder counter that will be incremented by 1 for each video. This will be appended to the file names of the video frames to keep frames from different videos separate.
    print("Splitting video into discrete images...")
    for video in videos: # Iterate through each video specified by the user.
        video_counter = video_counter + 1 # Increment the video counter by 1.
        frame_split_command = "mkdir " + root + "/frames; ffmpeg -i " + root + "/" + video + " -r " + str(1/framerate) + " " + root + "/frames/video" + str(video_counter) + "output%04d.png -loglevel quiet" # Set up the FFMPEG command that will be used to split each video into individual frames.
        os.system(frame_split_command) # Execute the FFMPEG command to split the video into individual frames.
     
    print("Done.\n")



    # Gather all of the individual frames generated previously.
    print("Gathering generated frames...")
    frames = os.listdir(root + "/frames") # Get all of the files in the folder designated for individual frames.
    frames.sort() # Sort the list alphabetically.
    print("Done.\n")



    # Crop the individual frames to make license plate recognition more efficient and accurate.
    print("Cropping individual frames...")
    for frame in frames:
        os.system(crop_script_path + " " + root + "/frames/" + frame + " " + left_margin + " " + right_margin + " " + top_margin + " " + bottom_margin)
    print("Done.\n")



    # If enabled, count how many vehicles are in each frame.
    if (object_recognition_preference == True and disable_object_recognition == False):
        print("Running object recognition...")
        time.sleep(1) # Wait for a short period of time to allow the images to finish saving.
        object_count = {} # Create an empty dictionary that will hold each frame and the object recognition counts.
        for frame in frames: # Iterate through each frame.
            object_count[frame] = {} # Initial the dictionary for this frame.
            frame_path = root + "/frames/" + frame # Set the file path of the current frame.
            image = cv2.imread(frame_path) # Load the frame.
            object_recognition_bounding_box, object_recognition_labels, object_recognition_confidence = cv.detect_common_objects(image) # Anaylze the image.
            for object_recognized in object_recognition_labels: # Iterate through each object recognized.
                if (object_recognized in object_count[frame]):
                    object_count[frame][object_recognized] = object_count[frame][object_recognized] + 1
                else:
                    object_count[frame][object_recognized] = 1

        print("Done.\n")



    # Analyze each individual frame, and collect possible plate IDs.
    print("Scanning for license plates...")
    lpr_scan = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
    for frame in frames:
        lpr_scan[frame] = [] # Set the license plate recognition information for this frame to an empty list as a placeholder.
        analysis_command = "alpr -j -n 5 " + root + "/frames/" + frame # Set up the OpenALPR command.
        reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
        reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.

        # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
        all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
        for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the OpenALPR command.
            all_current_plate_guesses[detected_plate["plate_index"]] = [] # Create an empty list for this plate so we can add all the potential plate guesses to it in the next step.
            for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                all_current_plate_guesses[detected_plate["plate_index"]].append(plate_guess["plate"]) # Add the current plate guess candidate to the list of plate guesses.

        if (len(all_current_plate_guesses) > 0): # Only add data to the current frame if data actually exists to add in the first place.
            lpr_scan[frame] = all_current_plate_guesses[0] # Collect the information for only the first plate detected by OpenALPR.
    print("Done.\n")




    raw_lpr_scan = lpr_scan # Save the data collected to a variable before sanitizing and validating it so we can access the raw data later.



    # Check the possible plate IDs and validate based on general plate formatting specified by the user.
    print("Validating license plates...")
    for frame in lpr_scan: # Iterate through each frame of video in the database of scanned plates.
        for i in range(0,len(lpr_scan)): # Run repeatedly to make sure the list shifting around doesn't lead to invalid license plates being skipped.
            for plate in lpr_scan[frame]: # Iterate through each plate detected per frame.
                if (plate in ignore_list): # Check to see if this plate is in the ignore list.
                    lpr_scan[frame].remove(plate) # Remove this plate, since it was found in the ignore list.
                elif (validate_plate(plate, license_plate_format) == False and license_plate_format != ""): # Remove the plate if it fails the validation test (and the license plate format isn't blank).
                    lpr_scan[frame].remove(plate) # Since the plate failed the validation test, delete it from the array.
    print("Done.\n")





    # Run through the data for each frame, and save only the first (most likely) license plate.
    print("Collecting most likely plate per frame...")
    plates_detected = [] # Create an empty list that the detected plates will be added to.
    for frame in lpr_scan:
        if (len(lpr_scan[frame]) >= 1): # Only grab the first plate if a plate was detected at all.
            plates_detected.append(lpr_scan[frame][0]) # Add the first plate in the list of plate guesses from OpenALPR to the list of plates detected by Predator.
    print("Done.\n")



    # De-duplicate the list of license plates detected.
    print("De-duplicating detected license plates...")
    plates_detected = list(dict.fromkeys(plates_detected))
    print("Done.\n")



    # Correlate the detected license plates with a GPX file.
    frame_locations = {} # Create a blank database that will be used during the process
    if (gpx_file != ""): # Check to make sure the user actually supplied a GPX file.
        print("Processing location data...")
        decoded_gpx_data = process_gpx(root + "/" + gpx_file) # Decode the data from the GPX file.
        iteration = 0 # Set the iteration counter to 0 so we can add one to it each frame we iterate through.
        for element in lpr_scan: # Iterate through each frame.
            iteration = iteration + 1 # Add one to the iteration counter.
            frame_timestamp = video_start_time + (iteration * framerate) # Calculate the timestamp of this frame.
            if (decoded_gpx_data[frame_timestamp] != None): # Check to see that the timestamp for this frame exists in the GPX data.
                frame_locations[frame_timestamp] = [decoded_gpx_data[frame_timestamp], lpr_scan[element]]
            else:
                frame_locations[frame_timestamp] = ["X", lpr_scan[element]]
                print(style.yellow + "Warning: There is no GPX data matching the timestamp of frame " + element + ". Does the GPX file specified line up with the video?" + style.end)
        print("Done.\n")




    # Analysis has been completed. Next, the user will choose what to do with the analysis data.


    input("Press enter to continue...")

    while True: # Run the pre-recorded mode menu in a loop forever until the user exits.
        clear()

        # Show the main menu for handling data collected in pre-recorded mode.
        print("Please select an option")
        print("0. Quit")
        print("1. Manage license plate data")
        print("2. Manage object recognition data")
        print("3. Manage license plate GPS data")
        print("4. View session statistics")
        selection = input("Selection: ")


        if (selection == "0"): # If the user selects option 0 on the main menu, then exit Predator.
            print("Shutting down...")
            break

        elif (selection == "1"): # If the user selects option 1 on the main menu, then load the license pl atedata viewing menu.
            print("    Please select an option")
            print("    0. Back")
            print("    1. View data")
            print("    2. Export data")
            selection = input("    Selection: ")

            if (selection == "1"): # The user has opened the license plate data viewing menu.
                print("        Please select an option")
                print("        0. Back")
                print("        1. View as Python data")
                print("        2. View as list")
                print("        3. View as CSV")
                print("        4. View as raw data")
            
                selection = input("        Selection: ")

                if (selection == "0"):
                    print("Returning to main menu.")
                elif (selection == "1"): # The user has selected to view license plate data as Python data.
                    print(str(plates_detected))
                elif (selection == "2"): # The user has selected to view license plate data as a list.
                    for plate in plates_detected:
                        print(plate)
                elif (selection == "3"): # The user has selected to view license plate data as CSV data.
                    for plate in plates_detected:
                        print(plate + ",")
                elif (selection == "4"): # The user has selected to view license plate data as raw data.
                    print(raw_lpr_scan)
                else:
                    print(style.yellow + "Warning: Invalid selection." + style.end)

            elif (selection == "2"): # The user has opened the license plate data exporting menu.
                print("        Please select an option")
                print("        0. Back")
                print("        1. Export as Python data")
                print("        2. Export as list")
                print("        3. Export as CSV")
                print("        4. Export as raw data")
                selection = input("        Selection: ")

                export_data = "" # Create a blank variable to store the export data.

                if (selection == "0"):
                    print("Returning to main menu.")
                elif (selection == "1"): # The user has selected to export license plate data as Python data.
                    export_data = str(plates_detected)
                    save_to_file(root + "/pre_recorded_license_plate_export.txt", export_data, silence_file_saving) # Save to disk.
                elif (selection == "2"): # The user has selected to export license plate data as a list.
                    for plate in plates_detected:
                        export_data = export_data + plate + "\n"
                    save_to_file(root + "/pre_recorded_license_plate_export.txt", export_data, silence_file_saving) # Save to disk.
                elif (selection == "3"): # The user has selected to export license plate data as CSV data.
                    for plate in plates_detected:
                        export_data = export_data + plate + ",\n"
                    save_to_file(root + "/pre_recorded_license_plate_export.csv", export_data, silence_file_saving) # Save to disk.
                elif (selection == "4"): # The user has selected to export license plate data as raw data.
                    save_to_file(root + "/pre_recorded_license_plate_export.txt", str(raw_lpr_scan), silence_file_saving) # Save raw license plate analysis data to disk.
                else:
                    print(style.yellow + "Warning: Invalid selection." + style.end)

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "2" and object_recognition_preference == True): # The user has selected to manage object recognition data.
            if (object_recognition_preference == True):
                print("    Please select an option")
                print("    0. Back")
                print("    1. View data")
                print("    2. Export data")
                selection = input("    Selection: ")

                if (selection == "1"): # The user has selected to view object recognition data.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. View as Python data")
                    print("        2. View as JSON data")
                    selection = input("        Selection: ")

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        print(object_count)
                    elif (selection == "2"):
                        print(json.dumps(object_count, indent=4))
                    else:
                        print(style.yellow + "Warning: Invalid selection." + style.end)

                elif (selection == "2"): # The user has selected to export object recognition data.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. Export as Python data")
                    print("        2. Export as JSON data")
                    selection = input("Selection: ")

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        save_to_file(root + "/pre_recorded_object_detection_export.txt", str(object_count), silence_file_saving) # Save to disk.
                    elif (selection == "2"):
                        save_to_file(root + "/pre_recorded_object_detection_export.json", json.dumps(object_count, indent=4), silence_file_saving) # Save to disk.
                    else:
                        print(style.yellow + "Warning: Invalid selection." + style.end)

                else: # The user has selected an invalid option in the object recognition data management menu.
                    print(style.yellow + "Warning: Invalid selection." + style.end)

            else: # The user has selected the object recognition data management menu, but object recognition has been disabled.
                print(style.yellow + "Warning: Object recognition has been disabled. There is not object recogntion data to manage." + style.end)

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "3"): # The user has selected to manage GPX location information.
            if (gpx_file != ""): # Check to see if a GPX file was provided for analysis.
                print("    Please select an option")
                print("    0. Back")
                print("    1. View data")
                print("    2. Export data")
                selection = input("    Selection: ")

                if (selection == "0"):
                    print("Returning to main menu.")
                elif (selection == "1"): # The user has selected to view GPX location information.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. View as Python data")
                    print("        2. View as JSON data")
                    selection = input("        Selection: ")

                    if (selection == 0):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        print(frame_locations)
                    elif (selection == "2"):
                        print(json.dumps(frame_locations, indent=4))
                    else:
                        print(style.yellow + "Warning: Invalid selection." + style.end)

                elif (selection == "2"): # The user has selected to export GPX location information.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. Export as Python data")
                    print("        2. Export as JSON data")
                    selection = input("        Selection: ")

                    if (selection == 0):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        save_to_file(root + "/pre_recorded_license_plate_location_data_export.txt", frame_locations, silence_file_saving) # Save to disk.
                    elif (selection == "2"):
                        save_to_file(root + "/pre_recorded_license_plate_location_data_export.json", json.dumps(frame_locations, indent=4), silence_file_saving) # Save to disk.
                    else:
                        print(style.yellow + "Warning: Invalid selection." + style.end)

                else:
                    print(style.yellow + "Warning: Invalid selection." + style.end)

            else:
                print(style.yellow + "Warning: GPX processing has been disabled since a GPX file wasn't provided. There is not GPX location data to manage." + style.end)

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "4"): # If the user selects option 4 on the main menu, then show the statstics for this session.
            print("    Frames analyzed: " + str(len(raw_lpr_scan))) # Show how many frames of video were analyzed.
            print("    Plates found: " + str(len(plates_detected))) # Show how many unique plates were detected.
            print("    Videos analyzed: " + str(len(videos))) # Show how many videos were analyzed.
            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.


        else: # If the user selects an unrecognized option on the main menu for pre-recorded mode, then show a warning.
            print(style.yellow + "Warning: Invalid selection." + style.end)
            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.









# Real-time mode

elif (mode_selection == "2" and realtime_mode_enabled == True): # The user has set Predator to boot into real-time mode.
    if (alert_database_license_plates != ""): # Check to see if the user has configured a file for alerts.
        alert_database = alert_database_license_plates
    else:
        alert_database = ""



    # Configure the user's preferences for this session.
    if (default_root != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = input("Project root directory path: ")

    if (default_license_plate_format != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for license plate formatting." + style.end)
        if (default_license_plate_format == " "): # If the default license plate format is configured as a single space, then skip the prompt, but don't load a license format guideline.
            license_plate_format = ""
        else:
            license_plate_format = default_license_plate_format
    else:
        license_plate_format = input("Optional: License plate validation format: ")

    if (default_save_license_plates_preference != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for license plate saving." + style.end)
        save_license_plates_preference = default_save_license_plates_preference
    else:
        save_license_plates_preference = input("Optional: Enable license plate saving (y/n): ")

    if (default_save_images_preference != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for image saving." + style.end)
        save_images_preference = default_save_images_preference
    else:
        save_images_preference = input("Optional: Enable image saving: (y/n): ")


    if (disable_object_recognition == True): # Check to see whether or not object recognition has been globally disabled in the Predator configuration.
        print(style.yellow + "Warning: Skipping object recognition prompt, since object recognition has been globally disabled in the Predator configuration. Adjust the `disable_object_recognition` configuration value to change this." + style.end)
        realtime_object_recognition = "n" # Automatically reject the realtime object recognition prompt.
    else:
        if (default_realtime_object_recognition != ""): # Check to see if the user has configured a default for this preference.
            print(style.bold + "Using default preference for real-time object recognition." + style.end)
            if (default_realtime_object_recognition != ""):
                realtime_object_recognition = default_realtime_object_recognition
        else:
            realtime_object_recognition = input("Enable real-time object recognition? (y/n): ")


    # Save yes/no preferences as boolean values for easier access.
    if (save_license_plates_preference.lower() == "y"):
        save_license_plates_preference = True
    else:
        save_license_plates_preference = False

    if (save_images_preference.lower() == "y"):
        save_images_preference = True
    else:
        save_images_preference = False

    if (realtime_object_recognition.lower() == "y"):
        realtime_object_recognition = True
    else:
        realtime_object_recognition = False



    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        print(style.yellow + "Warning: The root project directory entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")


    if (dashcam_background_mode_realtime == True): # Check to see if the user has enabled auto dashcam background recording in real-time mode.
        dashcam_process = [] # Create a placeholder list to store the dashcam processes.
        iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
        for device in dashcam_device: # Run through each camera device specified in the configuration, and launch an FFMPEG recording instance for it.
            dashcam_process.append(subprocess.Popen(["ffmpeg", "-y", "-nostdin", "-loglevel" , "error", "-f", "v4l2", "-framerate", dashcam_frame_rate, "-video_size", dashcam_resolution, "-input_format", "mjpeg", "-i",  dashcam_device[device], root + "/predator_dashcam_" + str(int(time.time())) + "_camera" + str(iteration_counter) + ".mkv"], shell=False))
            iteration_counter = iteration_counter + 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.
            print("Started background dashcam recording on " + str(dashcam_device[device])) # Inform the user that recording was initiation for this camera device.

        print("Started background dash-cam recording.")


    # Load the alert database
    alpr_alert_database_format = "none"
    if (alert_database != None and alert_database != ""): # Check to see if the user has supplied a database to scan for alerts.
        if (validators.url(alert_database)): # Check to see if the user supplied a URL as their alert database.
            if (config["developer"]["offline"] == False): # Check to see if offline mode is disabled.
                alert_database_list, alpr_alert_database_format = download_plate_database(alert_database) # If so, download the data at the URL as the database.
            else:
                alert_database_list = [] # Set the alert database to an empty list.
                print(style.yellow + "Warning: A remote alert database source was specified, but Predator is in offline mode. Alerts have been disabled." + style.end)
        else: # The input the user supplied doesn't appear to be a URL.
            if (os.path.exists(root + "/" + alert_database)): # Check to see if the database specified by the user actually exists.
                f = open(root + "/" + alert_database, "r") # Open the user-specified datbase file.
                file_contents = f.read() # Read the file.
                if (file_contents[0] == "{"): # Check to see if the first character in the file indicates that this alert database is a JSON database.
                    alert_database_list = json.loads(file_contents) # Load the alert database as JSON data.
                    alpr_alert_database_format = "json"
                else: # The alert database appears to be a plain text list.
                    alert_database_list = file_contents.split() # Read each line of the file as a seperate entry in the alert database list.
                    alpr_alert_database_format = "text"
                f.close() # Close the file.
            else: # If the alert database specified by the user does not exist, alert the user of the error.
                alert_database_list = [] # Set the alert database to an empty list.
                print(style.yellow + "Warning: The alert database specified at " + root + "/" + alert_database + " does not exist. Alerts have been disabled." + style.end)
    else: # The user has not entered in an alert database.
        alert_database_list = [] # Set the alert database to an empty list.


    detected_license_plates = [] # Create an empty list that will hold each license plate detected by Predator during this session.
    i = 0 # Set the increment counter to 0 so we can increment it by one each time Predator analyzes a frame.



    while True: # Run in a loop forever.

        time.sleep(float(delay_between_rounds)) # Sleep for a certain amount of time based on the configuration.


        if (clear_between_rounds == True): # Clear the output screen at the beginning of each round if the configuration indicates to.
            clear()


        if (speed_display_enabled == True and gps_enabled == True): # Display the current speed based on GPS, if enabled in the configuration.
            current_location = get_gps_location() # Get the current location.
            current_speed = convert_speed(float(current_location[2]), speed_display_unit) # Convert the speed data from the GPS into the units specified by the configuration.
            print("Current speed: " + str(current_speed) + " " + str(speed_display_unit)) # Print the current speed to the console.





        if (realtime_alpr_enabled == True): # Only run license plate recognition if enabled in the configuration.

            if (manual_trigger == True): # If the manual trigger configuration value is enabled, then wait for the user to press enter before continuing.
                input("Press enter to trigger image capture...")



            # Take an image using the camera device specified in the configuration.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Taking image...")
            if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                os.system("fswebcam --no-banner -r " + camera_resolution + " -d " + fswebcam_device + " --jpeg 100 " + fswebcam_flags + " " + root + "/realtime_image" + str(i) + ".jpg >/dev/null 2>&1") # Take a photo using FSWebcam, and save it to the root project folder specified by the user.
            else:
                os.system("fswebcam --no-banner -r " + camera_resolution + " -d " + fswebcam_device + " --jpeg 100 " + fswebcam_flags + " " + root + "/realtime_image.jpg >/dev/null 2>&1") # Take a photo using FSWebcam, and save it to the root project folder specified by the user.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")





            # If necessary, rotate the image.
            if (str(real_time_image_rotation) != "0"): # Check to make sure that rotating the image is actually necessary so processing time isn't wasted if the user doesn't have the rotating setting configured.
                if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                    print("Rotating image...")
                if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                    os.system("convert " + root + "/realtime_image" + str(i) + ".jpg -rotate " + real_time_image_rotation + " " + root + "/realtime_image" + str(i) + ".jpg") # Execute the command to rotate the image, based on the configuration.
                else:
                    os.system("convert " + root + "/realtime_image.jpg -rotate " + real_time_image_rotation + " " + root + "/realtime_image.jpg") # Execute the command to rotate the image, based on the configuration.
                if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.\n----------")




            # If enabled, crop the frame down.
            if (real_time_cropping_enabled == True): # Check to see if the user has enabled cropping in real-time mode.
                if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                    print("Cropping frame...")
                if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                    os.system(crop_script_path + " " + root + "/realtime_image" + str(i) + ".jpg " + real_time_left_margin + " " + real_time_right_margin + " " + real_time_top_margin + " " + real_time_bottom_margin) # Execute the command to crop the image.
                else:
                    os.system(crop_script_path + " " + root + "/realtime_image.jpg " + real_time_left_margin + " " + real_time_right_margin + " " + real_time_top_margin + " " + real_time_bottom_margin) # Execute the command to crop the image.
                if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.\n----------")
                




            # Run license plate analysis on the captured frame.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Running license plate recognition...")
            time.sleep(0.2) # Sleep to give the user time to quit Predator if they want to.
            if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                analysis_command = "alpr -j -n " + realtime_guesses  + " '" + root + "/realtime_image" + str(i) + ".jpg'" # Prepare the analysis command so we can run it next.
            else:
                analysis_command = "alpr -j -n " + realtime_guesses  + " '" + root + "/realtime_image.jpg'" # Prepare the analysis command so we can run it next.

            i = i + 1 # Increment the counter for this cycle so we can count how many images we've analyzed during this session.
            new_plate_detected = [] # This variable will be used to determine whether or not a plate was detected this round. If no plate is detected, this will remain blank. If a plate is detected, it will change to be that plate. This is used to determine whether or not the database of detected plates needs to updated.

            raw_reading_output = str(os.popen(analysis_command).read()) # Run the OpenALPR command, and save it's output to reading_output.
            try: # Run the JSON interpret command inside a 'try' block so the entire program doesn't fatally crash if the JSON data is malformed.
                reading_output = json.loads(raw_reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
            except:
                reading_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":1920,"img_height":1080,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":1920,"height":1080}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since the actual reading output was malformed.
                print(style.red + "The JSON data returned by the ALPR process is malformed. This likely means there's a problem with the ALPR library." + style.end)
                input(style.faint + "Press enter to continue" + style.end)




            # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
            all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
            for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the OpenALPR command.
                ignore_plate = False # Reset this value to false for each plate.
                for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                    if (plate_guess["plate"] in ignore_list): # Check to see if this plate guess matches in a plate in the loaded ignore list.
                        ignore_plate = True # Indicate that this plate should be ignored.

                if (ignore_plate == False): # Only process this plate if it isn't set to be ignored.
                    all_current_plate_guesses[detected_plate["plate_index"]] = [] # Create an empty list for this plate so we can add all the potential plate guesses to it in the next step.

                    for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                        all_current_plate_guesses[detected_plate["plate_index"]].append(plate_guess["plate"]) # Add the current plate guess candidate to the list of plate guesses.

            if (print_detected_plate_count == True): # Only print the number of plates detected this round if it's enabled in the configuration.
                print("Plates Detected: " + str(len(all_current_plate_guesses))) # Show the number of plates detected this round.

            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Done\n----------")







            # Reset the status lighting to normal before processing the license plate data from OpenALPR.
            if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                update_status_lighting("normal") # Run the function to update the status lighting.
        else: # If license plate recognition is disabled, then run some quick tasks that would be run during the license plate recognition process.
            time.sleep(float(realtime_alpr_disabled_delay)) # Wait for a specified amount of time based on the configuration.
            if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                update_status_lighting("normal") # Run the function to update the status lighting.







        # If enabled, run object recognition on the captured frame.
        if (realtime_object_recognition == True and disable_object_recognition == False):
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Running object recognition...")
            object_count = {} # Create an empty dictionary that will hold each frame and the object recognition counts.
            if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                frame_path = root + "/realtime_image" + str(i) + ".jpg" # Set the file path of the current frame.
            else:
                frame_path = root + "/realtime_image.jpg" # Set the file path of the current frame.

            image = cv2.imread(frame_path) # Load the frame.
            object_recognition_bounding_box, object_recognition_labels, object_recognition_confidence = cv.detect_common_objects(image) # Anaylze the image.
            objects_identified = str(object_recognition_labels) # Convert the list of objects identified into a plain string.
            if (objects_identified != "[]"): # Check to see that there were actually identified objects.
                if (realtime_output_level >= 2): # Only display this status message if the output level indicates to do so.
                    print("Objects identified: " + objects_identified)
                export_data = str(round(time.time())) + "," + objects_identified + "\n" # Add the timestamp to the export data, followed by the object's detected, followed by a line break to prepare for the next entry to be added later.
                if (save_real_time_object_recognition == True): # Check to make sure the user has configured Predator to save recognized objects to disk.
                    add_to_file(root + "/real_time_object_detection.csv", export_data, silence_file_saving) # Add the export data to the end of the file and write it to disk.
                
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Done\n----------")







        if (realtime_alpr_enabled == True): # Only run license plate recognition if enabled in the configuration.
            # Process information from the OpenALPR license plate analysis command.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Processing license plate recognition data...")
            if (len(all_current_plate_guesses) > 0): # Check to see if at least one license plate was actually detected.
                for individual_detected_plate in all_current_plate_guesses: # Iterate through each individual plate detected in the image frame.
                    successfully_found_plate = False # Reset the 'sucessfully_found_plate` variable to 'False'. This will be changed back if a valid plate is detected.

                    # Run validation according to the configuration on the plate(s) detected.
                    if (license_plate_format == ""): # If the user didn't supply a license plate format, then skip license plate validation.
                        detected_plate = str(all_current_plate_guesses[individual_detected_plate][1]) # Grab the most likely detected plate as the 'detected plate'.
                        successfully_found_plate = True # Plate validation wasn't needed, so the fact that a plate existed at all means a valid plate was detected. Indicate that a plate was successfully found this round.

                    else: # If the user did supply a license plate format, then check all of the results against the formatting example.
                        for plate_guess in all_current_plate_guesses[individual_detected_plate]: # Iterate through each plate and grab the first plate that matches the plate formatting guidelines as the 'detected plate'.
                            if (validate_plate(plate_guess, license_plate_format)): # Check to see whether or not the plate passes the validation based on the format specified by the user.
                                detected_plate = plate_guess # Grab the validated plate as the 'detected plate'.
                                successfully_found_plate = True # The plate was successfully validated, so indicate that a plate was successfully found this round.
                                if (print_invalid_plates == True): # Only print the invalid plate if the configuration says to do so.
                                    print(style.green + plate_guess + style.end) # Print the valid plate in green.
                                break
                            else: # This particular plate guess is invalid, since it didn't align with the user-supplied formatting guidelines.
                                if (print_invalid_plates == True): # Only print the invalid plate if the configuration says to do so.
                                    print(style.red + plate_guess + style.end) # Print the invalid plate in red.




                    # Run the appropriate tasks, based on whether or not a valid license plate was detected.
                    if (successfully_found_plate == True): # Check to see if a valid plate was detected this round after the validation process ran.
                        detected_license_plates.append(detected_plate) # Save the most likely license plate ID to the detected_license_plates complete list.
                        new_plate_detected.append(detected_plate) # Save the most likely license plate ID to this round's new_plate_detected list.
                        if (realtime_output_level >= 2): # Only display this status message if the output level indicates to do so.
                            print("Detected Plate: " + detected_plate) # Print the detected plate.

                        if (audio_alerts == True and int(alert_sounds_notice_repeat) > 0): # Check to see if the user has audio alerts enabled.
                            for i in range(0, int(alert_sounds_notice_repeat)): # Repeat the sound several times, if the configuration says to.
                                os.system("mpg321 " + alert_sounds_notice + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                                time.sleep(float(alert_sounds_notice_delay)) # Wait before playing the sound again.

                        if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications enabled.
                            os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=A license plate has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification via Gotify.

                        if (shape_alerts == True): # Check to see if the user has enabled shape notifications.
                            display_shape("square") # Display an ASCII square in the output.

                        if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                            update_status_lighting("warning") # Run the function to update the status lighting.



                    elif (successfully_found_plate == False): # A plate was found, but none of the guesses matched the formatting guidelines provided by the user.
                        if (realtime_output_level >= 2): # Only display this status message if the output level indicates to do so.
                            print("A plate was found, but none of the guesses matched the supplied plate format.\n----------")

                        if (shape_alerts == True): # Check to see if the user has enabled shape notifications.
                            display_shape("circle") # Display an ASCII circle in the output.


            else: # No license plate was detected at all.
                if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.")


            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("----------") # Print a dividing line after processing license plate analysis data.




            # Check the plate(s) detected this around against the alert database, if necessary.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Checking license plate data against alert database...")

            active_alert = False # Reset the alert status to false so we can check for alerts on the current plate (if one was detected) next.
            if (alerts_ignore_validation == True): # If the user has enabled alerts that ignore license plate validation, then check each of the OpenALPR guesses against the license plate alert database.
                if (len(all_current_plate_guesses) > 0): # Check to see that the all_current_plate_guesses variable isn't empty. This variable will only have entries if a plate was detected this round.
                    for alert_plate in alert_database_list: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.                        
                        for individual_detected_plate in all_current_plate_guesses: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                            for individual_detected_plate_guess in all_current_plate_guesses[individual_detected_plate]: # Run through each of the plate guesses generated by OpenALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                                if (fnmatch.fnmatch(individual_detected_plate_guess, alert_plate)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                    active_alert = True # If the plate does exist in the alert database, indicate that there is an active alert by changing this variable to True. This will reset on the next round.

                                    # Display an alert that is starkly different from the rest of the console output to make it stand out visually to the user.
                                    if (realtime_output_level >= 1): # Only display this status message if the output level indicates to do so.
                                        print(style.yellow + style.bold)
                                        print("===================")
                                        print("ALERT HIT - " + str(individual_detected_plate_guess))
                                        if (alpr_alert_database_format == "json"): # If the current alert plate database is a JSON file, then display other metadata.
                                            if ("name" in alert_database_list[alert_plate]): # Check to see if a name exists for this alert plate.
                                                print("Name: " + str(alert_database_list[alert_plate]["name"])) # Display this alert plate's name.
                                            if ("description" in alert_database_list[alert_plate]): # Check to see if a name exists for this alert plate.
                                                print("Description: " + str(alert_database_list[alert_plate]["description"])) # Display this alert plate's description.
                                        print("===================")
                                        print(style.end + style.end)

                                    if (shape_alerts == True): # Check to see if the user has enabled shape notifications.
                                        display_shape("triangle") # Display an ASCII triangle in the output.

                                    if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                                        update_status_lighting("alert") # Run the function to update the status lighting.

                                    if (audio_alerts == True and int(alert_sounds_alert_repeat) > 0): # Check to see if the user has audio alerts enabled.
                                        for i in range(0, int(alert_sounds_alert_repeat)): # Repeat the sound several times, if the configuration says to.
                                            os.system("mpg321 " + alert_sounds_alert + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                                            time.sleep(float(alert_sounds_alert_delay)) # Wait before playing the sound again.

                                    if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications enabled.
                                        os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=A license plate in the alert database has been detected: " + str(individual_detected_plate_guess) + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.


            else: #  If the user has disabled alerts that ignore license plate validation, then only check the validated plate against the alert database.
                for alert_plate in alert_database_list: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.                        
                    for each_new_plate_detected in new_plate_detected: # Iterate through each plate that was detected and validated this round.
                        if (fnmatch.fnmatch(each_new_plate_detected, alert_plate)): # Check to see the validated detected plate matches this particular plate in the alert database, taking wildcards into account.
                            active_alert = True # If the plate does exist in the alert database, indicate that there is an active alert by changing this variable to True. This will reset on the next round.

                            if (realtime_output_level >= 1): # Only display this status message if the output level indicates to do so.
                                # Display an alert that is starkly different from the rest of the console output.
                                print(style.yellow + style.bold)
                                print("===================")
                                print("ALERT HIT - " + str(individual_detected_plate_guess))
                                if (alpr_alert_database_format == "json"): # If the current alert plate database is a JSON file, then display other metadata.
                                    if ("name" in alert_database_list[alert_plate]): # Check to see if a name exists for this alert plate.
                                        print("Name: " + str(alert_database_list[alert_plate]["name"])) # Display this alert plate's name.
                                    if ("description" in alert_database_list[alert_plate]): # Check to see if a name exists for this alert plate.
                                        print("Description: " + str(alert_database_list[alert_plate]["description"])) # Display this alert plate's description.
                                print("===================")
                                print(style.end + style.end)

                            if (shape_alerts == True): # Check to see if the user has enabled shape notifications.
                                display_shape("triangle") # Display an ASCII triangle in the output.

                            if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                                update_status_lighting("alert") # Run the function to update the status lighting.

                            if (audio_alerts == True and int(alert_sounds_alert_repeat) > 0): # Check to see if the user has audio alerts enabled.
                                for i in range(0, int(alert_sounds_alert_repeat)): # Repeat the sound several times, if the configuration says to.
                                    os.system("mpg321 " + alert_sounds_alert + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                                    time.sleep(float(alert_sounds_alert_delay)) # Wait before playing the sound again.

                            if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications enabled.
                                os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=A license plate in the alert database has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.
            if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")




            # If enabled, submit data about each newly detected plate to a network server.
            if (realtime_output_level >= 3 and webhook != None and webhook != ""): # Only display this status message if the output level indicates to do so.
                print("Submitting data to webhook...")

            for each_new_plate_detected in new_plate_detected: # Iterate through each plate that was detected this round.
                if (webhook != None and webhook != ""): # Check to see if the user has specified a webhook to submit detected plates to.
                    url = webhook.replace("[L]", each_new_plate_detected) # Replace "[L]" with the license plate detected.
                    url = url.replace("[T]", str(round(time.time()))) # Replace "[T]" with the current timestamp, rounded to the nearest second.
                    url = url.replace("[A]", str(active_alert)) # Replace "[A]" with the current alert status.

                    try: # Try sending a request to the webook.
                        response = requests.get(url)
                    except Exception as e:
                        response = e

                    if (str(webhook_response) != "200"): # If the webhook didn't respond with a 200 code; Warn the user that there was an error.
                        print(style.yellow + "Warning: Unable to submit data to webhook." + style.end)

            if (realtime_output_level >= 3 and webhook != None and webhook != ""): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")





            # If enabled, save the detected license plate (if any) to a file on disk.
            if (realtime_output_level >= 3 and save_license_plates_preference == True): # Only display this status message if the output level indicates to do so.
                print("Saving license plate data to disk...")

            if (save_license_plates_preference == True): # Check to see if the user has the 'save detected license plates' preference enabled.
                if (len(new_plate_detected) > 0): # Check to see if the new_plate_detected value is empty. If it is blank, that means no new plate was detected this round.
                    for each_new_plate_detected in new_plate_detected: # Iterate through each plate that was detected this round.
                        if (alpr_location_tagging == True and gps_enabled == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                            current_location = get_gps_location() # Get the current location.
                            export_data = each_new_plate_detected + "," + str(round(time.time())) + "," + str(active_alert).lower() + "," + str(current_location[0]) + "," + str(current_location[1]) + "\n" # Add the individual plate to the export data.
                        else:
                            export_data = each_new_plate_detected + "," + str(round(time.time())) + "," + str(active_alert).lower() + ",0.000,0.000\n" # Add the individual plate to the export data.
                        add_to_file(root + "/real_time_plates.csv", export_data, silence_file_saving) # Add the export data to the end of the file and write it to disk.

            if (realtime_output_level >= 3 and save_license_plates_preference == True): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")










# Dash-cam mode

elif (mode_selection == "3" and dashcam_mode_enabled == True): # The user has set Predator to boot into dash-cam mode.

    # Configure the user's preferences for this session.
    if (default_root != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = input("Project root directory path: ")


    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        print(style.yellow + "Warning: The root project directory entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")



    print("\nStarting dashcam recording at " + dashcam_resolution + "@" + dashcam_frame_rate + "fps") # Print information about the recording settings.

    dashcam_process = [] # Create a placeholder list to store the dashcam processes.
    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
    for device in dashcam_device: # Run through each camera device specified in the configuration, and launch an FFMPEG recording instance for it.
        dashcam_process.append(subprocess.Popen(["ffmpeg", "-y", "-nostdin", "-loglevel" , "error", "-f", "v4l2", "-framerate", dashcam_frame_rate, "-video_size", dashcam_resolution, "-input_format", "mjpeg", "-i",  dashcam_device[device], root + "/predator_dashcam_" + str(int(time.time())) + "_" + str(device) + ".mkv"], shell=False))
        iteration_counter = iteration_counter + 1 # Iterate the counter. This value will be used to create unique file names for each recorded video.
        print("Started recording on " + str(dashcam_device[device])) # Inform the user that recording was initiation for this camera device.

    input("Press enter to cancel recording...") # Wait for the user to press enter before continuing, since continuing will cause Predator to terminate, causing the dashcam recording process(es) to stop as well.
    iteration_counter = 0 # Set the iteration counter to 0 so that we can increment it for each recording device specified.
    for device in dashcam_device: # Run a loop once for every camera device specified for dashcam recording.
        dashcam_process[iteration_counter].terminate() # Terminate the FFMPEG process for this iteration.
        iteration_counter = iteration_counter + 1 # Iterate the counter.

    print("Dashcam recording halted.")





else: # The user has selected an unrecognized mode.
    print(style.yellow + "Warning: Invalid mode selected." + style.end)
