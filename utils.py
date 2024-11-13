# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This script contains several functions and classes used in main.py



import global_variables

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


import sys # Required to process command line arguments.
import pytz # Required to handle timezones.
import time # Required to add delays and handle dates/times

if (time.daylight and time.localtime().tm_isdst >= 1):
    daylight_savings = True
else:
    daylight_savings = False
timezone_offset = -(time.altzone if daylight_savings else time.timezone) # This is the local timezone's offset from UTC in seconds.

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
            debugging_time_record[thread] = time.time()
        time_since_last_message = (time.time()-debugging_time_record[thread]) # Calculate the time since the last debug message.
        print(f"{style.italic}{style.faint}{time.time():.10f} ({time_since_last_message:.10f} - {thread}) - {message}{style.end}") # Print the message.
        debugging_time_record[thread] = time.time() # Record the current timestamp.


import threading


def manage_time_offset(): # This function watches the system time, and reset the time offset if the system time changes.
    global global_time_offset
    debug_message("Starting time offset management.")
    while global_variables.predator_running: # Run forever.
        start_time = time.time()
        time.sleep(1) # Wait for 1 second before checking the time again.
        end_time = time.time()
        difference_time = (end_time - start_time) - 1
        if (abs(difference_time) > 0.5): # Check to see if the system time changed by more than half a second.
            global_time_offset = global_time_offset - difference_time # Reset the global time offset.
            display_message("The system time appears to have been changed. The global time offset has been updated.", 2)
time_offset_management_thread = threading.Thread(target=manage_time_offset, name="TimeOffsetManager") # Create the time offset manager thread.
time_offset_management_thread.start() # Start the time offset.



process_timers = {}
def process_timing(action, identifier):
    global process_timers

    thread = threading.current_thread().name # Get the name of the current thread.

    if (config["developer"]["print_timings"] == True): # Only run timing if it is enabled in the configuration.
        if (thread not in process_timers and action != "dump"): # Check to see if the specified identifier doesn't exist in the process_timer dictionary.
            process_timers[thread] = {} # Initialize the timer for this thread.
        if (identifier not in process_timers[thread] and action != "dump"): # Check to see if the specified identifier doesn't exist in the process_timer dictionary.
            process_timers[thread][identifier] = {"total": 0, "start": 0} # Initialize the timer for this process.

        if (action == "dump"):
            return process_timers
        elif (action == "start"):
            process_timers[thread][identifier]["start"] = time.time()
        elif (action == "end"):
            if (process_timers[thread][identifier]["start"] != 0):
                process_timers[thread][identifier]["total"] = process_timers[thread][identifier]["total"] + (time.time() - process_timers[thread][identifier]["start"])
                process_timers[thread][identifier]["start"] = 0
            else:
                display_message("The `processing_timing` function was called setting the end of the timer (" + identifier + "), but the timer wasn't started. This is likely a bug.", 2)
        else:
            display_message("The `processing_timing` function was called with an unknown action. This likely a bug.", 2)





import subprocess # Required for starting some shell commands
import sys
try:
    if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
        if (config["general"]["status_lighting"]["enabled"] == True or config["realtime"]["push_notifications"]["enabled"] == True or len(config["general"]["alerts"]["databases"]) > 0):
            import requests # Required to make network requests
            import validators # Required to validate URLs
except:
    print("Failed to determine if network features are enabled in the configuration.")
if (len(config["general"]["alerts"]["databases"]) > 0):
    import hashlib
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
from xml.dom import minidom # Required for processing GPX data
if (config["general"]["gps"]["enabled"] == True): # Only import the GPS libraries if GPS settings are enabled.
    from gps import * # Required to access GPS information.
    import gpsd
import signal # Required to time out functions.
if ("developer" not in config or "frame_count_method" not in config["developer"]):
    config["developer"]["frame_count_method"] = "manual"
if (config["developer"]["frame_count_method"] in ["manual" or "opencv"]):
    try:
        import cv2
    except Exception as e:
        print(e)
        print("cv2 is required because the `developer>frame_count_method` value is set to 'manual' or 'opencv'")



if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    if (os.path.exists(config["general"]["interface_directory"]) == False): # Check to see if the interface directory is missing.
        try:
            os.makedirs(config["general"]["interface_directory"]) # Attempt to create the interface directory.
            os.system("chmod 777 " + config["general"]["interface_directory"]) # Make the interface directory accessible to all users and processes.
        except:
            print(style.red + "Failed to create interface directory. Is the `general>interface_directory` configuration value set to a valid file-path?" + style.end)
            exit()



# Define the function that will be used to clear the screen.
def clear(force=False):
    if (config["general"]["display"]["debugging_output"] == False or force == True): # Only clear the console if the debugging output configuration value is disabled.
        if ("--headless" not in sys.argv): # Only clear the console if Predator is not operating in headless mode.
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

    plate_log[time.time()] = detected_plates
    entries_to_remove = [] # Create a blank placeholder list to hold all of the entry keys that have expired and need to be removed.

    for entry in plate_log.keys(): # Iterate through each entry in the plate history.
        if (time.time() - float(entry) > 10): # Check to see if this entry has expired according the max age configuration value.
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

    alert_log[time.time()] = active_alerts
    entries_to_remove = [] # Create a blank placeholder list to hold all of the entry keys that have expired and need to be removed.

    for entry in alert_log.keys(): # Iterate through each entry in the alert history.
        if (time.time() - float(entry) > 10): # Check to see if this entry has expired according the max age configuration value.
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
    if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
        heartbeat_thread = threading.Thread(target=issue_heartbeat, name="InterfaceHeartbeatUpdate")
        heartbeat_thread.start()

def issue_heartbeat(): # This is the function that actually issues a heartbeat.
    global heartbeat_log
    heartbeat_log.append(time.time()) # Add this pulse to the heartbeat log file, using the current time as the key.
    if (len(heartbeat_log) >= 1):
        heartbeat_log = heartbeat_log[-10:] # Trim the list to only contain the last entries.
    save_to_file(heartbeat_file_location, json.dumps(heartbeat_log)) # Save the modified heartbeat log to the disk as JSON data.




# Define the function used to handle system state updates, which allow external services to see the current state of Predator.
if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
    state_file_location = config["general"]["interface_directory"] + "/state.json"
    save_to_file(state_file_location, "{}") # Save a blank placeholder dictionary to the state log file.

current_state = {}
def update_state(mode, performance={}): # This is the function that is called to issue a state update.
    global current_state
    current_state["mode"] = mode
    current_state["performance"] = performance
    if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
        state_update_thread = threading.Thread(target=update_state_file, args=[current_state], name="InterfaceStateUpdate")
        state_update_thread.start()
def update_state_file(current_state): # This is the function that actually issues a status update to disk.
    save_to_file(state_file_location, json.dumps(current_state)) # Save the modified state to the disk as JSON data.
def get_current_state():
    global current_state
    return current_state



# Define the function to display warning and error messages.

# Load the error log file.
if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
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

last_message = {"notice": 0, "warning": 0, "error": 0}
def display_message(message, level=1):
    if (level == 1): # Display the message as a notice.
        if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
            error_log[time.time()] = {"msg": message, "type": "notice"} # Add this message to the log file, using the current time as the key.
            save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        if (time.time() - last_message["notice"] > 10):
            play_sound("message_notice")
        last_message["notice"] = time.time()
        print("Notice: " + message)
    elif (level == 2): # Display the message as a warning.
        if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
            error_log[time.time()] = {"msg": message, "type": "warn"} # Add this message to the log file, using the current time as the key.
            save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        if (time.time() - last_message["warning"] > 10):
            play_sound("message_warning")
        last_message["warning"] = time.time()
        print(style.yellow + "Warning: " + message + style.end)
        prompt(style.faint + "Press enter to continue..." + style.end)
    elif (level == 3): # Display the message as an error.
        if (config["general"]["interface_directory"] != ""): # Check to see if the interface directory is enabled.
            error_log[time.time()] = {"msg": message, "type": "error"} # Add this message to the log file, using the current time as the key.
            save_to_file(error_file_location, json.dumps(error_log)) # Save the modified error log to the disk as JSON data.
        if (time.time() - last_message["error"] > 10):
            play_sound("message_error")
        last_message["error"] = time.time()
        print(style.red + "Error: " + message + style.end)
        if (config["developer"]["hard_crash_on_error"] == True):
            global_variables.predator_running = False
            os._exit(1)
        prompt(style.faint + "Press enter to continue..." + style.end)




def is_number(value):
    try:
        value = float(value)
        return True
    except ValueError:
        return False


# Define the function used to prompt the user for input.
def prompt(message, optional=True, input_type=str, default=""):
    if ("--headless" in sys.argv): # Check to see if the headless flag exists in the command line arguments.
        return default

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
            if (user_input[0].lower() == "y" or user_input[0].lower() == "t" or user_input[0].lower() == "1"):
                user_input = True
            elif (user_input[0].lower() == "n" or user_input[0].lower() == "f" or user_input[0].lower() == "0"):
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
    if (sound_id in config["general"]["audio"]["sounds"]): # Check to make sure this sound ID actually exists in the configuration.
        debug_message("Playing '" + sound_id + "' sound")
        if (config["general"]["audio"]["enabled"] == True): # Check if audio playback is enabled.
            if (int(config["general"]["audio"]["sounds"][sound_id]["repeat"]) > 0): # Check to see if the user has audio alerts enabled.
                for i in range(0, int(config["general"]["audio"]["sounds"][sound_id]["repeat"])): # Repeat the sound several times, if the configuration says to.
                    if (config["general"]["audio"]["player"]["backend"] == "mpg321"):
                        os.system("mpg321 \"" + config["general"]["audio"]["sounds"][sound_id]["path"] + "\" > /dev/null 2>&1 &") # Play the sound specified for this alert type in the configuration.
                    elif (config["general"]["audio"]["player"]["backend"] == "mplayer"):
                        if (len(config["general"]["audio"]["player"]["mplayer"]["device"]) == 0):
                            os.system("mplayer \"" + config["general"]["audio"]["sounds"][sound_id]["path"] + "\" -noconsolecontrols 2>&- 1>/dev/null &") # Play the sound specified for this alert type in the configuration.
                        else:
                            os.system("mplayer -ao " + config["general"]["audio"]["player"]["mplayer"]["device"] + " \"" + config["general"]["audio"]["sounds"][sound_id]["path"] + "\" -noconsolecontrols 2>&- 1>/dev/null &") # Play the sound specified for this alert type in the configuration.
                    else:
                        display_message("The configured audio player back-end is invalid.", 3)
                    time.sleep(float(config["general"]["audio"]["sounds"][sound_id]["delay"])) # Wait before playing the sound again.
    else: # No sound with this ID exists in the configuration database, and therefore the sound can't be played.
        display_message("No sound with the ID (" + str(sound_id) + ") exists in the configuration.", 3)







# This function is used to parse GPX files into a Python dictionary.
def process_gpx(gpx_file, modernize=False): # `gpx_file` is the absolute path to a GPX file. `modernize` determines if the timestamps will be offset such that the first timestamp is equal to the current time.
    gpx_file = open(gpx_file, 'r') # Open the GPX file.
    xmldoc = minidom.parse(gpx_file) # Read the full XML GPX document.

    track = xmldoc.getElementsByTagName('trkpt') # Get all of the location information from the GPX document.
    speed = xmldoc.getElementsByTagName('speed') # Get all of the speed information from the GPX document.
    altitude = xmldoc.getElementsByTagName('ele') # Get all of the elevation information from the GPX document.
    timing = xmldoc.getElementsByTagName('time') # Get all of the timing information from the GPX document.

    offset = 0 # This is the value that all timestamps in the file will be offset by.
    if (modernize == True): # Check to see if this GPX file should be modernized, such that the first entry in the file is the current time, and all subsequent points are offset by the same amount.
        first_point_time = str(timing[0].toxml().replace("<time>", "").replace("</time>", "").replace("Z", "").replace("T", " ")) # Get the time for the first point in human readable text format.

        first_point_time = round(time.mktime(datetime.datetime.strptime(first_point_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the human readable timestamp into a Unix timestamp.
        offset = get_time()-first_point_time # Calculate the offset to make the first point in this GPX file the current time.

    gpx_data = {} # This is a dictionary that will hold each location point, where the key is a timestamp.

    for i in range(0, len(track)): # Iterate through each point in the GPX file.
        point_lat = track[i].getAttribute('lat') # Get the latitude for this point.
        point_lon = track[i].getAttribute('lon') # Get the longitude for this point.
        try:
            point_speed = speed[i].toxml().replace("<speed>","").replace("</speed>","")
        except:
            point_speed = 0
        try:
            point_altitude = altitude[i].toxml().replace("<ele>","").replace("</ele>","")
        except:
            point_altitude = 0
        point_time = str(timing[i].toxml().replace("<time>", "").replace("</time>", "").replace("Z", "").replace("T", " ")) # Get the time for this point in human readable text format.

        point_time = round(time.mktime(datetime.datetime.strptime(point_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the human readable timestamp into a Unix timestamp.

        gpx_data[point_time + offset] = {"lat": float(point_lat), "lon": float(point_lon), "spd": float(point_speed), "alt": float(point_altitude)} # Add this point to the decoded GPX data.

    return gpx_data




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
if (len(config["general"]["gps"]["demo_file"]) > 0): # Check to see if there is a demo file set.
    display_message("The GPS is in demo mode. A pre-recorded file is being played back in place of live GPS data.", 1)
    demo_file_path = config["general"]["working_directory"] + "/" + config["general"]["gps"]["demo_file"]
    if (os.path.exists(demo_file_path)):
        gps_demo_gpx_data = process_gpx(demo_file_path, modernize=True)
    else:
        gps_demo_gpx_data = {}
        display_message("The configured GPS demo file does not exist. GPS functionality is currently disabled.", 2)
    del demo_file_path
elif (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled.
    gpsd.connect() # Connect to the GPS daemon.
last_gps_status = False # This will hold the state of the GPS during the previous location check.
last_gps_fault = 0 # This will hold a timestamp of the last time the GPS encountered a fault.
def get_gps_location():
    global gps_demo_gpx_data
    global current_state
    global global_time_offset
    global last_gps_status
    if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS is enabled.
        if (len(config["general"]["gps"]["demo_file"]) > 0): # Check to see if there is a demo file set.
            current_gpx_key = closest_key(gps_demo_gpx_data, get_time()) # Get the closest entry to the current time in the GPX file.
            current_location = gps_demo_gpx_data[current_gpx_key[0]]
            return current_location["lat"], current_location["lon"], current_location["spd"], current_location["alt"], 0.0, 0, 0 # Return the current location from the GPX file.
        else: # Otherwise, GPS demo mode is disabled.
            try:
                gps_data_packet = gpsd.get_current() # Query the GPS for the most recent information.

                current_state["gps"] = gps_data_packet.mode 
                if (gps_data_packet.mode >= 2): # Check to see if the GPS has a 2D fix yet.
                    try:
                        gps_time = datetime.datetime.strptime(str(gps_data_packet.time)[:-1]+"000" , '%Y-%m-%dT%H:%M:%S.%f').astimezone().timestamp() + timezone_offset # Determine the local Unix timestamp from the GPS timestamp.
                    except:
                        gps_time = 0
                    position = gps_data_packet.position()
                    speed = gps_data_packet.speed()
                else:
                    gps_time = 0
                    position = [0, 0]
                    speed = 0
                if (gps_data_packet.mode >= 3): # Check to see if the GPS has a 3D fix yet.
                    altitude = gps_data_packet.altitude()
                    heading = gps_data_packet.movement()["track"]
                    satellites = gps_data_packet.sats
                else:
                    altitude = 0 # Use a placeholder for altitude.
                    heading = 0 # Use a placeholder for heading.
                    satellites = 0 # Use a placeholder for satellites.

                if (config["general"]["gps"]["time_correction"]["enabled"] == True):
                    if (gps_time > 0 and abs(get_time() - gps_time) > config["general"]["gps"]["time_correction"]["threshold"]):
                        if (gps_time - time.time() < 0): # Check to see if the time offset is a negative number (the system time is in the future).
                            if (gps_time - time.time() < -2): # Only display a warning if the time offset is significantly into negative numbers.
                                display_message("The local system time is in the future relative to the GPS time by " + str(gps_time - time.time()) + "seconds. This can't be corrected by the GPS time offset, and is indicative of a more in-depth time desync problem.", 2)
                        else:
                            global_time_offset = gps_time - time.time()
                            display_message("The local system time differs significantly from the GPS time. Applied time offset of " + str(round(global_time_offset*10**3)/10**3) + " seconds.", 2)

                if (position == [0,0]):
                    if (last_gps_status != False):
                        play_sound("gps_disconnected")
                    last_gps_status = False
                else:
                    if (last_gps_status != True):
                        play_sound("gps_connected")
                    last_gps_status = True
                return position[0], position[1], speed, altitude, heading, satellites, gps_time
            except Exception as exception:
                display_message("A GPS error occurred: " + str(exception), 2)
                if (time.time() - last_gps_fault > 60):
                    play_sound("gps_fault")
                last_gps_fault = time.time()
                return 0.0000, 0.0000, 0.0, 0.0, 0.0, 0, 0 # Return a default placeholder location.
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        display_message("The `get_gps_location` function was called, even though GPS is disabled. This is a bug, and should never occur.", 3)
        if (time.time() - last_gps_fault > 60):
            play_sound("gps_fault")
        last_gps_fault = time.time()
        return 0.0000, 0.0000, 0.0, 0.0, 0.0, 0, 0 # Return a default placeholder location.

most_recent_gps_location = [0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]
def gps_daemon():
    debug_message("Starting lazy GPS daemon")
    global most_recent_gps_location
    while True:
        debug_message("Fetching lazy GPS location")
        most_recent_gps_location = get_gps_location()
        time.sleep(float(config["general"]["gps"]["lazy_polling_interval"])) # Wait before polling the GPS again.
def get_gps_location_lazy(): # This function gets the most recent GPS location from the lazy GPS monitor.
    try:
        return most_recent_gps_location
    except:
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]

if (config["general"]["gps"]["enabled"] == True): # Only start the GPS polling thread if the GPS is enabled.
    gps_daemon_thread = threading.Thread(target=gps_daemon, name="LazyGPSDaemon") # Create the lazy GPS manager thread.
    gps_daemon_thread.start() # Start the GPS daemon thread.




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
        display_message("An invalid unit for speed conversion was supplied. The speed could not be converted to the desired format.", 2) # Display a notice that the speed could not be converted.
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



def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def wait_for_input():
    prompt("Press enter to continue")


# This function takes the corners of a plate identified by the ALPR engine (
# Example input: [{"x": 737, "y": 188}, {"x": 795, "y": 189}, {"x": 795, "y": 219}, {"x": 736, "y": 217}]
# Example output: {"x", 737, "y": 188, "w": 59, "h": 31}
def convert_corners_to_bounding_box(corners):
    if (len(corners) == 4): # Check to see if the number of corners is the expected length.
        all_x = [] # This will hold all X coordinates.
        all_y = [] # This will hold all Y coordinates.
        for corner in corners:
            all_x.append(int(corner["x"]))
            all_y.append(int(corner["y"]))
        
        bounding_box = {
            "x": int(min(all_x)),
            "y": int(min(all_y)),
            "w": int(max(all_x) - min(all_x)),
            "h": int(max(all_y) - min(all_y)),
        }
        return bounding_box
    else: # The number of corners is not the expected length.
        return False


# This function counts the number of frames in a given video file.
def count_frames(video):
    debug_message("Counting frames")
    cap = cv2.VideoCapture(video)
    if (config["developer"]["frame_count_method"] == "opencv"):
        video_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # Count the number of frames in the video.
    elif (config["developer"]["frame_count_method"] == "ffprobe"):
        video_frame_count_command = "ffprobe -select_streams v -show_streams \"" + video + "\" 2>/dev/null | grep nb_frames | sed -e 's/nb_frames=//'" # Define the commmand to count the frames in the video.
        video_frame_count_process = subprocess.Popen(video_frame_count_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True) # Execute the command to count the frames in the video.
        video_frame_count, command_error = video_frame_count_process.communicate() # Fetch the results of the frame count command.
        video_frame_count = int(video_frame_count) # Convert the frame count to an integer.
    elif (config["developer"]["frame_count_method"] == "manual"):
        video_frame_count = 0
        while (cap.isOpened()):
            ret, frame = cap.read() # Get the next frame.
            if (ret == False):
                break
            video_frame_count += 1
    else:
        display_message("Invalid frame count method.", 3)
        video_frame_count = 0
    return video_frame_count


# Calling this function will gracefully stop Predator.
def stop_predator():
    global_variables.predator_running = False
    os._exit(1)
