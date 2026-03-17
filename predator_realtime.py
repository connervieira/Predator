import os
import subprocess
import sys
import json
import utils
import fnmatch # Required to use wildcards to check strings.

import global_variables # `global_variables.py`
import utils # `utils.py`
import alpr # `alpr.py`
import ignore # `ignore.py`
import config # `config.py`
load_config = config.load_config
validate_config = config.validate_config
config = load_config()


def realtime_mode():
    global config
    utils.debug_message("Started real-time mode")

    ignore_list = ignore.fetch_ignore_list() # Fetch the ignore lists.

    for device in config["realtime"]["image"]["camera"]["devices"]: # Iterate through each video device specified in the configuration.
        if (os.path.exists(config["realtime"]["image"]["camera"]["devices"][device]) == False): # Check to make sure that a camera device points to a valid file.
            utils.display_message("The 'realtime>image>camera>devices>" + device + "' configuration value does not point to a valid file.", 3)


    # Load the license plate history file.
    if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if the license plate logging file name is not empty. If the file name is empty, then license plate logging will be disabled.
        plate_log = alpr.load_alpr_log()


    # Load the license plate alert database.
    alert_database = alpr.load_alert_database(config["general"]["alerts"]["databases"], config["general"]["working_directory"])

    alpr.start_alpr_stream() # Start the ALPR stream.

    detected_license_plates = [] # Create an empty list that will hold each license plate detected by Predator during this session.

    frames_captured = 0 # Set the number of frames captured to 0 so we can increment it by one each time Predator analyzes a frame.
    utils.debug_message("Starting main processing loop")
    try:
        while global_variables.PREDATOR_RUNNING: # Run in a loop forever, (until Predator is terminated).
            if (config["realtime"]["interface"]["behavior"]["clearing"] == True): # Clear the output screen at the beginning of each round if the configuration indicates to.
                utils.clear()


            if (config["realtime"]["interface"]["display"]["speed"]["enabled"] == True and config["general"]["gps"]["enabled"] == True): # Display the current speed based on GPS, if enabled in the configuration.
                current_location = utils.get_gps_location() # Get the current location.
                current_speed = utils.convert_speed(float(current_location[2]), config["realtime"]["interface"]["display"]["speed"]["unit"]) # Convert the speed data from the GPS into the units specified by the configuration.
                print("Current speed: " + str(current_speed) + " " + str(config["realtime"]["interface"]["display"]["speed"]["unit"])) # Print the current speed to the console.




            new_plates_detected = [] # This variable will be used to determine whether or not a plate was detected this round. If no plate is detected, this will remain blank. If a plate is detected, it will change to be that plate. This is used to determine whether or not the database of detected plates needs to updated.

            # Reset the status lighting to normal before processing the license plate data from ALPR.
            if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                update_status_lighting("normal") # Run the function to update the status lighting.



            # Fetch the latest plates in the queue from the ALPR stream.
            utils.debug_message("Fetching ALPR results")
            reading_output = {}
            reading_output["results"] = alpr.alpr_get_queued_plates() 



            # Organize all of the detected license plates and their list of potential guess candidates to a dictionary to make them easier to manipulate.
            utils.debug_message("Organizing ALPR results")
            all_current_plate_guesses = {} # Create an empty place-holder dictionary that will be used to store all of the potential plates and their guesses.
            for detected_plate in reading_output["results"]: # Iterate through each potential plate detected by the ALPR command.
                ignore_plate = False # Reset this value to false for each plate.
                for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                    if (plate_guess["plate"] in ignore_list): # Check to see if this plate guess matches in a plate in the loaded ignore list.
                        ignore_plate = True # Indicate that this plate should be ignored.

                    if (fnmatch.fnmatch(plate_guess["plate"], config["developer"]["kill_plate"]) and config["developer"]["kill_plate"] != ""): # Check to see if this plate matches the kill plate, and if a kill plate is set.
                        exit() # Terminate the program.

                if (ignore_plate == False): # Only process this plate if it isn't set to be ignored.
                    all_current_plate_guesses[detected_plate["candidates"][0]["plate"]] = {"guesses": {}, "identifier": detected_plate["identifier"]} # Create an empty dictionary for this plate so we can add all the potential plate guesses to it in the next step.

                    for plate_guess in detected_plate["candidates"]: # Iterate through each plate guess candidate for each potential plate detected.
                        all_current_plate_guesses[detected_plate["candidates"][0]["plate"]]["guesses"][plate_guess["plate"]] = plate_guess["confidence"] # Add the current plate guess candidate to the list of plate guesses.

            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Done\n----------")





            utils.debug_message("Processing ALPR results")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Processing license plate recognition data...")
            if (len(all_current_plate_guesses) > 0): # Check to see if at least one license plate was detected.
                if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                    print("Plates detected: " + str(len(all_current_plate_guesses))) # Show the number of plates detected this round.
                for individual_detected_plate in all_current_plate_guesses: # Iterate through each individual plate detected in the image frame.
                    successfully_found_plate = False # Reset the 'successfully_found_plate` variable to 'False'. This will be changed back if a valid plate is detected.

                    # Run validation according to the configuration on the plate(s) detected.
                    if (len(config["general"]["alpr"]["validation"]["license_plate_format"]) == 0): # If the user didn't supply a license plate format, then skip license plate validation.
                        detected_plate = str(list(all_current_plate_guesses[individual_detected_plate].keys())[0]) # Grab the most likely detected plate as the 'detected plate'.
                        successfully_found_plate = True # Plate validation wasn't needed, so the fact that a plate existed at all means a valid plate was detected. Indicate that a plate was successfully found this round.

                    else: # If the user did supply a license plate format, then check all of the results against the formatting example.
                        if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                            print ("    Plate guesses:")
                        for plate_guess in all_current_plate_guesses[individual_detected_plate]["guesses"]: # Iterate through each plate and grab the first plate that matches the plate formatting guidelines as the 'detected plate'.
                            if (all_current_plate_guesses[individual_detected_plate]["guesses"][plate_guess] >= float(config["general"]["alpr"]["validation"]["confidence"])): # Check to make sure this plate's confidence is higher than the minimum threshold set in the configuration.
                                if any(alpr.validate_plate(plate_guess, format_template) for format_template in config["general"]["alpr"]["validation"]["license_plate_format"]): # Check to see whether or not the plate passes the validation based on the format specified by the user.
                                    detected_plate = plate_guess # Grab the validated plate as the 'detected plate'.
                                    successfully_found_plate = True # The plate was successfully validated, so indicate that a plate was successfully found this round.
                                    if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the validated plate if the configuration says to do so.
                                        print("        ", utils.style.green + plate_guess + utils.style.end) # Print the valid plate in green.
                                    break
                                else: # This particular plate guess is invalid, since it didn't align with the user-supplied formatting guidelines.
                                    if (config["realtime"]["interface"]["display"]["show_validation"] == True): # Only print the invalid plate if the configuration says to do so.
                                        print("        ", utils.style.red + plate_guess + utils.style.end) # Print the invalid plate in red.




                    # Run the appropriate tasks, based on whether or not a valid license plate was detected.
                    if (successfully_found_plate == True): # Check to see if a valid plate was detected this round after the validation process ran.
                        detected_license_plates.append(detected_plate) # Save the most likely license plate ID to the detected_license_plates complete list.
                        new_plates_detected.append([detected_plate, individual_detected_plate]) # Save the most likely license plate to this round's new_plates_detected list, as well as the plate from "all_current_plate_guesses" that it comes from.


                        if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications enabled.
                            utils.debug_message("Issuing detection push notification")
                            os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=A license plate has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification via Gotify.

                        if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                            utils.display_shape("square") # Display an ASCII square in the output.

                        if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                            update_status_lighting("alpr_detection") # Run the function to update the status lighting.



                    elif (successfully_found_plate == False): # A plate was found, but none of the guesses matched the formatting guidelines provided by the user.
                        if (config["general"]["alpr"]["validation"]["best_effort"] == True): # Check to see if 'best effort' validation is enabled.
                            new_plates_detected.append([next(iter(all_current_plate_guesses[individual_detected_plate]["guesses"])), individual_detected_plate]) # Add the most likely guess for this plate to the list of detected license plates.

                        if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                            utils.display_shape("circle") # Display an ASCII circle in the output.


            else: # No license plate was detected at all.
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.")


            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("----------") # Print a dividing line after processing license plate analysis data.




            utils.debug_message("Displaying detected plates")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Displaying detected license plates...")

            for plate in new_plates_detected:
                utils.play_sound("alpr_notification")
            if (config["realtime"]["interface"]["display"]["output_level"] >= 2): # Only display this status message if the output level indicates to do so.
                print("Plates detected: " + str(len(new_plates_detected))) # Display the number of license plates detected this round.
                for plate in new_plates_detected:
                    print("    Detected plate: " + plate[0]) # Print the detected plate.




            utils.debug_message("Processing ALPR alerts")
            # Check the plate(s) detected this around against the alert database, if necessary.
            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Checking license plate data against alert database...")

            active_alerts = {} # This is a placeholder dictionary that will hold all of the active alerts.

            if (config["general"]["alerts"]["alerts_ignore_validation"] == True): # If the user has enabled alerts that ignore license plate validation, then check each of the ALPR guesses against the license plate alert database.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                    for plate in all_current_plate_guesses: # Iterate through each of the plates detected this round, regardless of whether or not they were validated.
                        for guess in all_current_plate_guesses[plate]["guesses"]: # Run through each of the plate guesses generated by ALPR, regardless of whether or not they are valid according to the plate formatting guideline.
                            if (fnmatch.fnmatch(guess, rule)): # Check to see this detected plate guess matches this particular plate in the alert database, taking wildcards into account.
                                active_alerts[guess] = alert_database[rule] # Add this plate to the active alerts dictionary.
                                active_alerts[guess]["rule"] = rule # Add the rule that triggered this alert to the alert information.
                                if (config["general"]["alerts"]["allow_duplicate_alerts"] == False):
                                    break # Break the loop if an alert is found for this guess, in order to avoid triggering multiple alerts for each guess of the same plate.

            else: #  If the user has disabled alerts that ignore license plate validation, then only check the validated plate array against the alert database.
                for rule in alert_database: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                    for plate in new_plates_detected: # Iterate through each plate that was detected and validated this round.
                        if (fnmatch.fnmatch(plate[0], rule)): # Check to see the validated detected plate matches this particular plate in the alert database, taking wildcards into account.
                            active_alerts[plate[0]] = alert_database[rule] # Add this plate to the active alerts dictionary.
                            active_alerts[plate[0]]["rule"] = rule # Add the rule that triggered this alert to the alert information.




            # Save detected license plates to file.
            if (config["realtime"]["saving"]["license_plates"]["enabled"] == True): # Check to see if license plate history saving is enabled.
                utils.debug_message("Saving license plate history")

                if ((len(all_current_plate_guesses) > 0 and config["realtime"]["saving"]["license_plates"]["save_guesses"] == True) or (len(new_plates_detected) > 0 and config["realtime"]["saving"]["license_plates"]["save_guesses"] == False)): # Only save the license plate history for this round if 1 or more plates were detected.
                    current_time = time.time() # Get the current timestamp.

                    plate_log[current_time] = {} # Initialize an entry in the plate history log using the current time.

                    if (config["realtime"]["gps"]["alpr_location_tagging"] == True): # Check to see if the configuration value for geotagging license plate detections has been enabled.
                        if (config["general"]["gps"]["enabled"] == True): # Check to see if GPS functionality is enabled.
                            current_location = utils.get_gps_location() # Get the current location.
                        else:
                            current_location = [0.0, 0.0, 0, -1] # Grab a placeholder for the current location, since GPS functionality is disabled.

                        plate_log[current_time]["location"] = {"lat": current_location[0],"lon": current_location[1], "alt": current_location[3], "head": current_location[4]} # Add the current location to the plate history log entry.

                    plate_log[current_time]["plates"] = {}

                    if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Check if Predator is configured to save all plate guesses.
                        plate_log[current_time]["plates"][plate] = {"alerts": [], "guesses": {}} # Initialize this plate in the plate log.
                        for plate in all_current_plate_guesses: # Iterate though each plate detected this round.
                            for guess in all_current_plate_guesses[plate]["guesses"]: # Iterate through each guess in this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.
                                if (config["realtime"]["saving"]["license_plates"]["save_guesses"] == True): # Only add this guess to the log if Predator is configured to do so.
                                    plate_log[current_time]["plates"][plate]["guesses"][guess] = all_current_plate_guesses[plate]["guesses"][guess] # Add this guess to the log, with its confidence level.
                    else: # Predator is configured only to save the most likely plate guess to the plate log file.
                        for plate in new_plates_detected: # Iterate over each individual plate detected.
                            plate_log[current_time]["plates"][plate[0]] = {"alerts": []} # Initialize this plate in the plate log.
                            for guess in all_current_plate_guesses[plate[1]]["guesses"]: # Iterate through each guess associated with this plate.
                                if (guess in active_alerts): # Check to see if this guess matches one of the active alerts.
                                    plate_log[current_time]["plates"][plate[0]]["alerts"].append(active_alerts[guess]["rule"]) # Add the rule that triggered the alert to a separate list.


                            plate_log[current_time]["plates"][plate[0]]["alerts"] = list(dict.fromkeys(plate_log[current_time]["plates"][plate[0]]["alerts"])) # De-duplicate the 'alerts' list for this plate.

                    utils.save_to_file(config["general"]["working_directory"] + "/" + config["realtime"]["saving"]["license_plates"]["file"], json.dumps(plate_log)) # Save the modified plate log to the disk as JSON data.

            valid_plates_with_guesses = {} # This will hold a dictionary of all valid plates with their guesses as children.
            for plate in new_plates_detected:
                valid_plates_with_guesses[plate[0]] = {
                    "guesses": all_current_plate_guesses[plate[1]]["guesses"],
                    "identifier": all_current_plate_guesses[plate[1]]["identifier"]
                }



            # Issue interface file updates.
            if (config["general"]["interface_directory"] != ""):
                utils.debug_message("Issuing interface updates")
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Issuing interface updates...")
                utils.heartbeat() # Issue a status heartbeat.
                utils.update_state("realtime") # Update the system status.
                utils.log_plates(valid_plates_with_guesses) # Update the list of recently detected license plates.
                utils.log_alerts(active_alerts) # Update the list of active alerts.
                if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                    print("Done.\n----------")



            if (len(active_alerts) > 0): # Check to see if there are any active alerts to see if an alert state should be triggered.
                if (config["general"]["status_lighting"]["enabled"] == True): # Check to see if status lighting alerts are enabled in the Predator configuration.
                    update_status_lighting("alpr_alert") # Run the function to update the status lighting.

                if (config["realtime"]["interface"]["display"]["output_level"] >= 1): # Only display alerts if the configuration specifies to do so.
                    alpr.display_alerts(active_alerts) # Display all active alerts.

                for alert in active_alerts: # Run once for each active alert.
                    if (config["realtime"]["push_notifications"]["enabled"] == True): # Check to see if the user has Gotify notifications enabled.
                        utils.debug_message("Issuing alert push notification")
                        os.system("curl -X POST '" + config["realtime"]["push_notifications"]["server"] + "/message?token=" + config["realtime"]["push_notifications"]["token"] + "' -F 'title=Predator' -F 'message=A license plate in an alert database has been detected: " + detected_plate + "' > /dev/null 2>&1 &") # Send a push notification using Gotify.

                    if (config["realtime"]["interface"]["display"]["shape_alerts"] == True): # Check to see if the user has enabled shape notifications.
                        utils.display_shape("triangle") # Display an ASCII triangle in the output.

                    utils.play_sound("alpr_alert") # Play the alert sound, if configured to do so.

            if (config["realtime"]["interface"]["display"]["output_level"] >= 3): # Only display this status message if the output level indicates to do so.
                print("Done.\n----------")



            utils.debug_message("Delaying before loop restart")
            if (len(active_alerts) > 0): # Check to see if there are one or more active alerts.
                time.sleep(float(config["realtime"]["interface"]["behavior"]["delays"]["alert"])) # Trigger a delay based on the fact that there is at least one active alert.
            else:
                time.sleep(float(config["realtime"]["interface"]["behavior"]["delays"]["normal"])) # Trigger a normal delay.
    except KeyboardInterrupt:
        print("[Keyboard interrupt]")
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
        os.popen("killall alpr") # Kill the background ALPR process.
        utils.display_message("Real-time ALPR halted.", 1)
