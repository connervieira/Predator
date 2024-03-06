# Copyright (C) 2024 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.



import os # Required to interact with certain operating system functions
import json # Required to process JSON data

assassin_root_directory = str(os.path.dirname(os.path.realpath(__file__)))

import utils
debug_message = utils.debug_message
is_json = utils.is_json



def load_config(file_override=""):
    if (file_override != ""):
        configuration_file_path = file_override
    else:
        if (os.path.exists(str(assassin_root_directory + "/config.json")) == True): # Check to see if the configuration file exists in the default location.
            configuration_file_path = assassin_root_directory + "/config.json"
        elif (os.path.exists(str(assassin_root_directory + "/../config.json")) == True): # Check to see if the configuration file exists in the parent directory. This may occur if this script is being used in a subfolder of Assassin.
            configuration_file_path = assassin_root_directory + "/../config.json"
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
    config_outline = load_config("./assets/support/configoutline.json")

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
                                                            print("The configuration validation function hit a nested configuration outline section that exceeded 7 layers. The normal configuration outline file should never reach this point.")
                                                            exit()
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



config = load_config() # Execute the configuration loading.

