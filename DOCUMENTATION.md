# Documentation

This document contains the information you need to know to set up and use Predator.

### Definitions

For further clarification on the terms used in this document, see [DEFINITIONS.md](DEFINITIONS.md).


## Installation

### Quick Install Guide

If you're already familiar with Predator, and you just want a quick set-up guide, you can use the following steps to set everything up. However, if you're new to Predator, or you don't yet understand how it works, it is highly recommended that you use the follow installation instructions below instead.

1. Install Python packages: `pip3 install validators requests gps geopy gpsd-py3 opencv-python cvlib tensorflow keras silence-tensorflow psutil`
2. Install Linux packages: `sudo apt-get install ffmpeg mpg321 gpsd gpsd-clients imagemagick fswebcam`
3. Install an ALPR engine, like [Phantom](https://v0lttech.com/phantom.php).

### Full Install Guide

This is the installation process for Predator and all of its dependencies. This process is written assuming you're running a distribution of GNU/Linux, but it is possible to get Predator to function on MacOS as well.

1. Install the necessary Python packages.
    - Highly recommended: `pip3 install validators requests`
        - Without these packages, Predator will lose the a wide gamut of features, including push notifications, status light interfacing, remote alert lists, and more.
        - Unless you have good reason not to, it is highly recommended that you install these packages to avoid problems later.
    - Optional, but necessary for GPS functions: `pip3 install gps geopy gpsd-py3`
        - These packages are optional, but are required to enable live GPS features.
        - These packages are not necessary to handle information from GPX files, and are only required to interact with live GPS devices.
    - Optional, but necessary for object recognition and dashcam recording: `pip3 install opencv-python cvlib tensorflow keras silence-tensorflow`
        - These packages are optional, but are required to enable object recognition features.
        - If you do not install these packages, make sure object recognition is disabled in the configuration, and that the configuration isn't set to use the OpenCV back-end for dashcam recording.
        - These packages are not necessary for basic license plate recognition.
    - Optional, but necessary disk usage analysis: `pip3 install psutil`
        - This package is option, but enables the ability for Predator to view information regarding disk usage.
        - If you do not install this package, make sure you disable disk statistics in the configuration.
2. Install an ALPR engine.
    - Predator needs an ALPR engine to be able to process license plates. The two main options are Phantom ALPR and OpenALPR.
        - Phantom ALPR is a modified version of OpenALPR designed specifically for Predator. Phantom ALPR offers more in-depth integration, and is more fault tolerant.
            - If you want the best experience with Predator, and conflicts aren't a concern, Phantom ALPR is a great option.
            - You can download Phantom at <https://v0lttech.com/phantom.php>
        - OpenALPR is the arguably industry standard for open source license plate recognition, and is widely used.
            - If you already have OpenALPR installed, and don't want to replace it, you can use it with Predator.
    -  You can learn more about the installation process for each program in their respective documentation.
    - After installing, you should be able to run the ALPR engine of your choice using the `alpr` command. If not, Predator won't be able to run the ALPR process, and will fail to analyze license plates.
3. Optionally, install FFMPEG (Highly Recommended).
    - Predator uses FFMPEG to process videos.
    - If you don't install FFMPEG, Predator will encounter errors while operating in modes that require video processing.
        - More specifically, FFMPEG is required for the following tasks:
            1. Splitting videos into individual frames in pre-recorded mode.
            2. Merging audio and video files in dash-cam mode.
    - You can install FFMPEG using the following command on a Debian based Linux machine: `sudo apt-get install ffmpeg`
4. Optionally, install ImageMagick (Highly Recommended).
    - Predator uses ImageMagick to manipulate still frames of video.
    - If you don't install ImageMagick, Predator will encounter errors while operating in modes that require image processing.
    - You can install ImageMagick using the following command on a Debian based Linux machine: `sudo apt-get install imagemagick`
    - You can learn about the ImageMagick installation process at <https://imagemagick.org/script/download.php>
5. Optionally, install MPG321 (Recommended).
    - Predator requires MPG321 in order to play audio effects for alerts.
    - If you don't install MPG321, Predator will encounter errors when audio alerts are enabled in the configuration.
    - You can install MPG321 using the following command on a Debian based Linux machine: `sudo apt-get install mpg321`
6. Optionally, install GPSD (Recommended).
    - GPSD is required for Predator to receive GPS data.
    - If you don't install GPSD, Predator will encounter errors when GPS features are enabled in the configuration.
    - You can install GPSD using this command on a Debian based Linux machine: `sudo apt-get install gpsd gpsd-clients`
    - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
7. Optionally, install FSWebcam.
    - FSWebcam is a command line utility that captures still images from a connected video capture device.
    - Predator does not use or otherwise depend on FSWebcam, but it can be a helpful tool to verify camera functionality outside of Predator.
    - You can install FSWebcam on a design based Linux machine using this command: `sudo apt-get install fswebcam`
8. Optionally, install remote access software.
    - If you're installing Predator on a Raspberry Pi, you may find it useful to install a program like [RaspAP](https://github.com/RaspAP/raspap-webgui) (or similar program) in order to remotely manage your Predator instance, and eliminate the need for a full keyboard and display.
    - Predator works entirely via command line, meaning any set up that enables SSH access to the host will allow for remote management of Predator.
    - If you already have an access point installed in the same area as Predator, you can simply connect Predator to it, and use SSH on a separate device to access the instance remotely.
9. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from its GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using an unstable and potentially broken version of Predator.
    - V0LT website: <https://v0lttech.com/predator.php>
10. Extract Predator
    - After downloading Predator, regardless of where you get it from, extract it from the compressed archive (if necessary), and place it somewhere on your file-system.


## Configuration

After installing Predator, you should do some quick configuration in order to get the most out of it.

1. Open the Predator configuration
    - Open the `config.json` file in the Predator folder using your text editor of choice.
2. Make configuration changes
    - All configuration values are explained extensively in the [CONFIGURATION.md](CONFIGURATION.md) document.
    - Make changes to any of the configuration values to better fit your usage context.
    - This step is very open-ended. Depending on your situation, you may leave the configuration almost untouched, while other situations might involve intensive changes.


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to its folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a banner displaying the Predator name.
    - To force Predator to start into a particular mode, add the mode number to the end of the command.
        - Example: `python3 main.py 3`
            - This command will force Predator to start into mode 3, which is dash-cam mode.
        - To learn more about each mode, see the mode descriptions below.
        - If no mode number is supplied, Predator will respect the `auto_start_mode` configuration value instead. If the `auto_start_mode` configuration value is not set, then Predator will prompt the user to select an operating mode after start-up.
    - To force Predator to use a particular working directory, instead of the one specified in the configuration, add the directory path as the second command line argument.
        - A mode number must be entered as the first command line argument to specify a working directory.
        - Example: `python3 main.py 2 /home/pi/PredatorData/`
            - This command will force Predator to start into real-time mode, using the /home/pi/PredatorData directory as the working directory.
2. Select a mode
    - Predator can operate in 4 possible modes.
        - Management mode (Mode 0)
            - This mode isn't a main operating mode for Predator, and simply exists for doing management tasks.
            - In situations where Predator is hard-installed, like in a vehicle or security system, this mode makes it easy to clear folders, copy files, and maintain Predator without having to remove the central processing device from the installation.
        - Pre-recorded mode (Mode 1)
            - In this mode, Predator will analyze one or more pre-recorded video clips that you provide. This video can be in any format supported by FFMPEG.
            - You can use this mode to analyze both static and dash-cam video, whether it be from a generic dash-cam or from Predator running in dash-cam mode.
        - Real-time mode (Mode 2)
            - In this mode, Predator will use a connected camera to detect license plates in real-time.
            - In real-time mode, Predator will use the ALPR provider to stream video from a connected capture device directly.
        - Dash-cam mode (Mode 3)
            - In this mode, Predator will operate like a dash-cam, and simply record video without attempting to detect license plates.
            - This mode can be used to record video to be analyzed with pre-recorded mode later.
    - Select a mode by entering the number associated with it in the selection menu.
3. Set preferences
    - Next (depending on the mode) Predator will prompt you to set your preferences for the session. The settings you are prompted for will change depending on the mode you choose. Below are the preference menus you'll see for all modes.
    - Management mode:
        - In management mode, you'll only be asked for a working directory. Simply enter the absolute file path to a folder containing the project you'd like to manage.
            - Leave this option blank to use the default value.
            - Example: `/home/user/Downloads/MyProjectFolder`
    - Pre-recorded mode:
        - First, you'll be asked to set the working directory. Simply create an empty folder, then place your video(s) into it. Specify the absolute path to this folder here.
            - Leave this option blank to use the default value.
            - Example: `/home/pi/Downloads/MyProjectFolder`
        - Next, you'll be asked to enter the file name(s) of the video(s) you want to analyze. Video(s) should be placed in the working directory you just specified. If you have multiple video files, you can enter them as a comma-separated list. If you want to scan an entire directory, Use a `*` wildcard as the first character.
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
            - This preference is optional but will enabled the GPX file setting, which grants the ability to correlate license plates to physical GPS locations.
                - If you wish to correlate license plates to location data from a GPX file, simply place the GPX file in the working directory, then enter its file name at the prompt. Otherwise, leave it blank.
        - Finally, you'll be asked for the file name of a GPX file containing location information relevant to the video file you've specified.
            - This setting is optional, but supplying a GPX file with location data allows Predator to pin-point physical locations for each license plate it detects.
            - If you don't see this setting prompt when running Predator in pre-recorded mode, it is likely that you didn't supply a time and date in the previous prompt. This is required to enable GPX location correlation.
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
            - Note that while Predator is running its analysis, a directory named 'frames' will appear in the working directory.
                - Individual frames will begin to appear in this folder as Predator runs.
                - Do not modify or delete these, since Predator will repeatedly access and modify these during the course of its analysis.
                - After analysis completes, you can safely delete these files either manually, or by using Predator's management mode. These files will automatically be deleted the next time Predator runs in pre-recorded mode.
            - After Predator finishes running, you'll be sent to the analysis menu.
                - This menu allows you to manage, view, export, and manipulate the data collected in the current session.
                - To navigate this menu, simply enter the ID number of the menu item you want to select, then press enter.
        - Real-time mode
            - While in real-time mode, Predator will run in an endless loop until quit by holding `Ctrl + C` for a few seconds.
                - Since Predator launches some of its processes in different threads, pressing `Ctrl + C` a single time might not kill the entire Predator system.
            - When one or more license plates are detected, Predator will display it on screen, provided that it is configured to do so.
                - Depending on the configuration, Predator might also display a large text shape to make it easier to see important information at a glance.
                - Depending on the configuration, Predator might play an audio sound indicating the type of plate detected.
                - Depending on the configuration, Predator might submit the license plate detected to a push notification service.
                - If a plate detected is in one of the alert databases, it will show a prominent alert message in the console output.
        - Dash-cam mode
            - In dash-cam mode, Predator will record video indefinitely until `Ctrl + C` is pressed, the Predator process is terminated, or a problem is encountered.
            - Predator will not detect license plates in this mode. However, you can use video recorded dashcam video from this mode with pre-recorded mode in order to scan for license plates at a later time.
            - The dash-cam video recorded will be saved to the working directory as `predator_dashcam_TIME_CHANNEL_SEGMENT_TYPE.mkv`.
                - `TIME` is replaced by a Unix timestamp of when the file was created.
                - `CHANNEL` is replaced by the name of the device used, as specified in the configuration.
                - `SEGMENT` is replaced by the segment number, if dashcam video segmentation is enabled in the configuration.
                - `TYPE` is replaced by either the letter "N" or "P" to indicate "normal" or "parked" mode respectively.


## Debugging

After you've gotten Predator working, you may want to use some of its debugging features to solve issues and improve performance. This process is completely optional, provided Predator is working as expected.

1. Enable debugging messages.
    - To enable debugging messages, enable the `general>display>debugging_output` configuration value.
2. Run Predator.
    - After enabling debug messages, run Predator. You should see frequent grayed-out messages being printed to the console indicating important events behind the scenes.
3. Interpret messages.
    - Debugging messages may look complicated, but they follow a consistent structure: `[current_time] ([time_since_last_message] - [thread_name]) - [message]`
        - [current_time] is a Unix timestamp of the exact time the message was printed.
        - [time_since_last_message] is the length of time in seconds since the last message in the thread was printed.
        - [thread] is the name of the thread that the message was printed from.
        - [message] is the message itself.
    - Example: `1697686012.6295320988 (0.0000085831 - Main) - Processing ALPR alerts`
4. Locate source of delay.
    - One of the most useful implications of debugging messages is the ability to locate sources of delay during the operation of Predator.
    - To locate sources of slow-downs, you can use the `[time_since_last_message]` field described above.
        - This field will show how long the previous action in the thread took.
            - To clarify, processes in different threads work independently, and often run concurrently.
            - To locate sources of slow downs in a particular thread, pay attention to a specific thread's debug messages, and ignore other threads.
                - For example, to find slow downs in the "Main" thread, pay attention to messages marked as "Main", and ignore "ALPRStream" and "ALPRStreamMaintainer".
    - Example:
        1. Here's an example debug message sequence:
            - `1697686011.2565226555 (0.1619987488 - Main) - Loading networking libraries`
            - `1697686011.2566270828 (0.0000023842 - Main) - Loading ignore lists`
            - `1697686014.2589059357 (3.0022788525 - Main) - Initial loading complete`
        2. You'll notice that the time since the last message shown in the last line is just over 3 seconds.
            - This means that the previous action in the thread (in this case, loading the ignore lists), took 3 seconds.
        3. Resolve unnecessary delays.
            - After finding sources of delay, you may want to research their causes and attempt to resolve them.
            - In this example, the loading process for the ignore lists might be taking longer than expected because Predator doesn't have a reliable internet connection to download ignore lists from remote sources.


## Integration

Predator has several features that allow external programs to interface with it. To learn more about how to interface with Predator from external programs, see the [INTEGRATION.md](INTEGRATION.md) document.
