# Predator

# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Predator...")


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



import time # Required to add delays and handle dates/times.
import sys # Required to read command line arguments.
import re # Required to use Regex.
import datetime # Required for converting between timestamps and human readable date/time information.
import fnmatch # Required to use wildcards to check strings.

if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    if (config["realtime"]["status_lighting_enabled"] == True or config["realtime"]["push_notifications_enabled"] == True or config["realtime"]["webhook"] != "" or config["general"]["alert_databases"]["license_plates"] != ""):
        import requests # Required to make network requests.
        import validators # Required to validate URLs.

if (config["management"]["disk_statistics"] == True): # Only import the disk statistic library if it is enabled in the configuration.
    import psutil # Required to get disk usage information



import utils # Import the utils.py scripts.
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
prompt = utils.prompt # Load the user input prompt function from the utils script.
play_sound = utils.play_sound # Load the function used to play sounds from the utils script.
display_message = utils.display_message # Load the message display function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
validate_plate = utils.validate_plate # Load the plate validation function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
closest_key = utils.closest_key # Load the function used to find the closest entry in a dictionary to a given number.
start_dashcam = utils.start_dashcam # Load the function used to start dashcam recording.
display_alerts = utils.display_alerts # Load the function used to display license plate alerts given the dictionary of alerts.
load_alert_database = utils.load_alert_database # Load the function used to load license plate alert databases.


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
default_license_plate_format = config["general"]["default_license_plate_format"] # If this variable isn't empty, the "license plate format" prompt will be skipped when starting in real-time mode. This variable will be used as the license plate format.
alerts_ignore_validation = config["general"]["alerts_ignore_validation"] # This setting determines whether alerts will respect or ignore the license plate validation formatting template.
license_plate_alert_database_source = config["general"]["alert_databases"]["license_plates"] # This configuration value defines the file that Predator will load the alert list for license plates from.


# ----- Pre-recorded mode configuration -----
left_margin = config["prerecorded"]["left_margin"] # How many pixels will be cropped on the left side of the frame in pre-recorded mode.
right_margin = config["prerecorded"]["right_margin"] # How many pixels will be cropped on the right side of the frame in pre-recorded mode.
top_margin = config["prerecorded"]["top_margin"] # How many pixels will be cropped on the top of the frame in pre-recorded mode.
bottom_margin = config["prerecorded"]["bottom_margin"] # How many pixels will be cropped on the bottom of the frame in pre-recorded mode.



# ----- Real-time mode configuration -----
realtime_output_level = int(config["realtime"]["output_level"]) # This setting determines how much information Predator shows the user while operating in real-time mode.
clear_between_rounds = config["realtime"]["clear_between_rounds"] # This setting determines whether or not Predator will clear the output screen between analysis rounds in real-time mode.
delay_between_rounds = config["realtime"]["delay_between_rounds"] # This setting defines how long Predator will wait in between analysis rounds in real-time mode.
print_invalid_plates = config["realtime"]["print_invalid_plates"] # In real-time mode, print all plates that get invalided by the formatting rules in red. When this is set to false, only valid plates are displayed.
print_detected_plate_count = config["realtime"]["print_detected_plate_count"] # This setting determines whether or not Predator will print how many license plates it detects in each frame while operating in real-time mode.
manual_trigger = config["realtime"]["manual_trigger"] # This setting determines whether or not Predator will wait to be manually triggered before taking an image.
alpr_location_tagging = config["realtime"]["alpr_location_tagging"] # This setting determines whether or not detected license plates will be tagged with the current GPS location.
camera_resolution = config["realtime"]["camera_resolution"] # This is the resolution you want to use when taking images using the connected camera. Under normal circumstances, this should be the maximum resoultion supported by your camera.
real_time_cropping_enabled = config["realtime"]["real_time_cropping_enabled"] # This value determines whether or not each frame captured in real-time mode will be cropped.
real_time_left_margin = config["realtime"]["real_time_left_margin"] # How many pixels will be cropped from the left side of the frame in real-time mode.
real_time_right_margin = config["realtime"]["real_time_right_margin"] # How many pixels will be cropped from the right side of the frame in real-time mode.
real_time_top_margin = config["realtime"]["real_time_top_margin"] # How many pixels will be cropped from the bottom side of the frame in real-time mode.
real_time_bottom_margin = config["realtime"]["real_time_bottom_margin"] # How many pixels will be cropped from the top side of the frame in real-time mode.
real_time_image_rotation = config["realtime"]["real_time_image_rotation"] # How many degrees clockwise the image will be rotated in real-time mode.
fswebcam_device = config["realtime"]["fswebcam_device"] # This setting determines the video device that 'fswebcam' will use to take images in real-time mode.
fswebcam_flags = config["realtime"]["fswebcam_flags"] # These are command flags that will be added to the end of the FSWebcam command. You can use these to customize how FSWebcam takes images in real-time mode based on your camera set up.
webhook = config["realtime"]["webhook"] # This setting can be used to define a webhook that Predator will send a request to when it detects a license plate in real-time mode. See CONFIGURATION.md to learn more about how to use flags in this setting.
shape_alerts = config["realtime"]["shape_alerts"] # This setting determines whether or not prominent text-based shapes will be displayed for various actions. This is useful in vehicle installations where you may want to see whether or not Predator detected a plate at a glance.
save_real_time_object_recognition = config["realtime"]["save_real_time_object_recognition"] # This setting determines whether or not Predator will save the objects detected in real-time mode to a file. When this is turned off, object recognition data will only be printed to the console.
speed_display_enabled = config["realtime"]["speed_display_enabled"] # This setting determines whether or not Predator will display the current GPS speed each processing cycle in real-time mode.

# Default settings
default_save_license_plates_preference = config["realtime"]["default_save_license_plates_preference"] # If this variable isn't empty, the "save license plates" prompt will be skipped when starting in real-time mode. If this variable is set to "y", license plates will be saved.
default_save_images_preference = config["realtime"]["default_save_images_preference"] # If this variable isn't empty, the "save images" prompt will be skipped when starting in real-time mode. If this variable is set to "y", all images will be saved.
default_realtime_object_recognition = config["realtime"]["default_realtime_object_recognition"] # If this variable isn't empty, then the "real-time object detection" prompt will be skipped when starting in real-time mode. If this variable is set to "y", object recognition will be turned on.

# Push notification settings
push_notifications_enabled = config["realtime"]["push_notifications_enabled"] # This setting determines whether or not Predator will attempt to use Gotify to broadcast notifications for certain events.
gotify_server = config["realtime"]["gotify_server"] # This setting specifies the server address of the desired Gotify server, and should include the protocol (Ex: http://) and port (Ex: 80).
gotify_application_token = config["realtime"]["gotify_application_token"] # This setting specifies the Gotify application token that Predator will use to broadcast notifications.

# Status lighting system settings
status_lighting_enabled = config["realtime"]["status_lighting_enabled"]
status_lighting_base_url = config["realtime"]["status_lighting_base_url"]
status_lighting_values = config["realtime"]["status_lighting_values"]



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

play_sound("startup")

if (push_notifications_enabled == True): # Check to see if the user has push notifications enabled.
    os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=Predator has been started.' > /dev/null 2>&1 &") # Send a push notification via Gotify indicating that Predator has started.



# Run some basic error checks to see if any of the data supplied in the configuration seems wrong.
config["general"]["alpr_engine"] = config["general"]["alpr_engine"].lower().strip() # Convert the ALPR engine configuration value to all lowercase, and trim leading and trailing whitespaces.
if (config["general"]["alpr_engine"] != "phantom" and config["general"]["alpr_engine"] != "openalpr"): # Check to see if the configured ALPR engine is invalid.
    display_message("The configured ALPR engine is invalid. Please select either 'phantom' or 'openalpr' in the configuration.", 3)

if (os.path.exists(crop_script_path) == False): # Check to see that the cropping script exists at the path specified by the user in the configuration.
    display_message("The 'crop_script_path' defined in the configuration section doesn't point to a valid file. Image cropping will be broken. Please make sure the 'crop_script_path' points to a valid file.", 3)

if (int(left_margin) < 0 or int(right_margin) < 0 or int(bottom_margin) < 0 or int(top_margin) < 0): # Check to make sure that all of the pre-recorded mode cropping margins are positive numbers.
    display_message("One or more of the cropping margins for pre-recorded mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping margins have all been set to 0.", 3)
    left_margin = "0"
    right_margin = "0"
    bottom_margin = "0"
    top_margin = "0"

if (int(real_time_left_margin) < 0 or int(real_time_right_margin) < 0 or int(real_time_bottom_margin) < 0 or int(real_time_top_margin) < 0): # Check to make sure that all of the real-time mode cropping margins are positive numbers.
    display_message("One or more of the cropping margins for real-time mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping margins have all been set to 0.", 3)
    real_time_left_margin = "0"
    real_time_right_margin = "0"
    real_time_bottom_margin = "0"
    real_time_top_margin = "0"

if (re.fullmatch("(\d\d\dx\d\d\d)", dashcam_resolution) == None and re.fullmatch("(\d\d\d\dx\d\d\d)", dashcam_resolution) == None and re.fullmatch("(\d\d\d\dx\d\d\d\d)", dashcam_resolution) == None): # Verify that the dashcam_resolution setting matches the format 000x000, 0000x000, or 0000x0000.
    display_message("The 'dashcam_resolution' specified in the real-time configuration section doesn't seem to align with the '0000x0000' format. It's possible there has been a typo. defaulting to '1280x720'", 3)
    dashcam_resolution = "1280x720"

if (fswebcam_device == ""): # Check to make sure that a camera device has been specified in the real-time configuration section.
    display_message("The 'fswebcam_device' specified in the real-time configuration section is blank. It's possible there has been a typo. Defaulting to '/dev/video0'", 3)
    fswebcam_device = "/dev/video0"


shared_realtime_dashcam_device = False
for device in dashcam_device:
    if (dashcam_background_mode_realtime == True and dashcam_device[device] == fswebcam_device): # If Predator is configured to run background dashcam recording in real-time mode, then make sure the the dashcam camera device and real-time camera device are different.
        shared_realtime_dashcam_device = True
        dashcam_background_mode_realtime = False
if (shared_realtime_dashcam_device == True):
    display_message("The 'dashcam_background_mode_realtime' setting is turned on, but the same recording device has been specified for 'dashcam_device' and 'fswebcam_device'. Predator can't use the same device for two different tasks. Background dash-cam recording in real-time mode has been disabled.", 3)


if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications turned on in the configuration.
    if (gotify_server == "" or gotify_server == None): # Check to see if the gotify server has been left blank
        display_message("The 'push_notifications_enabled' setting is turned on, but the 'gotify_server' hasn't been set. Push notifications have been disabled.", 3)
        push_notifications_enabled = False
    if (gotify_application_token == "" or gotify_application_token == None): # Check to see if the Gotify application token has been left blank.
        display_message("The 'push_notifications_enabled' setting is turned on, but the 'gotify_application_token' hasn't been set. Push notifications have been disabled.", 3)
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
    display_message("The 'auto_start_mode' configuration value isn't properly set. This value should be blank, '0', '1', '2', '3'. It's possible there's been a typo.", 3)

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
    mode_selection = prompt("Selection: ")





# Intial setup has been completed, and Predator will now load into the specified mode.









if (mode_selection == "0" and management_mode_enabled == True): # The user has selected to boot into management mode.
    if (default_root != ""): # Check to see if the user has configured a default root directory path.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    # Run some validation to make sure the information just entered by the user is correct.
    while (os.path.exists(root) == False): # Run forever until the user enters a project directory that exists.
        display_message("The root project directory entered doesn't seem to exist.", 2)
        root = prompt("Project root directory path: ", optional=False, input_type=str)


    while True:
        clear()
        print("Please select an option")
        print("0. Quit")
        print("1. File Management")
        print("2. Information")
        print("3. Configuration")

        selection = prompt("Selection: ", optional=False, input_type=str)

        if (selection == "0"): # The user has selected to quit Predator.
            break # Break the 'while true' loop to terminate Predator.

        elif (selection == "1"): # The user has selected the "File Management" option.
            print("    Please select an option")
            print("    0. Back")
            print("    1. View")
            print("    2. Copy")
            print("    3. Delete")
            selection = prompt("    Selection: ", optional=False, input_type=str)

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

                    selection = prompt("Selection: ", optional=False, input_type=str) # Prompt the user for a selection.


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
                    copy_destination = prompt("Destination path: ", optional=False, input_type=str) # Prompt the user for a destination path.


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
                    os.system("cp " + root + "/pre_recorded_location_data_export.* " + copy_destination)
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

                    selection = prompt("Selection: ", optional=False, input_type=str) # Prompt the user for a selection.

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
                    delete_custom_file_name = prompt("Please specify the name of the additional file you'd like to delete from the current project folder: ")

                # Delete the files as per the user's inputs, after confirming the deletion process.
                if (prompt("Are you sure you want to delete the selected files permanently? (y/n): ").lower() == "y"):
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
                        os.system("rm " + root + "/pre_recorded_location_data_export.*")
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
                display_message("Invalid selection.", 2)



        elif (selection == "2"): # The user has selected the "Information" option.
            print("    Please select an option")
            print("    0. Back")
            print("    1. About")
            print("    2. Neofetch")
            print("    3. Print Current Configuration")
            if (config["management"]["disk_statistics"] == True): # Check to see if disk statistics are enabled.
                print("    4. Disk Usage") # Display the disk usage option in a normal style.
            else: # Otherwise, disk statistics are disabled.
                print("    " + style.faint + "4. Disk Usage" + style.end) # Display the disk usage option in a faint style to indicate that it is disabled.
            selection = prompt("    Selection: ", optional=False, input_type=str)
            if (selection == "0"): # The user has selected to return back to the previous menu.
                pass # Do nothing, and just finish this loop.
            elif (selection == "1"): # The user has selected the "about" option.
                clear()
                print(style.bold + "============" + style.end)
                print(style.bold + "  Predator" + style.end)
                print(style.bold + "    V0LT" + style.end)
                print(style.bold + "    V8.0" + style.end)
                print(style.bold + "   AGPLv3" + style.end)
                print(style.bold + "============" + style.end)
            elif (selection == "2"): # The user has selected the "neofetch" option.
                os.system("neofetch") # Execute neofetch to display information about the system.
            elif (selection == "3"): # The user has selected the "print configuration" option.
                os.system("cat " + predator_root_directory + "/config.json") # Print out the raw contents of the configuration database.
            elif (selection == "4"): # The user has selected the "disk usage" option.
                if (config["management"]["disk_statistics"] == True): # Check to make sure disk statistics are enabled before displaying disk statistics.
                    print("Free space: " + str(round(((psutil.disk_usage(path=root).free)/1000000000)*100)/100) + "GB") # Display the free space on the storage device containing the current root project folder.
                    print("Used space: " + str(round(((psutil.disk_usage(path=root).used)/1000000000)*100)/100) + "GB") # Display the used space on the storage device containing the current root project folder.
                    print("Total space: " + str(round(((psutil.disk_usage(path=root).total)/1000000000)*100)/100) + "GB") # Display the total space on the storage device containing the current root project folder.
                else: # Disk statistics are disabled, but the user has selected the disk usage option.
                    display_message("The disk usage could not be displayed because the 'disk_statistics' configuration option is disabled.", 2)
            else: # The user has selected an invalid option in the information menu.
                display_message("Invalid selection.", 2)
            


        elif (selection == "3"): # The user has selected the "Configuration" option.
            print("    Please enter the name of a configuration section to edit")
            for section in config: # Iterate through each top-level section of the configuration database, and display them all to the user.
                if (type(config[section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                    print("    '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                else:
                    print("    '" + style.italic + str(section) + style.end + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
            selection1 = prompt("=== Selection (Tier 1): ", optional=True, input_type=str, default="")

            if (selection1 in config): # Check to make sure the section entered by the user actually exists in the configuration database.
                if (type(config[selection1]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                    for section in config[selection1]: # Iterate through each second-level section of the configuration database, and display them all to the user.
                        if (type(config[selection1][section]) is dict): # Check to see if the current entry is a dictionary.
                            print("        '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                        else:
                            print("        '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                    selection2 = prompt("======= Selection (Tier 2): ", optional=True, input_type=str, default="")
                    if (selection2 in config[selection1]): # Check to make sure the section entered by the user actually exists in the configuration database.
                        if (type(config[selection1][selection2]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                            for section in config[selection1][selection2]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                if (type(config[selection1][selection2][section]) is dict): # Check to see if the current element is a dictionary.
                                    print("            '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                else:
                                    print("            '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                            selection3 = prompt("=========== Selection (Tier 3): ", optional=True, input_type=str, default="")
                            if (selection3 in config[selection1][selection2]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                if (type(config[selection1][selection2][selection3]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                    for section in config[selection1][selection2][selection3]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                        if (type(config[selection1][selection2][selection3][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                            print("                '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                        else:
                                            print("                '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                    selection4 = prompt("=============== Selection (Tier 4): ", optional=False, input_type=str)
                                else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 3)
                                    print("                Current Value: " + str(config[selection1][selection2][selection3]))
                                    config[selection1][selection2][selection3] = prompt("                New Value (" + str(type(config[selection1][selection2][selection3])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3]), default="")
                            elif (selection3 != ""):
                                display_message("Unknown configuration entry selected.", 3)
                        else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 2)
                            print("            Current Value: " + str(config[selection1][selection2]))
                            config[selection1][selection2] = prompt("            New Value (" + str(type(config[selection1][selection2])) + "): ", optional=True, input_type=type(config[selection1][selection2]), default="")
                    elif (selection2 != ""):
                        display_message("Unknown configuration entry selected.", 3)

                else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 1)
                    print("        Current Value: " + str(config[selection1]))
                    config[selection1] = prompt("        New Value (" + str(type(config[selection1])) + "): ", optional=True, input_type=type(config[selection1]), default="")
            elif (selection1 != ""):
                display_message("Unknown configuration entry selected.", 3)


            config_file = open(predator_root_directory + "/config.json", "w") # Open the configuration file.
            json.dump(config, config_file, indent=4) # Dump the JSON data into the configuration file on the disk.
            config_file.close() # Close the configuration file.
            config = json.load(open(predator_root_directory + "/config.json")) # Re-load the configuration database from disk.


        else: # The user has selected an invalid option in the main management menu.
            display_message("Invalid selection.", 2)








# Pre-recorded mode

elif (mode_selection == "1" and prerecorded_mode_enabled == True): # The user has selected to boot into pre-recorded mode.
    # Get the required information from the user.
    if (default_root != ""): # Check to see if the user has configured a default root directory path.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    while (os.path.exists(root) == False):
        display_message("The specified root project directory doesn't appear to exist", 2)
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    video = prompt("Video file name(s): ", optional=False, input_type=str)
    framerate = prompt("Optional: Frame analysis interval: ", optional=True, input_type=float, default=1.0)

    if (default_license_plate_format != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for license plate formatting." + style.end)
        if (default_license_plate_format == " "): # If the default license plate format is configured as a single space, then skip the prompt, but don't load a license format guideline.
            license_plate_format = ""
        else:
            license_plate_format = default_license_plate_format
    else:
        license_plate_format = prompt("Optional: License plate validation format: ", optional=True, input_type=str, default="")

    if (disable_object_recognition == True): # Check to see whether or not object recognition has been globally disabled in the Predator configuration.
        object_recognition_preference = "n"
    else:
        object_recognition_preference = prompt("Optional: Enable object recognition (y/n): ", optional=True, input_type=bool, default=False)
    video_start_time = prompt("Optional: Video starting time (YYYY-mm-dd HH:MM:SS): ") # Ask the user when the video recording started so we can correlate it's frames to a GPX file.
    if (video_start_time != ""):
        gpx_file = prompt("Optional: GPX file name: ", optional=True, input_type=str)
    else:
        gpx_file = ""


    if (video_start_time == ""): # If the video_start_time preference was left blank, then default to 0.
        video_start_time = 0
    else:
        video_start_time = round(time.mktime(datetime.datetime.strptime(video_start_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the video_start_time human readable date and time into a Unix timestamp.




    # Run some validation to make sure the information just entered by the user is correct.
    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        display_message("The root project directory entered doesn't seem to exist. Predator will almost certainly fail.", 3)

    if (video[0] == "*"): # Check to see if the first character is a wilcard.
        video_list_command = "ls " + root + "/" + video + " | tr '\n' ','";
        videos = str(os.popen(video_list_command).read())[:-1].split(",") # Run the command, and record the raw output string.
        for key, video in enumerate(videos):
            videos[key] = os.path.basename(video)
 
    else:
        videos = video.split(", ") # Split the video input into a list, based on the position of commas.
    for video in videos: # Iterate through each video specified by the user.
        if (os.path.exists(root + "/" + video) == False): # Check to see if each video file name supplied by the user actually exists in the root project folder.
            display_message("The video file " + str(video) + " entered doesn't seem to exist in the root project directory. Predator will almost certainly fail.", 3) # Inform the user that this video file couldn't be found.

    if (gpx_file != "" and os.path.exists(root + "/" + gpx_file) == False): # Check to see if the GPX file name supplied by the user actually exists in the root project folder.
        display_message("The GPX file name entered doesn't seem to exist. Predator will almost certainly encounter errors.", 3)

    if (len(license_plate_format) > 12): # Check to see if the license plate template supplied by the user abnormally long.
        display_message("The license plate template supplied is abnormally long. Processing can continue, but it's likely something has gone wrong.", 3)



    clear() # Clear the console output

    


    # Split the supplied video(s) into individual frames based on the user's input.
    video_counter = 0 # Create a placeholder counter that will be incremented by 1 for each video. This will be appended to the file names of the video frames to keep frames from different videos separate.
    print("Splitting video into discrete images...")
    if (os.path.exists(root + "/frames/")): # Check to see the frames directory already exists.
        os.system("rm -r " + root + "/frames") # Remove the frames directory.

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
    alpr_frames = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
    for frame in frames: # Iterate through each frame of video.
        alpr_frames[frame] = {} # Set the license plate recognition information for this frame to an empty list as a placeholder.

        # Run license plate analysis on this frame.
        if (config["general"]["alpr_engine"] == "phantom"): # Check to see if the configuration indicates that the Phantom ALPR engine should be used.
            analysis_command = "alpr -n " + str(config["general"]["alpr_guesses"]) + " " + root + "/frames/" + frame # Set up the Phantom ALPR command.
            reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
            reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
            if ("error" in reading_output): # Check to see if there were errors.
                print("Phantom ALPR encountered an error: " + reading_output["error"]) # Display the ALPR error.
                reading_output["results"] = [] # Set the results of the reading output to a blank placeholder list.
        elif (config["general"]["alpr_engine"] == "openalpr"): # Check to see if the configuration indicates that the OpenALPR engine should be used.
            analysis_command = "alpr -j -n " + str(config["general"]["alpr_guesses"]) + " " + root + "/frames/" + frame # Set up the OpenALPR command.
            reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
            reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
        else: # If the configured ALPR engine is unknown, then return an error.
            display_message("The configured ALPR engine is not recognized.", 3)

        # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
        all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
        plate_index = 0 # Reset the plate index counter to 0 before the loop.
        for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
            all_current_plate_guesses[plate_index] = [] # Create an empty list for this plate so we can add all the potential plate guesses to it in the next step.
            for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                all_current_plate_guesses[plate_index].append(plate_guess["plate"]) # Add the current plate guess candidate to the list of plate guesses.
            plate_index = plate_index + 1 # Increment the plate index counter.

        if (len(all_current_plate_guesses) > 0): # Only add license plate data to the current frame if data actually exists to add in the first place.
            #alpr_frames[frame] = all_current_plate_guesses[0] # Collect the information for only the first plate detected by ALPR.
            alpr_frames[frame] = all_current_plate_guesses # Record all of the detected plates for this frame.

    print("Done.\n")





    # Check the possible plate IDs and validate based on general plate formatting specified by the user.
    print("Validating license plates...")
    validated_alpr_frames = {} # This is a placeholder variable that will be used to store the validated ALPR information for each frame.

    # Handle ignore list processing.
    for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
        validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
        for plate in alpr_frames[frame].keys(): # Iterate through each plate detected per frame.
            for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                for ignore_plate in ignore_list: # Iterate through each plate in the ignore list.
                    if fnmatch.fnmatch(guess, ignore_plate):
                        alpr_frames[frame][plate] = [] # Remove this plate from the ALPR dictionary.
                        break # Break the loop, since this entire plate, including all of its guesses, has just been removed.

    # Remove any empty plates.
    for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
        plates = list(alpr_frames[frame].keys())
        for plate in plates:
            if (len(alpr_frames[frame][plate]) <= 0):
                print ("nuked")
                del alpr_frames[frame][plate]

    # Handle formatting validation.
    for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
        validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
        for plate in alpr_frames[frame].keys(): # Iterate through each plate detected per frame.
            for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                if (validate_plate(guess, license_plate_format) == True or license_plate_format == ""): # Check to see if this plate passes validation.
                    if (plate not in validated_alpr_frames[frame]): # Check to see if this plate hasn't been added to the validated information yet.
                        validated_alpr_frames[frame][plate] = [] # Add the plate to the validated information as a blank placeholder list.
                    validated_alpr_frames[frame][plate].append(guess) # Since this plate guess failed the validation test, delete it from the list of guesses.

    print("Done.\n")






    # Run through the data for each frame, and save only the first (most likely) license plate to the list of detected plates.
    print("Collecting most likely plate per guess...")
    plates_detected = [] # Create an empty list that the detected plates will be added to.
    for frame in validated_alpr_frames: # Iterate through all frames.
        for plate in validated_alpr_frames[frame]: # Iterate through all plates detected this frame.
            if (len(validated_alpr_frames[frame][plate]) > 0): # Check to see if this plate has any guesses associated with it.
                plates_detected.append(validated_alpr_frames[frame][plate][0]) # Add the first guess for this plate to this list of plates detected.
    print("Done.\n")




    # De-duplicate the list of license plates detected.
    print("De-duplicating detected license plates...")
    plates_detected = list(dict.fromkeys(plates_detected))
    print("Done.\n")





    print("Checking for alerts...")
    alert_database = load_alert_database(license_plate_alert_database_source, root) # Load the license plate alert database.
    active_alerts = {} # This is an empty placeholder that will hold all of the active alerts. 
    if (len(alert_database) > 0): # Only run alert processing if the alert database isn't empty.
        for rule in alert_database: # Run through every plate in the alert plate database supplied by the user.
            for frame in alpr_frames: # Iterate through each frame of video in the raw ALPR data.
                if (alerts_ignore_validation == True): # If the user has enabled alerts that ignore license plate validation, then use the unvalidated ALPR information.
                    alpr_frames_to_scan = alpr_frames
                else: # If the user hasn't enabled alerts that ignore license plate validation, then use the validated ALPR information.
                    alpr_frames_to_scan = validated_alpr_frames

                for plate in alpr_frames_to_scan[frame]: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                    for guess in alpr_frames_to_scan[frame][plate]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                        if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                            active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                            active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                            active_alerts[guess]["frame"] = frame # Add the rule that triggered this alert to the alert information.
                            break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

    display_alerts(active_alerts) # Display all active alerts.
    print("Done.\n")



    # Correlate the detected license plates with a GPX file.
    frame_locations = {} # Create a blank database that will be used during the process
    if (gpx_file != ""): # Check to make sure the user actually supplied a GPX file.
        print("Processing location data...")
        decoded_gpx_data = process_gpx(root + "/" + gpx_file) # Decode the data from the GPX file.
        iteration = 0 # Set the iteration counter to 0 so we can add one to it each frame we iterate through.
        for element in alpr_frames: # Iterate through each frame.
            iteration = iteration + 1 # Add one to the iteration counter.
            frame_timestamp = video_start_time + (iteration * framerate) # Calculate the timestamp of this frame.

            if (frame_timestamp in decoded_gpx_data): # Check to see if the exact timestamp for this frame exists in the GPX data.
                frame_locations[frame_timestamp] = [decoded_gpx_data[frame_timestamp], alpr_frames[element]]
            else: # If the exact timestamp doesn't exist, try to find a nearby timestamp.
                closest_gpx_entry = closest_key(decoded_gpx_data, frame_timestamp)

                if (closest_gpx_entry[1] < config["prerecorded"]["max_gpx_time_difference"]): # Check to see if the closest GPX entry is inside the maximum configured range.
                    frame_locations[frame_timestamp] = [decoded_gpx_data[closest_gpx_entry[0]], alpr_frames[element]]
                else: # Otherwise, indicate that a corresponding location couldn't be found.
                    frame_locations[frame_timestamp] = [{"lat": 0.0, "lon": 0.0}, alpr_frames[element]] # Set this location of this frame to latitude and longitude 0.0 as a placeholder.
                    display_message("There is no GPX data matching the timestamp of frame " + element + ". The closest location stamp is " + str(closest_gpx_entry[1]) + " seconds away. Does the GPX file specified line up with the video?", 3)

        print("Done.\n")




    # Analysis has been completed. Next, the user will choose what to do with the analysis data.


    prompt("Press enter to continue...")

    while True: # Run the pre-recorded mode menu in a loop forever until the user exits.
        clear()

        # Show the main menu for handling data collected in pre-recorded mode.
        print("Please select an option")
        print("0. Quit")
        print("1. Manage license plate data")
        if (object_recognition_preference == True): # Check to see if object recognition is enabled before displaying the object recognition option.
            print("2. Manage object recognition data")
        else:
            print(style.faint + "2. Manage object recognition data" + style.end)
        if (gpx_file != ""): # Check to see if a GPX correlation is enabled before displaying the position data option.
            print("3. Manage position data")
        else:
            print(style.faint + "3. Manage position data" + style.end)
        print("4. View session statistics")
        selection = prompt("Selection: ", optional=False, input_type=str)


        if (selection == "0"): # If the user selects option 0 on the main menu, then exit Predator.
            print("Shutting down...")
            break

        elif (selection == "1"): # If the user selects option 1 on the main menu, then load the license pl atedata viewing menu.
            print("    Please select an option")
            print("    0. Back")
            print("    1. View data")
            print("    2. Export data")
            selection = prompt("    Selection: ", optional=False, input_type=str)

            if (selection == "1"): # The user has opened the license plate data viewing menu.
                print("        Please select an option")
                print("        0. Back")
                print("        1. View as Python data")
                print("        2. View as list")
                print("        3. View as CSV")
                print("        4. View as JSON data")
            
                selection = prompt("        Selection: ", optional=False, input_type=str)

                if (selection == "0"):
                    print("Returning to main menu.")
                elif (selection == "1"): # The user has selected to view license plate data as Python data.
                    print(str(plates_detected))
                elif (selection == "2"): # The user has selected to view license plate data as a list.
                    for plate in plates_detected:
                        print(plate)
                elif (selection == "3"): # The user has selected to view license plate data as CSV data.
                    csv_data = ""
                    for plate in plates_detected: # Iterate through each of the plates detected.
                        csv_data = csv_data + plate + ","
                    print(csv_data[:-1]) # Print the CSV data without the last character, since it will always be a comma.
                elif (selection == "4"): # The user has selected to view license plate data as raw JSON data.
                    print("            Please select an option")
                    print("            0. Back")
                    print("            1. View all")
                    print("            2. View validated")
                    print("            3. View alerts")
                
                    selection = prompt("            Selection: ", optional=False, input_type=str)

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"): # The user has selected to view all license plate data as JSON.
                        print(json.dumps(alpr_frames))
                    elif (selection == "2"): # The user has selected to view validated license plate data as JSON.
                        print(json.dumps(validated_alpr_frames))
                    elif (selection == "3"): # The user has selected to view validated license plate data as JSON.
                        print(json.dumps(active_alerts))
                    else:
                        display_message("Invalid selection.", 2)
                else:
                    display_message("Invalid selection.", 2)

            elif (selection == "2"): # The user has opened the license plate data exporting menu.
                print("        Please select an option")
                print("        0. Back")
                print("        1. Export as Python data")
                print("        2. Export as list")
                print("        3. Export as CSV")
                print("        4. Export as JSON")
                selection = prompt("        Selection: ", optional=False, input_type=str)

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
                elif (selection == "4"): # The user has selected to export license plate data as JSON data.
                    print("            Please select an option")
                    print("            0. Back")
                    print("            1. Export all")
                    print("            2. Export validated")
                    print("            3. Export alerts")
                
                    selection = prompt("            Selection: ", optional=False, input_type=str)

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"): # The user has selected to export all license plate data as JSON.
                        save_to_file(root + "/pre_recorded_license_plate_export.json", json.dumps(alpr_frames), silence_file_saving) # Save the raw license plate analysis data to disk.
                    elif (selection == "2"): # The user has selected to export validated license plate data as JSON.
                        save_to_file(root + "/pre_recorded_license_plate_export.json", json.dumps(validated_alpr_frames), silence_file_saving) # Save the validated license plate analysis data to disk.
                    elif (selection == "3"): # The user has selected to alert license plate data as JSON.
                        save_to_file(root + "/pre_recorded_license_plate_export.json", json.dumps(active_alerts), silence_file_saving) # Save detected license plate alerts to disk.
                    else:
                        display_message("Invalid selection.", 2)
                else:
                    display_message("Invalid selection.", 2)

            prompt("\nPress enter to continue...", optional=True, input_type=str, default="") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "2"): # The user has selected to manage object recognition data.
            if (object_recognition_preference == True):
                print("    Please select an option")
                print("    0. Back")
                print("    1. View data")
                print("    2. Export data")
                selection = prompt("    Selection: ", optional=False, input_type=str)

                if (selection == "1"): # The user has selected to view object recognition data.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. View as Python data")
                    print("        2. View as JSON data")
                    selection = prompt("        Selection: ", optional=False, input_type=str)

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        print(object_count)
                    elif (selection == "2"):
                        print(json.dumps(object_count, indent=4))
                    else:
                        display_message("Invalid selection.", 2)

                elif (selection == "2"): # The user has selected to export object recognition data.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. Export as Python data")
                    print("        2. Export as JSON data")
                    selection = prompt("Selection: ", optional=False, input_type=str)

                    if (selection == "0"):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        save_to_file(root + "/pre_recorded_object_detection_export.txt", str(object_count), silence_file_saving) # Save to disk.
                    elif (selection == "2"):
                        save_to_file(root + "/pre_recorded_object_detection_export.json", json.dumps(object_count, indent=4), silence_file_saving) # Save to disk.
                    else:
                        display_message("Invalid selection.", 2)

                else: # The user has selected an invalid option in the object recognition data management menu.
                    display_message("Invalid selection.", 2)

            else: # The user has selected the object recognition data management menu, but object recognition has been disabled.
                display_message("Object recognition has been disabled. There is no object recogntion data to manage.", 2)

            prompt("\nPress enter to continue...", optional=True, input_type=str, default="") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "3"): # The user has selected to manage GPX location information.
            if (gpx_file != ""): # Check to see if a GPX file was provided for analysis.
                print("    Please select an option")
                print("    0. Back")
                print("    1. View data")
                print("    2. Export data")
                selection = prompt("    Selection: ", optional=False, input_type=str)

                if (selection == "0"):
                    print("Returning to main menu.")
                elif (selection == "1"): # The user has selected to view GPX location information.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. View as Python data")
                    print("        2. View as JSON data")
                    selection = prompt("        Selection: ", optional=False, input_type=str)

                    if (selection == 0):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        print(frame_locations)
                    elif (selection == "2"):
                        print(json.dumps(frame_locations, indent=4))
                    else:
                        display_message("Invalid selection.", 2)

                elif (selection == "2"): # The user has selected to export GPX location information.
                    print("        Please select an option")
                    print("        0. Back")
                    print("        1. Export as Python data")
                    print("        2. Export as JSON data")
                    selection = prompt("        Selection: ", optional=False, input_type=str)

                    if (selection == 0):
                        print("Returning to main menu.")
                    elif (selection == "1"):
                        save_to_file(root + "/pre_recorded_location_data_export.txt", frame_locations, silence_file_saving) # Save to disk.
                    elif (selection == "2"):
                        save_to_file(root + "/pre_recorded_location_data_export.json", json.dumps(frame_locations, indent=4), silence_file_saving) # Save to disk.
                    else:
                        display_message("Invalid selection.", 2)

                else:
                    display_message("Invalid selection.", 2)

            else:
                display_message("GPX processing has been disabled since a GPX file wasn't provided. There is no GPX location data to manage.", 2)

            prompt("\nPress enter to continue...", optional=True, input_type=str, default="") # Wait for the user to press enter before repeating the menu loop.


        elif (selection == "4"): # If the user selects option 4 on the main menu, then show the statstics for this session.
            print("    Frames analyzed: " + str(len(alpr_frames))) # Show how many frames of video were analyzed.
            print("    Plates found: " + str(len(plates_detected))) # Show how many unique plates were detected.
            print("    Videos analyzed: " + str(len(videos))) # Show how many videos were analyzed.
            print("    Alerts detected: " + str(len(active_alerts))) # Show how many videos were analyzed.
            prompt("\nPress enter to continue...", optional=True, input_type=str, default="") # Wait for the user to press enter before repeating the menu loop.


        else: # If the user selects an unrecognized option on the main menu for pre-recorded mode, then show a warning.
            display_message("Invalid selection.", 2)
            prompt("\nPress enter to continue...", optional=True, input_type=str, default="") # Wait for the user to press enter before repeating the menu loop.









# Real-time mode

elif (mode_selection == "2" and realtime_mode_enabled == True): # The user has set Predator to boot into real-time mode.
    # Configure the user's preferences for this session.
    if (default_root != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    while (os.path.exists(root) == False): # Run forever until the user enters a project directory that exists.
        display_message("The root project directory entered doesn't seem to exist.", 2)
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    if (default_license_plate_format != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for license plate formatting." + style.end)
        if (default_license_plate_format == " "): # If the default license plate format is configured as a single space, then skip the prompt, but don't load a license format guideline.
            license_plate_format = ""
        else:
            license_plate_format = default_license_plate_format
    else:
        license_plate_format = prompt("Optional: License plate validation format: ", optional=True, input_type=str, default="")

    if (default_save_license_plates_preference != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for license plate saving." + style.end)
        save_license_plates_preference = default_save_license_plates_preference
    else:
        save_license_plates_preference = prompt("Optional: Enable license plate saving (y/n): ", optional=True, input_type=bool, default=False)

    if (default_save_images_preference != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for image saving." + style.end)
        save_images_preference = default_save_images_preference
    else:
        save_images_preference = prompt("Optional: Enable image saving: (y/n): ", optional=True, input_type=bool, default=False)


    if (disable_object_recognition == True): # Check to see whether or not object recognition has been globally disabled in the Predator configuration.
        realtime_object_recognition = "n" # Automatically reject the realtime object recognition prompt.
    else:
        if (default_realtime_object_recognition != ""): # Check to see if the user has configured a default for this preference.
            print(style.bold + "Using default preference for real-time object recognition." + style.end)
            if (default_realtime_object_recognition != ""):
                realtime_object_recognition = default_realtime_object_recognition
        else:
            realtime_object_recognition = prompt("Enable real-time object recognition? (y/n): ", optional=True, input_type=bool, default=False)



    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        display_message("The root project directory entered doesn't seem to exist. Predator will almost certainly fail.", 3)



    
    if (dashcam_background_mode_realtime == True): # Check to see if the user has enabled auto dashcam background recording in real-time mode.
        start_dashcam(dashcam_device, int(config["dashcam"]["segment_length"]), config["dashcam"]["dashcam_resolution"], config["dashcam"]["dashcam_frame_rate"], root, True) # Start the dashcam recording process.

        print("Started background dash-cam recording.")


    # Load the license plate alert database.
    alert_database = load_alert_database(license_plate_alert_database_source, root)


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






        if (manual_trigger == True): # If the manual trigger configuration value is enabled, then wait for the user to press enter before continuing.
            prompt("Press enter to trigger image capture...", optional=True, input_type=str, default="")



        # Take an image using the camera device specified in the configuration.
        if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
            print("Taking image...")
        if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
            fswebcam_command = "fswebcam --no-banner -r " + camera_resolution + " -d " + fswebcam_device + " --jpeg 100 " + fswebcam_flags + " " + root + "/realtime_image" + str(i) + ".jpg >/dev/null 2>&1" # Set up the FSWebcam capture command.
        else:
            fswebcam_command = "fswebcam --no-banner -r " + camera_resolution + " -d " + fswebcam_device + " --jpeg 100 " + fswebcam_flags + " " + root + "/realtime_image.jpg >/dev/null 2>&1" # Set up the FSWebcam capture command.

        os.system(fswebcam_command) # Take a photo using FSWebcam, and save it to the root project folder specified by the user.

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
            if (config["general"]["alpr_engine"] == "phantom"): # Check to see if the configuration indicates that the Phantom ALPR engine should be used.
                analysis_command = "alpr -n " + str(config["general"]["alpr_guesses"])  + " '" + root + "/realtime_image" + str(i) + ".jpg'" # Prepare the analysis command so we can run it next.
            elif (config["general"]["alpr_engine"] == "openalpr"): # Check to see if the configuration indicates that the OpenALPR engine should be used.
                analysis_command = "alpr -j -n " + str(config["general"]["alpr_guesses"]) + " '" + root + "/realtime_image" + str(i) + ".jpg'" # Prepare the analysis command so we can run it next.
            else:
                display_message("The configured ALPR engine is not recognized.", 3)
        else:
            if (config["general"]["alpr_engine"] == "phantom"): # Check to see if the configuration indicates that the Phantom ALPR engine should be used.
                analysis_command = "alpr -n " + str(config["general"]["alpr_guesses"]) + " '" + root + "/realtime_image.jpg'" # Prepare the analysis command so we can run it next.
            elif (config["general"]["alpr_engine"] == "openalpr"): # Check to see if the configuration indicates that the OpenALPR engine should be used.
                analysis_command = "alpr -j -n " + str(config["general"]["alpr_guesses"]) + " '" + root + "/realtime_image.jpg'" # Prepare the analysis command so we can run it next.
            else:
                display_message("The configured ALPR engine is not recognized.", 3)

        i = i + 1 # Increment the counter for this cycle so we can count how many images we've analyzed during this session.
        new_plates_detected = [] # This variable will be used to determine whether or not a plate was detected this round. If no plate is detected, this will remain blank. If a plate is detected, it will change to be that plate. This is used to determine whether or not the database of detected plates needs to updated.

        raw_reading_output = str(os.popen(analysis_command).read()) # Run the ALPR command, and save it's output to reading_output.

        try: # Run the JSON interpret command inside a 'try' block so the entire program doesn't fatally crash if the JSON data is malformed.
            reading_output = json.loads(raw_reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
        except:
            reading_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":1920,"img_height":1080,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":1920,"height":1080}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since the actual reading output was malformed.
            display_message("The JSON data returned by the ALPR process is malformed. This likely means there's a problem with the ALPR library.", 3)

        if (config["general"]["alpr_engine"] == "phantom"): # Check to see if the configured ALPR engine is Phantom ALPR.
            if ("error" in raw_reading_output): # Check to see if there were errors reported by Phantom ALPR.
                print("Phantom ALPR encountered an error: " + reading_output["error"]) # Display the ALPR error.
                reading_output["results"] = [] # Set the results of the reading output to a blank placeholder list.





        # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
        all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
        for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
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






        # Reset the status lighting to normal before processing the license plate data from ALPR.
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
                    new_plates_detected.append(detected_plate) # Save the most likely license plate ID to this round's new_plates_detected list.
                    if (realtime_output_level >= 2): # Only display this status message if the output level indicates to do so.
                        print("Detected Plate: " + detected_plate) # Print the detected plate.

                    play_sound("notification")

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

        active_alerts = {} # This is a placeholder dictionary that will hold all of the active alerts.

        if (alerts_ignore_validation == True): # If the user has enabled alerts that ignore license plate validation, then check each of the ALPR guesses against the license plate alert database.
            for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                for plate in all_current_plate_guesses: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                    for guess in all_current_plate_guesses[plate]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                        if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                            active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                            active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                            break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

        else: #  If the user has disabled alerts that ignore license plate validation, then only check the validated plate array against the alert database.
            for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                for plate in new_plates_detected: # Iterate through each plate that was detected and validated this round.
                    if (fnmatch.fnmatch(plate, rule)): # Check to see the validated detected plate matches this particular plate in the alert database, taking wildcards into account.
                        active_alerts[plate] = alert_database[rule] # Add this plate to the active alerts dictionary.
                        active_alerts[plate]["rule"] = rule # Add the rule that triggered this alert to the alert information.


        if (len(active_alerts) > 0): # Check to see if there are any active alerts to see if an alert state should be triggered.
            if (status_lighting_enabled == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                update_status_lighting("alert") # Run the function to update the status lighting.

            if (realtime_output_level >= 1): # Only display alerts if the configuration specifies to do so.
                display_alerts(active_alerts) # Display all active alerts.

            for alert in active_alerts: # Run once for each active alert.
                if (push_notifications_enabled == True): # Check to see if the user has Gotify notifications enabled.
                    os.system("curl -X POST '" + gotify_server + "/message?token=" + gotify_application_token + "' -F 'title=Predator' -F 'message=A license plate in the alert database has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.

                if (shape_alerts == True): # Check to see if the user has enabled shape notifications.
                    display_shape("triangle") # Display an ASCII triangle in the output.

                play_sound("alert") # Play the alert sound, if configured to do so.


        if (realtime_output_level >= 3): # Only display this status message if the output level indicates to do so.
            print("Done.\n----------")




        # If enabled, submit data about each newly detected plate to a network server.
        if (realtime_output_level >= 3 and webhook != None and webhook != ""): # Only display this status message if the output level indicates to do so, and webhooks are enabled.
            print("Submitting data to webhook...")

        for plate in new_plates_detected: # Iterate through each plate that was detected this round.
            if (webhook != None and webhook != ""): # Check to see if the user has specified a webhook to submit detected plates to.
                url = webhook.replace("[L]", plate) # Replace "[L]" with the license plate detected.
                url = url.replace("[T]", str(round(time.time()))) # Replace "[T]" with the current timestamp, rounded to the nearest second.
                url = url.replace("[A]", str(plate in active_alerts)) # Replace "[A]" with the current alert status.

                try: # Try sending a request to the webook.
                    response = requests.get(url, timeout=4)
                except Exception as e:
                    response = e

                if (str(webhook_response) != "200"): # If the webhook didn't respond with a 200 code; Warn the user that there was an error.
                    display_message("Failed to submit data to webhook.", 2)

        if (realtime_output_level >= 3 and webhook != None and webhook != ""): # Only display this status message if the output level indicates to do so, and webhooks are enabled.
            print("Done.\n----------")





        # If enabled, save the detected license plate (if any) to a file on disk.
        if (realtime_output_level >= 3 and save_license_plates_preference == True): # Only display this status message if the output level indicates to do so.
            print("Saving license plate data to disk...")

        if (save_license_plates_preference == True): # Check to see if the user has the 'save detected license plates' preference enabled.
            if (len(new_plates_detected) > 0): # Check to see if the new_plates_detected value is empty. If it is blank, that means no new plate was detected this round.
                for plate in new_plates_detected: # Iterate through each plate that was detected this round.
                    if (alpr_location_tagging == True and gps_enabled == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                        current_location = get_gps_location() # Get the current location.
                        export_data = plate + "," + str(round(time.time())) + "," + str(plate in active_alerts).lower() + "," + str(current_location[0]) + "," + str(current_location[1]) + "\n" # Add the individual plate to the export data.
                    else:
                        export_data = plate + "," + str(round(time.time())) + "," + str(plate in active_alerts).lower() + ",0.000,0.000\n" # Add the individual plate to the export data.
                    add_to_file(root + "/real_time_plates.csv", export_data, silence_file_saving) # Add the export data to the end of the file and write it to disk.

        if (realtime_output_level >= 3 and save_license_plates_preference == True): # Only display this status message if the output level indicates to do so.
            print("Done.\n----------")

        if (len(active_alerts) > 0): # Check to see if there are one or more active alerts.
            time.sleep(float(config["realtime"]["delay_on_alert"])) # Trigger delay on alert.










# Dash-cam mode

elif (mode_selection == "3" and dashcam_mode_enabled == True): # The user has set Predator to boot into dash-cam mode.

    # Configure the user's preferences for this session.
    if (default_root != ""): # Check to see if the user has configured a default for this preference.
        print(style.bold + "Using default preference for root directory." + style.end)
        root = default_root
    else:
        root = prompt("Project root directory path: ", optional=False, input_type=str)

    while (os.path.exists(root) == False): # Run forever until the user enters a project directory that exists.
        display_message("The root project directory entered doesn't seem to exist.", 2)
        root = prompt("Project root directory path: ", optional=False, input_type=str)


    print("\nStarting dashcam recording at " + dashcam_resolution + "@" + dashcam_frame_rate + "fps") # Print information about the recording settings.
    start_dashcam(dashcam_device, int(config["dashcam"]["segment_length"]), config["dashcam"]["dashcam_resolution"], config["dashcam"]["dashcam_frame_rate"], root, False) # Start the dashcam recording process.






else: # The user has selected an unrecognized mode.
    display_message("The selected mode is invalid.", 3)
