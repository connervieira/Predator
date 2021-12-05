import os
import subprocess
import sys


# ----- Configuration Start -----
crop_script_path = "/path/to/crop_image/script" # Path to the cropping script in the Predator directory.
crop_script_path = "/home/cvieira/Software/ProgrammingLanguages/Python/Predator/crop_image"

# Define frame cropping margins. These defaults are designed for a 1440p dashcam facing directly forward. You are highly encouraged to change these to better fit your camera set up.
left_margin = "700" # How many pixels will be cropped on the left side of the frame.
right_margin = "700" # How many pixels will be cropped on the right side of the frame.
top_margin = "700" # How many pixels will be cropped on the top of the frame.
bottom_margin = "300" # How many pixels will be cropped on the bottom of the frame.
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
        print("Successfully saved at export.txt in the project directory.")
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


# Get the required information from the user.
root = input("Enter the root filepath for this project, without a forward slash at the end: ")
video = input("Please enter the file name of the video you would like to scan for license plates: ")
framerate = float(input("Please enter how many seconds you want to wait between taking frames to analyze: "))



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

# Check plates based on length. Ohio plates are typically 7 characters long.
for frame in lpr_scan:
    for i in range(0,5): # Run 5 times, to make sure the list shifting around doesn't mix anything up.
        for plate in lpr_scan[frame]:
            if (len(plate) != 7): # Remove the plate if it isn't the correct amount of characters long.
                lpr_scan[frame].remove(plate)

# Check the character types of each character to see if it aligns with the Ohio plate formatting guidelines (AAA 0000).
for frame in lpr_scan:
    for i in range(0,5): # Run 5 times, to make sure the list shifting around doesn't mix anything up.
        for plate in lpr_scan[frame]:
            if (plate[0].isalpha() == True and plate[1].isalpha() == True and plate[2].isalpha() == True and plate[3].isalpha() == False and plate[4].isalpha() == False and plate[5].isalpha() == False and plate[6].isalpha() == False):
                pass
            else:
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
