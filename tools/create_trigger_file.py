# This is a simple testing script that manually creates the dashcam video saving trigger file when executed.

import os
import json
import time

predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

try:
    if (os.path.exists(predator_root_directory + "/../config.json")):
        config = json.load(open(predator_root_directory + "/../config.json")) # Load the configuration database from config.json
    else:
        print("The configuration file doesn't appear to exist at " + predator_root_directory + "/../config.json.")
        exit()
except Exception as e:
    print(e)
    print("The configuration database couldn't be loaded. It may be corrupted.")
    exit()


if (os.path.isdir(config["general"]["interface_directory"]) == False): # Check to see if the interface directory has not yet been created.
    os.system("mkdir -p '" + str(config["general"]["interface_directory"]) + "'")
    os.system("chmod -R 777 '" + str(config["general"]["interface_directory"]) + "'")
if (os.path.exists(os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"])) == False): # Check to see if the trigger file hasn't already been created.
    os.system("echo " + str(time.time()) + " > \"" + os.path.join(config["general"]["interface_directory"], config["dashcam"]["saving"]["trigger"]) + "\"") # Save the trigger file with the current time as the timestamp.
