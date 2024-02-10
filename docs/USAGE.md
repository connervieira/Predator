# Usage

This document contains instructions for using Predator after it has been installed.


## Starting

This section describes the initial start-up process of Predator.

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
            - In situations where Predator is hard-installed, like in a vehicle or home security system, this mode makes it easy to clear folders, copy files, and maintain Predator without having to remove the central processing device from the installation.
        - Pre-recorded mode (Mode 1)
            - In this mode, Predator will analyze one or more pre-recorded video clips that you provide. These videos can be in any format supported by FFMPEG.
            - You can use this mode to analyze both stationary recordings and video captured while in motion.
        - Real-time mode (Mode 2)
            - In this mode, Predator will use a connected camera to detect license plates in real-time.
            - In real-time mode, Predator will use the ALPR provider to stream video from a connected capture device directly.
        - Dash-cam mode (Mode 3)
            - In this mode, Predator will operate like a dash-cam, and simply record video without attempting to detect license plates.
            - Optionally, video captured in this mode can be analyzed at a later time using pre-recorded mode.
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

## Operation

This section describes how each Predator mode works after the initial start-up.

### Management Mode
- Unlike the other modes, the management mode revolves entirely around user menus.
- To navigate through each menu, simply enter the characters associated with the menu selection you'd like to make.
    - Typically, menu items will be identified simply with numbers, but there may also be an additional letter, like in the case of the 'Copy' and 'Delete' menus.

### Pre-recorded Mode
- While Predator is running its analysis, a directory named 'frames' will appear in the working directory.
    - Individual frames will begin to appear in this folder.
    - Do not modify or delete this directory, or any files that it contains, since Predator will repeatedly access them during the course of its analysis.
    - After analysis completes, you can safely delete these files either manually, or by using Predator's management mode. These files will automatically be deleted the next time Predator runs in pre-recorded mode.
- After Predator finishes running, you'll be sent to the analysis menu.
    - This menu allows you to manage, view, export, and manipulate the data collected in the current session.
    - To navigate this menu, simply enter the ID number of the menu item you want to select, then press enter.

### Real-time Mode
- While in real-time mode, Predator will run in an endless loop until quit by holding `Ctrl + C` for a few seconds.
    - Since Predator launches some of its processes in different threads, pressing `Ctrl + C` a single time might not kill the entire Predator system.
- When one or more license plates are detected, Predator will display it on screen, provided that it is configured to do so.
    - Depending on the configuration, Predator might also display a large text shape to make it easier to see important information at a glance.
    - Depending on the configuration, Predator might play an audio sound indicating the type of plate detected.
    - Depending on the configuration, Predator might submit the license plate detected to a push notification service.
    - If a plate detected is in one of the alert databases, it will show a prominent alert message in the console output.

### Dash-cam Mode
    - In dash-cam mode, Predator will record video indefinitely until `Ctrl + C` is pressed, the Predator process is terminated, or a problem is encountered.
        - Predator records in a format that is resilient to being unexpectedly terminated. As such, suddenly killing Predator or turning off the system that it runs on shouldn't cause any meaningful data loss. That being said, certain tasks, like video/audio file merging, might not be completed if Predator is terminated before they are completed.
    - Predator will not detect license plates in this mode. However, you can analyze recorded dash-cam video using pre-recorded mode at a later time.
    - If configured to do so, Predator may automatically switch between "normal" and "parked" mode when the vehicle is stopped for a prolonged period of time.
        - In normal mode, Predator simply records dash-cam video as you would expect a traditional dash-cam to do. Separate video segments will be saved at regular intervals according to the configuration.
        - In parked mode, Predator sits dormant, waiting to detect motion on any of its configured capture devices. When motion is detected, Predator saves a certain number of past frames from a buffer, and begins recording until motion has not been detected for a certain period of time. Predator treats different capture devices as different zones, and will only record video on the camera that detects motion. If multiple cameras detect motion at the same time, Predator will record on them simultaneously.
    - The dash-cam video recorded will be saved to the working directory as `predator_dashcam_TIME_CHANNEL_SEGMENT_TYPE.mkv`.
        - `TIME` is replaced by a Unix timestamp of when the file was created.
        - `CHANNEL` is replaced by the name of the device used, as specified in the configuration.
        - `SEGMENT` is replaced by the segment number.
            - Videos recorded while parked will always have a segment number of 0.
        - `TYPE` is replaced by either the letter "N" or "P" to indicate "normal" or "parked" mode respectively.
