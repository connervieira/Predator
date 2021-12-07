# Changelog

This document contains all of the changes for each version of Predator.


## Version 0.9

### Initial release

December 4th, 2021

- Core functionality


## Version 1.0

### First stable release

December 5th, 2021

- Added a basic command line menu based user interface for managing data after analysis
- Added the ability to view and export collected data in different formats
    - Raw format
    - List format
    - CSV format
- Added the ability to view and export the raw data for license plate collection, before any validation or sanitization takes place
- Added a large ASCII title screen that displays when launching Predator


## Version 2.0

### Real-time update

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
