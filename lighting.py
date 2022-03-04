import validators
import urllib.request

import utils
style = utils.style # Load the style from the utils script
clear = utils.clear # Load the screen clearing function from the utils script


config = json.load(open(predator_root_directory + "/config.json")) # Load the configuration database.


def update_status_lighting(url_id):
    if (validators.url(config["realtime"]["status_lighting"][url_id])): # Check to make sure the URL ID supplied actually resolves to a valid URL in the configuration database.
        try: # Try sending a request to the webook.
            webhook_response = urllib.request.urlopen(config["realtime"]["status_lighting"][url_id]).getcode() # Save the raw data from the request to a variable.
        except Exception as e:
            webhook_response = e

        if (str(webhook_response) != "200"): # If the webhook didn't respond with a 200 code; Warn the user that there was an error.
            print(style.yellow + "Warning: Unable to update status lighting. Response code: " + str(webhook_response.getcode()) + style.end)
    else:
            print(style.yellow + "Warning: Unable to update status lighting. Invalid URL configured for " + url_id + style.end)
