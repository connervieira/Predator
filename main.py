# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





print("Loading Predator...")
import global_variables
global_variables.init()

import os # Required to interact with certain operating system functions
import json # Required to process JSON data



import config
load_config = config.load_config
validate_config = config.validate_config

config = load_config()

predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

import time # Required to add delays and handle dates/times.
import sys # Required to read command line arguments.

if ("--help" in sys.argv):
    print("\npython3 main.py [MODE] [DIRECTORY] [OPTIONS]")
    print("    MODE is the number representing operating mode Predator will use.")
    print("        0\t\tManagement Mode")
    print("        1\t\tPre-recorded Mode")
    print("        2\t\tReal-time Mode")
    print("        3\t\tDash-cam Mode")
    print("    DIRECTORY specifies the working directory Predator will use.")
    print("    OPTIONS is any number of command-line options from the list below.")
    print("        --headless\tenables headless mode, where all user prompts are skipped")
    print("        --help\t\tdisplays this help message, then exits")

    global_variables.predator_running = False
    exit()

import utils # Import the utils.py scripts.
style = utils.style # Load the style from the utils script.
debug_message  = utils.debug_message # Load the debug message function from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
prompt = utils.prompt # Load the user input prompt function from the utils script.
is_json = utils.is_json # Load the function used to determine if a given string is valid JSON.
display_message = utils.display_message # Load the message display function from the utils script.
process_gpx = utils.process_gpx # Load the GPX processing function from the utils script.
save_to_file = utils.save_to_file # Load the file saving function from the utils script.
add_to_file = utils.add_to_file # Load the file appending function from the utils script.
display_shape = utils.display_shape # Load the shape displaying function from the utils script.
countdown = utils.countdown # Load the timer countdown function from the utils script.
get_gps_location = utils.get_gps_location # Load the function to get the current GPS location.
convert_speed = utils.convert_speed # Load the function used to convert speeds from meters per second to other units.
display_number = utils.display_number # Load the function used to display numbers as large ASCII font.
closest_key = utils.closest_key # Load the function used to find the closest entry in a dictionary to a given number.
heartbeat = utils.heartbeat # Load the function to issue heartbeats to the interface directory.
update_state = utils.update_state # Load the function to issue state updates to the interface directory.
log_plates = utils.log_plates # Load the function to issue ALPR results to the interface directory.
log_alerts = utils.log_alerts # Load the function to issue active alerts to the interface directory.

import re # Required to use Regex.
import datetime # Required for converting between timestamps and human readable date/time information.
import fnmatch # Required to use wildcards to check strings.

if (config["general"]["modes"]["enabled"]["realtime"] == True):
    import alpr
    display_alerts = alpr.display_alerts # Load the function used to display license plate alerts given the dictionary of alerts.

if (config["general"]["modes"]["enabled"]["dashcam"] == True): # Check to see if OpenCV is needed.
    import dashcam

if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    if (config["general"]["status_lighting"]["enabled"] == True or config["realtime"]["push_notifications"]["enabled"] == True or len(config["general"]["alerts"]["databases"]) > 0): # Only import networking libraries if they are necessary.
        debug_message("Loading networking libraries")
        import requests # Required to make network requests.
        import validators # Required to validate URLs.

if (config["management"]["disk_statistics"] == True): # Only import the disk statistic library if it is enabled in the configuration.
    debug_message("Loading system utility library")
    import psutil # Required to get disk usage information



if (os.path.exists(predator_root_directory + "/install.json") == False): # Check to see if the install information file hasn't yet been created. This will be the case on the first start-up.
    import uuid
    install_data = {"first_start_time": int(time.time()), "id": str(uuid.uuid4())}
    clear()
    print(style.bold + style.red + "Predator - First Start" + style.end)
    print(style.italic + "This wizard is only displayed on the first start of Predator.")
    print("To reset so this message is displayed again, remove the `install.json` file inside the main install directory." + style.end)
    input(style.faint + "Press enter to continue..." + style.end)

    clear()
    print(style.bold + style.red + "Commercial Support" + style.end)
    print(style.bold + "V0LT offers the following commercial support services for Predator:" + style.end)
    print("  * Custom software modifications")
    print("  * Pre-assembled hardware products and kits")
    print("  * One-on-one technical support")
    print("  * Server hosting")
    print("    - Remotely-managed hot-lists and ignore-lists")
    print("    - Compiled data reports")
    print("    - Remote ALPR processing")
    print()
    print("To learn more, don't hesitate to get in contact: " + style.underline + "https://v0lttech.com/contact.php\n" + style.end)
    input(style.faint + "Press enter to continue..." + style.end)

    clear()
    print(style.bold + style.red + "Warranty" + style.end)
    print("While Predator is designed to be as reliable and consistent as possible, it comes with absolutely no warranty, it should not be used in a context where failure could cause harm to people or property.")
    print("For more information, see the `SECURITY.md` document.")
    input(style.faint + "Press enter to continue..." + style.end)

    clear()
    print(style.bold + style.red + "Privacy" + style.end)
    print("Predator does not share telemetry or usage data with V0LT, or any other entity. However, by default, Predator will attach a random identifier to requests made to remote license plate list sources (as configured under `general>alerts>databases`). This identifier allows administrators of servers hosting license plate lists to roughly count how many clients are using their lists. If you're concerned about the administrator of one of your remote license plate lists using this unique identifier to derive information about how often you use Predator (based on when you fetch their lists), you can disable this functionality using the `developer>identify_to_remote_sources` configuration value.")
    print("Additionally, by default, Predator will fetch a hardcoded ignore list from the V0LT website. This functionality does not send any identifiable information or telemetry data (even when identify_to_remote_sources is enabled). To disable this functionality, either enable the `developer>offline` configuration value to disable all network requests, or remove the hardcoded ignore list from `ignore.py`.")
    print("For more information, see the `docs/CONFIGURE.md` document.")
    input(style.faint + "Press enter to continue..." + style.end)

    clear()
    print(style.bold + style.red + "Funding" + style.end)
    print("Predator is completely free to use, and doesn't contain monetization like advertising or sponsorships. If you find the project to be useful, please consider supporting it financially.")
    print("For more information, see `https://v0lttech.com/donate.php`.")
    input(style.faint + "Press enter to continue..." + style.end)


    with open(predator_root_directory + "/install.json", 'w') as file:
        json.dump(install_data, file)


    print("")
    clear()
    print("The initial start-up process has completed. Predator will now return to the normal start-up sequence.")
    input(style.faint + "Press enter to continue..." + style.end)




debug_message("Loading ignore lists")
import ignore # Import the library to handle license plates in the ignore list.
ignore_list = ignore.fetch_ignore_list() # Fetch the ignore lists.


debug_message("Validating configuration values")
invalid_configuration_values = validate_config(config) # Validation the configuration, and display any potential problems.
for entry in invalid_configuration_values: # Iterate through each invalid configuration value in the list.
    display_message("Invalid configuration value: " + entry, 3) # Print each invalid configuration value as an error.
del invalid_configuration_values # Delete the variable holding the list of invalid configuration_values.
debug_message("Validated configuration values")


if (config["developer"]["offline"] == True): # If offline mode is enabled, then disable all network based features.
    config["realtime"]["push_notifications"]["enabled"] = False
    config["realtime"]["push_notifications"]["server"] = "" # This is redundant, since 'realtime>push_notifications>enabled' is disabled, but it serves as a backup.
    config["general"]["status_lighting"]["enabled"] = False
    config["developer"]["remote_sources"] = []



heartbeat() # Issue an initial heartbeat at start-up.


import lighting # Import the lighting.py script.
update_status_lighting = lighting.update_status_lighting # Load the status lighting update function from the lighting script.








debug_message("Initial loading complete")

# Display the start-up intro header.
clear()
if (config["general"]["display"]["ascii_art_header"] == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
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
    print("                                 COMPUTER VISION")
    if (config["general"]["display"]["startup_message"] != ""): # Only display the line for the custom message if the user has defined one.
        print("")
        print(config["general"]["display"]["startup_message"]) # Show the user's custom defined start-up message.
    print(style.end)
else: # If the user his disabled the large ASCII art header, then show a simple title header with minimal styling.
    print(style.red + style.bold + "PREDATOR" + style.end)
    print(style.bold + "Computer Vision" + style.end + "\n")
    if (config["general"]["display"]["startup_message"]!= ""): # Only display the line for the custom message if the user has defined one.
        print(config["general"]["display"]["startup_message"]) # Show the user's custom defined start-up message.

utils.play_sound("startup")

if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has push notifications enabled.
    debug_message("Issuing start-up push notification")
    os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=Predator has been started.' > /dev/null 2>&1 &") # Send a push notification via Gotify indicating that Predator has started.



# Run some basic error checks to see if any of the data supplied in the configuration seems wrong.
debug_message("Validating configuration")
config["general"]["alpr"]["engine"] = config["general"]["alpr"]["engine"].lower().strip() # Convert the ALPR engine configuration value to all lowercase, and trim leading and trailing white-spaces.
if (config["general"]["alpr"]["engine"] != "phantom" and config["general"]["alpr"]["engine"] != "openalpr"): # Check to see if the configured ALPR engine is invalid.
    display_message("The configured ALPR engine is invalid. Please select either 'phantom' or 'openalpr' in the configuration.", 3)

if (os.path.isdir(config["general"]["working_directory"]) == False): # Check to see if the configured working directory is missing.
    display_message("The 'general>working_directory' configuration value does not point to an existing directory.", 3)
elif ("'" in config["general"]["working_directory"]):
    display_message("The 'general>working_directory' configuration value contains an apostrophe. This will likely cause unexpected behavior.", 3)
elif ("\"" in config["general"]["working_directory"]):
    display_message("The 'general>working_directory' configuration value contains a quotation mark. This will likely cause unexpected behavior.", 3)

if (os.path.isdir(config["general"]["interface_directory"]) == False and config["general"]["interface_directory"] != ""): # Check to see if the configured interface directory is missing.
    display_message("The 'general>interface_directory' configuration value does not point to an existing directory.", 3)
elif ("'" in config["general"]["interface_directory"]):
    display_message("The 'general>interface_directory' configuration value contains an apostrophe. This will likely cause unexpected behavior.", 3)
elif ("\"" in config["general"]["interface_directory"]):
    display_message("The 'general>interface_directory' configuration value contains a quotation mark. This will likely cause unexpected behavior.", 3)

if (config["prerecorded"]["image"]["processing"]["cropping"]["left_margin"] < 0 or config["prerecorded"]["image"]["processing"]["cropping"]["right_margin"] < 0 or config["prerecorded"]["image"]["processing"]["cropping"]["bottom_margin"] < 0 or config["prerecorded"]["image"]["processing"]["cropping"]["top_margin"] < 0): # Check to make sure that all of the pre-recorded mode cropping margins are positive numbers.
    display_message("One or more of the cropping margins for pre-recorded mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping margins have all been set to 0.", 3)
    config["prerecorded"]["image"]["processing"]["cropping"]["left_margin"] = 0
    config["prerecorded"]["image"]["processing"]["cropping"]["right_margin"] = 0
    config["prerecorded"]["image"]["processing"]["cropping"]["bottom_margin"] = 0
    config["prerecorded"]["image"]["processing"]["cropping"]["top_margin"] = 0




if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications turned on in the configuration.
    if (config["realtime"]["push_notifications"]["server"] == "" or config["realtime"]["push_notifications"]["server"] == None): # Check to see if the gotify server configuration value has been left blank
        display_message("The 'realtime>push_notifications>enabled' setting is turned on, but the 'realtime>push_notifications>server' hasn't been set. Push notifications have been disabled.", 3)
        config["realtime"]["push_notifications"]["enabled"] = False
    if (config["realtime"]["push_notifications"]["token"] == "" or config["realtime"]["push_notifications"]["token"] == None): # Check to see if the Gotify application token has been left blank.
        display_message("The 'realtime>push_notifications>token' setting is turned on, but the 'realtime>push_notifications>token' hasn't been set. Push notifications have been disabled.", 3)
        config["realtime"]["push_notifications"]["enabled"] = False



# Figure out which mode to boot into.
print("Please select an operating mode.")
if (config["general"]["modes"]["enabled"]["management"] == True): # Only show the management mode option if it's enabled in the configuration.
    print("0. Management")
if (config["general"]["modes"]["enabled"]["prerecorded"] == True): # Only show the pre-recorded mode option if it's enabled in the configuration.
    print("1. Pre-recorded")
if (config["general"]["modes"]["enabled"]["realtime"] == True): # Only show the real-time mode option if it's enabled in the configuration.
    print("2. Real-time")
if (config["general"]["modes"]["enabled"]["dashcam"] == True): # Only show the dash-cam mode option if it's enabled in the configuration.
    print("3. Dash-cam")

# Check to see if the auto_start_mode configuration value is an expected value. If it isn't execution can continue, but the user will need to manually select what mode Predator should start in.
config["general"]["modes"]["auto_start"] = str(config["general"]["modes"]["auto_start"]) # Make sure the "general>modes>auto_start" configuration value is a string.
if (config["general"]["modes"]["auto_start"] != "" and config["general"]["modes"]["auto_start"] != "0" and config["general"]["modes"]["auto_start"] != "1" and config["general"]["modes"]["auto_start"] != "2" and config["general"]["modes"]["auto_start"]!= "3"):
    display_message("The 'auto_start_mode' configuration value isn't properly set. This value should be blank, '0', '1', '2', or '3'. It's possible there's been a typo.", 3)

if (len(sys.argv) > 1): # Check to see if there is at least 1 command line argument.
    if (sys.argv[1] == "0" or sys.argv[1] == "1" or sys.argv[1] == "2" or sys.argv[1] == "3"): # Check to see if a mode override was specified in the Predator command arguments.
        config["general"]["modes"]["auto_start"] = sys.argv[1] # Set the automatic start mode to the mode specified by the command line argument.

if (len(sys.argv) > 2): # Check to see if there are at least 2 command line arguments.
    if (sys.argv[2] not in ["--headless", "--help"]):
        config["general"]["working_directory"] = str(sys.argv[2]) # Set the working directory to the path specified by the command line argument.


if (config["general"]["modes"]["auto_start"] == "0" and config["general"]["modes"]["enabled"]["management"] == True): # Based on the configuration, Predator will automatically boot into management mode.
    print(style.bold + "Automatically starting into management mode." + style.end)
    mode_selection = "0"
elif (config["general"]["modes"]["auto_start"] == "1" and config["general"]["modes"]["enabled"]["prerecorded"] == True): # Based on the configuration, Predator will automatically boot into pre-recorded mode.
    print(style.bold + "Automatically starting into pre-recorded mode." + style.end)
    mode_selection = "1"
elif (config["general"]["modes"]["auto_start"] == "2" and config["general"]["modes"]["enabled"]["realtime"] == True): # Based on the configuration, Predator will automatically boot into real-time mode.
    print(style.bold + "Automatically starting into real-time mode." + style.end)
    mode_selection = "2"
elif (config["general"]["modes"]["auto_start"] == "3" and config["general"]["modes"]["enabled"]["dashcam"] == True): # Based on the configuration, Predator will automatically boot into dash-cam mode.
    print(style.bold + "Automatically starting into dash-cam mode." + style.end)
    mode_selection = "3"
else: # No 'auto start mode' has been configured, so ask the user to select manually.
    mode_selection = prompt("Selection: ")





# Initial setup has been completed, and Predator will now load into the specified mode.









# Management mode

if (mode_selection == "0" and config["general"]["modes"]["enabled"]["management"] == True): # The user has selected to boot into management mode.
    debug_message("Started management mode")


    working_directory_input = prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)
    if (working_directory_input == ""): # If the user leaves the 
        working_directory_input = config["general"]["working_directory"]

    while (os.path.exists(working_directory_input) == False): # Run forever until the user enters a working directory that exists.
        display_message("The specified working directory doesn't seem to exist.", 2)
        working_directory_input = prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)

    config["general"]["working_directory"] = working_directory_input



    while global_variables.predator_running:
        clear()
        print("Please select an option")
        print("0. Quit")
        print("1. File Management")
        print("2. Information")
        print("3. Configuration")

        selection = prompt("Selection: ", optional=False, input_type=str)

        if (selection == "0"): # The user has selected the "Quit" option.
            global_variables.predator_running = False
        elif (selection == "1"): # The user has selected the "File Management" option.
            print("    Please select an option")
            print("    0. Back")
            print("    1. View")
            print("    2. Copy")
            print("    3. Delete")
            selection = prompt("    Selection: ", optional=False, input_type=str)

            if (selection == "0"): # The user has selected to return back to the previous menu.
                continue # Do nothing, and just finish this loop.
            elif (selection == "1"): # The user has selected the "view files" option.
                os.system("find " + config["general"]["working_directory"]) # Run the 'find' command in the working directory.
                utils.wait_for_input()
            elif (selection == "2"): # The user has selected the "copy files" option.

                # Reset all of the file selections to un-selected.
                copy_management_configuration = False
                copy_prerecorded_processed_frames = False
                copy_prerecorded_gpx_files = False
                copy_prerecorded_license_plate_analysis_data = False
                copy_prerecorded_license_plate_location_data = False
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
                    if (copy_prerecorded_license_plate_location_data == True):
                        print("P5. [X] License plate location data files")
                    else:
                        print("P5. [ ] License plate location data files")
                    print("")
                    print("===== Real-time Mode =====")
                    if (copy_realtime_license_plate_recognition_data == True):
                        print("R1. [X] License plate recognition data files")
                    else:
                        print("R1. [ ] License plate recognition data files")
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
                        copy_prerecorded_license_plate_location_data = not copy_prerecorded_license_plate_location_data
                    elif (selection.lower() == "r1"):
                        copy_realtime_license_plate_recognition_data = not copy_realtime_license_plate_recognition_data
                    elif (selection.lower() == "d1"):
                        copy_dashcam_video = not copy_dashcam_video
                

                # Prompt the user for the copying destination.
                copy_destination = "" # Set the copy_destination as a blank placeholder.
                while os.path.isdir(copy_destination) == False: # Repeatedly ask the user for a valid copy destination until they enter one that is valid.
                    copy_destination = prompt("Destination directory: ", optional=False, input_type=str) # Prompt the user for a destination path.
                    if (os.path.isdir(copy_destination) == False):
                        display_message("The specified destination is not a valid directory.", 2)


                # Copy the files as per the user's inputs.
                print("Copying files...")
                if (copy_management_configuration):
                    os.system("cp \"" + predator_root_directory + "/config.json\" \"" + copy_destination + "\"")
                if (copy_prerecorded_processed_frames):
                    os.system("cp -r \"" + config["general"]["working_directory"] + "/frames\" \"" + copy_destination + "\"")
                if (copy_prerecorded_gpx_files):
                    os.system("cp \"" + config["general"]["working_directory"] + "/*.gpx\" \"" + copy_destination + "\"")
                if (copy_prerecorded_license_plate_analysis_data):
                    os.system("cp \"" + config["general"]["working_directory"] + "/pre_recorded_license_plate_export.*\" \"" + copy_destination + "\"")
                if (copy_prerecorded_license_plate_location_data):
                    os.system("cp \"" + config["general"]["working_directory"] + "/pre_recorded_location_data_export.*\" \"" + copy_destination + "\"")
                if (copy_realtime_license_plate_recognition_data):
                    os.system("cp \"" + config["general"]["working_directory"] + "/real_time_plates*\" \"" + copy_destination + "\"")
                if (copy_dashcam_video):
                    os.system("cp \"" + os.path.join(config["general"]["working_directory"], "*Predator*." + config["dashcam"]["saving"]["file"]["extension"]) + "\" \"" + copy_destination + "\"")

                clear()
                print("Files have finished copying.")


            elif (selection == "3"): # The user has selected the "delete files" option.
                # Reset all of the file selections to un-selected.
                delete_management_custom = False
                delete_prerecorded_processed_frames = False
                delete_prerecorded_gpx_files = False
                delete_prerecorded_license_plate_analysis_data = False
                delete_prerecorded_license_plate_location_data = False
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
                    if (delete_prerecorded_license_plate_location_data == True):
                        print("P4. [X] License plate location data files")
                    else:
                        print("P4. [ ] License plate location data files")
                    print("")
                    print("===== Real-time Mode =====")
                    if (delete_realtime_license_plate_recognition_data == True):
                        print("R1. [X] License plate recognition data files")
                    else:
                        print("R1. [ ] License plate recognition data files")
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
                        delete_prerecorded_license_plate_location_data = not delete_prerecorded_license_plate_location_data
                    elif (selection.lower() == "r1"):
                        delete_realtime_license_plate_recognition_data = not delete_realtime_license_plate_recognition_data
                    elif (selection.lower() == "d1"):
                        delete_dashcam_video = not delete_dashcam_video

                if (delete_management_custom):
                    delete_custom_file_name = prompt("Please specify the name of the additional file you'd like to delete from the current working directory: ")

                # Delete the files as per the user's inputs, after confirming the deletion process.
                if (prompt("Are you sure you want to delete the selected files permanently? (y/n): ").lower() == "y"):
                    print("Deleting files...")
                    if (delete_management_custom):
                        os.system("rm -r \"" + config["general"]["working_directory"] + "/" + delete_custom_file_name + "\"")
                    if (delete_prerecorded_processed_frames):
                        os.system("rm -r \"" + config["general"]["working_directory"] + "/frames\"")
                    if (delete_prerecorded_gpx_files):
                        os.system("rm \"" + config["general"]["working_directory"] + "/*.gpx\"")
                    if (delete_prerecorded_license_plate_analysis_data):
                        os.system("rm \"" + config["general"]["working_directory"] + "/pre_recorded_license_plate_export.*\"")
                    if (delete_prerecorded_license_plate_location_data):
                        os.system("rm \"" + config["general"]["working_directory"] + "/pre_recorded_location_data_export.*\"")
                    if (delete_realtime_license_plate_recognition_data):
                        os.system("rm \"" + config["general"]["working_directory"] + "/real_time_plates*\"")
                    if (delete_dashcam_video):
                        os.system("rm \"" + os.path.join(config["general"]["working_directory"], "*Predator*." + config["dashcam"]["saving"]["file"]["extension"]) + "\"")
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
                continue # Do nothing, and just finish this loop.
            elif (selection == "1"): # The user has selected the "about" option.
                clear()
                print(style.bold + "============" + style.end)
                print(style.bold + "  Predator" + style.end)
                print(style.bold + "    V0LT" + style.end)
                print(style.bold + "    V9.0" + style.end)
                print(style.bold + "   AGPLv3" + style.end)
                print(style.bold + "============" + style.end)
            elif (selection == "2"): # The user has selected the "neofetch" option.
                os.system("neofetch") # Execute neofetch to display information about the system.
            elif (selection == "3"): # The user has selected the "print configuration" option.
                os.system("cat " + predator_root_directory + "/config.json") # Print out the raw contents of the configuration database.
            elif (selection == "4"): # The user has selected the "disk usage" option.
                if (config["management"]["disk_statistics"] == True): # Check to make sure disk statistics are enabled before displaying disk statistics.
                    print("Free space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).free)/1000000000)*100)/100) + "GB") # Display the free space on the storage device containing the current working directory.
                    print("Used space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).used)/1000000000)*100)/100) + "GB") # Display the used space on the storage device containing the current working directory.
                    print("Total space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).total)/1000000000)*100)/100) + "GB") # Display the total space on the storage device containing the current working directory.
                else: # Disk statistics are disabled, but the user has selected the disk usage option.
                    display_message("The disk usage could not be displayed because the 'disk_statistics' configuration option is disabled.", 2)
            else: # The user has selected an invalid option in the information menu.
                display_message("Invalid selection.", 2)

            utils.wait_for_input()
            


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
                                    if (selection4 in config[selection1][selection2][selection3]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                        if (type(config[selection1][selection2][selection3][selection4]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                            for section in config[selection1][selection2][selection3][selection4]: # Iterate through each fourth-level section of the configuration database, and display them all to the user.
                                                if (type(config[selection1][selection2][selection3][selection4][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                    print("                    '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                                else:
                                                    print("                    '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][selection4][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                            selection5 = prompt("=================== Selection (Tier 5): ", optional=False, input_type=str)
                                            if (selection5 in config[selection1][selection2][selection3][selection4]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                if (type(config[selection1][selection2][selection3][selection4][selection5]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                    for section in config[selection1][selection2][selection3][selection4][selection5]: # Iterate through each fifth-level section of the configuration database, and display them all to the user.
                                                        if (type(config[selection1][selection2][selection3][selection4][selection5][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                            print("                        '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                                        else:
                                                            print("                        '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                    selection6 = prompt("======================= Selection (Tier 6): ", optional=False, input_type=str)
                                                    if (selection6 in config[selection1][selection2][selection3][selection4][selection5]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                        if (type(config[selection1][selection2][selection3][selection4][selection5][selection6]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                            for section in config[selection1][selection2][selection3][selection4][selection5][selection6]: # Iterate through each sixth-level section of the configuration database, and display them all to the user.
                                                                if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                                    print("                            '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                                                else:
                                                                    print("                            '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][selection6][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                            selection7 = prompt("=========================== Selection (Tier 7): ", optional=False, input_type=str)
                                                            if (selection7 in config[selection1][selection2][selection3][selection4][selection5][selection6]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                                if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                                    for section in config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]: # Iterate through each sixth-level section of the configuration database, and display them all to the user.
                                                                        if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                                            print("                                '" + style.bold + str(section) + style.end + "'") # If the entry is a dictionary, display it in bold.
                                                                        else:
                                                                            print("                                '" + style.italic + str(section) + style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                                    selection8 = prompt("=============================== Selection (Tier 8): ", optional=False, input_type=str)
                                                                else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 7)
                                                                    print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]))
                                                                    config[selection1][selection2][selection3][selection4][selection5][selection6][selection7] = prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]), default="")
                                                            elif (selection7 != ""):
                                                                display_message("Unknown configuration entry selected.", 3)
                                                        else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 6)
                                                            print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5][selection6]))
                                                            config[selection1][selection2][selection3][selection4][selection5][selection6] = prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5][selection6])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5][selection6]), default="")
                                                    elif (selection6 != ""):
                                                        display_message("Unknown configuration entry selected.", 3)
                                                else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 5)
                                                    print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5]))
                                                    config[selection1][selection2][selection3][selection4][selection5] = prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5]), default="")
                                            elif (selection5 != ""):
                                                display_message("Unknown configuration entry selected.", 3)
                                        else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 4)
                                            print("                Current Value: " + str(config[selection1][selection2][selection3][selection4]))
                                            config[selection1][selection2][selection3][selection4] = prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4]), default="")
                                    elif (selection4 != ""):
                                        display_message("Unknown configuration entry selected.", 3)
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

elif (mode_selection == "1" and config["general"]["modes"]["enabled"]["prerecorded"] == True): # The user has selected to boot into pre-recorded mode.
    debug_message("Started pre-recorded mode")
    debug_message("Taking user preferences")
    working_directory_input = prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)
    if (working_directory_input == ""): # If the user leaves the working directory blank, use the default.
        working_directory_input = config["general"]["working_directory"]
    while (os.path.exists(working_directory_input) == False): # Run forever until the user enters a working directory that exists.
        display_message("The specified working directory doesn't seem to exist.", 2)
        working_directory_input = prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)
    config["general"]["working_directory"] = working_directory_input # Apply an override to the configured working directory.
    del working_directory_input # Remove the working directory input now that it is no longer needed.
    working_directory_contents = os.listdir(config["general"]["working_directory"]) # Get the contents of the working directory.
    dashcam_videos = [] # This is a placeholder that will hold all Predator dashcam videos found in the working directory.
    for file in working_directory_contents:
        if (file[0:len("predator_dashcam_")] == "predator_dashcam_"):
            dashcam_videos.append(file)
        
    if (len(dashcam_videos) > 3):
        print("There appears to be several Predator dashcam videos in the working directory. Would you like to generate side-car files for these videos?")
        sidecar_mode = prompt("Enable side-car mode (Y/N): ", optional=False, input_type=bool)
    else:
        sidecar_mode = False

    if (sidecar_mode == True):
        print("\nRunning side-car file generation...")
        alpr.generate_dashcam_sidecar_files(config["general"]["working_directory"], dashcam_videos)
        print("Generation complete")
        global_variables.predator_running = False
    elif (sidecar_mode == False):
        video = prompt("Video file name(s): ", optional=False, input_type=str)

        frame_interval = prompt("Frame analysis interval (Default '1.0'): ", optional=True, input_type=float, default=1.0)

        current_formats = ', '.join(config["general"]["alpr"]["validation"]["license_plate_format"])
        license_plate_format_input = prompt(f"License plate format, separated by commas (Default '{current_formats}'): ", optional=True, input_type=str)
        if (license_plate_format_input == ""): # If the user leaves the license plate format input blank, then use the default.
            license_plate_format_input = current_formats
        # Convert and store the input string as a list of formats
        config["general"]["alpr"]["validation"]["license_plate_format"] = [format.strip() for format in license_plate_format_input.split(',')]

        video_start_time = prompt("Video starting time (YYYY-mm-dd HH:MM:SS): ", optional=True, input_type=str) # Ask the user when the video recording started so we can correlate it's frames to a GPX file.
        if (video_start_time != ""):
            gpx_file = prompt("GPX file name: ", optional=True, input_type=str)
            if (gpx_file != ""):
                while (os.path.exists(config["general"]["working_directory"] + "/" + gpx_file) == False): # Check to see if the GPX file name supplied by the user actually exists in the working directory.
                    display_message("The specified GPX file does not appear to exists.", 2)
                    gpx_file = prompt("GPX file name: ", optional=False, input_type=str)
        else:
            gpx_file = ""



        debug_message("Processing user preferences")
        if (video_start_time == ""): # If the video_start_time preference was left blank, then default to 0.
            video_start_time = 0
        else:
            try:
                video_start_time = round(time.mktime(datetime.datetime.strptime(video_start_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the video_start_time human readable date and time into a Unix timestamp.
            except:
                display_message("The video starting time specified doesn't appear to be valid. The starting time has been reset to 0. GPX correlation will almost certainly fail.", 3)
                video_start_time = 0


        if (video[0] == "*"): # Check to see if the first character is a wildcard.
            video_list_command = "ls " + config["general"]["working_directory"] + "/" + video + " | tr '\n' ','";
            videos = str(os.popen(video_list_command).read())[:-1].split(",") # Run the command, and record the raw output string.
            for key, video in enumerate(videos):
                videos[key] = os.path.basename(video)
     
        else:
            videos = video.split(",") # Split the video input into a list, based on the position of commas.
        for number, video in enumerate(videos): # Iterate through each video specified by the user.
            videos[number] = video.strip()
            if (os.path.exists(config["general"]["working_directory"] + "/" + video) == False): # Check to see if each video file name supplied by the user actually exists in the working directory.
                display_message("The video file " + str(video) + " entered doesn't seem to exist in the working directory. Predator will almost certainly fail.", 3) # Inform the user that this video file couldn't be found.


        clear() # Clear the console output

        


        # Split the supplied video(s) into individual frames based on the user's input.
        debug_message("Splitting video into discrete frames")
        video_counter = 0 # Create a placeholder counter that will be incremented by 1 for each video. This will be appended to the file names of the video frames to keep frames from different videos separate.
        print("Splitting video into discrete images...")
        if (os.path.exists(config["general"]["working_directory"] + "/frames/")): # Check to see the frames directory already exists.
            os.system("rm -r " + config["general"]["working_directory"] + "/frames") # Remove the frames directory.

        for video in videos: # Iterate through each video specified by the user.
            video_counter+=1 # Increment the video counter by 1.
            frame_split_command = "mkdir " + config["general"]["working_directory"] + "/frames; ffmpeg -i " + config["general"]["working_directory"] + "/" + video + " -r " + str(1/frame_interval) + " " + config["general"]["working_directory"] + "/frames/video" + str(video_counter) + "output%04d.png -loglevel quiet" # Set up the FFMPEG command that will be used to split each video into individual frames.
            os.system(frame_split_command) # Execute the FFMPEG command to split the video into individual frames.
         
        print("Done.\n")



        # Gather all of the individual frames generated previously.
        debug_message("Collecting discrete frames")
        print("Gathering generated frames...")
        frames = os.listdir(config["general"]["working_directory"] + "/frames") # Get all of the files in the folder designated for individual frames.
        frames.sort() # Sort the list alphabetically.
        print("Done.\n")



        # Crop the individual frames to make license plate recognition more efficient and accurate.
        if (config["prerecorded"]["image"]["processing"]["cropping"]["enabled"] == True): # Check to see if cropping is enabled in pre-recorded mode.
            debug_message("Cropping discrete frames")
            print("Cropping individual frames...")
            crop_script_path = predator_root_directory + "/crop_image" # Path to the cropping script in the Predator directory.
            for frame in frames:
                os.system(crop_script_path + " " + config["general"]["working_directory"] + "/frames/" + frame + " " + str(config["prerecorded"]["image"]["processing"]["cropping"]["left_margin"]) + " " + str(config["prerecorded"]["image"]["processing"]["cropping"]["right_margin"]) + " " + str(config["prerecorded"]["image"]["processing"]["cropping"]["top_margin"]) + " " + str(config["prerecorded"]["image"]["processing"]["cropping"]["bottom_margin"]))
            print("Done.\n")



        # Analyze each individual frame, and collect possible plate IDs.
        debug_message("Running ALPR")
        print("Scanning for license plates...")
        alpr_frames = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
        for frame in frames: # Iterate through each frame of video.
            alpr_frames[frame] = {} # Set the license plate recognition information for this frame to an empty list as a placeholder.

            # Run license plate analysis on this frame.
            reading_output = alpr.run_alpr(config["general"]["working_directory"] + "/frames/" + frame)

            # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
            all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
            plate_index = 0 # Reset the plate index counter to 0 before the loop.
            for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
                all_current_plate_guesses[plate_index] = {} # Create an empty dictionary for this plate so we can add all the potential plate guesses to it in the next step.
                for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                    all_current_plate_guesses[plate_index][plate_guess["plate"]] = plate_guess["confidence"] # Add the current plate guess candidate to the list of plate guesses.
                plate_index+=1 # Increment the plate index counter.

            if (len(all_current_plate_guesses) > 0): # Only add license plate data to the current frame if data actually exists to add in the first place.
                alpr_frames[frame] = all_current_plate_guesses # Record all of the detected plates for this frame.

        print("Done.\n")





        # Check the possible plate IDs and validate based on general plate formatting specified by the user.
        debug_message("Validating ALPR results")
        print("Validating license plates...")
        validated_alpr_frames = {} # This is a placeholder variable that will be used to store the validated ALPR information for each frame.

        # Handle ignore list processing.
        for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
            validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
            for plate in alpr_frames[frame].keys(): # Iterate through each plate detected per frame.
                for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                    for ignore_plate in ignore_list: # Iterate through each plate in the ignore list.
                        if (fnmatch.fnmatch(guess, ignore_plate)): # Check to see if this guess matches a plate in the ignore list.
                            alpr_frames[frame][plate] = [] # Remove this plate from the ALPR dictionary.
                            break # Break the loop, since this entire plate, including all of its guesses, has just been removed.
                        if (fnmatch.fnmatch(guess, config["developer"]["kill_plate"]) and config["developer"]["kill_plate"] != ""): # Check to see if this plate matches the kill plate, and if a kill plate is set.
                            exit() # Terminate the program.

        # Remove any empty plates.
        for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
            plates = list(alpr_frames[frame].keys())
            for plate in plates:
                if (len(alpr_frames[frame][plate]) <= 0):
                    del alpr_frames[frame][plate]

        # Handle formatting validation.
        for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
            validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
            for plate in alpr_frames[frame]: # Iterate through each plate detected per frame.
                for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                    if (alpr_frames[frame][plate][guess] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate's confidence is higher than the minimum threshold set in the configuration.
                        if any(alpr.validate_plate(guess, format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]) or len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0: # Check to see if this plate passes validation.
                            if (plate not in validated_alpr_frames[frame]): # Check to see if this plate hasn't been added to the validated information yet.
                                validated_alpr_frames[frame][plate] = [] # Add the plate to the validated information as a blank placeholder list.
                            validated_alpr_frames[frame][plate].append(guess) # Since this plate guess failed the validation test, delete it from the list of guesses.

        print("Done.\n")



        # Run through the data for each frame, and save only the first (most likely) license plate to the list of detected plates.
        debug_message("Organizing ALPR results")
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





        debug_message("Checking for alerts")
        print("Checking for alerts...")
        alert_database = alpr.load_alert_database(config["general"]["alerts"]["databases"], config["general"]["working_directory"]) # Load the license plate alert database.
        active_alerts = {} # This is an empty placeholder that will hold all of the active alerts. 
        if (len(alert_database) > 0): # Only run alert processing if the alert database isn't empty.
            for rule in alert_database: # Run through every plate in the alert plate database supplied by the user.
                for frame in alpr_frames: # Iterate through each frame of video in the raw ALPR data.
                    if (config["general"]["alerts"]["alerts_ignore_validation"] == True): # If the user has enabled alerts that ignore license plate validation, then use the unvalidated ALPR information.
                        alpr_frames_to_scan = alpr_frames
                    else: # If the user hasn't enabled alerts that ignore license plate validation, then use the validated ALPR information.
                        alpr_frames_to_scan = validated_alpr_frames

                    for plate in alpr_frames_to_scan[frame]: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                        for guess in alpr_frames_to_scan[frame][plate]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                            if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                                active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                                active_alerts[guess]["frame"] = frame # Add the rule that triggered this alert to the alert information.
                                if (config["general"]["alerts"]["allow_duplicate_alerts"] == False):
                                    break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

        display_alerts(active_alerts) # Display all active alerts.
        print("Done.\n")



        # Correlate the detected license plates with a GPX file.
        frame_locations = {} # Create a blank database that will be used during the process
        if (gpx_file != ""): # Check to make sure the user actually supplied a GPX file.
            debug_message("Correlated location data")
            print("Processing location data...")
            decoded_gpx_data = process_gpx(config["general"]["working_directory"] + "/" + gpx_file) # Decode the data from the GPX file.
            iteration = 0 # Set the iteration counter to 0 so we can add one to it each frame we iterate through.
            for element in alpr_frames: # Iterate through each frame.
                iteration+=1 # Add one to the iteration counter.
                frame_timestamp = video_start_time + (iteration * frame_interval) # Calculate the timestamp of this frame.

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


        utils.wait_for_input()

        debug_message("Starting menu loop")
        while global_variables.predator_running: # Run the pre-recorded mode menu in a loop forever until the user exits.
            clear()

            # Show the main menu for handling data collected in pre-recorded mode.
            print("Please select an option")
            print("0. Quit")
            print("1. Manage license plate data")
            if (gpx_file != ""): # Check to see if a GPX correlation is enabled before displaying the position data option.
                print("2. Manage position data")
            else:
                print(style.faint + "2. Manage position data" + style.end)
            print("3. View session statistics")
            selection = prompt("Selection: ", optional=False, input_type=str)


            if (selection == "0"):
                global_variables.predator_running = False
            elif (selection == "1"): # If the user selects option 1 on the main menu, then load the license plate data viewing menu.
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
                        save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.txt", export_data) # Save to disk.
                    elif (selection == "2"): # The user has selected to export license plate data as a list.
                        for plate in plates_detected:
                            export_data = export_data + plate + "\n"
                        save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.txt", export_data) # Save to disk.
                    elif (selection == "3"): # The user has selected to export license plate data as CSV data.
                        for plate in plates_detected:
                            export_data = export_data + plate + ",\n"
                        save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.csv", export_data) # Save to disk.
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
                            save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(alpr_frames)) # Save the raw license plate analysis data to disk.
                        elif (selection == "2"): # The user has selected to export validated license plate data as JSON.
                            save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(validated_alpr_frames)) # Save the validated license plate analysis data to disk.
                        elif (selection == "3"): # The user has selected to alert license plate data as JSON.
                            save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(active_alerts)) # Save detected license plate alerts to disk.
                        else:
                            display_message("Invalid selection.", 2)
                    else:
                        display_message("Invalid selection.", 2)

                utils.wait_for_input()


            elif (selection == "2"): # The user has selected to manage GPX location information.
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
                            save_to_file(config["general"]["working_directory"] + "/pre_recorded_location_data_export.txt", frame_locations) # Save to disk.
                        elif (selection == "2"):
                            save_to_file(config["general"]["working_directory"] + "/pre_recorded_location_data_export.json", json.dumps(frame_locations, indent=4)) # Save to disk.
                        else:
                            display_message("Invalid selection.", 2)

                    else:
                        display_message("Invalid selection.", 2)

                else:
                    display_message("GPX processing has been disabled since a GPX file wasn't provided. There is no GPX location data to manage.", 2)

                utils.wait_for_input()


            elif (selection == "3"): # If the user selects option 4 on the main menu, then show the statistics for this session.
                print("    Frames analyzed: " + str(len(alpr_frames))) # Show how many frames of video were analyzed.
                print("    Plates found: " + str(len(plates_detected))) # Show how many unique plates were detected.
                print("    Videos analyzed: " + str(len(videos))) # Show how many videos were analyzed.
                print("    Alerts detected: " + str(len(active_alerts))) # Show how many videos were analyzed.
                utils.wait_for_input()


            else: # If the user selects an unrecognized option on the main menu for pre-recorded mode, then show a warning.
                display_message("Invalid selection.", 2)
                utils.wait_for_input()






# Real-time mode

elif (mode_selection == "2" and config["general"]["modes"]["enabled"]["realtime"] == True): # The user has set Predator to boot into real-time mode.
    debug_message("Started real-time mode")
    for device in config["realtime"]["image"]["camera"]["devices"]: # Iterate through each video device specified in the configuration.
        if (os.path.exists(config["realtime"]["image"]["camera"]["devices"][device]) == False): # Check to make sure that a camera device points to a valid file.
            display_message("The 'realtime>image>camera>devices>" + device + "' configuration value does not point to a valid file.", 3)


    # Load the license plate history file.
    if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if the license plate logging file name is not empty. If the file name is empty, then license plate logging will be disabled.
        plate_log = alpr.load_alpr_log()


    # Load the license plate alert database.
    alert_database = alpr.load_alert_database(config["general"]["alerts"]["databases"], config["general"]["working_directory"])

    alpr.start_alpr_stream() # Start the ALPR stream.

    detected_license_plates = [] # Create an empty list that will hold each license plate detected by Predator during this session.

    frames_captured = 0 # Set the number of frames captured to 0 so we can increment it by one each time Predator analyzes a frame.
    debug_message("Starting main processing loop")
    try:
        while global_variables.predator_running: # Run in a loop forever, (until Predator is terminated).
            if (config["realtime"]["interface"]["behavior"]["clearing"] == True): # Clear the output screen at the beginning of each round if the configuration indicates to.
                clear()


            if (config["realtime"]["interface"]["display"]["speed"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Display the current speed based on GPS, if enabled in the configuration.
                current_location = get_gps_location() # Get the current location.
                current_speed = convert_speed(float(current_location[2]), config["realtime"]["interface"]["display"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
                print("Current speed: " + str(current_speed) + " " + str(config["realtime"]["interface"]["display"]["speed"]["unit"])) # Print the current speed to the console.




            new_plates_detected = [] # This variable will be used to determine whether or not a plate was detected this round. If no plate is detected, this will remain blank. If a plate is detected, it will change to be that plate. This is used to determine whether or not the database of detected plates needs to updated.

            # Reset the status lighting to normal before processing the license plate data from ALPR.
            if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                update_status_lighting("normal") # Run the function to update the status lighting.



            # Fetch the latest plates in the queue from the ALPR stream.
            debug_message("Fetching ALPR results")
            reading_output = {}
            reading_output["results"] = alpr.alpr_get_queued_plates() 



            # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
            debug_message("Organizing ALPR results")
            all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
            for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
                ignore_plate = False # Reset this value to false for each plate.
                for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                    if (plate_guess["plate"] in ignore_list): # Check to see if this plate guess matches in a plate in the loaded ignore list.
                        ignore_plate = True # Indicate that this plate should be ignored.

                    if (fnmatch.fnmatch(plate_guess["plate"], config["developer"]["kill_plate"]) and config["developer"]["kill_plate"] != ""): # Check to see if this plate matches the kill plate, and if a kill plate is set.
                        exit() # Terminate the program.

                if (ignore_plate == False): # Only process this plate if it isn't set to be ignored.
                    all_current_plate_guesses[detected_plate["candidates"][0]["plate"]] = {} # Create an empty dictionary for this plate so we can add all the potential plate guesses to it in the next step.

                    for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                        all_current_plate_guesses[detected_plate["candidates"][0]["plate"]][plate_guess["plate"]] = plate_guess["confidence"] # Add the current plate guess candidate to the list of plate guesses.

            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Done\n----------")





            debug_message("Processing ALPR results")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Processing license plate recognition data...")
            if (len(all_current_plate_guesses) > 0): # Check to see if at least one license plate was detected.
                if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                    print("Plates detected: " + str(len(all_current_plate_guesses))) # Show the number of plates detected this round.
                for individual_detected_plate in all_current_plate_guesses: # Iterate through each individual plate detected in the image frame.
                    successfully_found_plate = False # Reset the 'successfully_found_plate` variable to 'False'. This will be changed back if a valid plate is detected.

                    # Run validation according to the configuration on the plate(s) detected.
                    if (len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0): # If the user didn't supply a license plate format, then skip license plate validation.
                        detected_plate = str(list(all_current_plate_guesses[individual_detected_plate].keys())[0]) # Grab the most likely detected plate as the 'detected plate'.
                        successfully_found_plate = True # Plate validation wasn't needed, so the fact that a plate existed at all means a valid plate was detected. Indicate that a plate was successfully found this round.

                    else: # If the user did supply a license plate format, then check all of the results against the formatting example.
                        if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                            print ("    Plate guesses:")
                        for plate_guess in all_current_plate_guesses[individual_detected_plate]: # Iterate through each plate and grab the first plate that matches the plate formatting guidelines as the 'detected plate'.
                            if (all_current_plate_guesses[individual_detected_plate][plate_guess] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate's confidence is higher than the minimum threshold set in the configuration.
                                if any(alpr.validate_plate(plate_guess, format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]): # Check to see whether or not the plate passes the validation based on the format specified by the user.
                                    detected_plate = plate_guess # Grab the validated plate as the 'detected plate'.
                                    successfully_found_plate = True # The plate was successfully validated, so indicate that a plate was successfully found this round.
                                    if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                                        print("        ", style.green + plate_guess + style.end) # Print the valid plate in green.
                                    break
                                else: # This particular plate guess is invalid, since it didn't align with the user-supplied formatting guidelines.
                                    if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the invalid plate if the configuration says to do so.
                                        print("        ", style.red + plate_guess + style.end) # Print the invalid plate in red.




                    # Run the appropriate tasks, based on whether or not a valid license plate was detected.
                    if (successfully_found_plate == True): # Check to see if a valid plate was detected this round after the validation process ran.
                        detected_license_plates.append(detected_plate) # Save the most likely license plate ID to the detected_license_plates complete list.
                        new_plates_detected.append([detected_plate, individual_detected_plate]) # Save the most likely license plate to this round's new_plates_detected list, as well as the plate from "all_current_plate_guesses" that it comes from.


                        if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications enabled.
                            debug_message("Issuing detection push notification")
                            os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=A license plate has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification via Gotify.

                        if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                            display_shape("square") # Display an ASCII square in the output.

                        if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                            update_status_lighting("alpr_detection") # Run the function to update the status lighting.



                    elif (successfully_found_plate == False): # A plate was found, but none of the guesses matched the formatting guidelines provided by the user.
                        if (config["general"]["alpr"]["validation"]["best_effort"] == True): # Check to see if 'best effort' validation is enabled.
                            new_plates_detected.append([next(iter(all_current_plate_guesses[individual_detected_plate])), individual_detected_plate]) # Add the most likely guess for this plate to the list of detected license plates.

                        if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                            display_shape("circle") # Display an ASCII circle in the output.


            else: # No license plate was detected at all.
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.")


            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("----------") # Print a dividing line after processing license plate analysis data.




            debug_message("Displaying detected plates")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Displaying detected license plates...")

            for plate in new_plates_detected:
                utils.play_sound("alpr_notification")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 2): # Only display this status message if the output level indicates to do so.
                print("Plates detected: " + str(len(new_plates_detected))) # Display the number of license plates detected this round.
                for plate in new_plates_detected:
                    print("    Detected plate: " + plate[0]) # Print the detected plate.




            debug_message("Processing ALPR alerts")
            # Check the plate(s) detected this around against the alert database, if necessary.
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Checking license plate data against alert database...")

            active_alerts = {} # This is a placeholder dictionary that will hold all of the active alerts.

            if (config["general"]["alerts"]["alerts_ignore_validation"] == True): # If the user has enabled alerts that ignore license plate validation, then check each of the ALPR guesses against the license plate alert database.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                    for plate in all_current_plate_guesses: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                        for guess in all_current_plate_guesses[plate]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                            if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                                active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                                if (config["general"]["alerts"]["allow_duplicate_alerts"] == False):
                                    break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

            else: #  If the user has disabled alerts that ignore license plate validation, then only check the validated plate array against the alert database.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                    for plate in new_plates_detected: # Iterate through each plate that was detected and validated this round.
                        if (fnmatch.fnmatch(plate[0], rule)): # Check to see the validated detected plate matches this particular plate in the alert database, taking wildcards into account.
                            active_alerts[plate[0]] = alert_database[rule] # Add this plate to the active alerts dictionary.
                            active_alerts[plate[0]]["rule"] = rule # Add the rule that triggered this alert to the alert information.




            # Save detected license plates to file.
            if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if license plate history saving is enabled.
                debug_message("Saving license plate history")

                if (len(all_current_plate_guesses) > 0): # Only save the license plate history for this round if 1 or more plates were detected.
                    current_time = time.time() # Get the current timestamp.

                    plate_log[current_time] = {} # Initialize an entry in the plate history log using the current time.

                    if (config["realtime"]["gps"]["alpr_location_tagging"] == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                        if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS functionality is enabled.
                            current_location = get_gps_location() # Get the current location.
                        else:
                            current_location = [0.0, 0.0] # Grab a placeholder for the current location, since GPS functionality is disabled.

                        plate_log[current_time]["location"] = {"lat": current_location[0],"lon": current_location[1]} # Add the current location to the plate history log entry.

                    plate_log[current_time]["plates"] = {}


                    if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Check if Predator is configured to save all plate guesses.
                        plate_log[current_time]["plates"][plate] = {"alerts": [], "guesses": {}} # Initialize this plate in the plate log.
                        for plate in all_current_plate_guesses: # Iterate though each plate detected this round.
                            for guess in all_current_plate_guesses[plate]: # Iterate through each guess in this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.
                                if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Only add this guess to the log if Predator is configured to do so.
                                    plate_log[current_time]["plates"][plate]["guesses"][guess] = all_current_plate_guesses[plate][guess] # Add this guess to the log, with its confidence level.
                    else: # Predator is configured only to save the most likely plate guess to the plate log file.
                        for plate in new_plates_detected: # Iterate over each individual plate detected.
                            plate_log[current_time]["plates"][plate[0]] = {"alerts": []} # Initialize this plate in the plate log.
                            for guess in all_current_plate_guesses[plate[1]]: # Iterate through each guess associated with this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate[0]]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.


                            plate_log[current_time]["plates"][plate[0]]["alerts"] = list(dict.fromkeys(plate_log[current_time]["plates"][plate[0]]["alerts"])) # De-duplicate the 'alerts' list for this plate.

                    save_to_file(config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"], json.dumps(plate_log)) # Save the modified plate log to the disk as JSON data.



            # Issue interface file updates.
            if (config["general"]["interface_directory"] != ""):
                debug_message("Issuing interface updates")
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Issuing interface updates...")
                heartbeat() # Issue a status heartbeat.
                update_state("realtime") # Update the system status.
                log_plates(all_current_plate_guesses) # Update the list of recently detected license plates.
                log_alerts(active_alerts) # Update the list of active alerts.
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.\n----------")



            if (len(active_alerts) > 0): # Check to see if there are any active alerts to see if an alert state should be triggered.
                if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                    update_status_lighting("alpr_alert") # Run the function to update the status lighting.

                if (config["realtime"]["interface"]["display"]["output_level"] >= 1): # Only display alerts if the configuration specifies to do so.
                    display_alerts(active_alerts) # Display all active alerts.

                for alert in active_alerts: # Run once for each active alert.
                    if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications enabled.
                        debug_message("Issuing alert push notification")
                        os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=A license plate in an alert database has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.

                    if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                        display_shape("triangle") # Display an ASCII triangle in the output.

                    utils.play_sound("alpr_alert") # Play the alert sound, if configured to do so.

            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")



            debug_message("Delaying before loop restart")
            if (len(active_alerts) > 0): # Check to see if there are one or more active alerts.
                time.sleep(float(config["realtime"]["interface"]["behavior"]["delays"]["alert"])) # Trigger a delay based on the fact that there is at least one active alert.
            else:
                time.sleep(float(config["realtime"]["interface"]["behavior"]["delays"]["normal"])) # Trigger a normal delay.
    except Exception as e:
        print("Exiting Predator...")
        global_variables.predator_running = False
        os.popen("killall alpr") # Kill the background ALPR process.





# Dash-cam mode
elif (mode_selection == "3" and config["general"]["modes"]["enabled"]["dashcam"] == True): # The user has set Predator to boot into dash-cam mode.
    print("\nStarting dashcam recording")
    debug_message("Started dash-cam mode")
    try:
        print("Press Ctrl+C to exit")
        dashcam.dashcam()
    except:
        global_variables.predator_running = False
    display_message("Dashcam recording halted.", 1)
    utils.play_sound("recording_stopped")




else: # The user has selected an unrecognized mode.
    display_message("The selected mode is invalid.", 3) # Display an error message indicating that the selected mode isn't recognized.
