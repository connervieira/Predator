import os # Required to interact with certain operating system functions.
import json # Required to process JSON data.
import datetime # Required to handle timestamps.


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__ + "/.."))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


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

print(csv_contents)
