# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import time


config_default_filepath = "./assets/support/configdefault.json"
config_outline_filepath = "./assets/support/configoutline.json"
config_active_filepath = "./config.json"

if (os.path.exists("./config.json") == False):
    if (os.path.exists("../config.json") == True):
        config_active_filepath = "../config.json"
        config_default_filepath = "../assets/support/configdefault.json"
        config_outline_filepath = "../assets/support/configoutline.json"

if (os.path.exists(config_active_filepath) == False): # Check to see if the active config filed doesn't exit.
    # Copy the default config file as the active config file.
    with open(config_default_filepath) as configuration_file: config_default= configuration_file.read()

    fh = open(config_active_filepath, 'w')
    fh.write(config_default)
    fh.close()

import utils
style = utils.style
debug_message = utils.debug_message
display_message = utils.display_message
is_json = utils.is_json
save_to_file = utils.save_to_file


def load_config(file_override=""):
    if (file_override != ""):
        configuration_file_path = file_override
    else:
        if (os.path.exists(config_active_filepath) == True): # Check to see if the configuration file exists in the default location.
            configuration_file_path = config_active_filepath
        else: # The configuration file couldn't be located. Assassin can't continue to load.
            config = {} # Set the configuration to a blank placeholder dictionary.
            print("The configuration file could not be located from " + str(os.path.realpath(__file__)))
            exit()

    with open(configuration_file_path) as configuration_file: raw_configuration_file_contents = configuration_file.read() # Read the contents of the configuration file.

    if (is_json(raw_configuration_file_contents)):
        config = json.loads(raw_configuration_file_contents) # Load the configuration database from the contents of the config.json file.
    else:
        config = {} # Set the configuration to a blank placeholder dictionary.
        print("The configuration file found at " + configuration_file_path + " does not appear to be valid JSON.")
        exit()

    return config # Return the loaded configuration information.



def check_value(value, template):
    if (type(template) == list): # Check to see if the template for this value is a list of acceptable values.
        if (value not in template): # Check to see if the configuration value is in the list of acceptable values.
            return False
    elif (type(template) == str):
        if (template == "str"): # 'str' means this value needs to be a string.
            if (type(value) != str):
                return False
        elif (template == "bool"): # 'bool' means this value needs to be true or false.
            if (type(value) != bool):
                return False
        elif (template == "float"): # 'float' means this value needs to be a number.
            if (type(value) != float and type(value) != int):
                return False
        elif (template == "+float"): # '+float' means this value needs to be a number greater than or equal to 0.
            if (type(value) != float and type(value) != int):
                return False
            elif (value < 0.0):
                return False
        elif (template == "int"): # 'int' means this value needs to be a whole number.
            if (type(value) != int):
                return False
        elif (template == "+int"): # '+int' means this value needs to be a whole number greater than or equal to 0.
            if (type(value) != int):
                return False
            elif (value < 0.0):
                return False
        elif (template == "list"): # 'list' means this value needs to be a list.
            if (type(value) != list):
                return False
        elif (template == "dict"): # 'dict' means this value needs to be a dict.
            if (type(value) != dict):
                return False
        elif (template == "dir"): # 'dir' means this value needs to point to a directory that exists.
            if (os.path.isdir(value) == False):
                return False
        elif (template == "file"): # 'file' means this value needs to point to a file that exists.
            if (os.path.isfile(value) == False):
                return False
        else:
            print("An entry in the configuration outline template is an unexpected value.")
            return True
    else:
        print("An entry in the configuration outline template is an unexpected type.")
        return True

    return True



def validate_config(config):
    config_outline = load_config(config_outline_filepath)

    invalid_values = []

    for key1, section1 in config_outline.items():
        if (type(section1) == dict):
            for key2, section2 in section1.items():
                if (type(section2) == dict):
                    for key3, section3 in section2.items():
                        if (type(section3) == dict):
                            for key4, section4 in section3.items():
                                if (type(section4) == dict):
                                    for key5, section5 in section4.items():
                                        if (type(section5) == dict):
                                            for key6, section6 in section5.items():
                                                if (type(section6) == dict):
                                                    for key7, section7 in section6.items():
                                                        if (type(section7) == dict):
                                                            for key8, section8 in section6.items():
                                                                if (type(section8) == dict):
                                                                    print("The configuration validation function hit a nested configuration outline section that exceeded 8 layers. The normal configuration outline file should never reach this point.")
                                                                    exit()
                                                                else:
                                                                    try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                                                        if (check_value(config[key1][key2][key3][key4][key5][key6][key7][key8], section8) == False):
                                                                            invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6 + ">" + key7 + ">" + key8)
                                                                    except KeyError:
                                                                        invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6 + ">" + key7 + ">" + key8)
                                                        else:
                                                            try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                                                if (check_value(config[key1][key2][key3][key4][key5][key6][key7], section7) == False):
                                                                    invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6 + ">" + key7)
                                                            except KeyError:
                                                                invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6 + ">" + key7)
                                                else:
                                                    try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                                        if (check_value(config[key1][key2][key3][key4][key5][key6], section6) == False):
                                                            invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6)
                                                    except KeyError:
                                                        invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5 + ">" + key6)
                                        else:
                                            try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                                if (check_value(config[key1][key2][key3][key4][key5], section5) == False):
                                                    invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5)
                                            except KeyError:
                                                invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4 + ">" + key5)
                                else:
                                    try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                        if (check_value(config[key1][key2][key3][key4], section4) == False):
                                            invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4)
                                    except KeyError:
                                        invalid_values.append(key1 + ">" + key2 + ">" + key3 + ">" + key4)
                        else:
                            try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                                if (check_value(config[key1][key2][key3], section3) == False):
                                    invalid_values.append(key1 + ">" + key2 + ">" + key3)
                            except KeyError:
                                invalid_values.append(key1 + ">" + key2 + ">" + key3)
                else:
                    try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                        if (check_value(config[key1][key2], section2) == False):
                            invalid_values.append(key1 + ">" + key2)
                    except KeyError:
                        invalid_values.append(key1 + ">" + key2)
        else:
            try: # Run inside a try block to check if the corresponding value does not exist in the configuration file.
                if (check_value(config[key1], section1) == False):
                    invalid_values.append(key1)
            except KeyError:
                invalid_values.append(key1)

    return invalid_values




def del_nested_value(index, data):
    if (len(index) == 1):
        del data[index[0]]
    elif (len(index) == 2):
        del data[index[0]][index[1]]
    elif (len(index) == 3):
        del data[index[0]][index[1]][index[2]]
    elif (len(index) == 4):
        del data[index[0]][index[1]][index[2]][index[3]]
    elif (len(index) == 5):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]]
    elif (len(index) == 6):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]]
    elif (len(index) == 7):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]]
    elif (len(index) == 8):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]]
    elif (len(index) == 9):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]]
    elif (len(index) == 10):
        del data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]][index[9]]
    else:
        display_message("The del_nested_value() function was called with an index of unexpected length", 3)

    return data

def set_nested_value(index, data, value):
    if (len(index) == 1):
        data[index[0]] = value
    elif (len(index) == 2):
        data[index[0]][index[1]] = value
    elif (len(index) == 3):
        data[index[0]][index[1]][index[2]] = value
    elif (len(index) == 4):
        data[index[0]][index[1]][index[2]][index[3]] = value
    elif (len(index) == 5):
        data[index[0]][index[1]][index[2]][index[3]][index[4]] = value
    elif (len(index) == 6):
        data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]] = value
    elif (len(index) == 7):
        data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]] = value
    elif (len(index) == 8):
        data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]] = value
    elif (len(index) == 9):
        data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]] = value
    elif (len(index) == 10):
        data[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]][index[9]] = value
    else:
        display_message("The set_nested_value() function was called with an index of unexpected length", 3)

    return data


def get_nested_value(index, data):
    if (type(data) == dict and len(index) > 0):
        if (index[0] in data): # Check to see if this key exists in the data.
            next_data = data[index[0]]
            return get_nested_value(index[1:], next_data)
        else:
            return None
    else:
        return data

def print_nested_array(data, index=[]):
    if (type(data) == dict):
        for key, section in data.items():
            new_index = index.copy()
            new_index.append(key)
            print_nested_array(section, new_index)
    else:
        for key in index:
            print(str(key) + ">", end='')
        print(str(data))

def check_defaults_changed(config_defaults, config_active, index=[]):
    if (type(config_defaults) == dict):
        for key, section in config_defaults.items():
            new_index = index.copy()
            new_index.append(key)
            check_defaults_changed(section, config_active, new_index)
    else:
        config_active_value = get_nested_value(index, config_active)
        if (config_defaults != config_active_value): # Check to see if this value in the active configuration has been changed from the default.
            print("The following configuration value has been changed from the default: ", end='')
            for key in index:
                print(str(key) + ">", end='')
            print("") # Print a line break

def highest_different_index(config_active, config_default, index): # This function recursive moves to higher and higher level indexes until one that exists in both the default config and active config is found.
    last_index = ""
    for i in range(0, len(index)): # Run once for each level of the index.
        try:
            if (len(index) == 1):
                test = config_active[index[0]]
            elif (len(index) == 2):
                test = config_active[index[0]][index[1]]
            elif (len(index) == 3):
                test = config_active[index[0]][index[1]][index[2]]
            elif (len(index) == 4):
                test = config_active[index[0]][index[1]][index[2]][index[3]]
            elif (len(index) == 5):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]]
            elif (len(index) == 6):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]]
            elif (len(index) == 7):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]]
            elif (len(index) == 8):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]]
            elif (len(index) == 9):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]]
            elif (len(index) == 10):
                test = config_active[index[0]][index[1]][index[2]][index[3]][index[4]][index[5]][index[6]][index[7]][index[8]][index[9]]
            else:
                display_message("The highest_different_index() function was called with an index of unexpected length", 3)

            if (last_index != ""):
                index.append(last_index)
            return index
        except KeyError:
            last_index = index[-1]
            del index[-1] # Move one level up from the index.

    return []


ignore_indexes = [["realtime", "image", "camera", "devices"], ["dashcam", "stamps", "relay", "triggers"], ["dashcam", "capture", "video", "devices"]] # Configure values specified here will not be checked by the check_defaults_missing() and check_defaults_extra() functions.

# This function checks for values that exist in the default config that aren't present in the active config.
def check_defaults_missing(config_defaults, config_active, index=[], missing_values=[]):
    if (index not in ignore_indexes): # Only continue if the specified index is not ignored.
        if (type(config_defaults) == dict):
            for key, section in config_defaults.items():
                new_index = index.copy()
                new_index.append(key)
                config_active, missing_values = check_defaults_missing(section, config_active, new_index, missing_values)
        else:
            config_active_value = get_nested_value(index, config_active)
            if (config_active_value == None):
                index_to_set = highest_different_index(config_active, config_defaults, index)
                default_value = get_nested_value(index_to_set, load_config(config_default_filepath))
                config_active = set_nested_value(index_to_set, config_active, default_value)
                missing_values.append(index)
    return config_active, missing_values

# This function checks for values that exist on the active config that aren't present in the default config.
def check_defaults_extra(config_defaults, config_active, index=[], extra_values=[]):
    if (index not in ignore_indexes): # Only continue if the specified index is not ignored.
        if (type(config_active) == dict):
            for key, section in config_active.items():
                new_index = index.copy()
                new_index.append(key)
                extra_values = check_defaults_extra(config_defaults, section, new_index)
        else:
            config_default_value = get_nested_value(index, config_defaults)
            if (config_default_value == None):
                extra_values.append(index)
    return extra_values

# This function checks the active config file against the default config file, and attempts to reconcile any differences. Irreconcileable differences will cause Predator to exit, and a notice will be displayed.
def update_config():
    config_default = load_config(config_default_filepath)
    config_active = load_config(config_active_filepath)

    config_active, missing_values = check_defaults_missing(config_default, config_active)
    extra_values = check_defaults_extra(config_default, config_active)

    if (len(missing_values) > 0):
        print(style.yellow + "The following values were present in the default configuration, but not the active configuration. They may have been added in an update. The default values have been inserted into the active configuration." + style.end)
        for value in missing_values:
            print("    " + '>'.join(map(str, value)))
        print(style.faint + "Continuing in 5 seconds" + style.end)
        time.sleep(5)

    if (len(extra_values) > 0):
        print(style.yellow + "The following values were present in the active configuration, but not the default configuration. They may have been removed in an update. These values have been removed from the active configuration." + style.end)
        for value in extra_values:
            index = highest_different_index(config_default, config_active, value)
            if (get_nested_value(index, config_active) != None): # Check to see if this index hasn't already been removed.
                print("    " + '>'.join(map(str, index)))
                config_active = del_nested_value(index, config_active)
        print(style.faint + "Continuing in 5 seconds" + style.end)
        time.sleep(5)
    if (config_active != load_config(config_active_filepath)): # Check to see if the configuration has been modified.
        save_to_file(config_active_filepath, json.dumps(config_active, indent=4)) # Save the updated configuration.



update_config()
config = load_config() # Execute the configuration loading.
