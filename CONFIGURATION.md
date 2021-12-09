# Configuration

This document describes the configuration values found at the top of the `main.py` script in-depth.


## General Configuration

This section of configuration values will effect Predator's general operation.

- `crop_script_path`
    - This value is a string that points to the crop\_image script's exact file path. This script is typically located in the Predator folder.
    - Set this variable to an absolute file path pointing to the crop\_image script.
    - Example:
        - `/home/user/Predator/crop_image`
- `ascii_art_header`
    - This value is a boolean that determines whether or not Predator will display a large ASCII art banner on start up. When set to `False`, the ASCII art banner will be replaced with a small, normal text title.
    - This setting may be useful to change in the event that Predator is being run on a device with a tiny display, where a large ASCII art header might cause formatting issues.
- `auto_start_mode`
    - This setting is a string determines which mode (if any) that Predator will automatically load into when being started.
    - There are 3 possible values this can be set to.
        - When set to an empty string, Predator will prompt the user to select a mode each time it starts. This is the default.
        - When set to "1", Predator will skip the 'mode' prompt, and automatically boot into pre-recorded mode.
        - When set to "2", Predator will skip the 'mode' prompt, and automatically boot into real-time mode.
    - It may be useful to change this setting in several different situations:
        - If you only ever use the same mode when using Predator, setting this to your preferred mode can save time.
        - When installing Predator in a vehicle, this setting can allow Predator to load without any user input.
            - See the "default" settings later in this document for more information on auto-starting.


## Pre-recorded Mode Configuration

Configuration values in this section are settings specific to pre-recorded mode.

- `left_margin`, `right_margin`, `top_margin`, `bottom_margin`
    - This value determines how many pixels will be cropped from each side of each frame in pre-recorded mode.
    - This value should be specified as tight as reasonably possible to make Predator as accurate as it can be.
    - In most videos there will be a portion of the frame in which a license plate would never reasonably appear.
        - For example, in dash-cam video, there will rarely be a license plate in the top half of the frame when the camera is mounted facing straight forward.


## Real-time Mode Configuration

Configuration values in this section are settings specific to real-time mode.

- `print_invalid_plates`
    - This setting is a boolean that determines whether or not Predator will print every guess it makes as to the contents of a license plates, even if those guesses are invalidated by the license plate format sample.
    - This setting is usually set to False, but there may be some situations in which it would make sense to turn it on for sake of troubleshooting.
        - In the event that you consistently get Predator to identify a plate, but it can't find a valid guess as to what its contents are, turning this on can help you figure out what Predator thinks its seeing.
- `realtime_guesses`
    - This setting is a number in the form of a string that determines how many OpenALPR guesses Predator will take into account when analyzing a plate.
    - The higher this number is, the more likely Predator is to guess a plate incorrectly. The lower this number is, the less likely Predator will be to find a valid guess at all.
    - By default this value is set to 10, which tends to be a healthy balance for the majority of tasks.
- `camera_resoultion`
    - This setting is a string defines the resolution that FSWebcam will use when taking images through the connected camera.
    - It takes the format of `width x height`, with no spaces.
    - Example:
        - `1920x1080`
- `real_time_left_margin`, `real_time_right_margin`, `real_time_top_margin`, `real_time_bottom_margin`
    - This value determines how many pixels will be cropped from each side of each frame in real-time mode.
    - This value should be specified as tight as reasonably possible to make Predator as accurate as it can be.
    - It should be noted that it's better to physically move and zoom your camera if possible.
        - Use of optical zoom and framing will lead to higher quality images for Predator to process.
    - In most videos there will be a portion of the frame in which a license plate would never reasonably appear.
        - For example, in dash-cam video, there will rarely be a license plate in the top half of the frame when the camera is mounted facing straight forward.
- `fswebcam_flags`
    - This setting specifies any additional arguments that you want to add to the FSWebcam command in real-time mode.
    - This setting can be used to fine tune the way FSWebcam handles your camera.
    - Example:
        - `--set brightness=100% -F 15 -S 5`
    - For more information on what this setting can be used for, see the FSWebcam documentation by running `man fswebcam`.
- `audio_alerts`
    - This setting determines whether or not Predator will make use of audible alerts.
    - With this is set to `True`, Predator will play subtle alert noises when a plate is detected, and much more prominent noises when a plate in an alert database is detected.

### Real-time Mode Default Settings

Settings in the 'default settings' section allow you to configure Predator to skip some or all of the preferences prompts that appear when launching Predator in real-time mode. By configuring all of the default settings, as well as the `auto_start_mode` setting described above in the "General" section, it's possible to get Predator to start 100% autonomously after it's been executed.

- `default_root`
    - When this default setting isn't empty, Predator will use it's value as the default root project directory path, and will skip the 'root directory' prompt when running Predator in real-time mode.
- `default_alert_database`
    - When this default setting isn't empty, Predator will use it's value as the default alert database file path, and will skip the 'alert database' prompt when running Predator in real-time mode.
    - The 'alert database' preference specifies a file path to a plain text file containing a list of license plates that Predator should alert for.
        - The text file should simply contain one license plate per line, and no other characters.
    - Just like the standard prompt that appears when loading Predator, this setting also accepts URLs to alert databases hosted over a network.
    - If you want to skip the 'alert database' prompt without supply a database, simply set this variable to a single space.
        - Example: `default_alert_database = " "`
- `default_save_license_plates_preference`
    - When this default setting isn't empty, Predator will use it's value as the default license plate saving preference, and will skip the 'license plate saving preference' prompt when running Predator in real-time mode.
    - The 'license plate saving' preference specifies whether or not Predator will write each of the license plates it detects to the root project directory.
        - If you're running Predator in a headless configuration, this should almost certainly be turned on (set to `"y"`) so you can access the license plates detected at a later date.
    - This should be set to either `"y"`, `"n"`, or be left blank.
- `default_save_images_preference`
    - When this default setting isn't empty, Predator will use it's value as the default image saving preference, and will skip the 'image saving preference' prompt when running Predator in real-time mode.
    - The 'image saving' preference determines whether or not Predator will save every image it takes in real-time mode.
        - This should typically be turned off (set to "n"), but it might be useful to turn it on (set to `"y"`) if you want Predator to operate like a time-lapse dashcam while running.
    - This should be set to either `"y"`, `"n"`, or be left blank.
- `default_license_plate_format`
    - When this default setting isn't empty, Predator will use it's value as the default license plate format, and will skip the 'license plate format' prompt when running Predator in real-time mode.
    - The 'license plate format' preference provides Predator with an example of how license plates in your region should work.
        - For example, license plates in the state of Ohio generally follow the pattern of 3 letters followed by 4 numbers. In Ohio, this preference might be set to `AAA0000` to filter out plate guesses that don't match the most common formatting pattern.
        - This preference only considers the type of each character, not the character itself.
            - In other words, `AAA0000` and `ABC1234` will function identically.
            - This means you can simply enter a random plate from a car located in the region you're scanning in to have a reasonably good chance at matching your region's formatting guidelines for license plates.
        - It should be noted that some regions will have varying license plate formatting guidelines. In this case, setting this preference could inadvertently cause Predator to filter out valid plates.
            - If you want to skip the preference prompt associated with this setting, but you don't want to supply a license plate format, set this preference to a single space.
                - Example: `default_license_plate_format = " "`
