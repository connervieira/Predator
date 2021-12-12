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
6. Install the `mpg321` package.
    - `sudo apt-get install mpg321`
7. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from it's GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using a less stable version of Predator.
    - V0LT website: <https://v0lttech.com/predator.php>
    - GitHub page: <https://v0lttech.com/predator.php>
        - `git clone https://github.com/connervieira/Predator`
8. Extract Predator
    - After downloading Predator, regardless of where you get it from, extract it from the compressed archive (if necessary), and place it somewhere on your filesystem.


## Configuration

After installing Predator, you'll need to do some quick configuration to be able to use it properly.

1. Open the Predator configuration
    - Open the `main.py` file in the Predator folder using your text editor of choice.
    - Navigate to the top of the document, and locate the 'CONFIGURATION START' section.
2. Configure the real-time camera resolution.
    - The `camera_resolution` setting determines the resolution that Predator will use in real-time mode.
    - This setting should usually be set to the maximum resolution supported by the camera, but there might be situations in which it makes sense to reduce this to save storage.
3. Configure other optional values.
    - All configuration values are explained extensively in the CONFIGURING.md document.
    - Make changes to any of the configuration values to better fit your usage context.


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a large banner reading 'PREDATOR LPRS'
2. Select a mode
    - Predator can operate a three possible modes.
        - Pre-recorded mode
            - In this mode, Predator will analyze a pre-recorded video clip that you provide. This video can be in any format supported by FFMPEG.
            - Use this mode to analyze dash-cam video, whether it be from a generic dash-cam or from Predator running in dash-cam mode.
        - Real-time mode
            - In this mode, Predator will use a connected camera to detect license plates in real-time.
        - Dash-cam mode
            - In this mode, Predator will operate like a dash-cam, and simply record video without processing it.
            - This mode can be used to record video to be used analyzed with pre-recorded mode later.
    - Select a mode by entering the number associated with it in the selection menu.
3. Set preferences
    - Next Predator will prompt you to set your preferences for this session. The settings you are prompted for will change depending on the mode you choose. Below are the preference menus you'll see for all modes.
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
        - First, you'll be asked to set the root project folder. Simply create an empty folder, then place any files you want to use later into it. Specify the absolute path to this folder here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
        - Next, you'll be asked for an alert database. An alert database is simply a plain text file containing a list of license plates you want Predator to display an alert for.
            - This alert database should have one license plate per line, and no other characters.
            - This preference also accepts URLs. If a URL is entered, Predator will download the list of plates from a plain text file hosted at the URL specified.
            - If you leave this blank, no alerts will be displayed.
                - To be clear, messages indicating detected license plates will still appear, but all plates will be treated identically.
        - Next, you'll be asked whether or not you want to save the license plates detected by Predator in real-time mode. When this turned on, Predator will automatically save every plate it detects in a file named `real_time_plates.csv` in the root project directory, along with a timestamp and whether or not the plate was in the alert database you specified before.
            - This file follows this format: `PLATE,timestamp,alert_status`
        - Next, you'll be asked whether or not you want Predator to save every image it takes in real-time mode. For sake of storage, this should usually be turned off, but there may be times where you want Predator to act somewhat like a timelapse dashcam, and save every image it takes to the root project folder.
        - Next, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way.
            - For sake of simplicity, you can also just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
        - Next, you'll be prompted to enter the start time of the video.
            - This value is optional, but you'll need to enter it if you want to enable GPX correlation.
            - This value takes the format of `YYYY-mm-dd HH:MM:SS`
                - If this format is not matched, it's likely Predator will fail.
            - This value needs to be as exact as possible, since any deviation from reality could break GPX correlation, should you enable it.
            - Example: `2021-5-21 19:32:15`
        - Provided you enter a date and time for the 'video start time' preference described above, you'll now be given the option to specify a GPX file.
            - If you want to enable GPX correlation, enter the file name of a GPX file in the root project directory.
            - If left blank, GPX correlation will be disabled.
            - The GPX file specified should cover the entire duration that the video was recorded.
            - Example: `MyLocationRecording.gpx`
    - Dash-cam mode:
        - In dash-cam mode, you'll only be asked for a root project directory. Simply create an empty folder, and specify it's full absolute path here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
    
4. Run Predator
    - After finishing setting up your preferences, Predator will begin running automatically. Below you'll see information for all operation modes of Predator.
        - Pre-recorded mode
            - You should note that while Predator is running it's analysis, you'll notice a folder named 'frames' appear in the project folder. Individual frames will begin to appear in this folder as Predator runs. Do not modify or delete these, since Predator will repeatedly access and modify these during the course of it's analysis. After analysis completes, you can safely delete these files.
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
        - Dash-cam mode
            - In dash-cam mode, Predator will record video indefinitely until either disk space runs out, or `Ctrl + C` is pressed.
            - Predator will not detect license plates in this mode.
            - The dash-cam video recorded will be saved to the project folder as predator_dashcam.mkv
