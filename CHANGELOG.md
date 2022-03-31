# Changelog

This document contains all of the changes for each version of Predator.


## Version 0.9

### Initial Release

December 4th, 2021

- Core functionality


## Version 1.0

### First Stable Release

This is the first stable release of Predator, and contains the ability to detect license plates in pre-recorded video.

December 5th, 2021

- Added a basic command line menu based user interface for managing data after analysis
- Added the ability to view and export collected data in different formats
    - Raw format
    - List format
    - CSV format
- Added the ability to view and export the raw data for license plate collection, before any validation or sanitization takes place
- Added a large ASCII title screen that displays when launching Predator


## Version 2.0

### Real-time Update

This is the 'real-time update' of Predator, and adds real-time mode to Predator, where plates can be detected on a second-by-second basis, with automatic alerts and logging.

December 6th, 2021

- Added support for real-time license plate reading.
    - Predator runs a loop of taking a picture, then analyzing it.
    - Optionally, each plate detected, along with a timestamp, can be automatically saved to disk.
    - Optionally, each image taken can be saved to disk to be reviewed later, along with a timestamp and whether or not it was an alert plate.
    - Optionally, invalid plates can be printed to the screen, displayed in red, for debugging purposes.
    - Optionally, frames captured in real-time mode can be cropped down based on customizable values for the left, right, top, and bottom sides of the frame.
    - The number of guesses Predator makes in real-time mode can be customized.
    - The camera resolution in real-time mode can be customized.
    - Automatic alerts can be displayed based on a plain text file.
- Added basic validation when launching Predator.
    - When running in pre-recorded mode, Predator will validate the following:
        - Ensure the root project directory exists.
        - Ensure the specified video exists.
        - Ensure the license plate formatting template is a reasonable length.
            - However, this isn't a critical error, and Predator will still use the user-supplied template.
    - When running in real-time mode, Predator will validate the following:
        - Ensure the root project directory exists.
        - Ensure the alert database specified (if any) exists.
    - When running in any mode, Predator will validate the following:
        - Ensure the `crop_script_path` variable points to a valid file.
        - Ensure the pre-recorded cropping margins are positive values.
        - Ensure the real-time cropping margins are positive values.
- Made the license plate validation system much faster and easily customizable.
    - License plate validation now uses a function for easy customization. For example, the state of Ohio typically follows the format of AAA0000 on their license plates, while other states don't, so the function allows you to submit a plate along side a validation format template.
    - There is now a preference prompt for both pre-recorded and real-time mode that asks for a license plate validation template/example.


## Version 3.0

### Hard-wire Update

This update contains enhancements that make it much easier to install Predator in a hard-wire context, where Predator is seamlessly integrated with a more complete system in a car, building, or other location.

December 8th, 2021

- Added support for 'auto start'.
    - In the script configuration, the user can configure Predator to automatically start into either pre-recorded mode or real-time mode without asking for confirmation.
    - Added optional default preferences for real-time mode.
        - Each preference can be individually pre-set in the configuration. Any values pre-set will have their prompts skipped when starting real-time mode.
        - Preferences like 'alert database' and 'license plate format' can be skipped without providing a value by setting their default value to a single space.
    - Predator can now be configured to automatically load into real-time mode after starting without any user intervention.
    - For sake of debugging, messages will appear each time a prompt is skipped to inform the user why Predator is auto-starting.
- Yes/no preferences are no longer case-sensitive
    - Preferences that take input as 'y' or 'n' will be interpreted appropriate regardless of whether the character is capitalized.
- Added the ability to specify the alert database in real-time mode as a web URL.
    - When a URL is detected, Predator will request the file at the URL specified, and attempt to interpret it as an alert database the same way it would for a local file.
- Added the ability to set custom command arguments for FSWebcam, in case customizations need to be made to optimize performance on a camera-by-camera basis.
- Added support for audio notifications.
    - When enabled, Predator will play a subtle noise whenever a valid plate is detected, and a more prominent noise when a plate in an alert database is detected.
    - All notification sounds are sine waves with soft reverb, and will gently "rev up" as to not startle the driver when Predator is installed a vehicle.
    - All sounds can be found in the `/assets/sounds/` directory.
- Added warning messages when the user enters an invalid selection in pre-recorded mode.
- Added a simple statistics viewer for pre-recorded mode.


## Version 4.0

### Dashcam Update

This update adds 'dash-cam mode' to Predator, which allows it to record video without processing license plates in real-time. This allows you to use your Predator system as a dash-cam while driving, then analyze the video later using 'pre-recorded mode'.

December 29th, 2021

- Added dash-cam mode, with customizable resolution, frame rate, and recording device.
    - In dash-cam mode, Predator will record video in real-time to a video file, but it will not process it. This is useful if you run Predator on a low-powered device, and want to process the video at a later time.
    - Multiple recording devices can be used simultaneously using background recording.
- Added the ability to correlate pre-recorded video analysis with a GPX file.
- Added native support for push notifications via Gotify.
- Changed the audio backend from Python playsound to mpg321 in order to fix audio on Raspberry Pi.
- Fixed an issue where the 'separate line' wouldn't appear under detected plates in real-time mode.
- Added a hyphen to 'Real-time' in the mode selection menu.



## Version 5.0

### Object-Recognition Update

This update gives Predator the ability to recognize objects other than license plates, including cars, trucks, traffic lights, pedestrians, and dozens of other common items.

March 1st, 2022

- Added support for object recognition and counting in pre-recorded mode.
- Added support for object recognition and counting in real-time mode.
- Made it so pre-recorded mode will follow the `default_root` setting.
- Alert databases can now contain wildcards to further refine plate alerts.
- Simplified the start-up prompts for all modes.
- Clarified some menu prompts in pre-recorded mode.



## Version 6.0

### Management Update

This update adds "Management Mode", and improves the efficiency and organization of various user interfaces. This update also adds new functionality and several new features, including support for GPS.

March 26th, 2022

- Adjusted the default settings to reduce the amount of configuration that needs to be done for most use cases.
- Added support for customizable RGB status lighting.
- Changed the import process for Tensorflow and OpenCV to allow for failure without terminating Predator.
- Adjusted the status messages in real-time mode to more accurate represent the current processing step.
- Added the ability to export license plate GPX location data collected in pre-recorded mode.
- Added a new 'Management Mode', which allows the user to run basic system management tasks from inside the Predator interface.
    - Users can now view files in a given Predator project folder.
    - Users can copy any combination of Predator project files to any directory on the system, including an external drive.
    - Users can delete any combination of Predator project files from any project directory.
    - Users can view system information, like Predator's current configuration, the current operating system, processor specifications, RAM information, disk usage, etc.
    - Moved the Predator configuration to `config.json` in order to improve organization and extensibility.
        - The Predator configuration (`config.json` file) can now be edited directly from within Predator using a built in editing interface, or using an external text/JSON editor.
- Completely re-organized and re-structured the pre-recorded mode analysis menu in order to make the process drastically easier to understand and use.
    - The main menu is now grouped into sections for license plate data, object recognition data, location data, and statistics.
    - Tabs are used to indicate sub-menus, and to visually distinguish them from previous menus while making it easy for the user to determine where they are in the menu system.
- Added the ability to override the `auto_start_mode` configuration value using a command line argument.
    - The user can enter a number after the command used to start Predator in order to pre-select a mode that will override the `auto_start_mode` setting.
    - Examples:
        - Start into management mode: `python3 main.py 0`
        - Start into pre-recorded mode: `python3 main.py 1`
        - Start into real-time mode: `python3 main.py 2`
        - Start into dash-cam mode: `python3 main.py 3`
- Completely re-structured the dashcam recording system.
    - Multiple dashcam devices can now be used simultaneously without having to force FFMPEG to quit.
    - 'Background dashcam recording' has been removed, as it's no longer necessary.
    - Multiple camera devices can now be used during background realtime mode dashcam recording.
    - Dashcam recording can now be halted through Predator, without having to terminate Predator.
- Added several new configuration values.
    - The `realtime_output_level` setting changes how much information Predator prints to the console when operating in real-time mode.
    - The `clear_between_rounds` setting changes whether or not the output screen is cleared between rounds while running in the real-time mode loop.
    - The `delay_between_rounds` setting allows the user to define how long Predator will wait in between analysis rounds.
    - The `alerts_ignore_validation` setting allows alerts to override the license plate validation formatting guideline.
        - If a detected license plate fails the validation process, but matches a plate in the alert database, an alert can be shown anyways.
    - The `custom_startup_message` setting allows for a custom message to be shown to the user when Predator starts up.
    - The `modes_enabled` setting allows the user to individually enable and disable each of Predator's 4 modes.
    - Audio alerts are now much more configurable, and allow for custom sound effects and for each sound effect to be repeated multiple times, if desired.
    - The `real_time_image_rotation` configuration value allows the user to have Predator rotate each image it captures in real-time mode before cropping it.
        - This means that Predator now use cameras that are mounted at an angle for license plate analysis.
    - Added a configuration setting for globally disabling OpenCV and Tensorflow.
- Fixed an issue where various tasks, like push notifications, audio alerts, shape alerts, and webhooks wouldn't be completed if license plate validation was turned off.
- Changed the order in which object recognition and ALPR processing take place.
- Removed Predator's dependence on GNU AWK in order to improve stability, efficiency, and to make it easier to add features in the future.
    - Predator now uses OpenALPR's JSON option for it's back-end.
- Added the ability to detect and process multiple license per frame in real-time mode.
    - Added the `print_detected_plate_count` configuration value to allow the user to change whether or not Predator will display the count of how many license plates it detectes each round.
    - This makes Predator significantly more efficient by increasing the amount of plates that can be detected per processing cycle, without significantly increasing the time required to process each cycle.
- Added the ability to alert to nearby speed cameras, red light cameras, and other traffic cameras while operating in real-time mode.
    - Several configuration values were add to support this feature, including new sound effects.
        - New sounds: `camera1_sound`, `camera2_sound`, `camera3_sound`
	    - New configuration values: `traffic_camera_alerts_enabled`, `camera_alert_types`, `traffic_camera_alert_radius`, `traffic_camera_database`, `traffic_camera_loaded_radius` `status_lighting_values/camera`
- Adjusted the wording of some prompts to better mesh with the over all structure of the user interface.
- Predator can now interface with GPS using GPSD
    - GPS features can be toggled on and off by changing the `gps_enabled` configuration value.
- Increased the default real-time plate guesses to 20 guess per plate.



## Version 7.0

### Information Update

March 30th, 2022

This update adds 'information mode', which allows Predator to rapidly display useful information in the console output, as well as several new features to real-time mode.

- Adjusted some comments that had typos or confusing wording.
- License plate recognition can now be entirely disabled in real-time mode using the `realtime_alpr_enabled` configuration value.
    - A custom artificial delay can be (optionally) added when license plate recognition is disabled in order to prevent Predator from running through the real-time mode processing cycle unreasonably fast.
- Added the ability to display the current speed during each processing cycle in real-time mode.
    - This feature can be turned on and off in the configuration using the `speed_display_enabled` setting.
    - The current speed can be displayed in kilometers per hour, miles per hour, meters per second, feet per second, or knots.
- Moved the `gps_enabled` and `speed_display_unit` configuration values to the `general` section.
- Added 'Information' mode, which allows Predator to show customizable information displays in the console output.
    - This mode also adds several new configuration values.
        - `information_refresh_delay`
        - `displays`
            - `time`
            - `date`
            - `speed`
            - `location`
            - `altitude`
            - `track`
            - `satellites`
            - `nearest_camera`
        - `max_nearest_camera_range`
    - Information mode can also be used to record telemetry to a log file, using the `record_telemetry` configuration value.
- Added a start-up check to see if the traffic camera database file specified in the configuration actually exists.
- Added the ability to save the current location to the log of plates detected in real-time.
- Adjusted the default values for a couple settings.
- Moved the alert databases to a centralized configuration value for sake of efficiency and organization.
    - The start-up prompt asking the user to enter an alert database is no longer shown.



## Version 8.0

### Survey Update

*Release date: to be determined*

This update prefaces plans for future updates, and adds 'survey mode', which allows the user to mark the locations of various points of interest using a connected GPS.
