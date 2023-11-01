# Configuration

This document describes the configuration values found `config.json`.


## General Configuration

This section of configuration values will effect Predator's general operation.

- `working_directory` specifies the default directory that Predator will use for projects.
    - This value can be over-ridden using command line arguments.
    - In management mode and pre-recorded mode, this value serves as a default, but can be over-ridden by user input.
    - In real-time mode and dash-cam mode, this value will be automatically used without user input.
- `interface_directory` specifies the directory that predator will store files used to share real-time information with external programs.
    - This value is only used in real-time mode.
    - Setting this to a blank string will disable the interface directory.
- `alpr` contains settings related to license plate recognition.
    - `engine` is a string that determines what ALPR engine Predator will use.
        - This can be set to either `"openalpr"` or `"phantom"`.
    - `validation` contains settings for validating license plate candidates/guesses.
        - `guesses` is an integer that determines how many guesses the ALPR engine will make when analyzing a plate.
            - The higher this number is, the more likely Predator is to guess a plate incorrectly. The lower this number is, the less likely Predator will be to find a valid guess at all.
        - `confidence` is a number that determines the minimum confidence a license plate guess needs to have before Predator will consider it valid, where 100 is extremely confidence and 0 is a complete lack of confidence.
            - This value is only considered in real-time mode, and is ignored in pre-recorded mode.
            - This value is ignored by alerts when `general>alerts>alerts_ignore_validation` is enabled.
        - `license_plate_format` is a list of strings that provide Predator with examples of how license plates in your region should be formatted.
            - For example, license plates in the state of Ohio generally follow the pattern of 3 letters followed by 4 numbers. In Ohio, this preference might contain `"AAA0000"` to filter out plate guesses that don't match the most common formatting pattern.
            - This preference only considers the type of each character, not the character itself.
                - In other words, `AAA0000` and `ABC1234` will function identically.
                - This also means you can simply enter any given plate from a car located in the region you're scanning in to have a reasonably good chance at matching your region's formatting guidelines for license plates.
            - Leaving this as an empty list (a list with a length of 0) will disable license plate format validation.
        - `best_effort` is a boolean that determines whether Predator will accept the most confident guess when none of the guesses are considered valid by the validation rules.
            - This setting can override both the license plate validation format, as well as the minimum confidence threshold.
            - When set to `false`, Predator will discard plates that don't have any valid guesses.
            - This setting does not override `general>alerts>alerts_ignore_validation`, and can be set to `false` without interferring with license plate hotlist alerts.
- `alerts` contains settings related to license plate alerting.
    - `alerts_ignore_validation` is a boolean that determines whether alerts will respect or ignore the plate validation format.
        - When this is set to `true`, if a plate fails the validation test, but matches an alert database plate, the alert will be displayed anyway.
        - When set to `false`, only plates that have passed the validation test will be checked against the alert database.
    - `allow_duplicate_alerts` is a boolean that determines whether a single license plate can trigger multiple alert rules.
        - Setting this to `true` will cause Predator to check all guesses against all alert rules. This can lead to situations where alert rules with wildcards cause a single license plate to alert repeatedly, for each of its guesses.
    - `databases` is a list that contains strings, with each string pointing to either a local or remote license plate hot-list.
        - If a particular entry in this list is a file, the file path should be relative to the working directory.
            - For example, if your alert database is in `/home/pi/Data/alerts.json`, and your root project directory is `/home/pi/Data/`, then then the alert database value should simply be set to `"alerts.json"`, not the the full file path.
        - If a particular entry in this list is a remote source, the remote source should be a complete URL.
            - For example, an entry might be set to `"https://website.tld/alerts.json"`.
- `display` contains settings related to what is displayed in the command line interface.
    - `ascii_art_header` is a boolean that determines whether or not Predator will display a large ASCII art banner on start up.
        - When set to `false`, the ASCII art banner will be replaced with a small, normal text title.
        - This setting may be useful to change in the event that Predator is being run on a device with a tiny display, where a large ASCII art header might cause formatting issues.
    - `startup_message` is a string used to set a custom start-up message that displays after the initial Predator start-up header.
    - `silence_file_saving` is a boolean that determines whether or not Predator will display informational messages when saving files.
    - `debugging_output` is a boolean that determines whether or not Predator will display debugging messages through-out normal operation.
        - When this is set to `true`, console clearing is automatically disabled.
- `object_recognition` contains settings related to Predator's object recogntion capabilities.
    - `enabled` is a boolean that determines whether or not object recognition is enabled globally.
        - Setting this to `false` removes Predator's dependency on Tensorflow and OpenCV.
- `modes` contains settings related to Predator's operating modes.
    - `auto_start` is a string that determines which mode (if any) Predator will automatically load into upon start-up.
        - There are 4 possible values this can be set to, not including being left blank.
            - When set to an empty string, Predator will prompt the user to select a mode each time it starts. This is the default.
            - When set to `"0"`, Predator will skip the 'mode' prompt, and automatically boot into management mode.
            - When set to `"1"`, Predator will skip the 'mode' prompt, and automatically boot into pre-recorded mode.
            - When set to `"2"`, Predator will skip the 'mode' prompt, and automatically boot into real-time mode.
            - When set to `"3"`, Predator will skip the 'mode' prompt, and automatically boot into dash-cam mode.
    - `enabled` contains controls to enable and disable each operation mode of Predator.
        - When the value for a particular mode is set to `false`, that mode's option will be hidden from the mode selection menu shown to the user when Predator starts, and the auto-start-mode command line arguments won't allow the user to boot Predator directly to that mode.
        - Under normal circumstances, all of these settings should be left as 'true', in order to enable full functionality of Predator, but there may be certain situations in which is useful to block certain modes from starting.
            - This setting is not intended to a be a security feature. It's completely trivial to bypass this setting by simply modifying the configuration file directly.


## Management Mode Configuration

Configuration values in this section are settings specific to management mode.

- `disk_statistics` is a boolean that enables and disables the disk statistics feature of management mode.
    - Setting this to `false` disables disk statistics, and eliminates the need for the 'psutil' Python package to be installed.



## Pre-recorded Mode Configuration

Configuration values in this section are settings specific to pre-recorded mode.

- `image` contains settings related to image handling.
    - `processing` contains settings related to image processing.
        - `cropping` contains settings regarding image cropping.
            - `enabled` determines whether image cropping is enabled in pre-recorded mode.
            - `left_margin` determines how many pixels will be cropped off of the left side of the frame.
            - `right_margin` determines how many pixels will be cropped off of the right side of the frame.
            - `top_margin` determines how many pixels will be cropped off of the top of the frame.
            - `bottom_margin` determines how many pixels will be cropped off of the bottom of the frame.
- `max_gpx_time_difference`
    - This value is a number that determines the maximum time, in seconds, between the timestamp of a video frame and an entry in the corresponding GPX file, before they are considered to be different.
    - Setting this to lower values will force locations to be more accurate, but will increase the likelihood that no corresponding location is found for a given frame.


## Real-time Mode Configuration

Configuration values in this section are settings specific to real-time mode.

- `interface` contains settings related to the command line interface.
    - `display` contains settings related to what information is displayed.
        - `show_validation` is a boolean that determines whether or not Predator will print every guess it makes as to the contents of a license plates until it reaches a valid guess.
            - This setting doesn't change anything practically, but makes it easier to understand how Predator is filtering invalid license plate guesses.
        - `shape_alerts` is a boolean that determines whether or not large ASCII shapes will be printed to the console to indicate certain important events at a glance.
        - `output_level` is an integer that determines how verbose Predator's console output will be.
            - This setting only has 3 different options.
                - Level "1": Only alerts are displayed.
                - Level "2": Only detections and other important events are displayed.
                - Level "3": All messages are displayed.
        - `speed_display` contains settings related to displaying the current GPS speed. These settings are only applicable when the `realtime>gps>enabled` setting is set to `true`.
            - `enabled` is a boolean value that determines whether Predator will display the current speed at the beginning of each processing round.
            - `unit` determines the unit of measurement that Predator will display the current speed in. This can only be set to one of the following values:
                - `"mph"` for miles-per-hour
                - `"kph"` for kilometers-per-hour
                - `"mps"` for meters-per-second
                - `"fps"` for feet-per-second
                - `"knot"` for knots
    - `behavior` contains settings related to how information is displayed.
        - `delays` contains values related to delays between processing rounds.
            - `alert` is a decimal number that determines how long Predator will delay before starting the next round when there is an active alert.
            - `normal` is a decimal number that determines how long Predator will delay before starting the next round under normal circumstances.
        - `clearing` is a boolean that determines whether or not Predator will clear the output screen between analysis rounds during real-time mode.
- `object_recognition` contains settings related to object recognition in real-time mode.
    - `enabled` is a boolean value that enables and disables object recognition in real-time mode.
        - This setting does not override the `general>object_recognition>enabled` setting.
    - `video_still_path` is an absolute file-path to the image Predator should run object recognition on.
        - By default, Phantom stores video stills from the capture device stream to `/dev/shm/phantom-webcam.jpg`, so that is where this setting should point to in most cases.
- `gps` contains settings related to GPS-based features.
    - `enabled` is a boolean determines whether GPS features are enabled or disabled.
    - `alpr_location_tagging` is a boolean that determines whether or not the current GPS location will be saved to the log file each time a plate is logged.
- `image` contains settings related to image handling.
    - `camera` contains settings related to image capture.
        - `device` specifies the camera device that will be used to capture images.
            - Example: `"/dev/video0"`
- `sounds` contains the sound effects that Predator can play when certain events occur.
    - Each entry in this section has 3 attributes.
        - The `path` value should be set to the file path of the audio file you want to play.
        - The `repeat` value should be set to how many times you want the sound effect to be repeated.
            - To disable a sound from playing, set this to 0.
            - Under normal circumstances, this value should just be "1", but there might be some cases in which you want to play a particular sound repeatedly.
        - The `delay` value determines how long Predator will wait, in seconds, between repetitions, if `reptition` is set to more than 1.
            - Note that this delay includes the time it takes for the previous instances of the sound effect to play.
            - For example, if the audio clip you're repeating takes 2 seconds to play, and you want a 1 second delay between audio clips, this setting should be 3 seconds.
            - If the delay is set to zero, then all of the repetitions will play over top of each-other.
    - Each entry in this section corresponds to a sound effect.
        - `startup_sound` is the sound played just after Predator finishes loading.
        - `notification_sound` is the sound played when a valid plate is detected in real-time mode, and the plate is not in an alert database.
        - `alert_sound` is the sound played when a valid plate is detected, and the plate is in an alert database.
- `saving` contains settings related to information logging while operating in real-time mode.
    - `license_plates` contains settings related to saving detected license plates.
        - `enabled` is a boolean value that determines whether license plate saving is enabled.
        - `file` is a string that determines the JSON file name Predator will use to save the license plates it detects in real-time mode.
            - This file is created in the working directory.
            - Example: `"plate_history.json"`
        - `save_guesses` determines whether or not Predator will save all guesses for each license plate to the license plate log file.
            - When set to `false`, only the top guess will be logged. All other guesses will not be saved.
    - `object_recognition` contains settings related to saving detected objects.
        - `enabled` is a boolean value that determines whether object recognition saving is enabled.
        - `file` is a string that determines the CSV file name Predator will use to save the objects it detects in real-time mode.
            - This file is created in the working directory.
            - Example: `"object_recognition_log.csv"`
- `push_notifications` contains settings related to Gotify push notifications.
    - `enabled` is a boolean value that determines whether push notifications are enabled.
    - `server` is a string that specifies the Gotify server that Predator will attempt to use. It should include the protocol and port number.
        - Example: `"http://server.tld:8032"`
    - `token` is a string that specifies the Gotify application token that Predator will attempt to use to send notifications through the specified Gotify server.
        - Example: `"AJrhgGs83mL22kZ"`
- `status_lighting` contains settings for configuring Predator's status light interfacing capabilities.
    - `status_lighting_enabled` is a boolean value that determines whether or not Predator will attempt to make use of LED status lights
    - `status_lighting_base_url`
        - This is the base part of the URL that Predator will send requests to in order to update the status lighting.
        - By default, this setting is set to the default router IP address of the "WLED" lighting controller software. However, you should be able to modify it to fit any lighting controller software that supports GET network requests.
        - This is that value that precedes the `status_lighting_values` entries explained below.
    - `status_lighting_values`
        - These are individual values that will be appended to the `status_lighting_base_url` setting described above in order to form the URL that Predator will send a request to.
        - This is where you specify what RGB colors Predator will use for each status indication.
            - The "alert" status is used when Predator detects a license plate in an alert database.
            - The "notice" status is used when Predator detects any valid license plate.
            - The "normal" status is used when Predator is running, and hasn't detected any license plates in the past processing cycle.



## Dash-cam Mode Configuration

- `saving` contains settings related to "locking" dashcam video during important events.
    - `directory` is a string that sets the name of the directory where Predator will store locked dashcam video segments.
        - This directory is placed into the working directory.
        - Example: `"saved_dashcam_video"`
    - `trigger` is the name of a file inside the interface directory that will trigger Predator to save the current dashcam segment.
        - To trigger a save, create this file in the interface directory. Predator will save the video and remove the trigger file.
- `capture` contains settings related to the capturing of dashcam video.
    - `provider` determines which video back-end Predator will use. This can only be set to `"ffmpeg"` or `"opencv"`.
    - `opencv` contains settings that control how the OpenCV back-end records video. These settings are only considered when the `provider` value is set to "opencv".
        - `resolution` sets the resolution of the video.
            - `width` sets the width of the video, measured in pixels.
            - `height` sets the height of the video, measured in pixels.
        - `framerate` is a decimal number determines the playback frame-rate of the video file.
            - This value does not determine the frame-rate of video capture, but rather the frame-rate that the saved video file will play back at.
            - To estimate the frame-rate of your capture device, use the `tools/opencv_capture_benchmark.py` script.
                - This script can be configured using the variables on the first few lines of the file.
                - Run the script and wait several seconds for the benchmark to complete. The calculated frame-rate will be printed at the end of the test.
        - `segment_length` is a number that sets how many seconds long each video segment will be before another segment is created.
        - `devices` is a list that contains the indexes of camera devices Predator will attempt to use when recording video in dash-cam mode.
            - Each entry under this setting should contain a device identifier/name, as well as a reference to the device itself.
            - Examples:
                - `"main_camera": 0`
                - `"secondary_camera": 1`
        - `stamps` contains several configurable stamps that can be overlayed on the video recording.
            - `main`
                - `color` is a list of three values between 0 and 255 that determines the font cover of the overlay stamp.
                    - The first value represents red, the second value represents green, and the third value represents blue.
                - `unix_time` contains settings for configuring Predator showing the number of seconds since the Unix epoch in the video overlay stamp.
                    - `enabled` is a boolean value that determines whether the Unix timestamp will be displayed at all.
                - `date` contains settings for configuring the date video overlay stamp.
                    - `enabled` is a boolean value that determines whether Predator will show the current date in the video overlay stamp.
                - `time` contains settings for configuring the time video overlay stamp.
                    - `enabled` is a boolean value that determines whether Predator will show the current time in the video overlay stamp.
                - `message_1` is a string that is intended to display a short custom message. This is often set to the license plate of the car Predator is installed in.
                - `message_2` is a string that is intended to display a short custom message. This is often set to "Predator", or another name identifying the system the dashcam is running on.
            - `gps`
                - `color` is a list of three values between 0 and 255 that determines the font cover of the overlay stamp.
                    - The first value represents red, the second value represents green, and the third value represents blue.
                - `location` contains settings for configuring the GPS coordinate overlay stamp.
                    - `enabled` is a boolean value that determines whether Predator will include the current location in the GPS overlay stamp.
                - `altitude` contains settings for configuring the GPS altitude overlay stamp.
                    - `enabled` is a boolean value that determines whether Predator will include the current altitude in the GPS overlay stamp.
                - `speed` contains settings for configuring the GPS speed overlay stamp.
                    - `enabled` is a boolean value that determines whether Predator will include the current speed in the GPS overlay stamp.
                    - `unit` is a string that determines what unit of speed Predator will use for the speed overlay stamp.
                        - This value can only be set to one of the following values:
                            - `"mph"` for miles-per-hour
                            - `"kph"` for kilometers-per-hour
                            - `"mps"` for meters-per-second
                            - `"fps"` for feet-per-second
                            - `"knot"` for knots
    - `ffmpeg` contains settings that control how the FFMPEG back-end records video. These settings are only considered when the `provider` value is set to "ffmpeg".
        - `resolution` is a string that determines what resolution Predator will attmpt to record at, and takes the form of `"[width]x[height]"`
            - Be sure that your camera is capable of recording at resolution specified here. If you set an unsupported resolution, it's likely Predator will fail and not record anything.
            - Example: `"1920x1080"`
        - `frame_rate` is an integer that determines what frame-rate the dashcam will attempt to record at.
            - Be sure that your camera is capable of recording at the frame rate specified here. If you set an unsupported frame rate, it's likely Predator will fail and not record anything.
            - If you enter a frame rate too slow for the encoder, it might automatically be sped to a higher frame rate.
            - Example: `30`
        - `segment_length` is an integer that determines the length of each dashcam video clip before a new segment is created, measured in seconds.
            - It should be noted that video segments are not guaranteed to exactly match the length set here.
            - When this value is set to `0`, recordings will not be separated into segments.
        - `devices` is a list that contains the camera devices Predator will attempt to use when recording video in dash-cam mode.
            - Each entry under this setting should contain a device identifier/name, as well as a reference to the device itself.
            - Examples:
                - `"main_camera": "/dev/video0"`
                - `"secondary_camera": "/dev/video1"`
            - The device name will be appended to any video file names in order to give the user a quick indication of which camera recorded each file.
            - Note: While you can specify an infinite number of cameras here, be aware that Predator might not be able to record with all of them. Bottlenecks like processor speed, RAM, and USB controller capabilities can cause issues with high numbers of cameras. Be sure to test your configuration before you start using it formally.
- `background_recording` is a boolean that determines whether dashcam video will be recorded in the background while using real-time mode.
    - Note that Predator can only use each recording device for one task at a time, so if you run real-time mode with background recording enabled, you'll need to specify two different devices by changing `image>capture>device` and `dashcam>devices`.





## Developer Configuration

- `ignore_list` contains settings for configuring a list of license plates that Predator will ignore.
    - `enabled` is a boolean that determines whether custom ignore lists are enabled or disabled.
        - This does not disable any hard-coded remote ignore lists services that may be in place from the system administrator. To completely disable remote ignore lists, set the `offline` configuration value to `true`.
    - `local_file` is a string that specifies the absolute path to a local file to be used as an ignore list.
        - If you don't want to use a local ignore list file, this value can be left blank to disable it.
    - `remote_sources`
        - This setting defines a list of custom remote hosts that Predator will attempt to fetch ignore lists from.
        - These sources will be disabled if the `offline` developer configuration value is enabled.
- `offline` is a boolean that controls whether Predator is forced to run offline. When set to true, all network functions are disabled, even if Predator is connected to the internet.
    - To be clear, this setting does not need to be changed if you want to run Predator offline. If no internet connection is available, Predator will automatically adjust accordingly.
    - Enabling this will break any functionality that depends on network features, even LAN based features that don't require an internet connection. Notably, push notifications and status lighting will be disabled.
- `kill_plate` is a string that specifies a plate that will cause Predator to immediately exit, when detected.
    - This can be used for debugging purposes, when Predator is hard-installed, and the hardware can't easily be accessed.
    - During normal circumstances, this should be set to a a blank string in order to disable the kill plate feature.
