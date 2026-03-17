# Predator
# lighting.py
# This script is used to control RGB status lights using WLED. Learn more about WLED (a third party, open source project) at: https://kno.wled.ge/

# Copyright (C) 2026 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import global_variables # `global_variables.py`

if (config["general"]["status_lighting"]["enabled"] == True and config["developer"]["offline"] == False): # Only update the status lighting if it is enabled in the configuration.
    import validators # Required to validating URLs.
    import requests # Required to send network requests.
import json # Required to process JSON data.
import os # Required to interact with certain operating system functions.
import time

import utils # Import the utils.py script.
import config # `config.py`
load_config = config.load_config
config = load_config()


current_status_light_id = ""
start_time = time.time() # This stores the time that the status lighting engine was first loaded (when Predator started).
def update_status_lighting(url_id):
    global current_status_light_id
    global start_time
    utils.debug_message("Updating status lighting")
    if (time.time() - start_time >= config["general"]["status_lighting"]["delay_after_boot"]):
        if (url_id != current_status_light_id): # Check to see if the status light URL ID is different from the current state of the lights.
            current_status_light_id = url_id
            if (config["general"]["status_lighting"]["enabled"] == True): # Only update the status lighting if it is enabled in the configuration.
                status_lighting_update_url = str(config["general"]["status_lighting"]["values"][url_id]).replace("[U]", str(config["general"]["status_lighting"]["base_url"])) # Prepare the URL where a request will be sent in order to update the status lighting.
                if (config["developer"]["offline"] == False): # Check to make sure offline mode is disabled before sending the network request to update the status lighting.
                    if (validators.url(status_lighting_update_url)): # Check to make sure the URL ID supplied actually resolves to a valid URL in the configuration database.
                        try:
                            response = requests.get(status_lighting_update_url, timeout=0.5)
                        except:
                            utils.display_message("Failed to update status lighting. The request timed out.", 3) # Display a warning indicating that the status lighting request timed out.
                    else:
                        utils.display_message("Unable to update status lighting. Invalid URL configured for " + url_id, 3) # Display a warning indicating that the URL was invalid, and no network request was sent.
    utils.debug_message("Status light update complete")
