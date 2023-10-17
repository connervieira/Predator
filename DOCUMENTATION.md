# Documentation

This document contains the information you need to know to set up and use Predator

### Note

For further clarification on the terms used in this document, see DEFINITIONS.md.


## Installation

This is the installation process for Predator and all of it's dependencies. This process is written assuming you're running a distribution of GNU/Linux, but it's theoretically possible to get Predator to function on MacOS as well.

1. Install the necessary Python packages.
    - Highly recommended: `pip3 install validators requests`
        - Without these packages, Predator will lose the a wide gamut of features, including push notifications, status light interfacing, remote alert lists, and more.
        - Unless you have good reason not to, it is highly recommended that you install these packages to avoid problems later.
    - Optional, but necessary for GPS functions: `pip3 install gps geopy gpsd-py3`
        - These packages are optional, but are required to enable live GPS features.
        - These packages are not necessary to handle information from GPX files, and are only required to interact with live GPS devices.
    - Optional, but necessary for object recognition: `pip3 install opencv-python cvlib tensorflow keras silence-tensorflow`
        - These packages are optional, but are required to enable object recognition features.
        - If you do not install these packages, make sure object recognition is disabled in the configuration, and that the configuration isn't set to use the OpenCV back-end for dashcam recording.
        - These packages are not necessary for basic license plate recognition.
    - Optional, but necessary disk usage analysis: `pip3 install psutil`
        - This package is option, but enables the ability for Predator to view information regarding disk usage.
        - If you do not install this package, make sure you disable disk statistics in the configuration.
2. Install an ALPR engine.
    - Predator needs an ALPR engine to be able to process license plates. The two main options are Phantom ALPR and OpenALPR.
        - OpenALPR is the arguably industry standard for open source license plate recognition.
            - If you already have OpenALPR installed, and don't want to replace it, you can use it with Predator.
        - Phantom ALPR is a modified version of OpenALPR designed specifically for Predator. Phantom ALPR offers more in-depth integration, and is more fault tolerant.
            - If you want the best experience with Predator, and conflicts aren't a concern, Phantom ALPR is a great option.
            - You can download Phantom at <https://v0lttech.com/phantom.php>
    -  You can learn more about the installation process for each program in their respective documentation.
    - After installing, you should be able to run the ALPR engine of your choice using the `alpr` command. If not, Predator won't be able to run the ALPR process, and will fail to analyze license plates.
3. Optionally, install FFMPEG (Highly Recommended)
    - Predator uses FFMPEG to process videos.
    - If you don't install FFMPEG, Predator will encounter errors while operating in modes that require video processing.
    - You can install FFMPEG using the following command on a Debian based Linux machine: `sudo apt-get install ffmpeg`
4. Optionally, install ImageMagick (Highly Recommended)
    - Predator uses ImageMagick to manipulate still frames of video.
    - If you don't install ImageMagick, Predator will encounter errors while operating in modes that require image processing.
    - You can learn about the ImageMagick installation process at <https://imagemagick.org/script/download.php>
5. Optionally, install MPG321 (Recommended)
    - Predator requires MPG321 in order to play audio effects for alerts.
    - If you don't install MPG321, Predator will encounter errors when audio alerts are enabled in the configuration.
    - You can install MPG321 using the following command on a Debian based Linux machine: `sudo apt-get install mpg321`
6. Optionally, install GPSD (Recommended)
    - GPSD is required for Predator to receive GPS data.
    - If you don't install GPSD, Predator will encounter errors when GPS features are enabled in the configuration.
    - You can install GPSD using this command on a Debian based Linux machine: `sudo apt-get install gpsd gpsd-clients`
    - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
7. Optionally, install remote access software.
    - If you're installing Predator on a Raspberry Pi, you may find it useful to install a program like [RaspAP](https://github.com/RaspAP/raspap-webgui) (or similar program) in order to remotely manage your Predator instance, and eliminate the need for a full keyboard and display.
    - Predator works entirely via command line, meaning any set up that enables SSH access to the host will allow for remote management of Predator.
    - If you already have an access point installed in the same area as Predator, you can simply connect Predator to it, and use SSH on a separate device to access the instance remotely.
8. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from it's GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using an unstable and potentially broken version of Predator.
    - V0LT website: <https://v0lttech.com/predator.php>
    - GitHub page: <https://github.com/connervieira/Predator>
        - `git clone https://github.com/connervieira/Predator`
9. Extract Predator
    - After downloading Predator, regardless of where you get it from, extract it from the compressed archive (if necessary), and place it somewhere on your filesystem.


## Configuration

After installing Predator, you should do some quick configuration in order to get the most out of it.

1. Open the Predator configuration
    - Open the `config.json` file in the Predator folder using your text editor of choice.
2. Make configuration changes
    - All configuration values are explained extensively in the [CONFIGURATION.md](CONFIGURATION.md) document.
    - Make changes to any of the configuration values to better fit your usage context.
    - This step is very open-ended. Depending on your situation, you may leave the configuration almost untouched, while other situations might involve intensive changes.
3. In rare cases, Predator might not be able to locate the `config.json` file. If you encounter issues during the steps described in the "Usage" section, you might need to manually set Predator's directory. Under normal circumstances, this shouldn't be necessary.
    - At the top of the all Python scripts, you should see a variable titled `predator_root_directory`. By default, a Python function is used to find the current directory of the script.
    - If you receive errors related to missing configuration files when trying to run Predator, try setting this variable to a static file path.
    - Example:
        - `predator_root_directory = "/home/user/Predator/"`


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a banner displaying the Predator name.
    - To force Predator to start into a particular mode, add the mode number to the end of the command.
        - Example: `python3 main.py 3`
            - This command will force Predator to start into mode #3, which is dash-cam mode.
        - To learn more about each mode, see the mode descriptions below.
        - This command-line argument will override the `auto_start_mode` configuration value.
    - To force Predator to use a particular working directory, instead of the one specified in the configuration, add the directory path as the second command line argument.
        - A mode number must be entered as the first command line argument to specify a working directory.
        - Example: `python3 main.py 2 /home/pi/PredatorData/`
            - This command will force Predator to start into real-time mode, using the /home/pi/PredatorData directory as the working directory.
2. Select a mode
    - Predator can operate in 4 possible modes.
        - Management mode (Mode 0)
            - This mode isn't a main operating mode for Predator, and simply exists for doing management tasks.
            - In situations where Predator is hard-installed, like in a vehicle or security system, this mode makes it easy to clear folders, copy files, and maintain Predator without having to remove the central processor.
        - Pre-recorded mode (Mode 1)
            - In this mode, Predator will analyze one or more pre-recorded video clips that you provide. This video can be in any format supported by FFMPEG.
            - You can use this mode to analyze dash-cam video, whether it be from a generic dash-cam or from Predator running in dash-cam mode.
        - Real-time mode (Mode 2)
            - In this mode, Predator will use a connected camera to detect license plates in real-time.
            - In real-time mode, Predator will stream video from a connected camera directly.
        - Dash-cam mode (Mode 3)
            - In this mode, Predator will operate like a dash-cam, and simply record video without analyzing it.
            - This mode can be used to record video to be used analyzed with pre-recorded mode later.
    - Select a mode by entering the number associated with it in the selection menu.
3. Set preferences
    - Next Predator will prompt you to set your preferences for this session. The settings you are prompted for will change depending on the mode you choose. Below are the preference menus you'll see for all modes.
    - Management mode:
        - In management mode, you'll only be asked for a working directory. Simply enter the absolute file path to a folder containing the project you'd like to manage.
            - Leave this option blank to use the default value.
            - Example: `/home/user/Downloads/MyProjectFolder`
    - Pre-recorded mode:
        - First, you'll be asked to set the working directory. Simply create an empty folder, then place your video(s) into it. Specify the absolute path to this folder here.
            - Leave this option blank to use the default value.
            - Example: `/home/pi/Downloads/MyProjectFolder`
        - Next, you'll be asked to enter the file name(s) of the video(s) you want to analyze. Video(s) should be placed in the working directory you just specified. If you have multiple video files, separate their names with a comma and space. If you want to scan an entire directory, Use a `*` wildcard as the first character.
            - Example 1: `MyVideo.mp4`
            - Example 2: `MyFirstVideo.mp4, MySecondVideo.mp4`
            - Example 3: `*.mp4`
        - Next, you'll be asked how many seconds you want to wait between frames for analysis. Since it would be inefficient to process every single frame of video, this value is used to only take frames every N seconds. You can think of this value as "only process a frame every N seconds of video".
            - Example: `2` will take a frame to process every 2 seconds of video. This would break up a 10 second video into 5 frames.
            - Leave this option blank to use the default value.
        - Next, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way. Predator only looks at the type of each character, not the character itself.
                - For sake of simplicity, you can often just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
            - Leave this option blank to use the default value.
            - Example: `AAA0000`
        - Next, you'll be asked for the time and date that the specified video recording started.
            - This preference takes the following format: YYYY-mm-dd HH:MM:SS
            - This preference is optional but will enabled the GPX file setting which grants the ability to correlate license plates to physical GPS locations.
                - If you wish to correlate license plates to location data from a GPX file, simply place the GPX file in the working directory, then enter it's file name at the prompt. Otherwise, leave it blank.
        - Finally, you'll be asked for the file name of a GPX file containing location information relevant to the video file you've specified.
            - This setting is optional, but supplying a GPX file with location data allows Predator to pin-point physical locations for each license plate it detects.
            - If you don't see this setting prompt when running Predator in pre-recorded mode, it's likely that you didn't supply a time and date in the previous prompt. This is required to enable GPX location correlation.
            - Example: `DashcamVideoLocation.gpx`
    - Real-time mode:
        - Real-time mode has no preferences, and can only be modified in the configuration file.
    - Dash-cam mode:
        - Dash-cam mode has no preferences, and can only be modified in the configuration file.
4. Using Predator
    - After finishing setting up your preferences, Predator will begin running automatically. Below you'll see information for all operation modes of Predator.
        - Management mode
            - Unlike the other modes, the entirety of management mode involves user menus.
            - To navigate through each menu, simply enter the characters associated with the menu selection you'd like to make.
                - Typically, menu items will be identified simply with numbers, but there may also be an additional letter, like in the case of the 'Copy' and 'Delete' menus.
        - Pre-recorded mode
            - You should note that while Predator is running it's analysis, a folder named 'frames' will appear in the project folder.
                - Individual frames will begin to appear in this folder as Predator runs.
                - Do not modify or delete these, since Predator will repeatedly access and modify these during the course of it's analysis.
                - After analysis completes, you can safely delete these files either manually, or by using Predator's management mode. However, these files will automatically be deleted the next time Predator runs in pre-recorded mode.
            - After Predator finishes running, you'll be sent to the analysis menu.
                - This menu allows you to manage, view, export, and manipulate the data collected in the current session.
                - To navigate this menu, simply enter the ID number of the menu item you want to select, and press enter.
        - Real-time mode
            - While in real-time mode, Predator will run in an endless loop until quit by holding `Ctrl + C` for a few seconds.
                - Since Predator launches some of it's processes in different threads, pressing `Ctrl + C` a single time might not kill the entire Predator system.
            - When one or more license plates are detected, Predator will display it on screen, provided that it is configured to do so.
                - Depending on the configuration, Predator might also display a large ASCII shape to make it easier to see important information at a glance.
                - Depending on the configuration, Predator might play an audio sound indicating the type of plate detected.
                - Depending on the configuration, Predator might submit the license plate detected to a push notification service.
                - If a plate detected is in the alert database specified during the preferences stage earlier, it will show a prominent alert message in the console output.
        - Dash-cam mode
            - In dash-cam mode, Predator will record video indefinitely until disk space runs out, the return key is pressed, or the Predator process is terminated.
            - Predator will not detect license plates in this mode. However, you can use video recorded in this mode with pre-recorded mode in order to scan for license plates at a later date.
            - The dash-cam video recorded will be saved to the project folder as `predator_dashcam_TIME_CHANNEL_SEGMENT.mkv`.
                - `TIME` is replaced by a Unix timestamp of when the file was created.
                - `CHANNEL` is replaced by the name of the device used, as specified in the configuration.
                - `SEGMENT` is replaced by the segment number, if dashcam segmentation is enabled.
