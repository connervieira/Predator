# V0LT Predator
# GPIO Dashcam Save Trigger

# This is a stand-alone script that will create the dashcam save trigger file when a GPIO event occurs. This script is only useful when Predator is operating in dash-cam mode, but it doesn't necessarily depend on it to function. In other words, this script can be started as a separate service, before Predator starts.

gpio_pins = [17, 22, 27] # These are the pins that will be monitored for button presses.


import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import time
import threading

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
    os.system("chmod -R 777 '" + str(config["general"]["interface_directory"]) + "'")


def create_trigger_file():
    os.system("touch '" + trigger_file_location + "'")

def watch_button(pin, hold_time=0.2, event=create_trigger_file):
    print("Watching pin " + str(pin))
    button = Button(pin)

    time_pressed = 0
    last_triggered = 0
    while True:
        if (button.is_pressed and time_pressed == 0): # Check to see if the button was just pressed.
            #print("Pressed" + str(pin))
            time_pressed = time.time()
        elif (button.is_pressed and time.time() - time_pressed < hold_time): # Check to see if the button is being held, but the time threshold hasn't been reached.
            pass
            #print("Holding")
        elif (button.is_pressed and time.time() - time_pressed >= hold_time): # Check to see if the button is being held, and the time threshold has been reached.
            if (time.time() - last_triggered > 1):
                #print("Triggered " + str(pin))
                event()
            last_triggered = time.time()
        elif (button.is_pressed == False): # If the button is not pressed, reset the timer.
            time_pressed = 0

        time.sleep(0.02)


button_watch_threads = {}
for pin in gpio_pins:
    button_watch_threads[pin] = threading.Thread(target=watch_button, args=[pin], name="ButtonWatch" + str(pin))
    button_watch_threads[pin].start()

