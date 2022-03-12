import validators # Required to validating URLs
import urllib.request # Required to send network requests
import json # Required to process JSON data
import os # Required to interact with certain operating system functions

import utils # Import the utils.py script
style = utils.style # Load the style from the utils script
clear = utils.clear # Load the screen clearing function from the utils script


predator_root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database.


def update_status_lighting(url_id):
    status_lighting_update_url = config["realtime"]["status_lighting_base_url"].replace("[U]", config["realtime"]["status_lighting_values"]) # Prepare the URL where a request will be sent in order to update the status lighting.
    if (validators.url(status_lighting_update_url)): # Check to make sure the URL ID supplied actually resolves to a valid URL in the configuration database.
        try: # Try sending a request to the URL.
            webhook_response = urllib.request.urlopen(status_lighting_update_url).getcode() # Save the raw data from the request to a variable.
        except Exception as e:
            webhook_response = e

        if (str(webhook_response) != "200"): # If the server didn't respond with a 200 code; Warn the user that there was an error.
            print(style.yellow + "Warning: Unable to update status lighting. Response code: " + str(webhook_response.getcode()) + style.end)
    else:
            print(style.yellow + "Warning: Unable to update status lighting. Invalid URL configured for " + url_id + style.end) # Display a warning that the URL was invalid, and no network request was sent.
