# Documentation

This document contains the information you need to know to set up and use Predator


## Installation

This is the installation process for Predator and all of it's dependencies.

1. Install OpenALPR
    - Since Predator is a front-end for OpenALPR, you'll need to install it for it to work properly.
    - You can learn about the OpenALPR installation process at <https://github.com/openalpr/openalpr>
    - After installing, you should be able to run OpenALPR using the `alpr` command.
2. Install FFMPEG
    - Predator uses FFMPEG to process videos.
    - You can install FFMPEG using the following command on a Debian based Linux machine: `sudo apt-get install ffmpeg`
3. Install ImageMagick
    - Predator uses ImageMagick to manipulate frames of video.
    - You can learn about the ImageMagick installation process at <https://imagemagick.org/script/download.php>
4. Install FSWebcam
    - Predator uses FSWebcam to access cameras when using real-time mode.
    - You can install FSWebcam using the following command on a Debian based Linux machine: `sudo apt-get install fswebcam`
5. Install the `validators` Python package.
    - `pip3 install validators`
4. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from it's GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using a less stable version of Predator.
    - V0LT website: <https://v0lttech.com/predator.php>
    - GitHub page: <https://v0lttech.com/predator.php>
        - `git clone https://github.com/connervieira/Predator`
5. Extract Predator
    - After downloading Predator, regardless of where you get it from, extract it from the compressed archive (if necessary), and place it somewhere on your filesystem.


## Configuration

After installing Predator, you'll need to do some quick configuration to be able to use it properly.

1. Open the Predator configuration
    - Open the `main.py` file in the Predator folder using your text editor of choice.
    - Navigate to the top of the document, and locate the 'CONFIGURATION START' section.
2. Set the location of the `crop_image` script
    - The `crop_image` script is the script used by Predator to crop down individual frames of video.
    - The script is located in the Predator folder, along side the `main.py` file.
    - Simply set the `crop_script_path` to an absolute path pointing to the script.
    - For example: `crop_script_path = "/home/user/Downloads/Predator/crop_image"`
3. Configure the margin that will be cropped out of the frames.
    - Since the majority of camera setups (especially dashcams) will see far more than just license plates, it's important to crop images down to increase the likelihood of detecting license plates.
    - Determine how much Predator will crop out of each image by modifying the appropriate variables.
    - For example, setting `top_margin = "500"` will cause Predator to crop out the top 500 pixels of each frame.
    - To configure the cropping settings for real-time mode, follow the same guidelines, only make your changes to the `real_time_x_margin` values.
4. Configure whether invalid plates will display in real-time mode.
    - While in real-time mode, similar to pre-recorded mode, Predator will make several guesses at each plate it detects. It then runs validation on these plates based on a plate formatting example provided by the user.
    - In some situations, it might be useful to view the plates deemed invalid by Predator for sake of debugging.
    - When `print_invalid_plates` is set to True, these invalidated plates will display in red, but will not be saved to the log.
5. Configure how many guesses Predator will make per frame in real-time mode.
    - By default, Predator makes 10 guesses per license plate in real-time mode. However, if none of the guesses are correct, all of the results might be rejected for not fitting the plate formatting example provided by the user. In this case, it might make sense to increase the number of guesses made by Predator. Keep in mind that increasing this value may decrease accuracy.
    - To change this setting, set `realtime_guesses` to a number in the form of a string.
6. Configure the real-time camera resolution.
    - The `camera_resolution` setting determines the resolution that Predator will use in real-time mode.
    - This setting should usually be set to the maximum resolution supported by the camera, but there might be situations in which it makes sense to reduce this to save storage.


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a large banner reading 'PREDATOR LPRS'
2. Select a mode
    - Predator can operate a two possible modes: Pre-recorded and real-time
        - In pre-recorded mode, Predator will analyze a pre-recorded video clip that you provide.
        - In real-time mode, Predator will use a connected camera to detect license plates in real-time.
2. Set preferences
    - Next Predator will prompt you to set your preferences for this session. The settings you are prompted for will change depending on the mode you choose. Below are the preference menus you'll see for both modes.
    - Pre-recorded mode:
        - First, you'll be asked to set the root project folder. Simple create an empty folder, then place your video(s) into it. Specify the absolute path to this folder here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
        - Next, you'll be asked to enter the file name of the video you want to analyze. This video should be placed in the root project directory you just specified.
            - Example: `MyVideo.mp4`
        - Finally, you'll be asked how many second you want to wait between frames for analysis. Since it would be inefficient to process every single frame of video, this value is used to only take frames every N seconds. You can think of this value as "only process a frame every N seconds of video"
        - Example: `2` will take a frame to process every 2 seconds of video. This would break up a 10 second video into 5 frames.
        - Finally, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way.
            - For sake of simplicity, you can also just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
    - Real-time mode:
        - First, you'll be asked to set the root project folder. Simple create an empty folder, then place any files you want to use later into it. Specify the absolute path to this folder here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
        - Next, you'll be asked for an alert database. An alert database is simply a plain text file containing a list of license plates you want Predator to display an alert for.
            - This alert database should have one license plate per line, and no other characters.
            - This preference also accepts URLs. If a URL is entered, Predator will download the list of plates from a plain text file hosted at the URL specified.
            - If you leave this blank, no alerts will be displayed.
        - Next, you'll be asked whether or not you want to save the license plates detected by Predator in real-time mode. When this turned on, Predator will automatically save every plate it detects in a file named `real_time_plates.csv` in the root project directory, along with a timestamp and whether or not the plate was in the alert database you specified before.
            - This file follows this format: `PLATE,timestamp,alert_status`
        - Next, you'll be asked whether or not you want Predator to save every image it takes in real-time mode. For sake of storage, this should usually be turned off, but there may be times where you want Predator to act somewhat like a timelapse dashcam, and save every image it takes to the root project folder.
        - Finally, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way.
            - For sake of simplicity, you can also just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
    
3. Run Predator
    - After finishing setting up your preferences, Predator will begin running automatically. Below you'll see information for both operation modes of Predator.
    - Pre-recorded mode
        - You should note that while Predator is running it's analysis, you'll notice a folder named 'frames' appear in the project folder. Individual frames will begin to appear in this folder as Predator runs. Do not modify or delete these, since Predator will repeatedly access and modify these during the course of it's analysis. After analysis completes, you can safely delete these files.
    4. Manipulate results
        - After Predator finishes running, you'll be prompted to "Press enter to continue". After pressing enter, you'll see the analysis menu.
        - This menu has 4 options.
            0. Quit
                - Enter '0' into the selection to quit Predator.
            1. View data
                - Enter '1' into the selection to open up further options for viewing the data collected by Predator.
            2. Export data
                - Enter '2' into the selection to open up further options for exporting the data collected by Predator.
            3. Manage raw analysis data
                - Enter '3' into the selection to view or export the raw data collected by Predator, before sanitization and validations takes place. In other words, this data is every single plate detected by Predator, regardless of whether it matches the formatting guidelines.
    - Real-time mode
        - While in real-time mode, Predator will run in an endless loop until quit by holding `Ctrl + C`.
        - When a license plate is detected, Predator will display it on screen.
        - Depending on the preferences for the session, Predator might also save images taken and the license plates detected.
            - Images taken will be saved as `realtime_imageN.jpg` in the root project folder. If saving images is turned on, 'N' with the sequential image number. Otherwise, the N will be removed.
            - Saved license plates will be saved to `real_time_plates.csv` in the root project folder.
        - If a plate detected is in the alert database specified during the preferences stage earlier, it will show a large alert message in the console output.
