# This script loads the current license plate history file (according to the Predator configuration file), and prints the contents to the console as CSV with the following headers:
# Date,Plate,Alert,Latitude,Longitude
# 2024-09-05 12:29:44,ATY4912,false,41.251224,-86.125122

# Example use: `python3 convert_plate_history_csv.py > new_file.csv`

INCLUDE_HEADER = True # Determines whether or not the header line is printed at the top.


import os # Required to interact with certain operating system functions.
import json # Required to process JSON data.
import datetime # Required to handle timestamps.


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__ + "/.."))) # This identifies the root of the Predator project (the directory containing `main.py`, `config.json`, and the other scripts/support files.


try:
    if (os.path.exists(predator_root_directory + "/config.json")):
        config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database from config.json
    else:
        print("The configuration file doesn't appear to exist at " + predator_root_directory + "/config.json.")
        exit()
except:
    print("The configuration database couldn't be loaded. It may be corrupted.")
    exit()


def is_json(string):
    try:
        json_object = json.loads(string) # Try to load string as JSON information.
    except ValueError as error_message: # If the process fails, then the string is not valid JSON.
        return False # Return 'false' to indicate that the string is not JSON.
    return True # If the try statement is successful, then return 'true' to indicate that the string is valid JSON.


plate_history_filepath = config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"]


plate_log_file = open(plate_history_filepath, "r") # Open the plate log file for reading.
plate_log_file_contents = plate_log_file.read() # Read the raw contents of the plate file as a string.
plate_log_file.close() # Close the plate log file.

if (is_json(plate_log_file_contents) == True): # If the plate file contains valid JSON data, then load it.
    plate_log = json.loads(plate_log_file_contents) # Read and load the plate log from the file contents.
else: # If the plate log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
    print("The contents of the plate log file does not appear to be valid JSON data.")


csv_contents = ""
for time in plate_log.keys():
    human_date = datetime.datetime.fromtimestamp(float(time)).strftime('%Y-%m-%d %H:%M:%S')
    for plate in plate_log[time]["plates"].keys():
        csv_line = human_date + "," + plate
        if (len(plate_log[time]["plates"][plate]["alerts"]) > 0): # Check to see if this plate was associated with any alerts.
            csv_line = csv_line + ",true"
        else:
            csv_line = csv_line + ",false"
        csv_line = csv_line + "," + str(plate_log[time]["location"]["lat"]) + "," + str(plate_log[time]["location"]["lon"])
        csv_contents += csv_line + "\n"


if (INCLUDE_HEADER == True):
    print("Date,Plate,Alert,Latitude,Longitude")
print(csv_contents)
