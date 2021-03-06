# Predator

# Copyright (C) 2022 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE.md)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import validators # Required to validating URLs
import requests # Required to send network requests
import json # Required to process JSON data
import os # Required to interact with certain operating system functions

import utils # Import the utils.py script
style = utils.style # Load the style from the utils script
clear = utils.clear # Load the screen clearing function from the utils script


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database.


def update_status_lighting(url_id):
    status_lighting_update_url = str(config["realtime"]["status_lighting_values"][url_id]).replace("[U]", str(config["realtime"]["status_lighting_base_url"]))# Prepare the URL where a request will be sent in order to update the status lighting.
    if (validators.url(status_lighting_update_url)): # Check to make sure the URL ID supplied actually resolves to a valid URL in the configuration database.
        response = requests.get(status_lighting_update_url)
    else:
        print(style.yellow + "Warning: Unable to update status lighting. Invalid URL configured for " + url_id + style.end) # Display a warning that the URL was invalid, and no network request was sent.
