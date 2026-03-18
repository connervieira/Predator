import os
import subprocess
import sys
import json
import time
import fnmatch # Required to use wildcards to check strings.
import datetime # Required for converting between timestamps and human readable date/time information.

import global_variables # `global_variables.py`
import utils # `utils.py`
import alpr # `alpr.py`
import ignore # `ignore.py`
import config # `config.py`
load_config = config.load_config
validate_config = config.validate_config
config = load_config()


def prerecorded_mode():
    global config
    utils.debug_message("Started pre-recorded mode")

    ignore_list = ignore.fetch_ignore_list() # Fetch the ignore lists.

    try:
        utils.debug_message("Taking user preferences")

        working_directory_input = utils.prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str, default=config["general"]["working_directory"])
        while (os.path.exists(working_directory_input) == False): # Run forever until the user enters a working directory that exists.
            utils.display_message("The specified working directory doesn't seem to exist.", 2)
            working_directory_input = utils.prompt("Working directory (Default " + config["general"]["working_directory"] + "): ", optional=True, input_type=str)
        config["general"]["working_directory"] = working_directory_input # Apply an override to the configured working directory.

        del working_directory_input # Remove the working directory input now that it is no longer needed.
        working_directory_contents = os.listdir(config["general"]["working_directory"]) # Get the contents of the working directory.
        dashcam_videos = [] # This is a placeholder that will hold all Predator dashcam videos found in the working directory.
        for file in working_directory_contents:
            if (" Predator " in file and (file.endswith(config["dashcam"]["saving"]["file"]["extension"]) or file.endswith(".mkv"))): # Check to see if this file is a Predator dash-cam video.
                dashcam_videos.append(file)
            
        if (len(dashcam_videos) > 3):
            print("There appears to be several Predator dashcam videos in the working directory. Would you like to generate side-car files for these videos?")
            sidecar_mode = utils.prompt("Enable side-car mode (Y/N): ", optional=False, input_type=bool)
        else:
            sidecar_mode = False

        if (sidecar_mode == True):
            print("\nRunning side-car file generation...")
            alpr.generate_dashcam_sidecar_files(config["general"]["working_directory"], dashcam_videos)
            print("Generation complete")
        elif (sidecar_mode == False):
            video = utils.prompt("Video file name(s): ", optional=False, input_type=str)

            frame_interval = utils.prompt("Frame analysis interval (Default '1.0'): ", optional=True, input_type=float, default=1.0)

            current_formats = ', '.join(config["general"]["alpr"]["validation"]["license_plate_format"])
            license_plate_format_input = utils.prompt(f"License plate format, separated by commas (Default '{current_formats}'): ", optional=True, input_type=str)
            if (license_plate_format_input == ""): # If the user leaves the license plate format input blank, then use the default.
                license_plate_format_input = current_formats
            # Convert and store the input string as a list of formats
            config["general"]["alpr"]["validation"]["license_plate_format"] = [format.strip() for format in license_plate_format_input.split(',')]

            video_start_time = utils.prompt("Video starting time (YYYY-mm-dd HH:MM:SS): ", optional=True, input_type=str) # Ask the user when the video recording started so we can correlate it's frames to a GPX file.
            if (video_start_time != ""):
                gpx_file = utils.prompt("GPX file name: ", optional=True, input_type=str)
                if (gpx_file != ""):
                    while (os.path.exists(config["general"]["working_directory"] + "/" + gpx_file) == False): # Check to see if the GPX file name supplied by the user actually exists in the working directory.
                        utils.display_message("The specified GPX file does not appear to exists.", 2)
                        gpx_file = utils.prompt("GPX file name: ", optional=False, input_type=str)
            else:
                gpx_file = ""



            utils.debug_message("Processing user preferences")
            if (video_start_time == ""): # If the video_start_time preference was left blank, then default to 0.
                video_start_time = 0
            else:
                try:
                    video_start_time = round(time.mktime(datetime.datetime.strptime(video_start_time, "%Y-%m-%d %H:%M:%S").timetuple())) # Convert the video_start_time human readable date and time into a Unix timestamp.
                except:
                    utils.display_message("The video starting time specified doesn't appear to be valid. The starting time has been reset to 0. GPX correlation will almost certainly fail.", 3)
                    video_start_time = 0


            if (video[0] == "*"): # Check to see if the first character is a wildcard.
                video_list_command = "ls \"" + os.path.join(config["general"]["working_directory"], video) + "\" | tr '\n' ','";
                videos = str(os.popen(video_list_command).read())[:-1].split(",") # Run the command, and record the raw output string.
                for key, video in enumerate(videos):
                    videos[key] = os.path.basename(video)
         
            else:
                videos = video.split(",") # Split the video input into a list, based on the position of commas.
            for number, video in enumerate(videos): # Iterate through each video specified by the user.
                videos[number] = video.strip()
                if (os.path.exists(os.path.join(config["general"]["working_directory"], video)) == False): # Check to see if each video file name supplied by the user actually exists in the working directory.
                    utils.display_message("The video file " + str(video) + " entered doesn't seem to exist in the working directory. Predator will almost certainly fail.", 3) # Inform the user that this video file couldn't be found.


            utils.clear() # Clear the console output

            


            # Split the supplied video(s) into individual frames based on the user's input.
            utils.debug_message("Splitting video into discrete frames")
            video_counter = 0 # Create a placeholder counter that will be incremented by 1 for each video. This will be appended to the file names of the video frames to keep frames from different videos separate.
            print("Splitting video into discrete images...")
            if (os.path.exists(os.path.join(config["general"]["working_directory"], "frames"))): # Check to see the frames directory already exists.
                subprocess.run(["rm", "-r", os.path.join(config["general"]["working_directory"], "frames")], check=True)

            subprocess.run(["mkdir", os.path.join(config["general"]["working_directory"], "frames")], check=True)
            for video in videos: # Iterate through each video specified by the user.
                video_counter+=1 # Increment the video counter by 1.
                subprocess.run(["ffmpeg", "-i",  os.path.join(config["general"]["working_directory"], video), "-r", str(1/frame_interval), os.path.join(config["general"]["working_directory"], "frames/video" + str(video_counter) + "_output%04d.png"), "-loglevel", "quiet"], check=True)
             
            print("Done.\n")



            # Gather all of the individual frames generated previously.
            utils.debug_message("Collecting discrete frames")
            print("Gathering generated frames...")
            frames = os.listdir(os.path.join(config["general"]["working_directory"], "frames")) # Get all of the files in the folder designated for individual frames.
            frames.sort() # Sort the list alphabetically.
            print("Done.\n")



            # Crop the individual frames to make license plate recognition more efficient and accurate.
            if (config["prerecorded"]["image"]["processing"]["cropping"]["enabled"] == True): # Check to see if cropping is enabled in pre-recorded mode.
                utils.debug_message("Cropping discrete frames")
                print("Cropping individual frames...")
                crop_script_path = os.path.join(global_variables.PREDATOR_ROOT_DIRECTORY, "crop_image") # Path to the cropping script in the Predator directory.
                for frame in frames:
                    subprocess.run([
                        crop_script_path,
                        os.path.join(config["general"]["working_directory"], "frames/", frame),
                        str(config["prerecorded"]["image"]["processing"]["cropping"]["left_margin"]),
                        str(config["prerecorded"]["image"]["processing"]["cropping"]["right_margin"]),     
                        str(config["prerecorded"]["image"]["processing"]["cropping"]["top_margin"]),
                        str(config["prerecorded"]["image"]["processing"]["cropping"]["bottom_margin"])
                    ], check=True)
                print("Done.\n")



            # Analyze each individual frame, and collect possible plate IDs.
            utils.debug_message("Running ALPR")
            print("Scanning for license plates...")
            alpr_frames = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
            for frame in frames: # Iterate through each frame of video.
                alpr_frames[frame] = {} # Set the license plate recognition information for this frame to an empty list as a placeholder.

                # Run license plate analysis on this frame.
                reading_output = alpr.run_alpr(os.path.join(config["general"]["working_directory"], "frames", frame))

                # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
                all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
                plate_index = 0 # Reset the plate index counter to 0 before the loop.
                for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
                    all_current_plate_guesses[plate_index] = {} # Create an empty dictionary for this plate so we can add all the potential plate guesses to it in the next step.
                    for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                        all_current_plate_guesses[plate_index][plate_guess["plate"]] = plate_guess["confidence"] # Add the current plate guess candidate to the list of plate guesses.
                    plate_index+=1 # Increment the plate index counter.

                if (len(all_current_plate_guesses) > 0): # Only add license plate data to the current frame if data actually exists to add in the first place.
                    alpr_frames[frame] = all_current_plate_guesses # Record all of the detected plates for this frame.

            print("Done.\n")





            # Check the possible plate IDs and validate based on general plate formatting specified by the user.
            utils.debug_message("Validating ALPR results")
            print("Validating license plates...")
            validated_alpr_frames = {} # This is a placeholder variable that will be used to store the validated ALPR information for each frame.

            # Handle ignore list processing.
            for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
                validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
                for plate in alpr_frames[frame].keys(): # Iterate through each plate detected per frame.
                    for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                        for ignore_plate in ignore_list: # Iterate through each plate in the ignore list.
                            if (fnmatch.fnmatch(guess, ignore_plate)): # Check to see if this guess matches a plate in the ignore list.
                                alpr_frames[frame][plate] = [] # Remove this plate from the ALPR dictionary.
                                break # Break the loop, since this entire plate, including all of its guesses, has just been removed.
                            if (fnmatch.fnmatch(guess, config["developer"]["kill_plate"]) and config["developer"]["kill_plate"] != ""): # Check to see if this plate matches the kill plate, and if a kill plate is set.
                                utils.stop_predator()

            # Remove any empty plates.
            for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
                plates = list(alpr_frames[frame].keys())
                for plate in plates:
                    if (len(alpr_frames[frame][plate]) <= 0):
                        del alpr_frames[frame][plate]

            # Handle formatting validation.
            for frame in alpr_frames: # Iterate through each frame of video in the database of scanned plates.
                validated_alpr_frames[frame] = {} # Set the validated license plate recognition information for this frame to an empty list as a placeholder.
                for plate in alpr_frames[frame]: # Iterate through each plate detected per frame.
                    for guess in alpr_frames[frame][plate]: # Iterate through each guess for each plate.
                        if (alpr_frames[frame][plate][guess] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate's confidence is higher than the minimum threshold set in the configuration.
                            if any(alpr.validate_plate(guess, format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]) or len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0: # Check to see if this plate passes validation.
                                if (plate not in validated_alpr_frames[frame]): # Check to see if this plate hasn't been added to the validated information yet.
                                    validated_alpr_frames[frame][plate] = [] # Add the plate to the validated information as a blank placeholder list.
                                validated_alpr_frames[frame][plate].append(guess) # Since this plate guess failed the validation test, delete it from the list of guesses.

            print("Done.\n")



            # Run through the data for each frame, and save only the first (most likely) license plate to the list of detected plates.
            utils.debug_message("Organizing ALPR results")
            print("Collecting most likely plate per guess...")
            plates_detected = [] # Create an empty list that the detected plates will be added to.
            for frame in validated_alpr_frames: # Iterate through all frames.
                for plate in validated_alpr_frames[frame]: # Iterate through all plates detected this frame.
                    if (len(validated_alpr_frames[frame][plate]) > 0): # Check to see if this plate has any guesses associated with it.
                        plates_detected.append(validated_alpr_frames[frame][plate][0]) # Add the first guess for this plate to this list of plates detected.
            print("Done.\n")




            # De-duplicate the list of license plates detected.
            print("De-duplicating detected license plates...")
            plates_detected = list(dict.fromkeys(plates_detected))
            print("Done.\n")





            utils.debug_message("Checking for alerts")
            print("Checking for alerts...")
            alert_database = alpr.load_alert_database(config["general"]["alerts"]["databases"], config["general"]["working_directory"]) # Load the license plate alert database.
            active_alerts = {} # This is an empty placeholder that will hold all of the active alerts. 
            if (len(alert_database) > 0): # Only run alert processing if the alert database isn't empty.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user.
                    for frame in alpr_frames: # Iterate through each frame of video in the raw ALPR data.
                        if (config["general"]["alerts"]["alerts_ignore_validation"] == True): # If the user has enabled alerts that ignore license plate validation, then use the unvalidated ALPR information.
                            alpr_frames_to_scan = alpr_frames
                        else: # If the user hasn't enabled alerts that ignore license plate validation, then use the validated ALPR information.
                            alpr_frames_to_scan = validated_alpr_frames

                        for plate in alpr_frames_to_scan[frame]: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                            for guess in alpr_frames_to_scan[frame][plate]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                                if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                    active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                                    active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                                    active_alerts[guess]["frame"] = frame # Add the rule that triggered this alert to the alert information.
                                    if (config["general"]["alerts"]["allow_duplicate_alerts"] == False):
                                        break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

            alpr.display_alerts(active_alerts) # Display all active alerts.
            print("Done.\n")



            # Correlate the detected license plates with a GPX file.
            frame_locations = {} # Create a blank database that will be used during the process
            if (gpx_file != ""): # Check to make sure the user actually supplied a GPX file.
                utils.debug_message("Correlated location data")
                print("Processing location data...")
                decoded_gpx_data = utils.process_gpx(config["general"]["working_directory"] + "/" + gpx_file) # Decode the data from the GPX file.
                iteration = 0 # Set the iteration counter to 0 so we can add one to it each frame we iterate through.
                for element in alpr_frames: # Iterate through each frame.
                    iteration+=1 # Add one to the iteration counter.
                    frame_timestamp = video_start_time + (iteration * frame_interval) # Calculate the timestamp of this frame.

                    if (frame_timestamp in decoded_gpx_data): # Check to see if the exact timestamp for this frame exists in the GPX data.
                        frame_locations[frame_timestamp] = [decoded_gpx_data[frame_timestamp], alpr_frames[element]]
                    else: # If the exact timestamp doesn't exist, try to find a nearby timestamp.
                        closest_gpx_entry = utils.closest_key(decoded_gpx_data, frame_timestamp)

                        if (closest_gpx_entry[1] < config["prerecorded"]["max_gpx_time_difference"]): # Check to see if the closest GPX entry is inside the maximum configured range.
                            frame_locations[frame_timestamp] = [decoded_gpx_data[closest_gpx_entry[0]], alpr_frames[element]]
                        else: # Otherwise, indicate that a corresponding location couldn't be found.
                            frame_locations[frame_timestamp] = [{"lat": 0.0, "lon": 0.0}, alpr_frames[element]] # Set this location of this frame to latitude and longitude 0.0 as a placeholder.
                            utils.display_message("There is no GPX data matching the timestamp of frame " + element + ". The closest location stamp is " + str(closest_gpx_entry[1]) + " seconds away. Does the GPX file specified line up with the video?", 3)

                print("Done.\n")




            # Analysis has been completed. Next, the user will choose what to do with the analysis data.


            utils.wait_for_input()

            utils.debug_message("Starting menu loop")
            while global_variables.PREDATOR_RUNNING: # Run the pre-recorded mode menu in a loop forever until the user exits.
                utils.clear()

                # Show the main menu for handling data collected in pre-recorded mode.
                print("Please select an option")
                print("0. Quit")
                print("1. Manage license plate data")
                if (gpx_file != ""): # Check to see if a GPX correlation is enabled before displaying the position data option.
                    print("2. Manage position data")
                else:
                    print(utils.style.faint + "2. Manage position data" + utils.style.end)
                print("3. View session statistics")
                selection = utils.prompt("Selection: ", optional=False, input_type=str)


                if (selection == "0"):
                    break
                elif (selection == "1"): # If the user selects option 1 on the main menu, then load the license plate data viewing menu.
                    print("    Please select an option")
                    print("    0. Back")
                    print("    1. View data")
                    print("    2. Export data")
                    selection = utils.prompt("    Selection: ", optional=False, input_type=str)

                    if (selection == "1"): # The user has opened the license plate data viewing menu.
                        print("        Please select an option")
                        print("        0. Back")
                        print("        1. View as Python data")
                        print("        2. View as list")
                        print("        3. View as CSV")
                        print("        4. View as JSON data")
                    
                        selection = utils.prompt("        Selection: ", optional=False, input_type=str)

                        if (selection == "0"):
                            print("Returning to main menu.")
                        elif (selection == "1"): # The user has selected to view license plate data as Python data.
                            print(str(plates_detected))
                        elif (selection == "2"): # The user has selected to view license plate data as a list.
                            for plate in plates_detected:
                                print(plate)
                        elif (selection == "3"): # The user has selected to view license plate data as CSV data.
                            csv_data = ""
                            for plate in plates_detected: # Iterate through each of the plates detected.
                                csv_data = csv_data + plate + ","
                            print(csv_data[:-1]) # Print the CSV data without the last character, since it will always be a comma.
                        elif (selection == "4"): # The user has selected to view license plate data as raw JSON data.
                            print("            Please select an option")
                            print("            0. Back")
                            print("            1. View all")
                            print("            2. View validated")
                            print("            3. View alerts")
                        
                            selection = utils.prompt("            Selection: ", optional=False, input_type=str)

                            if (selection == "0"):
                                print("Returning to main menu.")
                            elif (selection == "1"): # The user has selected to view all license plate data as JSON.
                                print(json.dumps(alpr_frames))
                            elif (selection == "2"): # The user has selected to view validated license plate data as JSON.
                                print(json.dumps(validated_alpr_frames))
                            elif (selection == "3"): # The user has selected to view validated license plate data as JSON.
                                print(json.dumps(active_alerts))
                            else:
                                utils.display_message("Invalid selection.", 2)
                        else:
                            utils.display_message("Invalid selection.", 2)

                    elif (selection == "2"): # The user has opened the license plate data exporting menu.
                        print("        Please select an option")
                        print("        0. Back")
                        print("        1. Export as Python data")
                        print("        2. Export as list")
                        print("        3. Export as CSV")
                        print("        4. Export as JSON")
                        selection = utils.prompt("        Selection: ", optional=False, input_type=str)

                        export_data = "" # Create a blank variable to store the export data.

                        if (selection == "0"):
                            print("Returning to main menu.")
                        elif (selection == "1"): # The user has selected to export license plate data as Python data.
                            export_data = str(plates_detected)
                            utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.txt", export_data) # Save to disk.
                        elif (selection == "2"): # The user has selected to export license plate data as a list.
                            for plate in plates_detected:
                                export_data = export_data + plate + "\n"
                            utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.txt", export_data) # Save to disk.
                        elif (selection == "3"): # The user has selected to export license plate data as CSV data.
                            for plate in plates_detected:
                                export_data = export_data + plate + ",\n"
                            utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.csv", export_data) # Save to disk.
                        elif (selection == "4"): # The user has selected to export license plate data as JSON data.
                            print("            Please select an option")
                            print("            0. Back")
                            print("            1. Export all")
                            print("            2. Export validated")
                            print("            3. Export alerts")
                        
                            selection = utils.prompt("            Selection: ", optional=False, input_type=str)

                            if (selection == "0"):
                                print("Returning to main menu.")
                            elif (selection == "1"): # The user has selected to export all license plate data as JSON.
                                utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(alpr_frames)) # Save the raw license plate analysis data to disk.
                            elif (selection == "2"): # The user has selected to export validated license plate data as JSON.
                                utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(validated_alpr_frames)) # Save the validated license plate analysis data to disk.
                            elif (selection == "3"): # The user has selected to alert license plate data as JSON.
                                utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_license_plate_export.json", json.dumps(active_alerts)) # Save detected license plate alerts to disk.
                            else:
                                utils.display_message("Invalid selection.", 2)
                        else:
                            utils.display_message("Invalid selection.", 2)

                    utils.wait_for_input()


                elif (selection == "2"): # The user has selected to manage GPX location information.
                    if (gpx_file != ""): # Check to see if a GPX file was provided for analysis.
                        print("    Please select an option")
                        print("    0. Back")
                        print("    1. View data")
                        print("    2. Export data")
                        selection = utils.prompt("    Selection: ", optional=False, input_type=str)

                        if (selection == "0"):
                            print("Returning to main menu.")
                        elif (selection == "1"): # The user has selected to view GPX location information.
                            print("        Please select an option")
                            print("        0. Back")
                            print("        1. View as Python data")
                            print("        2. View as JSON data")
                            selection = utils.prompt("        Selection: ", optional=False, input_type=str)

                            if (selection == "0"):
                                print("Returning to main menu.")
                            elif (selection == "1"):
                                print(frame_locations)
                            elif (selection == "2"):
                                print(json.dumps(frame_locations, indent=4))
                            else:
                                utils.display_message("Invalid selection.", 2)

                        elif (selection == "2"): # The user has selected to export GPX location information.
                            print("        Please select an option")
                            print("        0. Back")
                            print("        1. Export as Python data")
                            print("        2. Export as JSON data")
                            selection = utils.prompt("        Selection: ", optional=False, input_type=str)

                            if (selection == "0"):
                                print("Returning to main menu.")
                            elif (selection == "1"):
                                utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_location_data_export.txt", str(frame_locations)) # Save to disk.
                            elif (selection == "2"):
                                utils.save_to_file(config["general"]["working_directory"] + "/pre_recorded_location_data_export.json", json.dumps(frame_locations, indent=4)) # Save to disk.
                            else:
                                utils.display_message("Invalid selection.", 2)

                        else:
                            utils.display_message("Invalid selection.", 2)

                    else:
                        utils.display_message("GPX processing has been disabled since a GPX file wasn't provided. There is no GPX location data to manage.", 2)

                    utils.wait_for_input()


                elif (selection == "3"): # If the user selects option 4 on the main menu, then show the statistics for this session.
                    print("    Frames analyzed: " + str(len(alpr_frames))) # Show how many frames of video were analyzed.
                    print("    Plates found: " + str(len(plates_detected))) # Show how many unique plates were detected.
                    print("    Videos analyzed: " + str(len(videos))) # Show how many videos were analyzed.
                    print("    Alerts detected: " + str(len(active_alerts))) # Show how many videos were analyzed.
                    utils.wait_for_input()


                else: # If the user selects an unrecognized option on the main menu for pre-recorded mode, then show a warning.
                    utils.display_message("Invalid selection.", 2)
                    utils.wait_for_input()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        e_type, e_object, e_traceback = sys.exc_info()
        e_filename = os.path.split(e_traceback.tb_frame.f_code.co_filename)[1]
        e_message = str(e)
        e_line_number = e_traceback.tb_lineno
        print(f'Exception type: {e_type}')
        print(f'Exception filename: {e_filename}')
        print(f'Exception line number: {e_line_number}')
        print(f'Exception message: {e_message}')
        utils.display_message("A fatal exception occurred", 3)
    finally:
        utils.display_message("Pre-recorded analysis halted.", 1)
