# To-Do

This document quickly explains features that may be added to Predator in the future. This is an informal document, and it's typically used as a simple task tracker, not as changelog or official feature list.


## Planned

These are the features actively planned for Predator and are likely to be added within the near future.

- [X] The ability to view plate data in different formats.
- [X] The ability to modify the cropping margins for frames.
- [X] The ability to natively export detected license plates to an external file.
- [X] The ability to format detected license plates as CSV.
- [X] Support for real-time license plate reading.
- [X] Support for saving real-time license plate readings to a file.
- [X] Support for saving all images taken in real-time mode to disk.
- [X] Real-time alerts for detected license plates based on a text file.
- [X] The ability to configure Predator to automatically start up in real-time mode using pre-configured preferences.
- [X] The ability to download alert databases from the internet.
- [X] Add audio based alerts.
- [X] The ability to automatically submit plates detected in real-time to a webhook.
- [X] Add statistics viewer to pre-recorded mode.
- [X] Add the ability to record video without processing plates in real-time.
- [X] The ability to correlate license plate detections with GPS data from a GPX file.
- [X] Push notification support.
- [X] Add support for using multiple recording devices in dash-cam mode.
- [X] Add basic object recognition.
- [X] Add the ability to toggle saving object recognition data to disk.
- [X] Add the ability to toggle verbose file saving data.
- [X] Move configuration from main.py to a separate files for better extensibility.
- [X] Fix Raspberry Pi AI packages.
- [X] Add support for LED status lights that indicate important Predator events discretely.
- [X] Add "Management Mode" which allows the user to execute administrative actions of Predator, like clearing root project folders.
- [X] Re-organize the pre-recorded mode menu.
- [X] Add the ability to change configuration values from nanagement mode.
- [X] Update real-time dashcam background recording.
- [X] Add more configuration values to better refine Predator's functionality.
- [X] Add the ability to configure custom alert sounds.
- [X] Add the ability for Predator to detect multiple license plates per frame in real-time mode.
- [X] The ability to interface with GPS data in order to provide new features and functionality.
- [X] Add a shape alert for traffic cameras.
- [X] Add "Information Mode" for displaying useful information through the console output.
- [X] Move alert databases to a configuration value instead of a start-up preference.
- [X] Add telemetry recording in Information Mode
- [X] Add the ability to process multiple videos sequentially in pre-recorded mode.
- [X] Add "Survey Mode", for reporting the locations of speed cameras, license plate reading cameras, and other potential points of interest.
- [X] Add GPS based notificaitons for automated license plate readers.
- [X] Redo CONFIGURATION.md to better represent the newly changed configuration values.
- [X] Test ALPR alerts.
- [X] Transition Real-time Mode license plate alert databases from plain text lists to JSON databases.
- [X] Remove speed camera and ALPR alerts (replaced by 'Assassin' to simplify Predator).
- [X] Add ignore-list support.
- [X] Add dashcam recording segmentation support.
- [X] Add Phantom ALPR support to real-time mode.
- [X] Add more resilent GPX position correlating.
- [ ] Add support for multiple plates in pre-recorded mode.
- [ ] Add more fault tolerance to user input prompt function.


# Hypothetical

These are features that may require more in-depth changes, and are purely hypothetical.

- [ ] A GUI front-end in addition to the existing command line interface.
