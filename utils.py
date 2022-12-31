# Predator

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This script contains several funtions and classes used in main.py







import os # Required to interact with certain operating system functions
import json # Required to process JSON data

predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database from config.json


import time # Required to add delays and handle dates/times
import subprocess # Required for starting some shell commands
import sys
if (config["realtime"]["status_lighting_enabled"] == True or config["realtime"]["push_notifications_enabled"] == True or config["realtime"]["webhook"] != ""):
    import requests # Required to make network requests
    import validators # Required to validate URLs
import re # Required to use Regex
import datetime # Required for converting between timestamps and human readable date/time information
from xml.dom import minidom # Required for processing GPX data
import fnmatch # Required to use wildcards to check strings
import lzma # Required to load ExCam database
import math # Required to run more complex math calculations
if (config["general"]["gps_enabled"] == True): # Only import the GPS libraries if GPS settings are enabled.
    from gps import * # Required to access GPS information.
    import gpsd





gps_enabled = config["general"]["gps_enabled"] # This setting determines whether or not Predator's GPS features are enabled.




# This function will be used to process GPX files into a Python dictionary.
def process_gpx(gpx_file):
    gpx_file = open(gpx_file, 'r') # Open the GPX document.

    xmldoc = minidom.parse(gpx_file) # Load the full XML GPX document.

    track = xmldoc.getElementsByTagName('trkpt') # Get all of the location information from the GPX document.
    timing = xmldoc.getElementsByTagName('time') # Get all of the timing information from the GPX document.

    gpx_data = {} 

    for i in range(0, len(timing)): # Iterate through each point in the GPX file.
        point_lat = track[i].getAttribute('lat') # Get the latitude for this point.
        point_lon = track[i].getAttribute('lon') # Get the longitude for this point.
        point_time = str(timing[i].toxml().replace("<time>", "").replace("</time>", "").replace("Z", "").replace("T", " ")) # Get the time for this point in human readable text format.

        point_time = round(time.mktime(datetime.datetime.strptime(point_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the human readable timestamp into a Unix timestamp.

        gpx_data[point_time] = {"lat":point_lat, "lon":point_lon} # Add this point to the decoded GPX data.


    return gpx_data




# Define the function that will be used to clear the screen.
def clear():
    os.system("clear")



# Define the function that will be used to save files for exported data.
def save_to_file(file_name, contents, silence=False):
    fh = None
    success = False
    try:
        fh = open(file_name, 'w')
        fh.write(contents)
        success = True   
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            print("Failed to save!")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success



# Define the fuction that will be used to add to the end of a file.
def add_to_file(file_name, contents, silence=False):
    fh = None
    success = False
    try:
        fh = open(file_name, 'a')
        fh.write(contents)
        success = True
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
    except IOError as e:
        success = False
        if (silence == False):
            print(e)
            print("Failed to save!")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success


def validate_plate(plate, template):
    plate_valid = True # By default, the plate is valid, until we find a character that doesn't align.

    if (len(template) == len(plate)): # Make sure the template and plate are the same length. If so, continue with validation. Otherwise, automatically invalidate the plate, and skip the rest of the validation process.
        for x in range(len(template)):
            if (template[x].isalpha() == plate[x].isalpha() or template[x].isnumeric() == plate[x].isnumeric()): # If this character is alphabetical in both the template and plate, or if this character is numeric in both the template and plate, then this character is valid.
                # This characteris valid, so don't change anything.
                pass
            else:
                # This character doesn't match between the template and plate, so mark the plate as invalid.
                plate_valid = False
    else:
        plate_valid = False

    return plate_valid # Return the results of the plate validation



# This function is used to download and process plain-text lists of license plates over a network.
def download_plate_database(url):
    raw_download_data = requests.get(url).text # Save the raw text data from the URL to a variable.

    # Process the downloaded data step by step to form a list of all of the plates in the database.
    processed_download_data = str(raw_download_data) # Convert the downloaded data to a string.

    if (processed_download_data[0] == "{" or processed_download_data[1] == "{" or processed_download_data[2] == "{"): # Check to see if the first character in the file indicates that this alert database is a JSON database.
        alert_database_list = json.loads(processed_download_data) # Load the alert database as JSON data.
        return alert_database_list, "json"
    else: # The alert database appears to be a plain text list.
        processed_download_data = processed_download_data.replace("\\n", "\n") # Replace the indicated line-breaks with true line-breaks.
        processed_download_data = re.sub('([^A-Z0-9\\n\\r\*\-\?\\[\\]])+', '', processed_download_data) # Remove all chracters except capital letters, numbers, and line-breaks.
        download_data_list = processed_download_data.split() # Split the downloaded data line-by-line into a Python list.
        return download_data_list, "text"






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




# Define a function for running a countdown timer.
def countdown(timer):
    for iteration in range(1, timer + 1): # Loop however many times specified by the `timer` variable.
        print(str(timer - iteration + 1)) # Display the current countdown number for this iteration, but subtracting the current iteration count from the total timer length.
        time.sleep(1) # Wait for 1 second.






# Define the function that will be used to get the current GPS coordinates.
def get_gps_location(): # Placeholder that should be updated at a later date.
    if (gps_enabled == True): # Check to see if GPS is enabled.
        try: # Don't terminate the entire script if the GPS location fails to be aquired.
            gpsd.connect() # Connect to the GPS daemon.
            gps_data_packet = gpsd.get_current() # Get the current information.
            return gps_data_packet.position()[0], gps_data_packet.position()[1], gps_data_packet.speed(), gps_data_packet.altitude(), gps_data_packet.movement()["track"], gps_data_packet.sats # Return GPS information.
        except: # If the current location can't be established, then return placeholder location data.
            return 0.0000, -0.0000, 0.0, 0.0, 0.0, 0 # Return a default placeholder location.
    else: # If GPS is disabled, then this function should never be called, but return a placeholder position regardless.
        return 0.0000, 0.0000, 0.0, 0.0, 0.0, 0 # Return a default placeholder location.





def convert_speed(speed, unit="mph"): # This function is used to convert speeds from meters per second, to other units.
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
        speed = 0

    return speed # Return the convert speed.





def display_number(display_number="0"): # This function is used to display a number as a large ASCII character.
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
