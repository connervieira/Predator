# Predator

# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import global_variables
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


try:
    if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
        if (config["general"]["status_lighting"]["enabled"] == True or config["realtime"]["push_notifications"]["enabled"] == True or len(config["general"]["alerts"]["databases"]) > 0):
            import requests # Required to make network requests
            import validators # Required to validate URLs
except:
    print("Failed to determine if network features are enabled in the configuration.")
if (len(config["general"]["alerts"]["databases"]) > 0):
    import hashlib


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
    while global_variables.predator_running:
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
                break # Exit the loop now, since we already know the plate is invalid.
    else:
        plate_valid = False

    return plate_valid # Return the results of the plate validation





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
        analysis_command = "alpr -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " \"" + image_filepath + "\""
        reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
        reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
        if ("error" in reading_output): # Check to see if there were errors.
            print("Phantom ALPR encountered an error: " + reading_output["error"]) # Display the ALPR error.
            reading_output["results"] = [] # Set the results of the reading output to a blank placeholder list.
    elif (config["general"]["alpr"]["engine"] == "openalpr"): # Check to see if the configuration indicates that the OpenALPR engine should be used.
        analysis_command = "alpr -j -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " \"" + image_filepath + "\"" # Set up the OpenALPR command.
        reading_output = str(os.popen(analysis_command).read()) # Run the command, and record the raw output string.
        reading_output = json.loads(reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
    else: # If the configured ALPR engine is unknown, then return an error.
        display_message("The configured ALPR engine is not recognized.", 3)
        reading_output = {}

    return reading_output





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




# The following functions are responsible for loading alert database.
def load_alert_database_remote(source, cache_directory):
    debug_message("Loading remote database source.")
    if (config["realtime"]["saving"]["remote_alert_sources"] == True):
        source_hash = hashlib.md5(source.encode()).hexdigest()
    if (config["developer"]["offline"] == False): # Check to see if offline mode is disabled.
        try:
            raw_download_data = requests.get(source, timeout=6).text # Save the raw text data from the URL to a variable.
        except:
            raw_download_data = "{}"
            display_message("The license plate alert database from " + source + " could not be loaded.", 2)
            if (config["realtime"]["saving"]["remote_alert_sources"] == True):
                if (os.path.exists(cache_directory + "/" + source_hash + ".json")): # Check to see if the cached file exists.
                    debug_message("Attempting to load locally cached data for this remote source.")
                    return load_alert_database_local(cache_directory + "/" + source_hash + ".json") # Load the locally cached file.
        processed_download_data = str(raw_download_data) # Convert the downloaded data to a string.
        try:
            alert_database = json.loads(processed_download_data) # Load the alert database as JSON data.
            if (config["realtime"]["saving"]["remote_alert_sources"] == True):
                if (os.path.isdir(cache_directory) == False):
                    os.system("mkdir -p '" + str(cache_directory) + "'")
                save_to_file(cache_directory + "/" + source_hash + ".json", json.dumps(alert_database))
        except:
            alert_database = {}
            display_message("The license plate alert database returned by the remote source " + source + " doesn't appear to be compatible JSON data. This source has not been loaded.", 2)
    else: # Predator is in offline mode, but a remote alert database source was specified.
        alert_database = {} # Set the alert database to an empty dictionary.
        display_message("A remote alert database source " + source + " was specified, but Predator is in offline mode. This source has not been loaded.", 2)

    save_to_file(config["general"]["interface_directory"] + "/hotlist.json", json.dumps(alert_database, indent=4)) # Save the active alert database to the interface directory.
    return alert_database

def load_alert_database_local(source):
    debug_message("Loading local database source.")
    if (os.path.exists(source)): # Check to see if the database specified by the user actually exists.
        f = open(source, "r") # Open the user-specified database file.
        file_contents = f.read() # Read the file.
        if (file_contents[0] == "{"): # Check to see if the first character in the file indicates that this alert database is a JSON database.
            alert_database = json.loads(file_contents) # Load the alert database as JSON data.
        else:
            alert_database = {}
            display_message("The alert database specified at " + source + " does appear to contain compatible JSON data. This source has not been loaded.", 3)
        f.close() # Close the file.
    else: # If the alert database specified by the user does not exist, alert the user of the error.
        alert_database = {}
        display_message("The alert database specified at " + source + " does not exist. This source has not been loaded.", 3)

    return alert_database

def load_alert_database(sources, project_directory): # This function compiles the provided list of sources into a single complete alert dictionary.
    cache_directory = project_directory + "/" + config["realtime"]["saving"]["remote_alert_sources"]["directory"]
    debug_message("Loading license plate alert list")
    complete_alert_database = {} # Set the complete alert database to a placeholder dictionary.
    for source in sources: # Iterate through each source in the list of sources.
        if (validators.url(source)): # Check to see if the user supplied a URL as their alert database.
            alert_database = load_alert_database_remote(source, cache_directory)
        else: # The input the user supplied doesn't appear to be a URL, so assume it is a file.
            alert_database = load_alert_database_local(project_directory + "/" + source)

        for rule in alert_database: # Iterate over each rule in this database.
            complete_alert_database[rule] = alert_database[rule] # Add this rule to the complete alert database.

    return complete_alert_database


# This function will generate sidecar files containing ALPR information for each video recorded by Predator in dash-cam mode.
def generate_dashcam_sidecar_files(working_directory, dashcam_files):
    global config
    for file in dashcam_files:
        file_basename = os.path.splitext(file)[0] # Get the base name of this video file, with no extension.
        print("Analyzing: " + file)
        sidecar_filepath = working_directory + "/" + file_basename + ".json"
        if (os.path.isfile(sidecar_filepath) == True): # This to see if there is already a side-car file associated with this video.
            print("    This file has already be analyzed.")
        else: # Otherwise, this file needs to be analyzed.
            if (config["general"]["alpr"]["engine"] == "phantom"): # Check to see if the configure ALPR engine is Phantom.
                alpr_command = ["alpr", "-n", str(config["general"]["alpr"]["validation"]["guesses"]),  working_directory + "/" + file] # Set up the OpenALPR command.
            if (config["general"]["alpr"]["engine"] == "openalpr"): # Check to see if the configure ALPR engine is OpenALPR.
                alpr_command = ["alpr", "-j", "-n", str(config["general"]["alpr"]["validation"]["guesses"]),  working_directory + "/" + file] # Set up the OpenALPR command.

            video_frame_count_command = "ffprobe -select_streams v -show_streams " + working_directory + "/" + file + " 2>/dev/null | grep nb_frames | sed -e 's/nb_frames=//'" # Define the commmand to count the frames in the video.
            video_frame_count_process = subprocess.Popen(video_frame_count_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True) # Execute the command to count the frames in the video.
            video_frame_count, command_error = video_frame_count_process.communicate() # Fetch the results of the frame count command.
            video_frame_count = int(video_frame_count) # Convert the frame count to an integer.

            alpr_process = subprocess.Popen(alpr_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # Execute the ALPR command.
            command_output, command_error = alpr_process.communicate()
            command_output = command_output.splitlines()
            if (len(command_output) == video_frame_count): # Check to make sure the number of frames analyzed is the same as the frame count.
                analysis_results = {} # This will hold the analysis results for this video file.
                for frame_number, frame_data in enumerate(command_output): # Iterate through each frame's analysis results from the commmand output.
                    frame_data = json.loads(frame_data)
                    frame_results = {} # This will hold the analysis results for this frame.
                    for result in frame_data["results"]: # Iterate through each plate detected in this frame.
                        top_guess = "" # This will be set to the top plate from the guesses, based on the validation rules.
                        for guess in result["candidates"]: # Iterate through each guess for this plate in order from most to least likely.
                            if (guess["confidence"] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to see if this guess exceeds the minimum confidence value.
                                if any(validate_plate(guess["plate"], format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]) or len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0: # Check to see if this plate passes validation.
                                    top_guess = guess["plate"] # This will be set to the top plate from the guesses, based on the validation rules.
                                    break # Exit the loop, since all subsequent guesses will have a lower confidence.
                        if (top_guess == ""): # Check to see if there weren't any valid guesses for this plate.
                            if (config["general"]["alpr"]["validation"]["best_effort"]): # Check to see if `best_effort` mode is enabled.
                                top_guess = result["candidates"][0]["plate"] # Use the most likely plate as the top guess.
                        if (top_guess != ""): # Check to see if the top guess is set for this plate.
                            frame_results[top_guess] = {} # Initialize this plate in the dictionary of plates for this frame.
                            frame_results[top_guess]["coordinates"] = utils.convert_corners_to_bounding_box(result["coordinates"]) # Add the position of this plate in the image.
                    if (len(frame_results) > 0): # Check to see if there is at least one result for this frame.
                        analysis_results[frame_number] = frame_results # Add this frame's data to the full analysis results.
                save_to_file(sidecar_filepath, json.dumps(analysis_results, indent=4)) # Save the analysis results for this file to the side-car file.
                print("    Analysis complete")
            else:
                print("    The number of frames in the video does not match the number of frames analyzed.")
                print("    Skipping analysis")
