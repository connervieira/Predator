import os
import time
import subprocess
import sys


# ----- Configuration Start -----
crop_script_path = "/path/to/crop_image/script" # Path to the cropping script in the Predator directory.
ascii_art_header = True # This setting determines whether or not the large ASCII art Predator title will show on start-up. When set to False, a small, normal text title will appear instead. This is useful when running Predator on a device with a small display to avoid weird formatting.

# Define frame cropping margins. These defaults are designed for a 1440p dashcam facing directly forward. You are highly encouraged to change these to better fit your camera set up.
left_margin = "700" # How many pixels will be cropped on the left side of the frame.
right_margin = "700" # How many pixels will be cropped on the right side of the frame.
top_margin = "700" # How many pixels will be cropped on the top of the frame.
bottom_margin = "300" # How many pixels will be cropped on the bottom of the frame.



print_invalid_plates = False # In real-time mode, print all plates that get invalided by the formatting rules in red. When this is set to false, only valid plates are displayed.
realtime_guesses = "10" # This setting determines how many guesses Predator will make per plate in real-time mode. The higher this number, the less accurate guesses will be, but the more likely it will be that a plate matching the formatting guidelines is found.
camera_resolution = "1920x1080" # This is the resolution you want to use when taking images using the connected camera. Under normal circumstances, this should be the maximum resoultion supported by your camera.
real_time_cropping_enabled = False # This value determines whether or not each frame captured in real-time mode will be cropped.
real_time_left_margin = "200" # How many pixels will be cropped from the left side of the frame in real-time mode.
real_time_right_margin = "200" # How many pixels will be cropped from the right side of the frame in real-time mode.
real_time_top_margin = "100" # How many pixels will be cropped from the bottom side of the frame in real-time mode.
real_time_bottom_margin = "100" # How many pixels will be cropped from the top side of the frame in real-time mode.

# ----- Configuration End -----


# Define the function that will be used to clear the screen.
def clear():
    os.system("clear")


# Define the function that will be used to save files for exported data.
def save_to_file(file_name, contents):
    fh = None
    success = False
    try:
        fh = open(file_name, 'w')
        fh.write(contents)
        success = True   
        print("Successfully saved at " + file_name + ".")
    except IOError as e:
        success = False
        print(e)
        print("Failed to save!")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success

# Define the fuction that will be used to add to the end of a file.
def add_to_file(file_name, contents):
    fh = None
    success = False
    try:
        fh = open(file_name, 'a')
        fh.write(contents)
        success = True   
        print("Successfully saved at " + file_name + ".")
    except IOError as e:
        success = False
        print(e)
        print("Failed to save!")
    finally:
        try:
            if fh:
                fh.close()
        except:
            success = False
    return success


def validate_plate(plate, template):
    plate_valid = True # By default, the plate is valid, until we find a character that doesn't align.

    if (len(template) == len(plate)): # Make sure the template and plate are the same length. If so, continue with validation. Otherwise, automatically invalidate the plate, and skip the rest of the validation process.
        for x in range(len(template)):
            if (template[x].isalpha() == plate[x].isalpha() or template[x].isnumeric() == plate[x].isnumeric()): # If this character is alphabetical in both the template and plate, or if this character is numeric in both the template and plate, then this character is valid.
                # This characteris valid, so don't change anything.
                pass
            else:
                # This character doesn't match between the template and plate, so mark the plate as invalid.
                plate_valid = False
    else:
        plate_valid = False

    return plate_valid # Return the results of the plate validation



# Define some styling information
class style:
    # Define colors
    purple = '\033[95m'
    cyan = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    gray = '\033[1;37m'
    red = '\033[91m'

    # Define text decoration
    bold = '\033[1m'
    underline = '\033[4m'
    italic = '\033[3m'
    faint = '\033[2m'

    # Define styling end marker
    end = '\033[0m'



# Display the start-up intro header.
if (ascii_art_header == True): # Check to see whether the user has configured there to be a large ASCII art header, or a standard text header.
    print(style.red + style.bold)
    print(" /$$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$ ")
    print("| $$__  $$| $$__  $$| $$_____/| $$__  $$ /$$__  $$|__  $$__//$$__  $$| $$__  $$")
    print("| $$  \ $$| $$  \ $$| $$      | $$  \ $$| $$  \ $$   | $$  | $$  \ $$| $$  \ $$")
    print("| $$$$$$$/| $$$$$$$/| $$$$$   | $$  | $$| $$$$$$$$   | $$  | $$  | $$| $$$$$$$/")
    print("| $$____/ | $$__  $$| $$__/   | $$  | $$| $$__  $$   | $$  | $$  | $$| $$__  $$")
    print("| $$      | $$  \ $$| $$      | $$  | $$| $$  | $$   | $$  | $$  | $$| $$  \ $$")
    print("| $$      | $$  | $$| $$$$$$$$| $$$$$$$/| $$  | $$   | $$  |  $$$$$$/| $$  | $$")
    print("|__/      |__/  |__/|________/|_______/ |__/  |__/   |__/   \______/ |__/  |__/" + style.end + style.bold)

    print("                              _    ___ ___  ___ ")
    print("                             | |  | _ \ _ \/ __|")
    print("                             | |__|  _/   /\__ \\")
    print("                             |____|_| |_|_\\|___/")
    print(style.end)
    print("\n")
else:
    print(style.red + style.bold + "Predator" + style.end)
    print(style.bold + "LPRS" + style.end + "\n")



# Run some basic error checks to see if any of the data supplied in the configuration seems wrong.

if (os.path.exists(crop_script_path) == False):
    print(style.yellow + "Warning: The 'crop_script_path' defined in the configuration section doesn't point to a valid file. Image cropping will be broken." + style.end)

if (int(left_margin) < 0 or int(right_margin) < 0 or int(bottom_margin) < 0 or int(top_margin) < 0):
    print(style.yellow + "Warning: One or more of the cropping margins for pre-recorded mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping has been disabled." + style.end)
    left_margin = "0"
    right_margin = "0"
    bottom_margin = "0"
    top_margin = "0"

if (int(real_time_left_margin) < 0 or int(real_time_right_margin) < 0 or int(real_time_bottom_margin) < 0 or int(real_time_top_margin) < 0):
    print(style.yellow + "Warning: One or more of the cropping margins for real-time mode are below 0. This should never happen, and it's likely there's a configuration issue somewhere. Cropping has been disabled." + style.end)
    real_time_left_margin = "0"
    real_time_right_margin = "0"
    real_time_bottom_margin = "0"
    real_time_top_margin = "0"



# Figure out which mode to boot into.

print("Please select an operating mode.")
print("1. Pre-recorded")
print("2. Real time")

mode_selection = input("Selection: ")


if (mode_selection == "1"): # The user has selected to boot into pre-recorded mode.
    # Get the required information from the user.
    root = input("Enter the root filepath for this project, without a forward slash at the end: ")
    video = input("Please enter the file name of the video you would like to scan for license plates: ")
    framerate = float(input("Please enter how many seconds you want to wait between taking frames to analyze: "))
    license_plate_format = input("Please enter the license plate format you would like to scan for. Leave blank for all: ")



    # Run some validation to make sure the information just entered by the user is correct.
    if (os.path.exists(root) == False): # Check to see if the root directory entered by the user exists.
        print(style.yellow + "Warning: The root project directory entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")

    if (os.path.exists(root + "/" + video) == False): # Check to see if the video file name supplied by the user actually exists in the root project folder.
        print(style.yellow + "Warning: The video file name entered doesn't seem to exist. Predator will almost certainly fail." + style.end)
        input("Press enter to continue...")

    if (len(license_plate_format) > 12): # Check to see if the license plate template supplied by the user abnormally long.
        print(style.yellow + "Warning: The license plate template supplied is abnormally long. Predator will still be able to operate as usual, but it's possible there's been a typo, since extremely few license plates are this long." + style.end)
        input("Press enter to continue...")



    # Split the supplied video into individual frames based on the user's input
    frame_split_command = "mkdir " + root + "/frames; ffmpeg -i " + root + "/" + video + " -r " + str(1/framerate) + " " + root + "/frames/output%04d.png -loglevel quiet"

    clear()
    print("Splitting video into discrete images...")
    os.system(frame_split_command)
    print("Done.\n")



    # Gather all of the individual frames generated previously.
    print("Gathering generated frames...")
    frames = os.listdir(root + "/frames") # Get all of the files in the folder designated for individual frames.
    frames.sort() # Sort the list alphabetically.
    print("Done.\n")



    # Crop the individual frames to make license plate recognition more efficient and accurate.
    print("Cropping individual frames...")
    for frame in frames:
        os.system(crop_script_path + " " + root + "/frames/" + frame + " " + left_margin + " " + right_margin + " " + top_margin + " " + bottom_margin)
    print("Done.\n")



    # Analyze each individual frame, and collect possible plate IDs.
    print("Scanning for license plates...")
    lpr_scan = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
    for frame in frames:
        analysis_command = "alpr -n 5 " + root + "/frames/" + frame + " | awk '{print $2}'"
        reading_output = str(os.popen(analysis_command).read())
        lpr_scan[frame] = reading_output.split()
    print("Done.\n")



    raw_lpr_scan = lpr_scan # Save the data collected to a variable before sanitizing and validating it so we can access the raw data later.



    # Check the possible plate IDs and validate based on general Ohio plate formatting.
    print("Validating license plates...")

    for frame in lpr_scan: # Iterate through each frame of video in the database of scanned plates.
        lpr_scan[frame].remove(lpr_scan[frame][0]) # Remove the first element in the data, since it will never be a license plate. The first line of output for open ALPR doesn't contain license plates.
        for i in range(0,len(lpr_scan)): # Run repeatedly to make sure the list shifting around doesn't mix anything up.
            for plate in lpr_scan[frame]:
                if (validate_plate(plate, license_plate_format) == False and license_plate_format != ""): # Remove the plate if it fails the validation test (and the license plate format isn't blank).
                    lpr_scan[frame].remove(plate)
    print("Done.\n")



    # Run through the data for each frame, and save only the first (most likely) license plate.
    print("Collecting most likely plate per frame...")
    plates_detected = [] # Create an empty list that the detected plates will be added to.
    for frame in lpr_scan:
        if (len(lpr_scan[frame]) >= 1): # Only grab the first plate if a plate was detected at all.
            plates_detected.append(lpr_scan[frame][0])
    print("Done.\n")



    # De-duplicate the list of license plates detected.
    print("De-duplicating detected license plates...")
    plates_detected = list(dict.fromkeys(plates_detected))
    print("Done.\n")



    # Analysis has been completed. Next, the user will choose what to do with the analysis data.


    input("Press enter to continue...")

    while True:
        clear()

        print("Please select an option")
        print("0. Quit")
        print("1. View data")
        print("2. Export data")
        print("3. Manage raw analysis data")

        selection = input("Selection: ")
        clear()


        if (selection == "0"):
            print("Shutting down")
            break

        elif (selection == "1"):
            print("Please select an option")
            print("0. Back")
            print("1. View raw Python data")
            print("2. View as list")
            print("3. View as CSV")
            
            selection = input("Selection: ")

            if (selection == "0"):
                print("Returning to main menu.")

            elif (selection == "1"): # Print raw plate data.
                print(plates_detected)

            elif (selection == "2"): # Print plate data as a list with one plate per line.
                for plate in plates_detected:
                    print(plate)

            elif (selection == "3"): # Print plate data as CSV (add a comma after each plate)
                for plate in plates_detected:
                    print(plate + ",")

            else:
                print("Unrecognized option.")

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.
            
        elif (selection == "2"):
            print("Please select an option")
            print("0. Back")
            print("1. Export raw Python data")
            print("2. Export as list")
            print("3. Export as CSV")
            
            selection = input("Selection: ")


            export_data = "" # Create a blank variable to store the export data.

            if (selection == "0"):
                print("Returning to main menu.")

            elif (selection == "1"): # Export raw plate data.
                export_data = str(plates_detected)

                save_to_file(root + "/export.txt", export_data) # Save to disk.
            
            elif (selection == "2"): # Export plate data as a list with one plate per line.
                for plate in plates_detected:
                    export_data = export_data + plate + "\n"

                save_to_file(root + "/export.txt", export_data) # Save to disk.

            elif (selection == "3"): # Export plate data as CSV (add comma after each plate)
                for plate in plates_detected:
                    export_data = export_data + plate + ",\n"

                save_to_file(root + "/export.txt", export_data) # Save to disk.

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.

        elif (selection == "3"):
            print("Please select an option")
            print("0. Back")
            print("1. View raw data")
            print("2. Export raw data")

            selection = input("Selection: ")

            if (selection == "0"):
                print("Returning to main menu.")

            elif (selection == "1"):
                print(raw_lpr_scan)

            elif (selection == "2"):
                save_to_file(root + "/export.txt", str(raw_lpr_scan)) # Save to disk.
                

            input("\nPress enter to continue...") # Wait for the user to press enter before repeating the menu loop.




elif (mode_selection == "2"): # The user has selected to boot into real time mode.
    root = input("Enter the root filepath for this project, without a forward slash at the end: ")
    alert_database = input("Enter the file name of the database you would like to scan for alert. Leave blank for none: ")
    save_license_plates_preference = input("Would you like to save all of the license plates detected? (y/n): ")
    save_images_preference = input("Would you like to save all of the images taken? (y/n): ")
    license_plate_format = input("Please enter the license plate format you would like to scan for. Leave blank for all: ")


    # Save yes/no preferences as boolean values for easier access.
    if (save_license_plates_preference == "y"):
        save_license_plates_preference = True
    else:
        save_license_plates_preference = False

    if (save_images_preference == "y"):
        save_images_preference = True
    else:
        save_images_preference = False


    # Load the alert database
    if (alert_database != None and alert_database != ""): # Check to see if the user has supplied a database to scan for alerts.
        if (os.path.exists(root + "/" + alert_database)): # Check to see if the database specified by the user actually exists.
            f = open(root + "/" + alert_database, "r") # Open the user-specified datbase file.
            alert_database_list = f.read().split() # Read each line of the file as a seperate entry in the alert database list.
            f.close() # Close the file.
        else: # If the alert database specified by the user does not exist, alert the user of the error.
            print(style.yellow + "Warning: The alert database specified at " + root + "/" + alert_database + " does not exist. Alerts have been disabled.")
            alert_database_list = [] # Set the alert database to an empty list.
    else: # The user has not entered in an alert database.
        alert_database_list = [] # Set the alert database to an empty list.



    detected_license_plates = [] # Create an empty dictionary that will hold each frame and the potential license plates IDs.

    i = 0 # Set the increment counter to 0 so we can increment it by one each time Predator analyzes a plate.

    while True: # Run in a loop forever.

        time.sleep(0.2) # Sleep to give the user time to quit Predator if they want to.
        print("Taking image...")
        if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
            os.system("fswebcam --no-banner -r " + camera_resolution + " --jpeg 100 " + root + "/realtime_image" + str(i) + ".jpg >/dev/null 2>&1") # Take a photo using FSWebcam, and save it to the root project folder specified by the user.
        else:
            os.system("fswebcam --no-banner -r " + camera_resolution + " --jpeg 100 " + root + "/realtime_image.jpg >/dev/null 2>&1") # Take a photo using FSWebcam, and save it to the root project folder specified by the user.
        print("Done.\n----------")



        if (real_time_cropping_enabled == True): # Check to see if the user has enabled cropping in real-time mode.
            print("Cropping frame...")
            if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
                os.system(crop_script_path + " " + root + "/realtime_image" + str(i) + ".jpg " + real_time_left_margin + " " + real_time_right_margin + " " + real_time_top_margin + " " + real_time_bottom_margin) # Execute the command to crop the image.
            else:
                os.system(crop_script_path + " " + root + "/realtime_image.jpg " + real_time_left_margin + " " + real_time_right_margin + " " + real_time_top_margin + " " + real_time_bottom_margin) # Execute the command to crop the image.
            print("Done.\n----------")
            





        print("Analyzing image...")
        time.sleep(0.2) # Sleep to give the user time to quit Predator if they want to.

        if (save_images_preference == True): # Check to see whether or not the user wants to save all images captured by Predator.
            analysis_command = "alpr -n " + realtime_guesses  + " " + root + "/realtime_image" + str(i) + ".jpg | awk '{print $2}'" # Prepare the analysis command so we can run it next.
        else:
            analysis_command = "alpr -n " + realtime_guesses  + " " + root + "/realtime_image.jpg | awk '{print $2}'" # Prepare the analysis command so we can run it next.



        i = i + 1 # Increment the counter.
        new_plate_detected = "" # This variable will be used to determine whether or not a plate was detected this round. If no plate is detected, this will remain blank. If a plate is detected, it will change to be that plate. This is used to determine whether or not the database of detected plates needs to updated.

        reading_output = str(os.popen(analysis_command).read()) # Run the OpenALPR command, and save it's output to reading_output.
        reading_output_plates = reading_output.split() # Take the output of the OpenALPR command (the detected plates), and save it as a Python array.

        if (len(reading_output_plates) >= 2): # Check to see if a license plate was actually detected.
            reading_output_plates.remove(reading_output_plates[0]) # Remove the first element of the output, since it isn't a plate. The first value will always be the first line of the ALPR output, which doesn't include plates.
            
            if (license_plate_format == ""): # If the user didn't supply a license plate format, then skip license plate validation.
                detected_plate = str(reading_output_plates[1]) # Grab the most likely detected plate as the 'detected plate'.
                detected_license_plates.append(detected_plate) # Save the most likely license plate ID to the detected_license_plates list.
                print("Detected plate: " + detected_plate + "\n") # Print the plate detected.
                new_plate_detected = detected_plate
            else: # If the user did supply a license plate format, then check all of the results against the formatting example.
                successfully_found_plate = False
                for plate in reading_output_plates: # Iterate through each plate and grab the first plate that matches the plate formatting guidelines as the 'detected plate'.
                    if (validate_plate(plate, license_plate_format)): # Check to see whether or not the plate passes the validation based on the format specified by the user.
                        # The plate was valid
                        detected_plate = plate
                        successfully_found_plate = True
                        if (print_invalid_plates == True):
                            print(style.green + plate + style.end) # Print the valid plate in green.
                        break
                    else:
                        # The plate was invalid, in that it didn't align with the user-supplied formatting guidelines.
                        if (print_invalid_plates == True):
                            print(style.red + plate + style.end) # Print the invalid plate in red.

                if (successfully_found_plate == True):
                    detected_license_plates.append(detected_plate) # Save the most likely license plate ID to the detected_license_plates list.
                    print("Detected plate: " + detected_plate + "\n")
                    new_plate_detected = detected_plate
                elif (successfully_found_plate == False):
                    print("A plate was found, but none of the guesses matched the supplied plate format.\n----------")

        else: # No license plate was detected.
            print("Done.\n----------")



        # Check to see if the license plate detected (if any) is in an alert database.
        active_alert = False
        if (new_plate_detected != ""): # Check to see that the new_plate_detected variable isn't blank. This variable will only have a string if a plate was detected this round.
            for alert_plate in alert_database_list: # Run through every plate in the alert plate database supplied by the user. If no database was supplied, this list will be empty, and will not run.
                if (new_plate_detected == alert_plate): # Check to see if the detected plate matches the current plate in the alert database as we iterate through all of them.
                    active_alert = True # If the plate does exist in the alert database, indicate that there is an active alert by changing this variable to True. This will reset on the next round.

                    # Display an alert that is starkly different from the rest of the console output.
                    print(style.yellow + style.bold)
                    print("===================")
                    print("ALERT HIT - " + new_plate_detected)
                    print("===================")
                    print(style.end)

        if (save_license_plates_preference == True): # Check to see if the user has the 'save detected license plates' preference enabled.
            if (new_plate_detected != ""): # Check to see if the new_plate_detected value is blank. If it is blank, that means no new plate was detected this round.
                if (active_alert == True): # Check to see if the current plate has an active alert.
                    export_data = new_plate_detected + "," + str(round(time.time())) + ",true\n" # Add the individual plate to the export data, followed a timestamp, followed by a line break to prepare for the next plate to be added later.
                else:
                    export_data = new_plate_detected + "," + str(round(time.time())) + ",false\n" # Add the individual plate to the export data, followed a timestamp, followed by a line break to prepare for the next plate to be added later.
                add_to_file(root + "/real_time_plates.csv", export_data) # Add the export data to the end of the file and write it to disk.
