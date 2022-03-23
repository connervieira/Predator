# Documentation

This document contains the information you need to know to set up and use Predator


## Installation

This is the installation process for Predator and all of it's dependencies. This process is written assuming you're running a distribution of GNU/Linux, but it's theoretically possible to get Predator to function on MacOS as well.

1. Install OpenALPR
    - Since Predator depends on OpenALPR as the core of its license plate recognition, you'll need to install it for it to work properly.
    - You can learn about the OpenALPR installation process at <https://github.com/openalpr/openalpr>
    - After installing, you should be able to run OpenALPR using the `alpr` command. If not, Predator won't be able to run OpenALPR, and will fail to analyze license plates.
2. Install FFMPEG
    - Predator uses FFMPEG to process videos.
    - You can install FFMPEG using the following command on a Debian based Linux machine: `sudo apt-get install ffmpeg`
3. Install FSWebcam
    - Predator uses FSWebcam to access cameras when using real-time mode and dash-cam mode.
    - You can install FSWebcam using the following command on a Debian based Linux machine: `sudo apt-get install fswebcam`
4. Install ImageMagick
    - Predator uses ImageMagick to manipulate still frames of video.
    - You can learn about the ImageMagick installation process at <https://imagemagick.org/script/download.php>
5. Install the required Python packages.
    - `pip3 install validators opencv-python-headless==4.5.3.56 cvlib tensorflow keras silence-tensorflow psutil`
    - When tested on a Raspberry Pi 3, this step caused some issues. If you receive errors related to OpenCV when attempting to run Predator later, try uninstalling OpenCV Headless and replace it with the standard OpenCV library.
        - `pip3 uninstall opencv-python-headless; pip3 install opencv-python`
6. Install the `mpg321` package.
    - Predator requires MPG321 in order to play audio effects for alerts.
    - You can install MPG321 using the following command on a Debian based Linux machine: `sudo apt-get install mpg321`
7. Optionally, install software to remotely manage Predator.
    - If you're installing Predator on a Raspberry Pi, you may find it useful to install a program like [RaspAP](https://github.com/RaspAP/raspap-webgui) in order to remotely manage your Predator instance, and eliminate the need for a full keyboard and display.
    - Predator works entirely via command line, meaning any set up that enables SSH access to the host will allow for remote management of Predator.
8. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from it's GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using a less stable version of Predator.
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
3. Depending on the platform, Predator might not be able to locate the `config.json` file. If you encounter issues during the steps described in the "Usage" section, you may need to manually set Predator's directory in `main.py`
    - At the top of the `main.py` and `lighting.py` scripts, you should see a variable titled `predator_root_directory`. By default, a Python function is used to find the current directory of the script.
    - If you receive errors related to missing configuration files when trying to run Predator, try setting this variable to a static file path.
    - Example:
        - `predator_root_directory = "/home/user/Predator/"`


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a large banner displaying the Predator name.
    - To force Predator to start into a particular mode, add the mode number to the end of the command.
        - Example: `python3 main.py 3`
            - This command will force Predator to start into mode #3, which is dash-cam mode.
        - To learn more about each mode, see the mode descriptions below.
        - This command-line argument will override the `auto_start_mode` configuration value.
2. Select a mode
    - Predator can operate in 4 possible modes.
        - Management mode (Mode 0)
            - This mode isn't a main operating mode for Predator, and simply exists for doing management tasks.
            - In situations where Predator is hard-installed, like in a vehicle or security system, this mode makes it easy to clear folders, copy files, and maintain Predator without having to remove the central processor.
        - Pre-recorded mode (Mode 1)
            - In this mode, Predator will analyze a pre-recorded video clip that you provide. This video can be in any format supported by FFMPEG.
            - Use this mode to analyze dash-cam video, whether it be from a generic dash-cam or from Predator running in dash-cam mode.
        - Real-time mode (Mode 2)
            - In this mode, Predator will use a connected camera to detect license plates in real-time.
            - In real-time mode, Predator will repeatedly take still frames to analyze, and will not record video..
        - Dash-cam mode (Mode 3)
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
        - Next, you'll be asked how many seconds you want to wait between frames for analysis. Since it would be inefficient to process every single frame of video, this value is used to only take frames every N seconds. You can think of this value as "only process a frame every N seconds of video"
            - Example: `2` will take a frame to process every 2 seconds of video. This would break up a 10 second video into 5 frames.
            - If you leave this setting blank, Predator will default to 1 frame per second.
        - Next, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way. Predator only looks at the type of each character, not the character itself.
            - For sake of simplicity, you can also just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
            - Example: `AAA0000`
        - Next, you'll be asked whether or not you want Predator to use object recognition to count objects in each frame.
            - This will slow down processing time, but might be useful in certain cases.
            - Example: `y`
        - Next, you'll be asked for the time and date that the specified video recording started.
            - This preference takes the following format: YYYY-mm-dd HH:MM:SS
            - This preference is optional but will enabled the GPX file setting which grants the ability to correlate license plates to physical GPS locations.
                - If you wish to correlate license plates to location data from a GPX file, simply place the GPX file in the root project directory, then enter it's file name at the prompt. Otherwise, leave it blank.
        - Finally, you'll be asked for the file name of a GPX file containing information relevant to the video file you've specified.
            - This setting is optional, but supplying a GPX file with location data allows Predator to pin-point physical locations for each license plate it detects.
            - If you don't see this setting prompt when running Predator in pre-recorded mode, it's likely that you didn't supply a time and date in the previous prompt. This is required to enable GPX location correlation.
            - Example: `DashcamVideoLocation.gpx`
    - Real-time mode:
        - First, you'll be asked to set the root project folder. Simply create an empty folder, then place any files you want to use later into it. Specify the absolute path to this folder here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
            - Don't include a forward slash at the end of the path. However, in the event that you do, Predator should be able to filter out to prevent errors on most systems. Regardless, it's best practice to avoid this.
        - Next, you'll be asked for an alert database. An alert database is simply a plain text file containing a list of license plates you want Predator to display an alert for.
            - This alert database should be a plain text file, and have one license plate per line, and no other characters.
            - This preference also accepts URLs. If a URL is entered, Predator will download the list of plates from a plain text file hosted at the URL specified.
            - If you leave this blank, no alerts will be displayed.
                - To clarify, messages indicating detected license plates will still appear, but all plates will be treated identically, and there won't be any heightened alerts.
            - Example: `ImportantPlates.txt`
        - Next, you'll be asked whether or not you want to save the license plates detected by Predator in real-time mode. When this turned on, Predator will automatically save every plate it detects in a file named `real_time_plates.csv` in the root project directory, along with a timestamp and whether or not the plate was in the alert database you specified before.
            - This file follows this format: `PLATE,timestamp,alert_status`
            - If you leave this setting blank, license plate saving will be disabled by default.
            - Example: `y`
        - Next, you'll be asked whether or not you want Predator to save every image it takes in real-time mode. For sake of storage, this should usually be turned off, but there may be times where you want Predator to act somewhat like a timelapse dashcam, and save every image it takes to the root project folder.
            - If you leave this setting blank, image saving will be disabled by default.
        - Next, you'll be asked for a license plate format example. Filling out this value is highly recommended, since it will greatly reduce the number of incorrectly read plates. If this is left blank, no formatting validation will be used.
            - This value can be set to any alphanumeric string. For example, if all the plates in your state have 3 letters followed by 4 numbers, you could set this value to "AAA0000" or "ABC1234". Both values will work the exact same way.
            - For sake of simplicity, you can also just enter the license plate of another car in your state or region. Since Predator only looks to see whether a character is a number or letter, not the character itself, "EGY4011" will act identically to "AAA0000".
            - If you leave this setting blank, plate format validation will be disabled, and Predator will display/record every license plate it detects, regardless of formatting.
        - Next, you'll be asked if you want to enable real-time object detection.
            - Unless you have a good reason to enable this, it's generally advised to leave it disabled, since it can dramatically slow down Predator's processing speed.
            - When this is enabled, Predator will search each image it takes for common objects, like cars, pedestrians, traffic signals, etc.
    - Dash-cam mode:
        - In dash-cam mode, you'll only be asked for a root project directory. Simply create an empty folder, and specify it's full absolute path here.
            - Example: `/home/cvieira/Downloads/MyProjectFolder`
            - Don't include a forward slash at the end of the path. However, in the event that you do, Predator should be able to filter out to prevent errors on most systems. Regardless, it's best practice to avoid this.
    
4. Run Predator
    - After finishing setting up your preferences, Predator will begin running automatically. Below you'll see information for all operation modes of Predator.
        - Pre-recorded mode
            - You should note that while Predator is running it's analysis, you'll notice a folder named 'frames' appear in the project folder. Individual frames will begin to appear in this folder as Predator runs. Do not modify or delete these, since Predator will repeatedly access and modify these during the course of it's analysis. After analysis completes, you can safely delete these files either manually, or by using Predator's management mode.
            - After Predator finishes running, you'll be sent to the analysis menu.
                - This menu allows you to manage, view, export, and manipulate the data collected in the current session.
                - To navigate this menu, simply enter the ID number of the menu item you want to select.
        - Real-time mode
            - While in real-time mode, Predator will run in an endless loop until quit by holding `Ctrl + C` for a few seconds.
                - Since Predator launches some of it's dependencies in different threads, pressing `Ctrl + C` a single time might not kill the entire Predator system.
                - Simply hold `Ctrl + C` until you see a Linux command prompt again.
            - When a license plate is detected, Predator will display it on screen.
                - Depending on the preferences, Predator might also display a large ASCII shape to make it easier to see important information at a glance.
                - Depending on the preferences, Predator might play an audio sound indicating the type of plate detected.
                - Depending on the preferences, Predator might submit the license plate detected to a webhook and/or push notification service.
                - Depending on the preferences for the session, Predator might also save images taken and the license plates detected.
                    - Images taken will be saved as `realtime_imageN.jpg` in the root project folder. If saving images is turned on, 'N' with the sequential image number. Otherwise, the N will be removed.
                    - Saved license plates will be saved to `real_time_plates.csv` in the root project folder, provided license plate saving is enabled.
                - If a plate detected is in the alert database specified during the preferences stage earlier, it will show a large alert message in the console output.
        - Dash-cam mode
            - In dash-cam mode, Predator will record video indefinitely until either disk space runs out, or `Ctrl + C` is pressed.
            - Predator will not detect license plates in this mode. However, you can use video recorded in this mode with pre-recorded mode in order to scan for license plates at a later date.
            - The dash-cam video recorded will be saved to the project folder as `predator_dashcam_TIME_CHANNEL.mkv`.
                - `TIME` is replaced by a Unix timestamp of when the file was created.
                - `CHANNEL` is replaced by the number of the camera device used.
                    - For example, if you have two camera devices running simultaneously, the first camera will be represented as camera 1, and the second camera will be represented as camera 2.
