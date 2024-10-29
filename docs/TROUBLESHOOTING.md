# Troubleshooting

This document lists specific problems that you may encounter, and suggested solutions.

All of these solutions assume you have already completed the full installation/configuration process.


## General

### Predator crashes, and shows an error containing "config" with a "KeyError".

It's possible you've encountered an undiscovered bug. However, if you've recently upgrade Predator, it's possible your active configuration file was not updated properly. Ideally, Predator should automatically update the configuration file, but this may not always work as expected, especially when jumping between versions. Try temporarily re-naming your active configuration file (`mv config.json configbkp.json`), then re-running Predator. A fresh configuration file will be generated. Check to see if the key specified in the error is present in the fresh configuration file, but missing from your original configuration file. If so, try copying over the contents of the key from the fresh configuration to your normal configuration, then rename your normal configuration back to the original (`mv configbkp.json config.json`).

These kinds of issues can be difficult to troubleshoot, so if you run into additional problems, consider using a fresh configuration file, and manually updating each of the values.


## ALPR

### Predator occasionally detects sequences of repeated similar characters (example: II1I1I1, ODDDDOD)

First, define the formats of the plates you want to detect under the `general>alpr>validation>license_plate_format` configuration value. You can define as many formats as you need to. Then, set the `general>alpr>validation>best_effort` value to `false` to strictly enforce validation.

If this is not sufficient, try increasing the `general>alpr>validation>confidence` configuration value to increase the minimum required confidence.

### Predator regularly detects the same false plate (for example, a text-stamp on a dash-cam overlay)

Provided the problem can't be solved with the other validation options in the `general>alpr>validation` configuration section, you can hard-code an "ignore list". Simply create a plain text file, where each line is a plate you would like to ignore (wild-cards supported). Then, specify the path to this file under the `developer>ignore_list>local_file` configuration option. Additionally, ensure that `developer>ignore_list>enabled` is set to `true`. If a detected plate has an associated guess that matches a plate in the ignore list, that plate will be thrown out.


## Dash-cam Recording

### The audio recording process works for the first segment, but then occasionally fails for subsequent segments.

Try increasing the `dashcam>capture>audio>start_delay` value. It's likely the audio capture device is not being fully released by the previous segment before it tries to be accessed by the new segment.


### The audio is not synced up with the video (the audio is longer or shorter than the video).

Ensure that the video recording is running at a consistent frame-rate (and therefore, is a consistent length of time). For example, if your video flucuates between 32 and 37 FPS, try capping it at 30FPS to ensure a consistent frame-rate. This can be done with the `dashcam>capture>video>devices>DEVICE_NAME>frame_rate>max` configuration value.


### Predator enters parking mode doesn't reliably exit it [OR] Predator occasionally enters parking mode while driving.

Ensure that your GPS is enabled (`general>gps>enabled`) and working correctly. If the GPS loses a lock, Predator may consider the vehicle to be stationary, even if it is moving. Ensure the GPS is reporting the correct data using the `cgps` command at the shell. Consider increasing `dashcam>parked>conditions>time` to prevent Predator from entering parking mode if the GPS loses its lock for a short time (like when driving through a tunnel)
