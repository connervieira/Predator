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
debug_message  = utils.debug_message # Load the debug message function from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
prompt = utils.prompt # Load the user input prompt function from the utils script.
save_to_file = utils.save_to_file # Load the user input prompt function from the utils script.

import subprocess
import threading


alpr_stream_file_location = "/dev/shm/predator_alpr_stream" # This determines where the text file for streaming ALPR information will be stored.


global queued_plate_reads
queued_plate_reads = []


def alpr_stream():
    if (config["general"]["alpr"]["engine"] == "phantom"): # Check to see if the configure ALPR engine is Phantom.
        alpr_command = "alpr -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " " + config["realtime"]["image"]["camera"]["device"] + " >> " + alpr_stream_file_location # Set up the Phantom ALPR command.
    if (config["general"]["alpr"]["engine"] == "openalpr"): # Check to see if the configure ALPR engine is OpenALPR.
        alpr_command = "alpr -j -n " + str(config["general"]["alpr"]["validation"]["guesses"]) + " " + config["realtime"]["image"]["camera"]["device"] + " >> " + alpr_stream_file_location # Set up the Phantom ALPR command.
    alpr_stream_process = os.popen(alpr_command) # Execute the ALPR command.

def alpr_stream_maintainer():
    global queued_plate_reads
    while True:
        time.sleep(1)
        stream_file = open(alpr_stream_file_location) # Open the ALPR stream file.
        stream_file_contents = stream_file.readlines() # Read the stream file line by line.
        stream_file.close() # Close the ALPR stream file.
        save_to_file(alpr_stream_file_location, "", True) # Erase the contents of the ALPR stream file.

        for message in stream_file_contents:
            message = json.loads(message)
            for plate in message["results"]:
                queued_plate_reads.append(plate)

def start_alpr_stream():
    debug_message("Opening ALPR message stream")
    alpr_stream_thread = threading.Thread(target=alpr_stream, name="ALPRStream") # Initialize the ALPR stream thread.
    alpr_stream_thread.start() # Start the ALPR stream thread.
    alpr_stream_maintainer_thread = threading.Thread(target=alpr_stream_maintainer, name="ALPRStreamMaintainer") # Initialize the ALPR stream maintainer thread.
    alpr_stream_maintainer_thread.start() # Start the ALPR stream maintainer thread.


def alpr_get_queued_plates():
    global queued_plate_reads
    results_to_return = queued_plate_reads
    queued_plate_reads = []
    return results_to_return
