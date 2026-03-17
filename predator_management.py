import os
import subprocess
import sys
import json
import utils

import global_variables # `global_variables.py`
import utils # `utils.py`
import config # `config.py`
load_config = config.load_config
validate_config = config.validate_config
config = load_config()

if (config["management"]["disk_statistics"] == True): # Only import the disk statistic library if it is enabled in the configuration.
    utils.debug_message("Loading system utility library")
    import psutil # Required to get disk usage information


# This function is the entry point for management mode, and is called directly when management mode starts.
def management_mode():
    global config
    try:
        utils.debug_message("Started management mode")

        working_directory_input = utils.prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str, default=config["general"]["working_directory"])
        while (os.path.exists(working_directory_input) == False): # Run forever until the user enters a working directory that exists.
            utils.display_message("The specified working directory doesn't seem to exist.", 2)
            working_directory_input = utils.prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)

        config["general"]["working_directory"] = working_directory_input


        while global_variables.PREDATOR_RUNNING:
            utils.clear()
            print("Please select an option")
            print("0. Quit")
            print("1. File Management")
            print("2. Information")
            print("3. Configuration")
            selection = utils.prompt("Selection: ", optional=False, input_type=str)

            if (selection == "0"): # The user has selected the "Quit" option.
                break
            elif (selection == "1"): # The user has selected the "File Management" option.
                print("    Please select an option")
                print("    0. Back")
                print("    1. View")
                print("    2. Copy")
                print("    3. Delete")
                selection = utils.prompt("    Selection: ", optional=False, input_type=str)

                if (selection == "0"): # The user has selected to return back to the previous menu.
                    continue # Do nothing, and just finish this loop.
                elif (selection == "1"): # The user has selected the "view files" option.
                    subprocess.run(["find", config["general"]["working_directory"]], check=True) # Run the 'find' command in the working directory to recursively list all files/directories.
                    utils.wait_for_input()
                elif (selection == "2"): # The user has selected the "copy files" option.

                    # Reset all of the file selections to un-selected.
                    copy_management_configuration = False
                    copy_prerecorded_processed_frames = False
                    copy_prerecorded_gpx_files = False
                    copy_prerecorded_license_plate_analysis_data = False
                    copy_prerecorded_license_plate_location_data = False
                    copy_realtime_license_plate_recognition_data = False
                    copy_dashcam_video = False
                    copy_dashcam_video_saved = False

                    while True: # Run the "copy files" selection menu on a loop forever until the user is finished selecting files.
                        utils.clear() # Clear the console output before each loop.
                        print("Please select which files to copy")
                        print("0. Continue")
                        print("")
                        print("===== Management Mode =====")
                        if (copy_management_configuration == True):
                            print("M1. [X] Configuration files")
                        else:
                            print("M1. [ ] Configuration files")
                        print("")
                        print("===== Pre-recorded Mode =====")
                        if (copy_prerecorded_processed_frames == True):
                            print("P1. [X] Processed video frames")
                        else:
                            print("P1. [ ] Processed video frames")
                        if (copy_prerecorded_gpx_files == True):
                            print("P2. [X] GPX files")
                        else:
                            print("P2. [ ] GPX files")
                        if (copy_prerecorded_license_plate_analysis_data == True):
                            print("P3. [X] License plate analysis data files")
                        else:
                            print("P3. [ ] License plate analysis data files")
                        if (copy_prerecorded_license_plate_location_data == True):
                            print("P5. [X] License plate location data files")
                        else:
                            print("P5. [ ] License plate location data files")
                        print("")
                        print("===== Real-time Mode =====")
                        if (copy_realtime_license_plate_recognition_data == True):
                            print("R1. [X] License plate recognition data files")
                        else:
                            print("R1. [ ] License plate recognition data files")
                        print("")
                        print("===== Dash-cam Mode =====")
                        if (copy_dashcam_video == True):
                            print("D1. [X] Dash-cam videos (unsaved)")
                        else:
                            print("D1. [ ] Dash-cam videos (unsaved)")
                        if (copy_dashcam_video_saved == True):
                            print("D2. [X] Dash-cam videos (saved)")
                        else:
                            print("D2. [ ] Dash-cam videos (saved)")
                        print("")

                        selection = utils.prompt("Selection: ", optional=False, input_type=str) # Prompt the user for a selection.


                        if (selection == "0"):
                            break

                        # Toggle the file indicated by the user.
                        elif (selection.lower() == "m1"):
                            copy_management_configuration = not copy_management_configuration
                        elif (selection.lower() == "p1"):
                            copy_prerecorded_processed_frames = not copy_prerecorded_processed_frames
                        elif (selection.lower() == "p2"):
                            copy_prerecorded_gpx_files = not copy_prerecorded_gpx_files
                        elif (selection.lower() == "p3"):
                            copy_prerecorded_license_plate_analysis_data = not copy_prerecorded_license_plate_analysis_data
                        elif (selection.lower() == "p4"):
                            copy_prerecorded_license_plate_location_data = not copy_prerecorded_license_plate_location_data
                        elif (selection.lower() == "r1"):
                            copy_realtime_license_plate_recognition_data = not copy_realtime_license_plate_recognition_data
                        elif (selection.lower() == "d1"):
                            copy_dashcam_video = not copy_dashcam_video
                        elif (selection.lower() == "d2"):
                            copy_dashcam_video_saved = not copy_dashcam_video_saved
                    

                    # Prompt the user for the copying destination.
                    copy_destination = "" # Set the copy_destination as a blank placeholder.
                    while os.path.isdir(copy_destination) == False: # Repeatedly ask the user for a valid copy destination until they enter one that is valid.
                        copy_destination = utils.prompt("Destination directory: ", optional=False, input_type=str) # Prompt the user for a destination path.
                        if (os.path.isdir(copy_destination) == False):
                            utils.display_message("The specified destination is not a valid directory.", 2)


                    # Copy the files as per the user's inputs.
                    print("Copying files...")
                    if (copy_management_configuration):
                        try:
                            subprocess.run(["cp", global_variables.CONFIG_PATH, copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy configuration file: " + str(e), 2)

                    if (copy_prerecorded_processed_frames):
                        try:
                            subprocess.run(["cp", "-r", os.path.join(config["general"]["working_directory"], "frames"), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy pre-recorded processed frames: " + str(e), 2)
                    if (copy_prerecorded_gpx_files):
                        try:
                            subprocess.run(["cp", os.path.join(config["general"]["working_directory"], "*.gpx"), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy GPX files: " + str(e), 2)
                    if (copy_prerecorded_license_plate_analysis_data):
                        try:
                            subprocess.run(["cp", os.path.join(config["general"]["working_directory"], "pre_recorded_license_plate_export.*"), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy pre-recorded license plate analysis export files: " + str(e), 2)
                    if (copy_prerecorded_license_plate_location_data):
                        try:
                            subprocess.run(["cp", os.path.join(config["general"]["working_directory"], "/pre_recorded_location_data_export.*"), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy pre-recorded license plate location export files: " + str(e), 2)

                    if (copy_realtime_license_plate_recognition_data):
                        try:
                            subprocess.run(["cp", os.path.join(config["general"]["working_directory"], config["realtime"]["saving"]["license_plates"]["file"]), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy real-time license plate log files: " + str(e), 2)

                    if (config["dashcam"]["capture"]["audio"]["merge"] == True):
                        extension = "mkv"
                    else:
                        extension = config["dashcam"]["saving"]["file"]["extension"]
                    if (copy_dashcam_video):
                        try:
                            subprocess.run(["cp", os.path.join(config["general"]["working_directory"], "* Predator *." + extension), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy dash-cam video: " + str(e), 2)
                    if (copy_dashcam_video_saved):
                        try:
                            subprocess.run(["cp", "-r", os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"]), copy_destination], check=True)
                        except Exception as e:
                            utils.display_message("Failed to copy dash-cam video: " + str(e), 2)

                    utils.clear()
                    utils.display_message("Files have finished copying.", 1)


                elif (selection == "3"): # The user has selected the "delete files" option.
                    # Reset all of the file selections to un-selected.
                    delete_management_custom = False
                    delete_prerecorded_processed_frames = False
                    delete_prerecorded_gpx_files = False
                    delete_prerecorded_license_plate_analysis_data = False
                    delete_prerecorded_license_plate_location_data = False
                    delete_realtime_license_plate_recognition_data = False
                    delete_dashcam_video = False
                    delete_dashcam_video_saved = False

                    while True: # Run the "delete files" selection menu on a loop forever until the user is finished selecting files.
                        utils.clear() # Clear the console output before each loop.
                        print("Please select which files to delete")
                        print("0. Continue")
                        print("")
                        print("===== Management Mode =====")
                        if (delete_management_custom == True):
                            print("M1. [X] Custom file-name (Specified in next step)")
                        else:
                            print("M1. [ ] Custom file-name (Specified in next step)")
                        print("")
                        print("===== Pre-recorded Mode =====")
                        if (delete_prerecorded_processed_frames == True):
                            print("P1. [X] Processed video frames")
                        else:
                            print("P1. [ ] Processed video frames")
                        if (delete_prerecorded_gpx_files == True):
                            print("P2. [X] GPX files")
                        else:
                            print("P2. [ ] GPX files")
                        if (delete_prerecorded_license_plate_analysis_data == True):
                            print("P3. [X] License plate analysis data files")
                        else:
                            print("P3. [ ] License plate analysis data files")
                        if (delete_prerecorded_license_plate_location_data == True):
                            print("P4. [X] License plate location data files")
                        else:
                            print("P4. [ ] License plate location data files")
                        print("")
                        print("===== Real-time Mode =====")
                        if (delete_realtime_license_plate_recognition_data == True):
                            print("R1. [X] License plate recognition data files")
                        else:
                            print("R1. [ ] License plate recognition data files")
                        print("")
                        print("===== Dash-cam Mode =====")
                        if (delete_dashcam_video == True):
                            print("D1. [X] Dash-cam videos (unsaved)")
                        else:
                            print("D1. [ ] Dash-cam videos (unsaved)")
                        if (delete_dashcam_video == True):
                            print("D2. [X] Dash-cam videos (saved)")
                        else:
                            print("D2. [ ] Dash-cam videos (saved)")
                        print("")

                        selection = utils.prompt("Selection: ", optional=False, input_type=str) # Prompt the user for a selection.

                        if (selection == "0"):
                            break

                        # Toggle the file indicated by the user.
                        elif (selection.lower() == "m1"):
                            delete_management_custom = not delete_management_custom
                        elif (selection.lower() == "p1"):
                            delete_prerecorded_processed_frames = not delete_prerecorded_processed_frames
                        elif (selection.lower() == "p2"):
                            delete_prerecorded_gpx_files = not delete_prerecorded_gpx_files
                        elif (selection.lower() == "p3"):
                            delete_prerecorded_license_plate_analysis_data = not delete_prerecorded_license_plate_analysis_data
                        elif (selection.lower() == "p4"):
                            delete_prerecorded_license_plate_location_data = not delete_prerecorded_license_plate_location_data
                        elif (selection.lower() == "r1"):
                            delete_realtime_license_plate_recognition_data = not delete_realtime_license_plate_recognition_data
                        elif (selection.lower() == "d1"):
                            delete_dashcam_video = not delete_dashcam_video
                        elif (selection.lower() == "d2"):
                            delete_dashcam_video_saved = not delete_dashcam_video_saved

                    if (delete_management_custom):
                        delete_custom_file_name = utils.prompt("Please specify the name of the additional file you'd like to delete from the current working directory: ")

                    # Delete the files as per the user's inputs, after confirming the deletion process.
                    if (utils.prompt("Are you sure you want to delete the selected files permanently? (y/n): ").lower() == "y"):
                        print("Deleting files...")
                        if (delete_management_custom):
                            try:
                                subprocess.run(["rm", "-r", os.path.join(config["general"]["working_directory"], delete_custom_file_name)], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete custom file-path: " + str(e), 2)

                        if (delete_prerecorded_processed_frames):
                            try:
                                subprocess.run(["rm", "-r", os.path.join(config["general"]["working_directory"], "/frames")], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete copy pre-recorded processed frames: " + str(e), 2)
                        if (delete_prerecorded_gpx_files):
                            try:
                                subprocess.run(["rm", os.path.join(config["general"]["working_directory"], "/*.gpx")], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete GPX files: " + str(e), 2)
                        if (delete_prerecorded_license_plate_analysis_data):
                            try:
                                subprocess.run(["rm", os.path.join(config["general"]["working_directory"], "/pre_recorded_license_plate_export.*")], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete pre-recorded license plate analysis export files: " + str(e), 2)
                        if (delete_prerecorded_license_plate_location_data):
                            try:
                                subprocess.run(["rm", os.path.join(config["general"]["working_directory"], "/pre_recorded_location_data_export.*")], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete pre-recorded license plate location export files: " + str(e), 2)

                        if (delete_realtime_license_plate_recognition_data):
                            try:
                                subprocess.run(["rm", os.path.join(config["general"]["working_directory"], config["realtime"]["saving"]["license_plates"]["file"])], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete real-time license plate log files: " + str(e), 2)

                        if (delete_dashcam_video):
                            try:
                                subprocess.run(["rm", os.path.join(config["general"]["working_directory"], "* Predator *." + extension)], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete unsaved dash-cam video: " + str(e), 2)
                        if (delete_dashcam_video_saved):
                            try:
                                subprocess.run(["rm", "-r", os.path.join(config["general"]["working_directory"], config["dashcam"]["saving"]["directory"])], check=True)
                            except Exception as e:
                                utils.display_message("Failed to delete saved dash-cam video: " + str(e), 2)

                        utils.clear()
                        utils.display_message("Files have finished deleting.", 1)
                    else:
                        utils.display_message("No files have been deleted.", 1)


                else: # The user has selected an invalid option in the file management menu.
                    utils.display_message("Invalid selection.", 2)



            elif (selection == "2"): # The user has selected the "Information" option.
                print("    Please select an option")
                print("    0. Back")
                print("    1. About")
                print("    2. Neofetch")
                print("    3. Print Current Configuration")
                if (config["management"]["disk_statistics"] == True): # Check to see if disk statistics are enabled.
                    print("    4. Disk Usage") # Display the disk usage option in a normal utils.style.
                else: # Otherwise, disk statistics are disabled.
                    print("    " + utils.style.faint + "4. Disk Usage" + utils.style.end) # Display the disk usage option in a faint style to indicate that it is disabled.
                selection = utils.prompt("    Selection: ", optional=False, input_type=str)
                if (selection == "0"): # The user has selected to return back to the previous menu.
                    continue # Do nothing, and just finish this loop.
                elif (selection == "1"): # The user has selected the "about" option.
                    utils.clear()
                    lines = ["Predator", "V0LT", str(global_variables.PREDATOR_VERSION), "AGPLv3"]
                    print(utils.style.bold + "="*max(map(len, lines)) + utils.style.end) # Print N number of equal signs, where N is the length of the longest line.
                    for line in lines:
                        print(utils.style.bold + line + utils.style.end)
                    print(utils.style.bold + "="*max(map(len, lines)) + utils.style.end) # Print N number of equal signs, where N is the length of the longest line.
                elif (selection == "2"): # The user has selected the "neofetch" option.
                    os.system("neofetch") # Execute neofetch to display information about the system.
                elif (selection == "3"): # The user has selected the "print configuration" option.
                    os.system("cat \"" + global_variables.CONFIG_PATH + "\"") # Print out the raw contents of the configuration database.
                elif (selection == "4"): # The user has selected the "disk usage" option.
                    if (config["management"]["disk_statistics"] == True): # Check to make sure disk statistics are enabled before displaying disk statistics.
                        print("Free space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).free)/1000000000)*100)/100) + "GB") # Display the free space on the storage device containing the current working directory.
                        print("Used space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).used)/1000000000)*100)/100) + "GB") # Display the used space on the storage device containing the current working directory.
                        print("Total space: " + str(round(((psutil.disk_usage(path=config["general"]["working_directory"]).total)/1000000000)*100)/100) + "GB") # Display the total space on the storage device containing the current working directory.
                    else: # Disk statistics are disabled, but the user has selected the disk usage option.
                        utils.display_message("The disk usage could not be displayed because the 'disk_statistics' configuration option is disabled.", 2)
                else: # The user has selected an invalid option in the information menu.
                    utils.display_message("Invalid selection.", 2)

                utils.wait_for_input()
                


            elif (selection == "3"): # The user has selected the "Configuration" option.
                print("    Please enter the name of a configuration section to edit")
                for section in config: # Iterate through each top-level section of the configuration database, and display them all to the user.
                    if (type(config[section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                        print("    '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                    else:
                        print("    '" + utils.style.italic + str(section) + utils.style.end + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                selection1 = utils.prompt("=== Selection (Tier 1): ", optional=True, input_type=str, default="")

                if (selection1 in config): # Check to make sure the section entered by the user actually exists in the configuration database.
                    if (type(config[selection1]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                        for section in config[selection1]: # Iterate through each second-level section of the configuration database, and display them all to the user.
                            if (type(config[selection1][section]) is dict): # Check to see if the current entry is a dictionary.
                                print("        '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                            else:
                                print("        '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                        selection2 = utils.prompt("======= Selection (Tier 2): ", optional=True, input_type=str, default="")
                        if (selection2 in config[selection1]): # Check to make sure the section entered by the user actually exists in the configuration database.
                            if (type(config[selection1][selection2]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                for section in config[selection1][selection2]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                    if (type(config[selection1][selection2][section]) is dict): # Check to see if the current element is a dictionary.
                                        print("            '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                    else:
                                        print("            '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                selection3 = utils.prompt("=========== Selection (Tier 3): ", optional=True, input_type=str, default="")
                                if (selection3 in config[selection1][selection2]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                    if (type(config[selection1][selection2][selection3]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                        for section in config[selection1][selection2][selection3]: # Iterate through each third-level section of the configuration database, and display them all to the user.
                                            if (type(config[selection1][selection2][selection3][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                print("                '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                            else:
                                                print("                '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][selection3][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                        selection4 = utils.prompt("=============== Selection (Tier 4): ", optional=False, input_type=str)
                                        if (selection4 in config[selection1][selection2][selection3]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                            if (type(config[selection1][selection2][selection3][selection4]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                for section in config[selection1][selection2][selection3][selection4]: # Iterate through each fourth-level section of the configuration database, and display them all to the user.
                                                    if (type(config[selection1][selection2][selection3][selection4][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                        print("                    '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                                    else:
                                                        print("                    '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][selection3][selection4][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                selection5 = utils.prompt("=================== Selection (Tier 5): ", optional=False, input_type=str)
                                                if (selection5 in config[selection1][selection2][selection3][selection4]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                    if (type(config[selection1][selection2][selection3][selection4][selection5]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                        for section in config[selection1][selection2][selection3][selection4][selection5]: # Iterate through each fifth-level section of the configuration database, and display them all to the user.
                                                            if (type(config[selection1][selection2][selection3][selection4][selection5][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                                print("                        '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                                            else:
                                                                print("                        '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                        selection6 = utils.prompt("======================= Selection (Tier 6): ", optional=False, input_type=str)
                                                        if (selection6 in config[selection1][selection2][selection3][selection4][selection5]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                            if (type(config[selection1][selection2][selection3][selection4][selection5][selection6]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                                for section in config[selection1][selection2][selection3][selection4][selection5][selection6]: # Iterate through each sixth-level section of the configuration database, and display them all to the user.
                                                                    if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                                        print("                            '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                                                    else:
                                                                        print("                            '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][selection6][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                                selection7 = utils.prompt("=========================== Selection (Tier 7): ", optional=False, input_type=str)
                                                                if (selection7 in config[selection1][selection2][selection3][selection4][selection5][selection6]): # Check to make sure the section entered by the user actually exists in the configuration database.
                                                                    if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]) is dict): # Check to make sure the current selection is a dictionary before trying to iterate through it.
                                                                        for section in config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]: # Iterate through each sixth-level section of the configuration database, and display them all to the user.
                                                                            if (type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7][section]) is dict): # Check to see if the current section we're iterating over is a dictionary.
                                                                                print("                                '" + utils.style.bold + str(section) + utils.style.end + "'") # If the entry is a dictionary, display it in bold.
                                                                            else:
                                                                                print("                                '" + utils.style.italic + str(section) + utils.style.end + "': '" + str(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7][section]) + "'") # If the entry is not a dictionary (meaning it's an actual configuration value), display it in italics.
                                                                        selection8 = utils.prompt("=============================== Selection (Tier 8): ", optional=False, input_type=str)
                                                                    else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 7)
                                                                        print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]))
                                                                        config[selection1][selection2][selection3][selection4][selection5][selection6][selection7] = utils.prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5][selection6][selection7]), default="")
                                                                elif (selection7 != ""):
                                                                    utils.display_message("Unknown configuration entry selected.", 3)
                                                            else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 6)
                                                                print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5][selection6]))
                                                                config[selection1][selection2][selection3][selection4][selection5][selection6] = utils.prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5][selection6])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5][selection6]), default="")
                                                        elif (selection6 != ""):
                                                            utils.display_message("Unknown configuration entry selected.", 3)
                                                    else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 5)
                                                        print("                Current Value: " + str(config[selection1][selection2][selection3][selection4][selection5]))
                                                        config[selection1][selection2][selection3][selection4][selection5] = utils.prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4][selection5])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4][selection5]), default="")
                                                elif (selection5 != ""):
                                                    utils.display_message("Unknown configuration entry selected.", 3)
                                            else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 4)
                                                print("                Current Value: " + str(config[selection1][selection2][selection3][selection4]))
                                                config[selection1][selection2][selection3][selection4] = utils.prompt("                New Value (" + str(type(config[selection1][selection2][selection3][selection4])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3][selection4]), default="")
                                        elif (selection4 != ""):
                                            utils.display_message("Unknown configuration entry selected.", 3)
                                    else: # If the current selection isn't a dictionary, assume that it's an configuration entry. (Tier 3)
                                        print("                Current Value: " + str(config[selection1][selection2][selection3]))
                                        config[selection1][selection2][selection3] = utils.prompt("                New Value (" + str(type(config[selection1][selection2][selection3])) + "): ", optional=True, input_type=type(config[selection1][selection2][selection3]), default="")
                                elif (selection3 != ""):
                                    utils.display_message("Unknown configuration entry selected.", 3)
                            else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 2)
                                print("            Current Value: " + str(config[selection1][selection2]))
                                config[selection1][selection2] = utils.prompt("            New Value (" + str(type(config[selection1][selection2])) + "): ", optional=True, input_type=type(config[selection1][selection2]), default="")
                        elif (selection2 != ""):
                            utils.display_message("Unknown configuration entry selected.", 3)

                    else: # If the current selection isn't a dictionary or list, assume that it's an configuration entry. (Tier 1)
                        print("        Current Value: " + str(config[selection1]))
                        config[selection1] = utils.prompt("        New Value (" + str(type(config[selection1])) + "): ", optional=True, input_type=type(config[selection1]), default="")
                elif (selection1 != ""):
                    utils.display_message("Unknown configuration entry selected.", 3)


                config_file = open(global_variables.CONFIG_PATH, "w") # Open the configuration file.
                json.dump(config, config_file, indent=4) # Dump the JSON data into the configuration file on the disk.
                config_file.close() # Close the configuration file.
                config = json.load(open(global_variables.CONFIG_PATH)) # Re-load the configuration database from disk.


            else: # The user has selected an invalid option in the main management menu.
                utils.display_message("Invalid selection.", 2)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        utils.display_message("A fatal exception occurred", 3)
        e_type, e_object, e_traceback = sys.exc_info()
        e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
        e_message = str(e)
        e_line_number = e_traceback.tb_lineno
        print(f'exception type: {e_type}')
        print(f'exception filename: {e_filename}')
        print(f'exception line number: {e_line_number}')
        print(f'exception message: {e_message}')
    finally:
        utils.display_message("Management mode halted.", 1)
