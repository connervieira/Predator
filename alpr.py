# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import csv
import os
import time
import json # Required to process JSON data


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but if it doesn't, you can change it manually.


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
style = utils.style # Load style information from the utils script.
is_json = utils.is_json # Load the function to check if a given string is valid JSON.
debug_message  = utils.debug_message # Load the debug message function from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
prompt = utils.prompt # Load the user input prompt function from the utils script.
save_to_file = utils.save_to_file # Load the user input prompt function from the utils script.
display_message = utils.display_message # Load the display message function from the utils script.

import subprocess
import threading


alpr_stream_file_location = "/dev/shm/predator_alpr_stream" # This determines where the text file for streaming ALPR information will be stored.


global queued_plate_reads
queued_plate_reads = []


def alpr_stream(device):
    debug_message("Starting ALPR stream")
    if (config["general"]["alpr"]["engine"] == "phantom"): # Check to see if the configure ALPR engine is Phantom.
        alpr_command = "alpr -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " " + config["realtime"]["image"]["camera"]["devices"][device] + " >> " + alpr_stream_file_location # Set up the Phantom ALPR command.
    if (config["general"]["alpr"]["engine"] == "openalpr"): # Check to see if the configure ALPR engine is OpenALPR.
        alpr_command = "alpr -j -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " " + config["realtime"]["image"]["camera"]["devices"][device] + " >> " + alpr_stream_file_location # Set up the Phantom ALPR command.
    alpr_stream_process = os.popen(alpr_command) # Execute the ALPR command.

def alpr_stream_maintainer(): # This function runs an endless loop that maintains
    global queued_plate_reads
    last_message_received = utils.get_time() + 5 # This variable holds the time that the last ALPR message was received. Initialize it to a time a few seconds into the future to allow the ALPR process extra time to start before a warning is displayed.
    while True:
        debug_message("Starting ALPR stream maintainance cycle")
        time.sleep(0.3) # Delay for a short period of time before each loop so that the ALPR stream has time to output some results.
        stream_file = open(alpr_stream_file_location) # Open the ALPR stream file.
        stream_file_contents = stream_file.readlines() # Read the stream file line by line.
        stream_file.close() # Close the ALPR stream file.
        save_to_file(alpr_stream_file_location, "") # Erase the contents of the ALPR stream file.

        for message in stream_file_contents: # Iterate through each line in the loaded stream file contents.
            if (is_json(message) == True):
                last_message_received = utils.get_time() # Update the last message received time to the current time.
                message = json.loads(message) # Parse each line into JSON.
                if ("error" in message): # Check to see if there were errors while executing the ALPR process. This will only work for alerts issued by Phantom, not OpenALPR.
                    display_message("Phantom ALPR encountered an error: " + message["error"], 2) # Display the ALPR error.
                for plate in message["results"]: # Iterate through each license plate in this line.
                    queued_plate_reads.append(plate) # Add each license plate to the license plate queue.
            else:
                display_message("The information returned by the ALPR engine is not valid JSON. Maybe you've specified the wrong ALPR engine in the configuration?", 2)

        if (utils.get_time() - last_message_received > 3): # Check to see if a certain number of seconds have passed without receiving any messages from the ALPR process.
            display_message("The ALPR stream hasn't received any ALPR messages in several seconds. The ALPR process may not be running.", 2)


def start_alpr_stream(): # This function starts the ALPR stream threads.
    save_to_file(alpr_stream_file_location, "") # Erase the contents of the ALPR stream file.
    alpr_stream_count = 0 # This will keep track of the number of ALPR streams running.
    alpr_stream_threads = {} # This is a dictionary that will hold the ALPR sub-threads.
    os.popen("killall alpr") # Kill any ALPR processes that are running in the background in case they weren't terminated properly the last time Predator was run.
    time.sleep(1) # Wait for 1 second before launching the new ALPR processes.
    for device in config["realtime"]["image"]["camera"]["devices"]: # Iterate through each device in the configuration.
        debug_message("Starting ALPR stream " + str(alpr_stream_count))
        alpr_stream_threads[alpr_stream_count] = threading.Thread(target=alpr_stream, args=([device]), name="ALPRStream" + str(device)) # Initialize the ALPR stream thread.
        alpr_stream_threads[alpr_stream_count].start() # Start the ALPR stream thread.
        alpr_stream_count = alpr_stream_count + 1
    alpr_stream_maintainer_thread = threading.Thread(target=alpr_stream_maintainer, name="ALPRStreamMaintainer") # Initialize the ALPR stream maintainer thread.
    alpr_stream_maintainer_thread.start() # Start the ALPR stream maintainer thread.


def alpr_get_queued_plates(): # This function is used to fetch the latest queue of detected license plates.
    global queued_plate_reads
    results_to_return = queued_plate_reads
    queued_plate_reads = [] # Clear the license plate queue.
    return results_to_return




# This function loads the license plate log, and initializes the file if necessary.
def load_alpr_log():
    global config
    debug_message("Loading license plate history")
    plate_log_file_location = config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"]
    if (os.path.exists(plate_log_file_location) == False): # If the plate log file doesn't exist, create it.
        save_to_file(plate_log_file_location, "{}") # Save a blank placeholder dictionary to the plate log file.

    plate_log_file = open(plate_log_file_location, "r") # Open the plate log file for reading.
    plate_log_file_contents = plate_log_file.read() # Read the raw contents of the plate file as a string.
    plate_log_file.close() # Close the plate log file.

    if (is_json(plate_log_file_contents) == True): # If the plate file contains valid JSON data, then load it.
        plate_log = json.loads(plate_log_file_contents) # Read and load the plate log from the file contents.
    else: # If the plate log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
        plate_log = json.loads("{}") # Load a blank placeholder dictionary.

    return plate_log



# This function runs ALPR on a given image file, and returns the results.
def run_alpr(image_filepath):
    global config
    if (config["general"]["alpr"]["engine"] == "phantom"): # Check to see if the configuration indicates that the Phantom ALPR engine should be used.
        analysis_command = "alpr -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " '" + image_filepath + "'"
        reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
        reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
        if ("error" in reading_output): # Check to see if there were errors.
            print("Phantom ALPR encountered an error: " + reading_output["error"]) # Display the ALPR error.
            reading_output["results"] = [] # Set the results of the reading output to a blank placeholder list.
    elif (config["general"]["alpr"]["engine"] == "openalpr"): # Check to see if the configuration indicates that the OpenALPR engine should be used.
        analysis_command = "alpr -j -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " " + config["general"]["working_directory"] + "/frames/" + frame # Set up the OpenALPR command.
        reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
        reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
    else: # If the configured ALPR engine is unknown, then return an error.
        display_message("The configured ALPR engine is not recognized.", 3)
        reading_output = {}

    return reading_output
