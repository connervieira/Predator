# Configuration

This document describes the configuration values found `config.json`.


## General Configuration

This section of configuration values will effect Predator's general operation.

- `ascii_art_header`
    - This value is a boolean that determines whether or not Predator will display a large ASCII art banner on start up. When set to `false`, the ASCII art banner will be replaced with a small, normal text title.
    - This setting may be useful to change in the event that Predator is being run on a device with a tiny display, where a large ASCII art header might cause formatting issues.
- `custom_startup_message`
    - This setting is a string used to set a custom start-up message that display after the initial Predator start-up header.
    - By default, this is left blank, but you can use this to show a custom message to the user when Predator starts.
- `auto_start_mode`
    - This setting is a string determines which mode (if any) that Predator will automatically load into when being started.
    - There are 6 possible values this can be set to, not including being left blank.
        - When set to an empty string, Predator will prompt the user to select a mode each time it starts. This is the default.
        - When set to "0", Predator will skip the 'mode' prompt, and automatically boot into Management Mode.
        - When set to "1", Predator will skip the 'mode' prompt, and automatically boot into Pre-recorded Mode.
        - When set to "2", Predator will skip the 'mode' prompt, and automatically boot into Real-time Mode.
        - When set to "3", Predator will skip the 'mode' prompt, and automatically boot into Dash-cam Mode.
        - When set to "4", Predator will skip the 'mode' prompt, and automatically boot into Information Mode.
        - When set to "5", Predator will skip the 'mode' prompt, and automatically boot into Survey Mode.
    - It may be useful to change this setting in several different situations:
        - If you only ever use the same mode when using Predator, setting this to your preferred mode can save time.
        - When installing Predator in a vehicle, this setting can allow Predator to load without any user input.
            - See the "default" settings later in this document for more information on auto-starting.
- `default_root`
    - When this default setting isn't empty, Predator will use it's value as the default root project directory path, and will skip the 'root directory' prompt when running Predator in Real-time Mode and Dash-cam Node.
    - This setting has no effect on Pre-recorded Mode.
- `silence_file_saving`
    - This setting determines whether or not Predator will display informational messages about file saving.
    - When this is set to `true`, Predator won't show information or notices when it saves information to disk.
    - Under normal circumstances, this setting should be set to `false` in order to allow Predator to inform the user when it saves files, and whether or not errors were encountered.
- `disable_object_recognition`
    - This setting can be used to globally disable object recognition (Tensorflow and OpenCV).
    - If you're on a platform that doesn't support OpenCV or Tensorflow, then you can set this to 'true' in order to prevent errors while using Predator.
    - Under normal usage, this should be set to `false`, since this will allow Predator to use it's full functionality.
- `gps_enabled`
    - This configuration value is used to globally enable and disable Predator's GPS functionality.
    - If you don't have a GPS connected, or don't want to use location aware features, set this to `false`.
    - To enable location aware features like traffic camera alerts, this must be set to `true`.
- `speed_display_unit`
    - This configuration value determines what units Predator will use to display the current speed.
    - This value can only be set to the following strings:
        - "mph" for miles-per-hour
        - "kph" for kilometers-per-hour
        - "mps" for meters-per-second
        - "fps" for feet-per-second
        - "knot" for knots
- `modes_enabled`
    - This setting determines whether or not each mode is activated in Predator.
    - When the value for a particular mode is set to `false`, that mode's option will be hidden from the mode selection menu shown to the user when Predator starts, and the auto-start-mode command line arguments won't allow the user to boot Predator directly to that mode.
    - Under normal circumstances, all of these settings should be left as 'true', in order to enable full functionality of Predator, but there may be certain situations in which is useful to block certain modes from starting.
        - This setting is not intended to a be a security feature. It's completely trivial to bypass this setting by simply modifying the configuration file directly.
- `alert_databases`
    - This setting contains the file names all of the alert databases used by Predator.
        - `license_plates` should be set to (if anything), a plain-text list of license plates that Predator should show a heightened alert for.
        - `traffic_cameras` should be set to (if anything), an ExCam database of speed, red-light, and traffic cameras. Leaving this blank will disable traffic camera alerts.
        - `alpr_cameras` should be set to (if anything), a Predator JSON database of ALPR cameras. Leaving this blank will disable ALPR camera alerts.
    - Each value in this section should either be left blank, or be a file path relative to the root project folder.
        - For example, if your alert database is in `/home/pi/Data/alerts.txt`, and your root project directory is `/home/pi/Data/`, then then the alert database value should simply be set to `alerts.txt`, not the the full file path.
- `traffic_camera_alerts_enabled`
    - This configuration value determines whether or not traffic camera alerts are enabled.
    - When this is set to `true`, Predator will use information from the following traffic camera alert settings in order to notify the user of nearby traffic cameras.
- `camera_alert_types`
    - This configuration value determines which camera types Predator will consider when displaying alerts to the user. All of the values under this setting should be set to a boolean value indicating whether or not alerts should be shown for each respective camera type.
    - There are currently 3 types of cameras.
        - `speed` includes both radar and average speed enforcement cameras.
        - `redlight` includes traffic light enforcement cameras.
        - `misc` includes all traffic cameras that don't fall into the other two categories. 
- `traffic_camera_loaded_radius`
    - This is the radius, in miles, that Predator will load traffic cameras from during the initial loading process.
    - For example, if this value is set to `100`, then Predator will only load traffic cameras in a 100 mile radius from the current location when it boots. If you travel more than 100 miles away from your original location without reloading Predator then you won't get traffic camera alerts.
    - If you're running Predator on a high performance processor, you can comfortable set this to a very high number, which could be useful on long road trips where you might not restart Predator for hundreds of miles at a time. However, if you're running Predator on a low powered device, like a Raspberry Pi, you should reduce this radius to make Predator faster at checking traffic camera proximity when running in Real-time Mode.
    - This setting does not determine the distance at which alerts will be displayed. To configure the alert distance for traffic cameras, see the `alerts` configuration value in the Information Mode section below.



## Pre-recorded Mode Configuration

Configuration values in this section are settings specific to Pre-recorded Mode.

- `left_margin`, `right_margin`, `top_margin`, `bottom_margin`
    - This value determines how many pixels will be cropped from each side of each frame in Pre-recorded Mode.
    - This value should be specified as tight as reasonably possible to make Predator as accurate and efficient as it can be.
    - In most videos there will be a portion of the frame in which a license plate would never reasonably appear.
        - For example, in dash-cam video, there will rarely be a license plate in the top half of the frame when the camera is mounted facing straight forward.


## Real-time Mode Configuration

Configuration values in this section are settings specific to Real-time Mode.

- `realtime_alpr_enabled`
    - This setting is a boolean that determines whether or not Predator will run license plate recognition while operating in Real-time Mode.
    - Under normal circumstances, this should be left as `true`, since it will allow Predator to use it's full functionality. However, if you don't want license plate recognition, and only care about some of Predator's other functionality, then license plate recognition can be disabled to save time and improve efficiency.
- `realtime_alpr_disabled_delay`
    - This setting is used to add an artificial delay when Predator's real-time license plate recogition is disabled.
    - Typically, the license plate recognition process will take at least a second or two, allowing the user to read any on-screen messages before the processing cycle continues. This setting allows the user to specify in time, in seconds, that Predator will wait when `realtime_alpr_enabled` is set to `false`.
- `realtime_output_level`
    - This setting determines how much information Predator prints to the console while operating in Real-time Mode.
    - This setting has 3 different options.
        - Level "1": Only alerts are displayed.
        - Level "2": Only detections and other important events are displayed.
        - Level "3": All messages are displayed.
- `clear_between_rounds`
    - This setting determines whether or not Predator will clear the output screen between analysis rounds during Real-time Mode.
- `delay_between_rounds`
    - This setting changes how long Predator will wait in between analysis rounds.
    - This should usually be set to something very short, in order to allow Predator to process as much data as possible. However, there might be some cases in which it makes sense to slow down the process to allow the user to see what's happening.
- `print_invalid_plates`
    - This setting is a boolean that determines whether or not Predator will print every guess it makes as to the contents of a license plates, even if those guesses are invalidated by the license plate format sample.
    - This setting is usually set to `false`, but there may be some situations in which it would make sense to turn it on for sake of troubleshooting.
        - In the event that you consistently get Predator to identify a plate, but it can't find a valid guess as to what its contents are, turning this on can help you figure out what Predator thinks its seeing.
- `print_detected_plate_count`
    - This setting is a boolean that determines whether or not Predator will show how many plates are detected in each frame while operating in Real-time Mode.
- `realtime_guesses`
    - This setting is a number in the form of a string that determines how many OpenALPR guesses Predator will take into account when analyzing a plate.
    - The higher this number is, the more likely Predator is to guess a plate incorrectly. The lower this number is, the less likely Predator will be to find a valid guess at all.
    - By default this value is set to 10, which tends to be a healthy balance for the majority of tasks.
- `alpr_location_tagging`
    - This setting determines whether or not the current GPS location will be saved to the log file when each plate is detected.
    - For this setting to do anything, both the "save license plates" preference, and `gps_enabled` configuration value need to be turned on.
- `alerts_ignore_validation`
    - This setting determines whether alerts will respect or ignore the plate validation format.
    - When this setting is set to `true`, if a plate fails the validation test, but matches an alert database plate, the alert will be displayed anyway.
    - When set to `false`, only plates that have passed the validation test will be checked against the alert database.
- `camera_resoultion`
    - This setting is a string that defines the resolution that FSWebcam will use when taking images through the connected camera.
    - It takes the format of `width x height`, with no spaces.
    - Example:
        - `"1920x1080"`
- `real_time_left_margin`, `real_time_right_margin`, `real_time_top_margin`, `real_time_bottom_margin`
    - This value determines how many pixels will be cropped from each side of each frame in Real-time Mode.
    - This value should be specified as tight as reasonably possible to make Predator as accurate as it can be.
    - It should be noted that it's better to physically move and zoom your camera if possible.
        - Use of optical zoom and framing will lead to higher quality images for Predator to process.
    - In most videos there will be a portion of the frame in which a license plate would never reasonably appear.
        - For example, in dash-cam video, there will rarely be a license plate in the top half of the frame when the camera is mounted facing straight forward.
    - Note: The cropping process takes place after the rotating process described under `real_time_image_rotation`.
- `real_time_image_rotation`
    - This setting can be used to rotate images if your camera is mounted at an angle.
    - Set this value to a number between 0 and 360 in order to rotate your images a certain number of degrees clockwise.
        - For example, setting this value to '180' would flip the image upside down.
    - Note: The rotating process takes place before the cropping process.
- `fswebcam_device`
    - This setting simply determines the video device that Predator will use FSWebcam to access.
    - This should almost always be set to `"/dev/video0"`, but there may be some situations it which it would make sense to change this, such as when you want to run multiple cameras.
- `fswebcam_flags`
    - This setting specifies any additional arguments that you want to add to the FSWebcam command in Real-time Mode.
    - This setting can be used to fine tune the way FSWebcam handles your camera.
    - Example:
        - `"--set brightness=100% -F 15 -S 5"`
    - For more information on what this setting can be used for, see the FSWebcam documentation by running `man fswebcam`.
- `audio_alerts`
    - This setting determines whether or not Predator will make use of audible alerts.
    - With this is set to `true`, Predator will play subtle alert noises when a plate is detected, and much more prominent noises when a plate in an alert database is detected.
- `startup_sound`, `notification_sound`, `alert_sound`, `camera1_sound`, `camera2_sound`, `camera3_sound`
    - These are the audio sound effects played when `audio_alerts` is enabled.
        - `startup_sound` is the sound played just after Predator finishes loading.
        - `notification_sound` is the sound played when a valid plate is detected in Real-time Mode, and the plate is not in an alert database.
        - `alert_sound` is the sound played when a valid plate is detected, and the plate is in an alert database.
        - `camera1_sound` is the sound played to alert the user of a traffic camera (speed/red-light camera) detected at a far distance.
        - `camera2_sound` is the sound played to alert the user of a traffic camera (speed/red-light camera) detected at a moderate distance.
        - `camera3_sound` is the sound played to alert the user of a traffic camera (speed/red-light camera) detected at a critically near distance.
        - `alpr_sound` is played to alert the user of an ALPR camera detected within the configured distance in Information Mode.
    - The `path` value should be set to the file path of the audio file you want to play.
    - The `repeat` value should be set to how many times you want the sound effect to be repeated.
        - Under normal circumstances, this value should just be "1", but there might be some cases in which you want to play a particular sound repeatedly.
    - The `delay` value determines how long Predator will wait, in seconds, between repetitions, if `reptition` is set to more than 1.
        - Note that this delay includes the time it takes for the previous instances of the sound effect to play.
        - For example, if the audio clip you're repeating takes 2 seconds to play, and you want a 1 second delay between audio clips, this setting should be 3 seconds.
        - If the delay is set to zero, then all of the repetitions will play over top of each-other.
- `webhook`
    - This setting is a string used to define a webhook that Predator will send a request to when it detects a license plate in Real-time Mode.
    - This setting should either be left blank, or be set to a URL.
    - Flags can be used to supply information to the webhook.
        - Predator will replace `[L]` with the detected license plate.
        - Predator will replace `[T]` with the current time as a Unix epoch timestamp.
        - Predator will replace `[A]` with the current alert status (`true` or `false`).
            - Note that if multiple license plates are detected simultaneously, and one of them is in an alert database, then all of the license plates detected that frame will be marked as `true` for alert status, regardless of whether the individual plates are actually in the alert database themselves.
    - Examples:
        - `http://localhost/app.php?plate=[L]&time=[T]&alert=[A]`
        - `http://domain.tld/app/[L]`
- `shape_alerts`
    - This setting determines whether or not Predator will use large shapes printed to the console to indicate certain important events.
    - When set to `true`, Predator will use things like large ASCII circles, squares, and triangles to indicate when a plate has been detected, when an alert has been triggered, and when a plate has been read, but failed validation.
    - If you intend on using Predator in a vehicle, this setting can drastically reduce the time it takes for you to look at the console output in order to figure out what Predator is doing.
- `save_real_time_object_recognition`
    - This setting determines whether or not Predator will save all of the objects it recognizes to disk while running in Real-time Mode.
    - When this is set to `false`, the objects recognized will only be printed to the console, and won't be saved to a file.
- `speed_display_enabled`
    - This configuration value is a boolean that determines whether or not the driver's current speed will be printed to the console during each processing cycle in Real-time Mode.
    - For this configuration value to be active, `gps_enabled` needs to be enabled as well.


### Real-time Mode Default Settings

Settings in the 'default settings' section allow you to configure Predator to skip some or all of the preferences prompts that appear when launching Predator in Real-time Mode. By configuring all of the default settings, as well as the `auto_start_mode` setting described above in the "General" section, it's possible to get Predator to start 100% autonomously after it's been executed.

- `default_alert_database`
    - When this default setting isn't empty, Predator will use it's value as the default alert database file path, and will skip the 'alert database' prompt when running Predator in Real-time Mode.
    - The 'alert database' preference specifies a file path to a plain text file containing a list of license plates that Predator should alert for.
        - The text file should simply contain one license plate per line, and no other characters.
    - Just like the standard prompt that appears when loading Predator, this setting also accepts URLs to alert databases hosted over a network.
    - If you want to skip the 'alert database' prompt without supplying a database, simply set this variable to a single space.
        - Example: `"default_alert_database": " "`
- `default_save_license_plates_preference`
    - When this default setting isn't empty, Predator will use it's value as the default license plate saving preference, and will skip the 'license plate saving preference' prompt when running Predator in Real-time Mode.
    - The 'license plate saving' preference specifies whether or not Predator will write each of the license plates it detects to the root project directory.
        - If you're running Predator in a headless configuration, this should almost certainly be turned on (set to `"y"`) so you can access the license plates detected at a later date.
    - This should be set to either `"y"`, `"n"`, or be left blank.
- `default_save_images_preference`
    - When this default setting isn't empty, Predator will use it's value as the default image saving preference, and will skip the 'image saving preference' prompt when running Predator in Real-time Mode.
    - The 'image saving' preference determines whether or not Predator will save every image it takes in Real-time Mode.
        - This should typically be turned off (set to "n"), but it might be useful to turn it on (set to `"y"`) if you want Predator to operate like a time-lapse dashcam while running.
    - This should be set to either `"y"`, `"n"`, or be left blank.
- `default_license_plate_format`
    - When this default setting isn't empty, Predator will use it's value as the default license plate format, and will skip the 'license plate format' prompt when running Predator in Real-time Mode.
    - The 'license plate format' preference provides Predator with an example of how license plates in your region should work.
        - For example, license plates in the state of Ohio generally follow the pattern of 3 letters followed by 4 numbers. In Ohio, this preference might be set to `AAA0000` to filter out plate guesses that don't match the most common formatting pattern.
        - This preference only considers the type of each character, not the character itself.
            - In other words, `AAA0000` and `ABC1234` will function identically.
            - This also means you can simply enter a random plate from a car located in the region you're scanning in to have a reasonably good chance at matching your region's formatting guidelines for license plates.
        - It should be noted that some regions will have varying license plate formatting guidelines. In this case, setting this preference could inadvertently cause Predator to filter out valid plates.
            - If you want to skip the preference prompt associated with this setting, but you don't want to supply a license plate format, set this preference to a single space.
                - Example: `"default_license_plate_format": " "`


### Real-time Mode Push Notification Settings

All settings in this section are related to network-based push notifications via Gotify.

- `push_notifications_enabled`
    - This setting determines whether or not Predator will attempt to send push notifications using a Gotify server.
    - This value is a boolean value, and should only ever be set to `true` or `false`
- `gotify_server`
    - This setting specifies the Gotify server that Predator will attempt to use. It should include the protocol and port number.
    - This value must be configured if `push_notifications_enabled` is set to `true`
    - Example:
- `gotify_application_token`
    - This setting specifies the Gotify application token that Predator will attempt to use to send notifications through the specified Gotify server.
    - This value must be configured if `push_notifications_enabled` is set to `true`
    - Example:
        `AJrhgGs83mL22kZ`


### Real-time Mode Status Lighting Settings

In order to better integrate with an existing system, Predator can communicate with LEDs via GET requests to display basic information.

- `status_lighting_enabled`
    - This setting is simply a boolean value that determines whether or not Predator will attempt to make use of LED status lights
    - If you don't have status lighting set up, then leave this configuration value set to `false` to prevent Predator from attempting to update non-existent status lights.
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

- `dashcam_resolution`
    - This setting determines what resolution Predator will attmpt to record at.
    - Be sure that your camera is capable of recording at resolution specified here. If you set an unsupported resolution, it's likely Predator will fail and not record anything.
    - Example: `"dashcam_resolution": "1920x1080"`
- `dashcam_frame_rate`
    - This setting determines what frame rate Predator will attmpt to record at.
    - Even though this setting is a number, it should be entered as a string with quotes around it. See the example below for more context.
    - Be sure that your camera is capable of recording at the frame rate specified here. If you set an unsupported frame rate, it's likely Predator will fail and not record anything.
    - If you enter a frame rate too slow for the encoder, it might automatically be sped to a higher frame rate.
    - Example: `"dashcam_frame_rate": "30"`
- `dashcam_device`
    - This setting contains the camera devices Predator will attempt to use when recording video in Dash-cam Mode.
    - Each entry under this setting should contain a device identifier/name, as well as a reference to the device itself.
    - Example:
        - `"main_camera": "/dev/video0"`
        - `"secondary_camera": "/dev/video1"`
    - The device name will be appended to any video file names in order to give the user a quick indication of which camera recorded each file.
    - Note: While you can specify an infinite number of cameras here, be aware that Predator might not be able to record with all of them. Bottlenecks like processor speed, RAM, and USB controller capabilities can cause issues with high numbers of cameras. Be sure to test your configuration before you start using it formally.
- `dashcam_background_mode_realtime`
    - This setting determines whether Predator will automatically enabled background dashcam recording when starting in Real-time Mode.
    - Note that Predator can only use each recording device for one task at a time, so if you run Real-time Mode with background recording enabled, you'll need to specify two different devices by changing `fswebcam_device` and `dashcam_device`.



## Information Mode Configuration

- `information_refresh_delay`
    - This setting determines how long Predator will wait before refreshes while operating in Information Mode.
    - Having a short pause between refreshes allows the user to read the information displayed on the screen.
- `displays`
    - The configuration values in this section are used to enabled and disable whether or not certain pieces of information are displayed.
    - Below are all the values that can be turned on and off.
        - `time`
            - This setting determines whether the current time will be displayed while operating in Information Mode.
        - `date`
            - This setting determines whether the current date will be displayed while operating in Information Mode.
        - `speed`
            - This setting determines whether the current speed will be displayed while operating in Information Mode.
        - `location`
            - This setting determines whether the current location will be displayed while operating in Information Mode.
        - `altitude`
            - This setting determines whether the current altitude will be displayed while operating in Information Mode.
        - `track`
            - This setting determines whether the current track will be displayed while operating in Information Mode.
        - `satellites`
            - This setting determines whether the current connected satellite count will be displayed while operating in Information Mode.
- `record_telemetry`
    - This setting determines whether or not Predator will log the information it displays while operating in Information Mode.
    - When set to `true`, all of the the raw information displays that are available under the `displays` configuration value will be recorded, regardless of whether they are turned on.
        - This configuration value only records raw data, like speed, altitude, and number of connected satellites. It does not record the nearest traffic camera, or similar information.
        - If `gps_enabled` is set to `false`, then all GPS-dependent information will be left as placeholders.
    - When enabled, a log file will be created in the root project directory named `information_recording.csv`.
        - This file follows this format: `time,current_speed,current_latitude,current_longitude,current_altitude,current_track,current_connected_satellite_count`
- `alerts`
    - Configurations made in this section may also influence Predator while operating in Real-time Mode.
    - This setting is a dictonary of alert databases and their alert ranges, in miles.
        - The `traffic_cameras` alert database is used for speed and red-light camera alerts. Use this value to specify the distance (in miles) at which Predator should consider a speed camera to be within alert distance.
            - Example: `"traffic_cameras": 0.5` will show alerts for the `traffic_cameras` database within 0.5 miles of a point-of-interest.
    - The databases in this section correspond the databases specified by the `alert_databases` configuration value in the general configuration section.
        - In a future update, the user will be able to add custom alert databases by adding the databases to `alert_databases`, then referencing them in this configuration value with an alert distance.
