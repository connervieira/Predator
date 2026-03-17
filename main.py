# Predator
# main.py
# This is the main driver script for Predator, and is the starting point for all other functionality. Run Predator with `python3 main.py --help`.

# Copyright (C) 2026 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE). If not, see https://www.gnu.org/licenses/ to read the license agreement.



print("Loading Predator...")
import global_variables # `global_variables.py`
global_variables.init()

import os # Required to interact with certain operating system functions
import json # Required to process JSON data


import config # `config.py`
load_config = config.load_config
validate_config = config.validate_config
config = load_config()

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

    global_variables.PREDATOR_RUNNING = False
    global_variables.shutdown_event.set()
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
import threading # Required to check which threads are alive when Predator fails to exit in a timely manner.

if (config["general"]["modes"]["enabled"]["realtime"] == True):
    import alpr
    display_alerts = alpr.display_alerts # Load the function used to display license plate alerts given the dictionary of alerts.


if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    if (config["general"]["status_lighting"]["enabled"] == True or config["realtime"]["push_notifications"]["enabled"] == True or len(config["general"]["alerts"]["databases"]) > 0): # Only import networking libraries if they are necessary.
        debug_message("Loading networking libraries")
        import requests # Required to make network requests.
        import validators # Required to validate URLs.




if (os.path.exists(os.path.join(global_variables.PREDATOR_ROOT_DIRECTORY, "install.json")) == False): # Check to see if the install information file hasn't yet been created. This will be the case on the first start-up.
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


    with open(os.path.join(global_variables.PREDATOR_ROOT_DIRECTORY, "/install.json"), 'w') as file:
        json.dump(install_data, file)


    print("")
    clear()
    print("The initial start-up process has completed. Predator will now return to the normal start-up sequence.")
    input(style.faint + "Press enter to continue..." + style.end)




debug_message("Loading ignore lists")
import ignore # `ignore.py` Import the library to handle license plates in the ignore list.
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
    print("| $$  \\ $$| $$  \\ $$| $$      | $$  \\ $$| $$  \\ $$   | $$  | $$  \\ $$| $$  \\ $$")
    print("| $$$$$$$/| $$$$$$$/| $$$$$   | $$  | $$| $$$$$$$$   | $$  | $$  | $$| $$$$$$$/")
    print("| $$____/ | $$__  $$| $$__/   | $$  | $$| $$__  $$   | $$  | $$  | $$| $$__  $$")
    print("| $$      | $$  \\ $$| $$      | $$  | $$| $$  | $$   | $$  | $$  | $$| $$  \\ $$")
    print("| $$      | $$  | $$| $$$$$$$$| $$$$$$$/| $$  | $$   | $$  |  $$$$$$/| $$  | $$")
    print("|__/      |__/  |__/|________/|_______/ |__/  |__/   |__/   \\______/ |__/  |__/" + style.end + style.bold)
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
print("")





# Initial setup has been completed, and Predator will now load into the specified mode.








# Management mode
if (mode_selection == "0" and config["general"]["modes"]["enabled"]["management"] == True): # The user has selected to boot into management mode.
    import predator_management # `predator_management.py`
    predator_management.management_mode()




# Pre-recorded mode
elif (mode_selection == "1" and config["general"]["modes"]["enabled"]["prerecorded"] == True): # The user has selected to boot into pre-recorded mode.
    import predator_prerecorded # `predator_prerecorded.py`
    predator_prerecorded.prerecorded_mode()






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
        while global_variables.PREDATOR_RUNNING: # Run in a loop forever, (until Predator is terminated).
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
                    all_current_plate_guesses[detected_plate["candidates"][0]["plate"]] = {"guesses": {}, "identifier": detected_plate["identifier"]} # Create an empty dictionary for this plate so we can add all the potential plate guesses to it in the next step.

                    for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                        all_current_plate_guesses[detected_plate["candidates"][0]["plate"]]["guesses"][plate_guess["plate"]] = plate_guess["confidence"] # Add the current plate guess candidate to the list of plate guesses.

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
                        for plate_guess in all_current_plate_guesses[individual_detected_plate]["guesses"]: # Iterate through each plate and grab the first plate that matches the plate formatting guidelines as the 'detected plate'.
                            if (all_current_plate_guesses[individual_detected_plate]["guesses"][plate_guess] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate's confidence is higher than the minimum threshold set in the configuration.
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
                            new_plates_detected.append([next(iter(all_current_plate_guesses[individual_detected_plate]["guesses"])), individual_detected_plate]) # Add the most likely guess for this plate to the list of detected license plates.

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
                        for guess in all_current_plate_guesses[plate]["guesses"]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
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

                if ((len(all_current_plate_guesses) > 0 and config["realtime"]["saving"]["license_plates"]["save_guesses"] == True) or (len(new_plates_detected) > 0 and config["realtime"]["saving"]["license_plates"]["save_guesses"] == False)): # Only save the license plate history for this round if 1 or more plates were detected.
                    current_time = time.time() # Get the current timestamp.

                    plate_log[current_time] = {} # Initialize an entry in the plate history log using the current time.

                    if (config["realtime"]["gps"]["alpr_location_tagging"] == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                        if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS functionality is enabled.
                            current_location = get_gps_location() # Get the current location.
                        else:
                            current_location = [0.0, 0.0, 0, -1] # Grab a placeholder for the current location, since GPS functionality is disabled.

                        plate_log[current_time]["location"] = {"lat": current_location[0],"lon": current_location[1], "alt": current_location[3], "head": current_location[4]} # Add the current location to the plate history log entry.

                    plate_log[current_time]["plates"] = {}

                    if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Check if Predator is configured to save all plate guesses.
                        plate_log[current_time]["plates"][plate] = {"alerts": [], "guesses": {}} # Initialize this plate in the plate log.
                        for plate in all_current_plate_guesses: # Iterate though each plate detected this round.
                            for guess in all_current_plate_guesses[plate]["guesses"]: # Iterate through each guess in this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.
                                if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Only add this guess to the log if Predator is configured to do so.
                                    plate_log[current_time]["plates"][plate]["guesses"][guess] = all_current_plate_guesses[plate]["guesses"][guess] # Add this guess to the log, with its confidence level.
                    else: # Predator is configured only to save the most likely plate guess to the plate log file.
                        for plate in new_plates_detected: # Iterate over each individual plate detected.
                            plate_log[current_time]["plates"][plate[0]] = {"alerts": []} # Initialize this plate in the plate log.
                            for guess in all_current_plate_guesses[plate[1]]["guesses"]: # Iterate through each guess associated with this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate[0]]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.


                            plate_log[current_time]["plates"][plate[0]]["alerts"] = list(dict.fromkeys(plate_log[current_time]["plates"][plate[0]]["alerts"])) # De-duplicate the 'alerts' list for this plate.

                    save_to_file(config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"], json.dumps(plate_log)) # Save the modified plate log to the disk as JSON data.

            valid_plates_with_guesses = {} # This will hold a dictionary of all valid plates with their guesses as children.
            for plate in new_plates_detected:
                valid_plates_with_guesses[plate[0]] = {
                    "guesses": all_current_plate_guesses[plate[1]]["guesses"],
                    "identifier": all_current_plate_guesses[plate[1]]["identifier"]
                }



            # Issue interface file updates.
            if (config["general"]["interface_directory"] != ""):
                debug_message("Issuing interface updates")
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Issuing interface updates...")
                heartbeat() # Issue a status heartbeat.
                update_state("realtime") # Update the system status.
                log_plates(valid_plates_with_guesses) # Update the list of recently detected license plates.
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
    except KeyboardInterrupt:
        print("[Keyboard interrupt]")
    except Exception as e:
        e_type, e_object, e_traceback = sys.exc_info()
        e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
        e_message = str(e)
        e_line_number = e_traceback.tb_lineno
        print(f'Exception type: {e_type}')
        print(f'Exception filename: {e_filename}')
        print(f'Exception line number: {e_line_number}')
        print(f'Exception message: {e_message}')
        utils.display_message("A fatal exception occurred", 3)
    finally:
        os.popen("killall alpr") # Kill the background ALPR process.
        utils.display_message("Real-time ALPR halted.", 1)





# Dash-cam mode
elif (mode_selection == "3" and config["general"]["modes"]["enabled"]["dashcam"] == True): # The user has set Predator to boot into dash-cam mode.
    import predator_dashcam

    utils.display_message("Starting dashcam recording", 1)
    utils.debug_message("Started dash-cam mode")
    try:
        print("Press Ctrl+C to exit")
        predator_dashcam.dashcam()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        e_type, e_object, e_traceback = sys.exc_info()
        e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
        e_message = str(e)
        e_line_number = e_traceback.tb_lineno
        print(f'Exception type: {e_type}')
        print(f'Exception filename: {e_filename}')
        print(f'Exception line number: {e_line_number}')
        print(f'Exception message: {e_message}')
        utils.display_message("A fatal exception occurred", 3)
    finally:
        utils.display_message("Dashcam recording halted.", 1)
        utils.play_sound("recording_stopped")


else: # The user has selected an unrecognized mode.
    display_message("The selected mode is invalid.", 3) # Display an error message indicating that the selected mode isn't recognized.



utils.stop_predator()
