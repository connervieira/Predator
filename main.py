# Predator
# main.py
# This is the main driver script for Predator, and is the starting point for all other functionality. Run Predator with `python3 main.py --help`.

# Copyright (C) 2026 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE). If not, see https://www.gnu.org/licenses/ to read the license agreement.



print("Loading Predator...")
import global_variables # `global_variables.py`
global_variables.init()

import os # Required to interact with certain operating system functions
import json # Required to process JSON data


import config # `config.py`
load_config = config.load_config
validate_config = config.validate_config
config = load_config()

import time # Required to add delays and handle dates/times.
import sys # Required to read command line arguments.

if ("--help" in sys.argv):
    print("\npython3 main.py [MODE] [DIRECTORY] [OPTIONS]")
    print("    MODE is the number representing operating mode Predator will use.")
    print("        0\t\tManagement Mode")
    print("        1\t\tPre-recorded Mode")
    print("        2\t\tReal-time Mode")
    print("        3\t\tDash-cam Mode")
    print("    DIRECTORY specifies the working directory Predator will use.")
    print("    OPTIONS is any number of command-line options from the list below.")
    print("        --headless\tenables headless mode, where all user prompts are skipped")
    print("        --help\t\tdisplays this help message, then exits")

    global_variables.PREDATOR_RUNNING = False
    global_variables.shutdown_event.set()
    exit()

import utils # `utils.py`





if (os.path.exists(os.path.join(global_variables.PREDATOR_ROOT_DIRECTORY, "install.json")) == False): # Check to see if the install information file hasn't yet been created. This will be the case on the first start-up.
    import uuid
    install_data = {"first_start_time": int(time.time()), "id": str(uuid.uuid4())}
    utils.clear()
    print(utils.style.bold + utils.style.red + "Predator - First Start" + utils.style.end)
    print(utils.style.italic + "This wizard is only displayed on the first start of Predator.")
    print("To reset so this message is displayed again, remove the `install.json` file inside the main install directory." + utils.style.end)
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)

    utils.clear()
    print(utils.style.bold + utils.style.red + "Commercial Support" + utils.style.end)
    print(utils.style.bold + "V0LT offers the following commercial support services for Predator:" + utils.style.end)
    print("  * Custom software modifications")
    print("  * Pre-assembled hardware products and kits")
    print("  * One-on-one technical support")
    print("  * Server hosting")
    print("    - Remotely-managed hot-lists and ignore-lists")
    print("    - Compiled data reports")
    print("    - Remote ALPR processing")
    print()
    print("To learn more, don't hesitate to get in contact: " + utils.style.underline + "https://v0lttech.com/contact.php\n" + utils.style.end)
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)

    utils.clear()
    print(utils.style.bold + utils.style.red + "Warranty" + utils.style.end)
    print("While Predator is designed to be as reliable and consistent as possible, it comes with absolutely no warranty, it should not be used in a context where failure could cause harm to people or property.")
    print("For more information, see the `SECURITY.md` document.")
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)

    utils.clear()
    print(utils.style.bold + utils.style.red + "Privacy" + utils.style.end)
    print("Predator does not share telemetry or usage data with V0LT, or any other entity. However, by default, Predator will attach a random identifier to requests made to remote license plate list sources (as configured under `general>alerts>databases`). This identifier allows administrators of servers hosting license plate lists to roughly count how many clients are using their lists. If you're concerned about the administrator of one of your remote license plate lists using this unique identifier to derive information about how often you use Predator (based on when you fetch their lists), you can disable this functionality using the `developer>identify_to_remote_sources` configuration value.")
    print("Additionally, by default, Predator will fetch a hardcoded ignore list from the V0LT website. This functionality does not send any identifiable information or telemetry data (even when identify_to_remote_sources is enabled). To disable this functionality, either enable the `developer>offline` configuration value to disable all network requests, or remove the hardcoded ignore list from `ignore.py`.")
    print("For more information, see the `docs/CONFIGURE.md` document.")
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)

    utils.clear()
    print(utils.style.bold + utils.style.red + "Funding" + utils.style.end)
    print("Predator is completely free to use, and doesn't contain monetization like advertising or sponsorships. If you find the project to be useful, please consider supporting it financially.")
    print("For more information, see `https://v0lttech.com/donate.php`.")
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)


    with open(os.path.join(global_variables.PREDATOR_ROOT_DIRECTORY, "install.json"), 'w') as file:
        json.dump(install_data, file)


    print("")
    utils.clear()
    print("The initial start-up process has completed. Predator will now return to the normal start-up sequence.")
    input(utils.style.faint + "Press enter to continue..." + utils.style.end)



utils.debug_message("Validating configuration values")
invalid_configuration_values = validate_config(config) # Validation the configuration, and display any potential problems.
for entry in invalid_configuration_values: # Iterate through each invalid configuration value in the list.
    utils.display_message("Invalid configuration value: " + entry, 3) # Print each invalid configuration value as an error.
del invalid_configuration_values # Delete the variable holding the list of invalid configuration_values.
utils.debug_message("Validated configuration values")


if (config["developer"]["offline"] == True): # If offline mode is enabled, then disable all network based features.
    config["realtime"]["push_notifications"]["enabled"] = False
    config["realtime"]["push_notifications"]["server"] = "" # This is redundant, since 'realtime>push_notifications>enabled' is disabled, but it serves as a backup.
    config["general"]["status_lighting"]["enabled"] = False
    config["developer"]["remote_sources"] = []



utils.heartbeat() # Issue an initial heartbeat at start-up.

utils.debug_message("Initial loading complete")

# Display the start-up intro header.
utils.clear()
if (config["general"]["display"]["ascii_art_header"] == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
    print(utils.style.red + utils.style.bold)
    print(" /$$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$ ")
    print("| $$__  $$| $$__  $$| $$_____/| $$__  $$ /$$__  $$|__  $$__//$$__  $$| $$__  $$")
    print("| $$  \\ $$| $$  \\ $$| $$      | $$  \\ $$| $$  \\ $$   | $$  | $$  \\ $$| $$  \\ $$")
    print("| $$$$$$$/| $$$$$$$/| $$$$$   | $$  | $$| $$$$$$$$   | $$  | $$  | $$| $$$$$$$/")
    print("| $$____/ | $$__  $$| $$__/   | $$  | $$| $$__  $$   | $$  | $$  | $$| $$__  $$")
    print("| $$      | $$  \\ $$| $$      | $$  | $$| $$  | $$   | $$  | $$  | $$| $$  \\ $$")
    print("| $$      | $$  | $$| $$$$$$$$| $$$$$$$/| $$  | $$   | $$  |  $$$$$$/| $$  | $$")
    print("|__/      |__/  |__/|________/|_______/ |__/  |__/   |__/   \\______/ |__/  |__/" + utils.style.end + utils.style.bold)
    print("")
    print("                                 COMPUTER VISION")
    if (config["general"]["display"]["startup_message"] != ""): # Only display the line for the custom message if the user has defined one.
        print("")
        print(config["general"]["display"]["startup_message"]) # Show the user's custom defined start-up message.
    print(utils.style.end)
else: # If the user his disabled the large ASCII art header, then show a simple title header with minimal styling.
    print(utils.style.red + utils.style.bold + "PREDATOR" + utils.style.end)
    print(utils.style.bold + "Computer Vision" + utils.style.end + "\n")
    if (config["general"]["display"]["startup_message"]!= ""): # Only display the line for the custom message if the user has defined one.
        print(config["general"]["display"]["startup_message"]) # Show the user's custom defined start-up message.

utils.play_sound("startup")

if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has push notifications enabled.
    utils.send_notification("Predator", "Predator has been started")



# Figure out which mode to boot into.
print("Please select an operating mode.")
if (config["general"]["modes"]["enabled"]["management"] == True): # Only show the management mode option if it's enabled in the configuration.
    print("0. Management")
if (config["general"]["modes"]["enabled"]["prerecorded"] == True): # Only show the pre-recorded mode option if it's enabled in the configuration.
    print("1. Pre-recorded")
if (config["general"]["modes"]["enabled"]["realtime"] == True): # Only show the real-time mode option if it's enabled in the configuration.
    print("2. Real-time")
if (config["general"]["modes"]["enabled"]["dashcam"] == True): # Only show the dash-cam mode option if it's enabled in the configuration.
    print("3. Dash-cam")


if (len(sys.argv) > 1): # Check to see if there is at least 1 command line argument.
    if (sys.argv[1] == "0" or sys.argv[1] == "1" or sys.argv[1] == "2" or sys.argv[1] == "3"): # Check to see if a mode override was specified in the Predator command arguments.
        config["general"]["modes"]["auto_start"] = sys.argv[1] # Set the automatic start mode to the mode specified by the command line argument.

if (len(sys.argv) > 2): # Check to see if there are at least 2 command line arguments.
    if (sys.argv[2] not in ["--headless", "--help"]):
        config["general"]["working_directory"] = str(sys.argv[2]) # Set the working directory to the path specified by the command line argument.


if (config["general"]["modes"]["auto_start"] == "0" and config["general"]["modes"]["enabled"]["management"] == True): # Based on the configuration, Predator will automatically boot into management mode.
    print(utils.style.bold + "Automatically starting into management mode." + utils.style.end)
    mode_selection = "0"
elif (config["general"]["modes"]["auto_start"] == "1" and config["general"]["modes"]["enabled"]["prerecorded"] == True): # Based on the configuration, Predator will automatically boot into pre-recorded mode.
    print(utils.style.bold + "Automatically starting into pre-recorded mode." + utils.style.end)
    mode_selection = "1"
elif (config["general"]["modes"]["auto_start"] == "2" and config["general"]["modes"]["enabled"]["realtime"] == True): # Based on the configuration, Predator will automatically boot into real-time mode.
    print(utils.style.bold + "Automatically starting into real-time mode." + utils.style.end)
    mode_selection = "2"
elif (config["general"]["modes"]["auto_start"] == "3" and config["general"]["modes"]["enabled"]["dashcam"] == True): # Based on the configuration, Predator will automatically boot into dash-cam mode.
    print(utils.style.bold + "Automatically starting into dash-cam mode." + utils.style.end)
    mode_selection = "3"
else: # No 'auto start mode' has been configured, so ask the user to select manually.
    mode_selection = utils.prompt("Selection: ")
print("")





# Initial setup has been completed, and Predator will now load into the specified mode.



# Management mode
if (mode_selection == "0" and config["general"]["modes"]["enabled"]["management"] == True): # The user has selected to boot into management mode.
    import predator_management # `predator_management.py`
    predator_management.management_mode()


# Pre-recorded mode
elif (mode_selection == "1" and config["general"]["modes"]["enabled"]["prerecorded"] == True): # The user has selected to boot into pre-recorded mode.
    import predator_prerecorded # `predator_prerecorded.py`
    predator_prerecorded.prerecorded_mode()


# Real-time mode
elif (mode_selection == "2" and config["general"]["modes"]["enabled"]["realtime"] == True): # The user has set Predator to boot into real-time mode.
    import predator_realtime # `predator_realtime.py`
    predator_realtime.realtime_mode()


# Dash-cam mode
elif (mode_selection == "3" and config["general"]["modes"]["enabled"]["dashcam"] == True): # The user has set Predator to boot into dash-cam mode.
    import predator_dashcam
    predator_dashcam.dashcam_mode()


else: # The user has selected an unrecognized mode.
    utils.display_message("The selected mode is invalid.", 3) # Display an error message indicating that the selected mode isn't recognized.



utils.stop_predator()
