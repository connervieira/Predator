import os
import subprocess
import sys


# ----- Configuration Start -----
crop_script_path = "/path/to/crop_image/script"
# ----- Configuration End -----



# Get the required information from the user.
root = input("Enter the root filepath for this project, without a forward slash at the end: ")
video = input("Please enter the file name of the video you would like to scan for license plates: ")
framerate = float(input("Please enter how many seconds you want to wait between taking frames to analyze: "))



# Split the supplied video into individual frames based on the user's input
frame_split_command = "mkdir " + root + "/frames; ffmpeg -i " + root + "/" + video + " -r " + str(1/framerate) + " " + root + "/frames/output%04d.png -loglevel quiet"

os.system("clear")
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
    os.system(crop_script_path + " " + root + "/frames/" + frame + " 600 600 700 300")
print("Done.\n")



# Analyze each individual frame, and collect possible plate IDs.
print("Scanning for license plates...")
lpr_scan = {} # Create an empty dictionary that will hold each frame and the potential license plates IDs.
for frame in frames:
    analysis_command = "alpr -n 5 " + root + "/frames/" + frame + " | awk '{print $2}'"
    reading_output = str(os.popen(analysis_command).read())
    lpr_scan[frame] = reading_output.split()
print("Done.\n")




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


input("Press enter to view results...")
print(plates_detected)
