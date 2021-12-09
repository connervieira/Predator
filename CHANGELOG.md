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
