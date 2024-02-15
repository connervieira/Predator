# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This script contains several functions and classes used in main.py




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



# Define some styling information
class style:
    # Define colors
    purple = '\033[95m'
    cyan = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    gray = '\033[1;37m'
    red = '\033[91m'

    # Define text decoration
    bold = '\033[1m'
    underline = '\033[4m'
    italic = '\033[3m'
    faint = '\033[2m'

    # Define styling end marker
    end = '\033[0m'


import time # Required to add delays and handle dates/times

global_time_offset = 0 
def get_time():
    global global_time_offset
    adjusted_time = time.time() + global_time_offset
    return adjusted_time


# Define the function to print debugging information when the configuration specifies to do so.
debugging_time_record = {}
def debug_message(message, thread="MainThread"):
    if (config["general"]["display"]["debugging_output"] == True): # Only print the message if the debugging output configuration value is set to true.
        global debugging_time_record
        thread = threading.current_thread().name
        if (thread not in debugging_time_record):
            debugging_time_record[thread] = get_time()
        time_since_last_message = (get_time()-debugging_time_record[thread]) # Calculate the time since the last debug message.
        print(f"{style.italic}{style.faint}{get_time():.10f} ({time_since_last_message:.10f} - {thread}) - {message}{style.end}") # Print the message.
        debugging_time_record[thread] = get_time() # Record the current timestamp.




import subprocess # Required for starting some shell commands
import sys
if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    if (config["realtime"]["status_lighting"]["enabled"] == True or config["realtime"]["push_notifications"]["enabled"] == True or len(config["general"]["alerts"]["databases"]) > 0):
        import requests # Required to make network requests
        import validators # Required to validate URLs
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
from xml.dom import minidom # Required for processing GPX data
if (config["general"]["gps"]["enabled"] == True): # Only import the GPS libraries if GPS settings are enabled.
    from gps import * # Required to access GPS information.
    import gpsd
import threading



if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    if (os.path.exists(config["general"]["interface_directory"]) == False): # Check to see if the interface directory is missing.
        os.makedirs(config["general"]["interface_directory"]) # Attempt to create the interface directory.
        os.system("chmod 777 " + config["general"]["interface_directory"]) # Make the interface directory accessible to all users and processes.



# Define the function that will be used to clear the screen.
def clear():
    if (config["general"]["display"]["debugging_output"] == False): # Only clear the console if the debugging output configuration value is disabled.
        os.system("clear")



def is_json(string):
    try:
        json_object = json.loads(string) # Try to load string as JSON information.
    except ValueError as error_message: # If the process fails, then the string is not valid JSON.
        return False # Return 'false' to indicate that the string is not JSON.

    return True # If the try statement is successful, then return 'true' to indicate that the string is valid JSON.



# Define a function for running a countdown timer.
def countdown(timer):
    for iteration in range(1, timer + 1): # Loop however many times specified by the `timer` variable.
        print(str(timer - iteration + 1)) # Display the current countdown number for this iteration, but subtracting the current iteration count from the total timer length.
        time.sleep(1) # Wait for 1 second.



# This function can be called from within threads to exit Predator.
def trigger_exit():
    exit()



# Define the function that will be used to save files for exported data.
def save_to_file(file_name, contents):
    fh = None
    success = False
    try:
        fh = open(file_name, 'w')
        fh.write(contents)
        success = True   
    except IOError as e:
        success = False
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success



# Define the function that will be used to add to the end of a file.
def add_to_file(file_name, contents):
    fh = None
    success = False
    try:
        fh = open(file_name, 'a')
        fh.write(contents)
        success = True
    except IOError as e:
        success = False
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success






# Define the function used to handle the license plate interface file. This function is extremely similar to the `log_alerts()` function.
if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    plate_file_location = config["general"]["interface_directory"] + "/plates.json"
    if (os.path.exists(plate_file_location) == False): # If the plate log file doesn't exist, create it.
        save_to_file(plate_file_location, "{}") # Save a blank placeholder dictionary to the plate log file.

    plate_file = open(plate_file_location, "r") # Open the plate log file for reading.
    plate_file_contents = plate_file.read() # Read the raw contents of the plate file as a string.
    plate_file.close() # Close the plate log file.

    if (is_json(plate_file_contents) == True): # If the plate file contains valid JSON data, then load it.
        plate_log = json.loads(plate_file_contents) # Read and load the plate log from the file contents.
    else: # If the plate log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        plate_log = json.loads("{}") # Load a blank placeholder dictionary.

def log_plates(detected_plates):
    global plate_log

    plate_log[get_time()] = detected_plates
    entries_to_remove = [] # Create a blank placeholder list to hold all of the entry keys that have expired and need to be removed.

    for entry in plate_log.keys(): # Iterate through each entry in the plate history.
        if (get_time() - float(entry) > 10): # Check to see if this entry has expired according the max age configuration value.
            entries_to_remove.append(entry) # Add this entry key to the list of entries to remove.

    for key in entries_to_remove: # Iterate through each of the keys designated to be removed.
        plate_log.pop(key)

    save_to_file(plate_file_location, json.dumps(plate_log)) # Save the modified plate log to the disk as JSON data.




# Define the function used to handle the alert interface file. This function is extremely similar to the `log_plates()` function.
if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    alert_file_location = config["general"]["interface_directory"] + "/alerts.json"
    if (os.path.exists(alert_file_location) == False): # If the alert log file doesn't exist, create it.
        save_to_file(alert_file_location, "{}") # Save a blank placeholder dictionary to the alert log file.

    alert_file = open(alert_file_location, "r") # Open the alert log file for reading.
    alert_file_contents = alert_file.read() # Read the raw contents of the alert file as a string.
    alert_file.close() # Close the alert log file.

    if (is_json(alert_file_contents) == True): # If the alert file contains valid JSON data, then load it.
        alert_log = json.loads(alert_file_contents) # Read and load the alert log from the file contents.
    else: # If the alert log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        alert_log = json.loads("{}") # Load a blank placeholder dictionary.

def log_alerts(active_alerts):
    global alert_log

    alert_log[get_time()] = active_alerts
    entries_to_remove = [] # Create a blank placeholder list to hold all of the entry keys that have expired and need to be removed.

    for entry in alert_log.keys(): # Iterate through each entry in the alert history.
        if (get_time() - float(entry) > 10): # Check to see if this entry has expired according the max age configuration value.
            entries_to_remove.append(entry) # Add this entry key to the list of entries to remove.

    for key in entries_to_remove: # Iterate through each of the keys designated to be removed.
        alert_log.pop(key)

    save_to_file(alert_file_location, json.dumps(alert_log)) # Save the modified alert log to the disk as JSON data.




# Define the function used to handle system heartbeats, which allow external services to verify that Predator is running.
if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    heartbeat_file_location = config["general"]["interface_directory"] + "/heartbeat.json"
    if (os.path.exists(heartbeat_file_location) == False): # If the heartbeat log file doesn't exist, create it.
        save_to_file(heartbeat_file_location, "[]") # Save a blank placeholder list to the heartbeat log file.

    heartbeat_file = open(heartbeat_file_location, "r") # Open the heartbeat log file for reading.
    heartbeat_file_contents = heartbeat_file.read() # Read the raw contents of the heartbeat file as a string.
    heartbeat_file.close() # Close the heartbeat log file.

    if (is_json(heartbeat_file_contents) == True): # If the heartbeat file contains valid JSON data, then load it.
        heartbeat_log = json.loads(heartbeat_file_contents) # Read and load the heartbeat log from the file.
    else: # If the heartbeat file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        heartbeat_log = json.loads("[]") # Load a blank placeholder list.

def heartbeat(): # This is the function that is called to issue a heartbeat.
    heartbeat_thread = threading.Thread(target=issue_heartbeat)
    heartbeat_thread.start()

def issue_heartbeat(): # This is the function that actually issues a heartbeat.
    global heartbeat_log
    if (len(heartbeat_log) < 1):
        heartbeat_log.append(get_time()) # Add this pulse to the heartbeat log file, using the current time as the key.
        save_to_file(heartbeat_file_location, json.dumps(heartbeat_log)) # Save the modified heartbeat log to the disk as JSON data.
    elif (get_time() - float(heartbeat_log[-1]) > 0.25): # Check to see if it has been more than a brief period of time since the last heartbeat to avoid spamming heartbeat updates.
        heartbeat_log.append(get_time()) # Add this pulse to the heartbeat log file, using the current time as the key.
        heartbeat_log = heartbeat_log[-10:] # Trim the list to only contain the last entries.
        save_to_file(heartbeat_file_location, json.dumps(heartbeat_log)) # Save the modified heartbeat log to the disk as JSON data.




# Define the function to display warning and error messages.

# Load the error log file.
error_file_location = config["general"]["interface_directory"] + "/errors.json"
if (os.path.exists(error_file_location) == False): # If the error log file doesn't exist, create it.
    save_to_file(error_file_location, "{}") # Save a blank placeholder dictionary to the error log file.

error_file = open(error_file_location, "r") # Open the error log file for reading.
error_file_contents = error_file.read() # Read the raw contents of the error file as a string.
error_file.close() # Close the error log file.

if (is_json(error_file_contents) == True): # If the error file contains valid JSON data, then load it.
    error_log = json.loads(error_file_contents) # Read and load the error log from the file.
else: # If the error file doesn't contain valid JSON data, then load a blank placeholder in it's place.
    error_log = json.loads("{}") # Load a blank placeholder dictionary.

def display_message(message, level=1):
    if (level == 1): # Display the message as a notice.
        error_log[get_time()] = {"msg": message, "type": "notice"} # Add this message to the log file, using the current time as the key.
        save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        print("Notice: " + message)
    elif (level == 2): # Display the message as a warning.
        error_log[get_time()] = {"msg": message, "type": "warn"} # Add this message to the log file, using the current time as the key.
        save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        print(style.yellow + "Warning: " + message + style.end)
    elif (level == 3): # Display the message as an error.
        error_log[get_time()] = {"msg": message, "type": "error"} # Add this message to the log file, using the current time as the key.
        save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        print(style.red + "Error: " + message + style.end)
        prompt(style.faint + "Press enter to continue..." + style.end)




# Define the function used to prompt the user for input.
def prompt(message, optional=True, input_type=str, default=""):
    user_input = input(message)

    if (optional == True and user_input == ""): # If the this input is optional, and the user left the input blank, then simply return the default value.
        if (input_type == str):
            return default
        elif (input_type == int):
            return int(default)
        elif (input_type == float):
            return float(default)
        elif (input_type == bool):
            if (type(default) != bool): # Check to see if the default is not a boolean value.
                return False # Default to returning `false`.
            else:
                return default
        elif (input_type == list):
            if (type(default) != list):
                return []
            else:
                return default

    if (optional == False): # If this input is not optional, then repeatedly take an input until an input is given.
        while (user_input == ""): # Repeated take the user's input until something is entered.
            display_message("This input is not optional.", 2)
            user_input = input(message)

    if (input_type == str):
        return str(user_input)

    elif (input_type == float or input_type == int):
        while (is_number(user_input) == False):
            display_message("The input needs to be a number.", 2)
            user_input = input(message)
        return float(user_input)

    elif (input_type == bool):
        if (len(user_input) > 0):
            if (user_input[0].lower() == "y" or user_input[0].lower() == "t"):
                user_input = True
            elif (user_input[0].lower() == "n" or user_input[0].lower() == "f"):
                user_input = False

        while (type(user_input) != bool): # Run repeatedly until the input is a boolean.
            display_message("The input needs to be a boolean.", 2)
            user_input = input(message)
            if (len(user_input) > 0):
                if (user_input[0].lower() == "y" or user_input[0].lower() == "t"):
                    user_input = True
                elif (user_input[0].lower() == "n" or user_input[0].lower() == "f"):
                    user_input = False

    elif (input_type == list):
        user_input = user_input.split(",") # Convert the user's input into a list.
        user_input = [element.strip() for element in user_input] # Strip any leading or trailing white space on each element in the list.

    return user_input




def play_sound(sound_id):
    sound_key = sound_id + "_sound"
    if (sound_key in config["realtime"]["sounds"]): # Check to make sure this sound ID actually exists in the configuration
        debug_message("Playing '" + sound_id + "' sound")
        if (int(config["realtime"]["sounds"][sound_key]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
            for i in range(0, int(config["realtime"]["sounds"][sound_key]["repeat"])): # Repeat the sound several times, if the configuration says to.
                os.system("mpg321 " + config["realtime"]["sounds"][sound_key]["path"] + " > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                time.sleep(float(config["realtime"]["sounds"][sound_key]["delay"])) # Wait before playing the sound again.
    else: # No sound with this ID exists in the configuration database, and therefore the sound can't be played.
        display_message("No sound with the ID (" + str(sound_id) + ") exists in the configuration.", 3)



# This function validates a license plate given a template.
def validate_plate(plate, template):
    plate_valid = True # By default, the plate is valid, until we find a character that doesn't align.

    if (len(template) == len(plate)): # Make sure the template and plate are the same length. If so, continue with validation. Otherwise, automatically invalidate the plate, and skip the rest of the validation process.
        for x in range(len(template)):
            if (template[x].isalpha() == plate[x].isalpha() or template[x].isnumeric() == plate[x].isnumeric()): # If this character is alphabetical in both the template and plate, or if this character is numeric in both the template and plate, then this character is valid.
                # This character is valid, so don't change anything.
                pass
            else:
                # This character doesn't match between the template and plate, so mark the plate as invalid.
                plate_valid = False
    else:
        plate_valid = False

    return plate_valid # Return the results of the plate validation




# This is a simple function used to display large ASCII shapes.
def display_shape(shape):
    if (shape == "square"):
        print(style.bold)
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print("######################")
        print(style.end)

    elif (shape == "circle"):
        print(style.bold)
        print("        ######")
        print("     ############")
        print("   ################")
        print("  ##################")
        print(" ####################")
        print("######################")
        print("######################")
        print("######################")
        print(" ####################")
        print("  ##################")
        print("   ################")
        print("     ############")
        print("        ######")
        print(style.end)

    elif (shape == "triangle"):
        print(style.bold)
        print("           #")
        print("          ###")
        print("         #####")
        print("        #######")
        print("       #########")
        print("      ###########")
        print("     #############")
        print("    ###############")
        print("   #################")
        print("  ###################")
        print(" #####################")
        print("#######################")
        print(style.end)

    elif (shape == "diamond"):
        print(style.bold)
        print("           #")
        print("          ###")
        print("         #####")
        print("        #######")
        print("       #########")
        print("      ###########")
        print("      ###########")
        print("       #########")
        print("        #######")
        print("         #####")
        print("          ###")
        print("           #")
        print(style.end)

    elif (shape == "cross"):
        print(style.bold)
        print("########              ########")
        print("  ########          ########")
        print("    ########      ########")
        print("      ########  ########")
        print("        ##############")
        print("          ##########")
        print("        ##############")
        print("      ########  ########")
        print("    ########      ########")
        print("  ########          ########")
        print("########              ########")
        print(style.end)







# Define the function that will be used to get the current GPS coordinates.
last_gps_request = {} # This is a placeholder that will store information regarding the last GPS request.
def get_gps_location():
    global last_gps_request
    if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled.
        gpsd.connect() # Connect to the GPS daemon.
        gps_data_packet = gpsd.get_current() # Query the GPS for the most recent information.
        if (gps_data_packet.mode >= 2): # Check to see if the GPS has a fix yet.
            gps_time = gps_data_packet.time
            position = gps_data_packet.position()
            speed = gps_data_packet.speed()
        else:
            position = [0, 0]
            speed = 0
            gps_time = 0
        if (gps_data_packet.mode >= 3): # Check to see if the GPS has a 3D fix yet.
            altitude = gps_data_packet.altitude()
            heading = gps_data_packet.movement()["track"]
            satellites = gps_data_packet.sats
        else:
            altitude = 0 # Use a placeholder for altitude.
            heading = 0 # Use a placeholder for heading.
            satellites = 0 # Use a placeholder for satellites.

        return position[0], position[1], speed, altitude, heading, satellites, gps_time
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        display_message("The `get_gps_location` function was called, even though GPS is disabled. This is a bug, and should never occur.", 2)
        return 0.0000, 0.0000, 0.0, 0.0, 0.0, 0, 0 # Return a default placeholder location.




# This function is used to convert speeds from meters per second, to other units.
def convert_speed(speed, unit="mph"):
    unit = unit.lower() # Convert the unit to all lowercase in order to make it easier to work with and remove inconsistencies in configuration setups.

    if (unit == "kph"): # Convert the speed to kilometers per hour.
        speed = speed * 3.6 # The speed is already measured in kilometers per hour, so there is no reason to convert it.
    elif (unit == "mph"): # Convert the speed to miles per hour.
        speed = speed * 2.236936
    elif (unit == "mps"): # Convert the speed to meters per second.
        speed = speed # The speed is already measured in meters per second, so there is no reason to convert it.
    elif (unit == "knot"): # Convert the speed to meters per second.
        speed = speed * 1.943844
    elif (unit == "fps"): # Convert the speed to feet per second.
        speed = speed * 3.28084
    else: # If an invalid unit was supplied, then simply return a speed of zero.
        debug_message("An invalid unit for speed conversion was supplied. The speed could not be converted to the desired format.", 2) # Display a notice that the speed could not be converted.
        speed = 0 # Set the converted speed to 0 as a placeholder.


    return speed # Return the converted speed.




# This function is used to display a number as a large ASCII character.
def display_number(display_number="0"):
    numbers = {} # Create a placeholder dictionary for all numbers.
    numbers["."] = ["    ", "    ", "    ", "    ", "    ", "    ", " ## ", " ## "] # Define each line in the ASCII art for zero.
    numbers["0"] = [" $$$$$$\\  ", "$$$ __$$\\ ", "$$$$\\ $$ |", "$$\\$$\\$$ |", "$$ \\$$$$ |", "$$ |\\$$$ |", "\\$$$$$$  /", " \\______/ "] # Define each line in the ASCII art for zero.
    numbers["1"] = ["  $$\\   ", "$$$$ |  ", "\\_$$ |  ", "  $$ |  ", "  $$ |  ", "  $$ |  ", "$$$$$$\ ", "\\______|"] # Define each line in the ASCII art for one.
    numbers["2"] = [" $$$$$$\\  ", "$$  __$$\\ ", "\\__/  $$ |", " $$$$$$  |", "$$  ____/ ", "$$ |      ", "$$$$$$$$\\ ", "\\________|"] # Define each line in the ASCII art for two.
    numbers["3"] = [" $$$$$$\\  ", "$$ ___$$\\ ", "\\_/   $$ |", "  $$$$$ / ", "  \\___$$\\ ", "$$\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for three.
    numbers["4"] = ["$$\\   $$\\ ", "$$ |  $$ |", "$$ |  $$ |", "$$$$$$$$ |", "\\_____$$ |", "      $$ |", "      $$ |", "      \\__|"] # Define each line in the ASCII art for four.
    numbers["5"] = ["$$$$$$$\\  ", "$$  ____| ", "$$ |      ", "$$$$$$$\\  ", "\_____$$\\ ", "$$\\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for five.
    numbers["6"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  \\__|", "$$$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", " $$$$$$  |", " \\______/ "] # Define each line in the ASCII art for six.
    numbers["7"] = ["$$$$$$$$\\ ", "\\____$$  |", "    $$  / ", "   $$  /  ", "  $$  /   ", " $$  /    ", "$$  /     ", "\\__/      "] # Define each line in the ASCII art for seven.
    numbers["8"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", " $$$$$$  |", "$$  __$$< ", "$$ /  $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for eight.
    numbers["9"] = [" $$$$$$\\  ", "$$  __$$\\ ", "$$ /  $$ |", "\\$$$$$$$ |", " \\____$$ |", "$$\\   $$ |", "\\$$$$$$  |", " \\______/ "] # Define each line in the ASCII art for nine.

    display_lines = {} # Create a placeholder for each line that will be printed to the console.

    for line_count in range(0, 8): # Iterate through each of the 8 lines that the output will have.
        display_lines[line_count] = "" # Set each line to an empty placeholder string.

    for display_character in str(display_number): # Iterate through each character that needs to be displayed.
        for individual_display_line in range(0, 8): # Iterate through each line that will be displayed to the console output.
            display_lines[individual_display_line] = str(display_lines[individual_display_line]) + numbers[str(display_character)][individual_display_line] # Add each number to each line of the output.

    for line_index in display_lines: # Iterate through each line that needs to displayed.
        print(display_lines[line_index]) # Print each individual line.




# This function returns the nearest timestamp key in dictionary to a given timestamp.
def closest_key(array, search_key):
    current_best = [0, get_time()]
    for key in array: # Iterate through each timestamp in the given dictionary.
        difference = abs(float(search_key) - float(key)) # Calculate the difference in time between the given timestamp, and this timestamp.
        if (difference < current_best[1]): # Check to see if this entry is closer than the current best.
            current_best = [key, difference] # Make this entry the current best.

    return current_best # Return the closest found entry.




# This function is used to display a list of provided license plate alerts.
def display_alerts(active_alerts):
    for alert in active_alerts: # Iterate through each active alert.
        # Display an alert that is starkly different from the rest of the console output.
        print(style.yellow + style.bold)
        print("===================")
        print("ALERT HIT - " + str(alert))
        if ("rule" in active_alerts[alert]): # Check to see if a rule exists for this alert plate. This should always be the case, but it's worth checking for sake of stability.
            print("Rule: " + str(active_alerts[alert]["rule"])) # Display the rule that triggered this alert.
        if ("name" in active_alerts[alert]): # Check to see if a name exists for this alert plate.
            print("Name: " + str(active_alerts[alert]["name"])) # Display this alert plate's name.
        if ("description" in active_alerts[alert]): # Check to see if a name exists for this alert plate.
            print("Description: " + str(active_alerts[alert]["description"])) # Display this alert plate's description.
        print("===================")
        print(style.end + style.end)



# This function compiles the provided list of sources into a single complete alert dictionary.
def load_alert_database(sources, project_directory):
    debug_message("Loading license plate alert list")
    complete_alert_database = {} # Set the complete alert database to a placeholder dictionary.
    for source in sources: # Iterate through each source in the list of sources.
        if (validators.url(source)): # Check to see if the user supplied a URL as their alert database.
            if (config["developer"]["offline"] == False): # Check to see if offline mode is disabled.
                try:
                    raw_download_data = requests.get(source, timeout=6).text # Save the raw text data from the URL to a variable.
                except:
                    raw_download_data = ""
                processed_download_data = str(raw_download_data) # Convert the downloaded data to a string.
                try:
                    alert_database = json.loads(processed_download_data) # Load the alert database as JSON data.
                except:
                    alert_database = {}
                    display_message("The license plate alert database returned by the remote source " + source + " doesn't appear to be compatible JSON data. This source has not been loaded.", 3)
            else: # Predator is in offline mode, but a remote alert database source was specified.
                alert_database = {} # Set the alert database to an empty dictionary.
                display_message("A remote alert database source " + source + " was specified, but Predator is in offline mode. This source has not been loaded.", 2)
        else: # The input the user supplied doesn't appear to be a URL, so assume it is a file.
            if (os.path.exists(project_directory + "/" + source)): # Check to see if the database specified by the user actually exists.
                f = open(project_directory + "/" + source, "r") # Open the user-specified database file.
                file_contents = f.read() # Read the file.
                if (file_contents[0] == "{"): # Check to see if the first character in the file indicates that this alert database is a JSON database.
                    alert_database = json.loads(file_contents) # Load the alert database as JSON data.
                else:
                    alert_database = {}
                    display_message("The alert database specified at " + project_directory + "/" + source + " does appear to contain compatible JSON data. This source has not been loaded.", 3)
                f.close() # Close the file.
            else: # If the alert database specified by the user does not exist, alert the user of the error.
                alert_database = {}
                display_message("The alert database specified at " + project_directory + "/" + source + " does not exist. This source has not been loaded.", 3)

        for rule in alert_database: # Iterate over each rule in this database.
            complete_alert_database[rule] = alert_database[rule] # Add this rule to the complete alert database.

    return complete_alert_database




# This function is used to parse GPX files into a Python dictionary.
def process_gpx(gpx_file):
    gpx_file = open(gpx_file, 'r') # Open the GPX file.
    xmldoc = minidom.parse(gpx_file) # Read the full XML GPX document.

    track = xmldoc.getElementsByTagName('trkpt') # Get all of the location information from the GPX document.
    timing = xmldoc.getElementsByTagName('time') # Get all of the timing information from the GPX document.

    gpx_data = {} # This is a dictionary that will hold each location point, where the key is a timestamp.

    for i in range(0, len(timing)): # Iterate through each point in the GPX file.
        point_lat = track[i].getAttribute('lat') # Get the latitude for this point.
        point_lon = track[i].getAttribute('lon') # Get the longitude for this point.
        point_time = str(timing[i].toxml().replace("<time>", "").replace("</time>", "").replace("Z", "").replace("T", " ")) # Get the time for this point in human readable text format.

        point_time = round(time.mktime(datetime.datetime.strptime(point_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the human readable timestamp into a Unix timestamp.

        gpx_data[point_time] = {"lat": point_lat, "lon": point_lon} # Add this point to the decoded GPX data.


    return gpx_data



