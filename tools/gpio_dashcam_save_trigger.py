# V0LT Predator
# GPIO Dashcam Save Trigger

# This is a stand-alone script that will create the dashcam save trigger file when a GPIO event occurs. This script is only useful when Predator is operating in dash-cam mode, but it doesn't necessarily depend on it to function. In other words, this script can be started as a separate service, before Predator starts.

gpio_pins = [17, 22, 27] # These are the pins that will be monitored for button presses.


import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import time

from gpiozero import Button
from signal import pause

base_directory = str(os.path.dirname(os.path.realpath(__file__)))
try:
    if (os.path.exists(base_directory + "/../config.json")):
        config = json.load(open(base_directory + "/../config.json")) # Load the configuration database from config.json
    else:
        print("The configuration file doesn't appear to exist at " + base_directory + "/../config.json.")
        exit()
except:
    print("The configuration database couldn't be loaded. It may be corrupted.")
    exit()

trigger_file_location = config["general"]["interface_directory"] + "/" + config["dashcam"]["saving"]["trigger"] # Define the path of the dashcam lock trigger file.
trigger_file_location = trigger_file_location.replace("//", "/") # Remove any duplicate slashes in the file path.
if (os.path.isdir(config["general"]["interface_directory"]) == False): # Check to see if the interface directory has not yet been created.
    os.system("mkdir -p '" + str(config["general"]["interface_directory"]) + "'")


last_trigger_time = 0
def create_trigger_file():
    global last_trigger_time
    if (time.time() - last_trigger_time > 1): # Check to see if at least 1 second has passed since the last dash-cam save trigger.
        os.system("touch '" + trigger_file_location + "'")
    last_trigger_time = time.time()


buttons = []
for pin in gpio_pins:
    buttons.append(Button(pin))
for button in buttons:
    button.when_pressed = create_trigger_file

pause()
