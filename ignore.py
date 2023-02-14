# Copyright (C) 2023 V0LT - Conner Vieira

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This library is responsible to handling 'ignore lists', which allows administrators to define a list of license plates that should be ignored.

# Ignore lists might be used to prevent common vehicles from being logged in order to keep logs organized, or to prevent privacy-concerned visitors from having their license plate processed.

# License plates in the ignore list are still processed locally, but won't be sent to an external service.

# Ignore lists can be enabled and disabled in the configuration.


import os # Required to interact with certain operating system functions.
import json # Required to process JSON data.
import time # Required to manage delays.
import validators # Required to validate URLs.

import utils
style = utils.style

root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.
config = json.load(open(root_directory + "/config.json")) # Load the configuration database from config.json

if (config["developer"]["offline"] == False): # Only import networking libraries if offline mode is turned off.
    import requests # Required to fetch information from network hosts.


def fetch_ignore_list():
    root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

    config = json.load(open(root_directory + "/config.json")) # Load the configuration database from config.json



    complete_ignore_list = [] # This will hold the complete list of plates to ignore, after all ignore list sources have been loaded.

    if (config["developer"]["ignore_list"]["enabled"] == True): # Only load the local ignore list file if the ignore list is enabled in the configuration.

        local_ignore_list_file = config["developer"]["ignore_list"]["local_file"]

        if (os.path.exists(local_ignore_list_file) == True):
            loaded_local_ignore_list_file = open(local_ignore_list_file, "r") # Open the local ignore list file.
            local_ignore_list = json.loads(loaded_local_ignore_list_file.read()) # Read the contents of the file.
            loaded_local_ignore_list_file.close() # Close the file.

            for entry in local_ignore_list: # Iterate through each entry in the local ignore list, and add it to the complete ignore list.
                complete_ignore_list.append(entry)
        else:
            print(style.red + "The local ignore list file does not exist. The local ignore list is effectively disabled." + style.end)
            input("Press enter to continue...")


    remote_ignore_sources = ["https://v0lttech.com/predator/ignorelist/serve.php?key=public"] # This holds a list of hard-coded remote sources that ignore lists will be fetched from. This allows administrators to automatically issue ignore lists from an external services. Administrators can create ignore lists without needing to manually modify the local ignore list for all their devices. Remote sources don't receive any telemetry from Predator, only a simple JSON list is fetched. Custom remote sources from the configuration are added in the next steps.

    if (config["developer"]["ignore_list"]["enabled"] == True): # Only add custom remote sources if custom ignore lists are enabled in the configuration
        for source in config["developer"]["ignore_list"]["remote_sources"]: # Iterate through each source in the list of remote ignore list sources.
            remote_ignore_sources.append(source) # Add the remote source to the list of remote sources.

    if (config["developer"]["offline"] == True): # If offline mode is enabled, then remove all remote ignore list sources.
        remote_ignore_sources = [] # Set this list of remote ignore list sources to a blank list.

    for host in remote_ignore_sources: # Iterate through all of the hosts specified in the list of remote ignore list sources.
        if (validators.url(host)): # Verify that this 'host' value is a valid URL.
            try: # Run the network request in a try block so the entire program doesn't fail if something goes wrong.
                response = requests.get(host, timeout=3.0) # Make a request to this host that times out after 3 seconds.
                response_content = response.text # Grab the text from the response.
            except: # If the network request fails, do the following steps instead.
                response_content = "[]" # Use a blank placeholder response database.

            try: # Run the JSON load function in a 'try' block to prevent fatal crashes if the data returned by the remote source isn't valid JSON.
                remote_ignore_list = json.loads(response_content)
            except: # If the list fails to load, it's likely because it's not valid JSON data.
                remote_ignore_list = [] # Set the loaded list to a blank placeholder list.

            for entry in remote_ignore_list: # Iterate through each entry in this remote ignore list, and add it to the complete ignore list.
                complete_ignore_list.append(entry)

        else: # This remote ignore list source is not a valid URL.
            pass



    sanitized_ignore_list = []
    for entry in complete_ignore_list:
        if (len(entry) < 25): # Verify that this entry is a reasonable length.
            sanitized_ignore_list.append(entry.upper()) # Convert this entry to all uppercase letters, and add it to the sanitized list.


    final_ignore_list = list(dict.fromkeys(sanitized_ignore_list)) # De-duplicate the ignore list to make processing more efficient.
    return final_ignore_list
