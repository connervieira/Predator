# Change-log

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
- Added the ability to view and export the raw data for license plate collection, before any validation or sanitation takes place
- Added a large ASCII title screen that displays when launching Predator


## Version 2.0

### Real-time Update

This update adds real-time mode to Predator, where plates can be detected on a second-by-second basis, with automatic alerts and logging.

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
- Changed the audio back-end from Python playsound to mpg321 in order to fix audio on Raspberry Pi.
- Fixed an issue where the 'separate line' wouldn't appear under detected plates in real-time mode.
- Added a hyphen to 'real-time' in the mode selection menu.



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

This update adds "management mode", and improves the efficiency and organization of various user interfaces. This update also adds new functionality and several new features, including support for GPS.

March 26th, 2022

- Adjusted the default settings to reduce the amount of configuration that needs to be done for most use cases.
- Added support for customizable RGB status lighting.
- Changed the import process for Tensorflow and OpenCV to allow for failure without terminating Predator.
- Adjusted the status messages in real-time mode to more accurate represent the current processing step.
- Added the ability to export license plate GPX location data collected in pre-recorded mode.
- Added a new 'management mode', which allows the user to run basic system management tasks from inside the Predator interface.
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
    - Multiple camera devices can now be used during background real-time mode dashcam recording.
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
- Fixed an issue where various tasks, like push notifications, audio alerts, shape alerts, and web-hooks wouldn't be completed if license plate validation was turned off.
- Changed the order in which object recognition and ALPR processing take place.
- Removed Predator's dependence on GNU AWK in order to improve stability, efficiency, and to make it easier to add features in the future.
    - Predator now uses OpenALPR's JSON option for it's back-end.
- Added the ability to detect and process multiple license per frame in real-time mode.
    - Added the `print_detected_plate_count` configuration value to allow the user to change whether or not Predator will display the count of how many license plates it detects each round.
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

This update adds "information mode", which allows Predator to rapidly display useful information in the console output, as well as several new features to real-time mode.

- Adjusted some comments that had typos or confusing wording.
- License plate recognition can now be entirely disabled in real-time mode using the `realtime_alpr_enabled` configuration value.
    - A custom artificial delay can be (optionally) added when license plate recognition is disabled in order to prevent Predator from running through the real-time mode processing cycle unreasonably fast.
- Added the ability to display the current speed during each processing cycle in real-time mode.
    - This feature can be turned on and off in the configuration using the `speed_display_enabled` setting.
    - The current speed can be displayed in kilometers per hour, miles per hour, meters per second, feet per second, or knots.
- Moved the `gps_enabled` and `speed_display_unit` configuration values to the `general` section.
- Added 'information mode', which allows Predator to show customizable information displays in the console output.
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
    - Information Mode can also be used to record telemetry to a log file, using the `record_telemetry` configuration value.
- Added a start-up check to see if the traffic camera database file specified in the configuration actually exists.
- Added the ability to save the current location to the log of plates detected in real-time.
- Adjusted the default values for a couple settings.
- Moved the alert databases to a centralized configuration value for sake of efficiency and organization.
    - The start-up prompt asking the user to enter an alert database is no longer shown.



## Version 8.0

### Simplification Update

February 15th, 2023

This update refines Predator's functionality, and focuses its purpose back on license plate and object recognition. Irrelevant features are moved to external programs that retain compatibility with Predator, but are entirely independent platforms. This update also emphasizes stability, reliability, and consistency.

- Removed 'information mode'
    - All of the functionality of information mode has been moved to a new platform, called 'Assassin' in an effort to keep Predator focused and effective.
- Added `manual_trigger` configuration value.
    - This configuration value allows for Predator to be manually trigger in real-time mode, where images are only captured when a button is pressed by the user.
- Simplified library importing process.
    - Libraries are now only imported if the configuration causes Predator to need them.
- Removed logic for traffic camera alert processing.
- Removed the `realtime_alpr_enabled` configuration option.
- Fixed a bug that could cause Predator to crash when object recognition was globally disabled in the configuration.
- Added support for 'ignore lists' which allow users and administrators to set a list of license plates that should be ignored.
- Updated the way several messages are displayed to be more concise and organized.
- Added 'offline mode', which restricts all network functions globally.
- Refined dashcam recording.
    - Dashcam recording now launches from a function, for sake of consistency and organization.
    - Dashcam recording now uses consistent file names between background and foreground mode.
    - Added dashcam video segmentation support.
- Upgraded ALPR engine
    - Added support for the Phantom ALPR engine.
    - Added a default fall-back ALPR output in the event that the ALPR process fails.
- Organized various code sections.
- Added a timeout to all network functions to improve reliability.
- Added more consistent error handling.
    - Errors messages are now handled using a function.
- Create a dedicated function for user input prompts.
    - User inputs are now much more fault tolerant, and will repeatedly prompt the user if they don't enter an expected input.
- Made various improvements to pre-recorded mode.
    - Predator now accepts wildcard file names in pre-recorded mode.
    - Fixed an issue where selecting the object recognition menu in pre-recorded mode would give an unexpected error when object recognition was disabled.
    - Updated the pre-recorded mode post-processing menu.
        - CSV data display in the menu no longer has a trailing comma.
        - Renamed the "raw data" option to "JSON data" through-out the menu.
        - Renamed the "GPS data" option to "position data".
        - Options that are disabled now appear in a darker style.
    - License plates detected in pre-recorded mode can now be correlated to nearby GPX points, even if they don't match timestamps exactly.
    - Multiple license plates can now be detected per frame.
        - This change indirectly fixed an issue where fractional frame intervals could cause crashes.
    - The license plate validation process is now exponentially more efficient.
    - Pre-recorded mode now respects the `default_license_plate_format` configuration value.
        - Moved the `default_license_plate_format` configuration value to the 'general' section.
    - Pre-recorded mode now supports alerts.
        - The `alerts_ignore_validation` configuration value has been moved to the 'general' section.
- Dramatically improved alert handling.
    - Alerts detected in real-time mode are now recorded to a dictionary every round, which makes processing and handling alerts more efficient and organized.
    - Alerts are now handled on a plate-by-plate basis, instead of frame-by-frame.
        - This means only the plates that match alert rules will be marked as alerts in web-hook submissions, logs, and similar context.
        - When the `alerts_ignore_validation` configuration value is enabled, a single rule matching multiple guesses for a particular plate will only be considered one alert.
            - This prevents an alert with wildcards from repeatedly triggering for every similar guess.
            - Separate rules and separate plates will still trigger multiple alerts.
    - Added `delay_on_alert` configuration value, which allows for an additional delay to be triggered when a heightened alert is displayed in real-time mode.
    - Removed support for plain text license plate alert databases.
        - This dramatically simplifies the license plate alert database loading process, so the function to download remote alert databases was removed and replaced with a complete database loading function.
    - Multiple alert databases can now be specified.
- Improved sound playing process.
    - Sounds are now played with a function for sake of reliability and organization.
- Updated the configuration manager in management mode.
    - Lists can now be edited.
    - The back-end structure is more organized and simplified.
    - The configuration interface can now detect when an unrecognized configuration value is entered.
- Added a check during loading to verify that the configuration file exists, and is valid.



## Version 9.0

### Performance Update

October 26th, 2023

This update makes several changes to Predator that dramatically improve its processing performance and stability.

- Removed web-hook functionality, since this functionality is being replaced by Predator Fabric.
- Dramatically changed the configuration layout.
    - Configuration values are now much more organized.
    - Configuration values are now referenced directly through-out the program, rather than all being assigned to variables at start-up.
    - Removed the `detected_plate_count` configuration value from the real-time display section.
        - The number of plates detected is now always displayed in the console output.
    - Dramatically changed 'preferences' system.
        - Real-time mode and dash-cam mode no longer have run-time preferences, and only consider configuration values.
        - Management mode and pre-recorded mode have modified run-time preferences, and place more emphasis on configuration values.
    - Added several configuration values.
        - Added `developer>kill_plate` configuration option.
            - This option sets a plate that will cause Predator to immediately exit for debugging purposes.
        - Added `general>alerts>allow_duplicate_alerts` configuration option.
        - Added `general>alpr>validation>confidence` configuration value to set a minimum required confidence level for ALPR results.
        - The configuration value to globally disable object recognition has been removed, and replaced with a single control that enables object recognition.
- The normal delay and alert delay are now mutually exclusive, and only one is triggered each round, depending on whether there are one or more active alerts.
- Timestamp input parsing in pre-recorded mode is now more fault tolerant.
- Added support for interfacing with external local services.
- Improved dashcam recording.
    - Fixed an issue where dashcam recording would cause a crash when displaying the process start message.
    - Added support for OpenCV recording alongside the existing FFMPEG back-end.
        - OpenCV dashcam recording supports overlay stamps for the current time, location, speed, altitude, and other data.
- Added support for multiple license plate validation formats.
- Overhauled real-time mode.
    - Entries are now only added to the license plate history log file if one or more license plates were detected.
    - Real-time mode now streams constant video from the configured camera, rather than capturing discrete still frames.
        - This dramatically improves the likelihood of plate detection, especially under challenging conditions.
    - Real-time mode now supports multiple video capture devices at once.
    - Removed some features to accommodate the new ALPR back-end.
        - Removed image post-processing.
        - Removed image saving.
    - Refined the real-time mode interface to better accommodate multiple plates being displayed at once.
    - License plate analysis now takes place in a separate thread from the rest of the Predator.
    - The license plate log file is now a JSON file, and contains more information than before, including license plate guesses.
- Re-implemented object recognition to support updated ALPR processing back-end.
    - Re-organized the real-time object recognition configuration section.
        - A custom file name for logging detected objects can now be configured.
- Added multi-threaded debug message support.
- Expanded management mode capabilities to allow for setting deeper nested configuration values.
- Slightly modified the start-up title.



## Version 10.0

### Dashcam Update 2

March 4th, 2024

This update overhauls Predator's dashcam functionality and adds various features to allow it to be used a fully-featured dedicated dashcam.

- Refined OpenCV dashcam recording.
    - Improved video overlay stamps.
        - Added the ability to set the units for speed in the OpenCV GPS dashcam video overlay stamp.
        - Made the font color of the video overlay stamps configurable.
        - Made the font size configurable.
        - The GPS coordinates are now always displayed to 5 decimal points for sake of consistency.
    - Improved dashcam video file saving.
        - Added customizable video segmentation.
        - Added dashcam video segment saving.
            - Dashcam video saving can be triggered to copy the current and last video segment to a different location on disk.
            - At the moment the save is trigger, both the previous segment, and current segment are saved. Once the current segment is completed, the updated file is saved again.
        - OpenCV dashcam segments now include the name of the capture device, rather than the ID number.
        - Added support for looped video recording, where older unsaved dashcam segments are erased to make space for new ones.
        - Dashcam video file names now end with either an "N" or "P" to indicate "normal" or "parked" mode respectively.
    - Improved the way frame-rate is handled in OpenCV recording.
        - The frame-rate configuration value has been removed in favor of calculating FPS on the fly.
            - The frame-rate of each capture device is individually benchmarked when dashcam recording starts, and is re-calculated at the start of every subsequent segment.
        - Simplified the OpenCV FPS benchmark tool.
            - The script has been re-named to `framerate_benchmark.py` for clarity.
            - The script now uses the information from `config.json`, instead of being configured by manually changing variables at the top of the script.
            - The script is now able to benchmark multiple cameras in one run.
    - Added parking-mode functionality.
        - Predator can be configured to enter into parking mode when the vehicle has been stopped for a certain period of time.
        - Predator will resume recording temporarily when motion is detected.
            - Added a new tool (`motion_detect_test.py`) to test motion detection settings.
        - Added offline push notifications to dash-cam mode via Reticulum LXMF.
    - Added audio recording.
        - Predator can now record audio along side dashcam video, and merge them into a single file when each segment completes.
    - Moved the dashcam recording system to a separate script for sake of organization.
        - Removed the FFMPEG recording back-end for stability and simplicity.
    - Added a configuration option to flip the video output individual dash-cam capture devices to support more camera mounting possibilities.
    - Switched to MJPEG codec for improved resolution and frame-rate.
        - Predator now sets the intended OpenCV video capture frame-rate to an arbitrarily high value in order to request the fastest frame-rate option.
- The ALPR stream library is now only imported if real-time mode is enabled in the configuration.
- Fixed a typo in a debug message inside `alpr_stream_maintainer()`.
- Improved debug message handling when multiple threads are running concurrently.
- Added a configuration value to disable the logging of all license plate guesses alongside the top guess.
- Fixed some broken references to configuration values.
- Updated the way errors and warnings are saved in the interface directory.
    - Both errors and warnings are now logged to the error log file in the interface directory, instead of just errors.
- Fixed an issue where information displayed in management mode would not wait for user input before clearing the screen.
- Prompts that ask the user to press enter to continue are now displayed in a faint font.
- Made the 'plates detected' count display in real-time mode more consistent.
- Added additional configuration error checking.
- The option to view files in the working directory in management mode now shows all files, including those inside sub-directories.
- Created a dedicated function to wait for user input before continuing.
- Removed the the `general>display>silence_file_saving` configuration value.
    - File saving is now always silenced unless an error is encountered.
- The heartbeat log file is now only updated once every 0.25 seconds, even if a heartbeat issue call is made faster than that.
    - This prevents the heartbeat log file from being written to disk every frame during dashcam recording.
- Refined the debug message system.
    - Thread names are now automatically determined and assignment when debug messages are displayed.
- Fixed speed display in real-time mode.
- Improved GPS integration.
    - 2D position information can now be displayed even when a 3D fix has not been aquired yet.
    - Predator now only opens a single GPS connection, instead of repeatedly opening and closing a connection every time the GPS is queried.
    - Predator can now be configured to replay a GPX file to simulate GPS data for sake of demonstration and testing.
    - Updated the time handling back-end to allow for custom time offsets.
        - Predator can automatically apply an offset to the current time if the system time drifts from the GPS time.
- Improved configuration validation.
- Added `state.json` interface file to communicate Predator's current mode of operation to external programs.
- Added headless operation mode, where all user input prompts are skipped.


## Version 10.0.1

March 6th, 2024

- Fixed a bug where the audio file name wouldn't be properly updated when a new dash-cam video segment starts.
- Warnings now wait for user input before continuing, just like errors.


## Version 11.0

### Refinement Update

This update emphasizes improving the reliability of Predator, especially when operating in dash-cam mode. This update also expands the functionality of dash-cam mode to allow simultaneous dash-cam recording and ALPR analysis.

November 4th, 2024

- Added more descriptive error messages when the interface directory fails to be created.
- Added performance monitoring to state interface file to allow external programs to see basic performance diagnostics.
- Updated the way automatic GPS time correction is handled.
    - Predator will no longer try to apply a time offset when the system time is in the future relative to the GPS time.
    - Predator no longer displays warnings about the time being desynced when GPS time correction is disabled.
    - Predator will now reset the time offset if the system time changes (i.e. the system connects to the internet and refreshes the time).
- Updated dash-cam mode.
    - Added customizable frame-rate restrictions.
        - Added a per-device configuration value to set a maximum allowed frame-rate. When this frame-rate is exceeded, Predator will throttle dash-cam recording to stay below the limit.
            - A threshold can be set to allow Predator to round up to the maximum framerate if it is within a small difference.
                - This means that minor fluctations in frame-rate will not cause the frame-rate to change from file to file.
                - For example, a frame-rate of 29.85 FPS can be configured to round up to 30 FPS because it is within 0.15 FPS
        - Added a per-device configuration to set a minimum expected frame-rate, below which a warning is displayed. This value does not have any impact on the actual recording frame-rate.
    - Overhauled dash-cam saving.
        - Frames captured during dash-cam recording are now saved in a separate thread.
        - The video file extension and codec are now both configurable.
        - Predator now gracefully closes the file writing process when terminated.
    - Improved the reliability of dash-cam operation.
        - The file saving back-end now handles sudden time jumps into the future much more reliably.
            - Instead of creating each segment between the original time and new time, Predator skips directly to the next segment.
        - Predator will now attempt to resume recording if the video capture drops on a particular device.
            - The delay between attempts will increase progressively with each try.
        - A failure on a single capture device will no longer kill recording on other capture devices.
        - Predator now shows a warning instead of an error when the merged audio/video file is missing at the end of a saved segment.
            - This occurs when the audio recording process fails, and doesn't necessarily mean that the video capture has encountered a fatal problem.
    - Updated dash-cam overlay stamps.
        - Added more dash-cam stamp options.
            - Added diagnostic stamp, which is capable of displaying various pieces of technical information.
                - Added a frame-rate stamp, which shows the instantaneous frame-rate.
                - Added a state stamp, which shows Predator's current operating mode.
            - Added support for GPIO-based relay stamps.
                - Predator can display custom stamps that change color based on the state of a GPIO pin. This allows for vehicle integrated overlay stamps, such has the horn, warning lights, or brakes.
        - Improved the GPS overlay stamp.
            - The GPS query now uses a "lazy" method, which trades data recency for response time.
                - This significantly improves frame-rate by reducing the time Predator spends waiting for a GPS response.
    - Updated audio recording.
        - Improved the reliability of audio recording.
        - Fixed unexpected behavior when the working directory path contained spaces.
        - Added configuration options for audio recording.
            - Added configuration option to use a different audio recording device.
            - Added configuration option to determine which user on the system will be used to run the audio recording process.
            - Added configuration option to set the format used by the recording device.
            - Added configuration option to slightly delay the start of audio recording to prevent the capture device from being opened by two threads at once.
    - Added per-device resolution configuration.
    - Added the ability to disable capture devices in the configuration without removing them from the configuration entirely.
    - Predator now changes the status light color when a video is being locked.
    - Dashcam video save events can now be triggered using buttons via GPIO pins.
    - Improved looped recording.
        - Each thread now checks to see if old segments have already been deleted before deleting them themselves.
    - Added optional background ALPR to dash-cam mode.
        - The user can now configure Predator to conduct ALPR in the background while simultaneously capturing video.
        - Removed the old "background recording" functionality in real-time mode, and it's corresponding configuration value.
    - Improved the dashcam output handler.
        - Fixed a bug where Predator would initialize new video segments twice.
        - The output handler will now finish writing the list of frames to write before exiting when Predator is closed, then release the output gracefully.
- Updated status lighting.
    - Moved the status lighting configuration to the "general" section.
    - Network requests are only made to update the status lighting if it has changed since the last update.
        - This means that the status lighting can be turned off, and it will only turn back on when an update is made.
    - Changed the default `dashcam_save` status light color to blue, to avoid confusion with `alpr_alert`.
- Updated configuration back-end.
    - Predator can now automatically update the configuration file between versions when configuration values are added or removed.
    - Added comprehensive configuration validation.
        - Predator now checks to see if each value in the configuration matches the expected data type.
    - Improved the consistency of the configuration file location when starting Predator from an external source, like Assassin.
- Added an initial start-up sequence, where Predator shows some basic information before the normal start-up.
    - Predator now creates a file named `install.json` containing some basic install information on the first start-up.
- Updated the ALPR handler.
    - Updated how license plate hot-lists are loaded.
        - Predator now saves the complete loaded alert database (all loaded databases combined) to the `hotlist.json` file in the interface directory.
        - Remote alert database sources can now be cached.
            - This allows Predator to continue using entries from a remote alert database even when the source goes offline.
    - Migrated most of the ALPR processing logic to a dedicated file for sake of organization.
- Updated real-time mode.
    - The "detected plate" notification sound now plays regardless of the console output level.
    - Audio alerts in real-time mode are now played at the end of the processing cycle.
        - Previously, interface updates would have to wait for the audio alerts to finish playing.
- Updated pre-recorded mode.
    - Improved how Predator handles comma-separated video file names.
        - Video file names now have any trailing or leading whitespace removed after separation.
    - Added support for "side-car" mode, where Predator will generate files containing ALPR information for videos that were captured previously using dash-cam mode.
- Improved how Predator exits.
    - Fixed the "Quit" options in pre-recorded and management mode.
        - Previously, the time offset manager thread would keep Predator alive after using the "Quit" option.
    - All threads now watch a global variable, and will exit when it is changed.
        - This means the user can simply press Ctrl+C once, and all threads will clean up and exit.
- Updated sound effects.
    - Removed unused sound files.
    - Replaced the default start-up sound.
