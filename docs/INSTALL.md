# Installation

This document contains detailed instructions on how to install Predator.


## Quick Install Guide

If you're already familiar with Predator, and you just want a quick set-up guide, you can use the following steps to set everything up. However, if you're new to Predator, or you don't yet understand how it works, it is recommended that you use the full installation instructions below instead.

1. Install Python packages: `pip3 install validators requests gps geopy gpsd-py3 opencv-python cvlib tensorflow keras silence-tensorflow psutil`
2. Install Linux packages: `sudo apt-get install ffmpeg mpg321 gpsd gpsd-clients imagemagick fswebcam`
3. Install an ALPR engine, like [Phantom](https://v0lttech.com/phantom.php).



## Full Install Guide

This is the installation process for Predator and all of its dependencies. This process is written assuming you're running a distribution of GNU/Linux, but it is generally possible to get Predator to function on MacOS and BSD-based operating systems as well.

### Dependencies

- Python packages: `pip3 install validators requests gps geopy gpsd-py3 opencv-python cvlib tensorflow keras silence-tensorflow psutil`
    - Highly recommended:
        - `validators` and `requests`: Required to network functionality, like push notifications, status light interfacing, remove alert lists, and more.
    - Recommended:
        - `gps`, `geopy`, and `gpsd-py3`: Required to enable GPS features.
            - These packages are not required for reading GPX files, and are only necessary for interacting with live GPS devices.
        - `opencv-python`, `cvlib`, `tensorflow`, `keras`, `silence-tensorflow`: Required for object recognition features and dash-cam video capture.
            - These packages are not required for basic license plate recognition.
    - Optional:
       - `psutil`: Required to process disk usage information.
- System packages: `sudo apt-get install ffmpeg mpg321 gpsd gpsd-clients imagemagick fswebcam`
    - Highly recommended:
        - `ffmpeg`: Required for audio/video merging in dash-cam mode, and video processing in pre-recorded mode.
        - `imagemagick`: Required for manipulating still frames of video in pre-recorded mode.
    - Recommended:
        - `mpg321`: Required to play audio alerts.
        - `gpsd` and `gpsd-clients`: Required to receive and process live GPS data.
            - It may also be necessary to start GPSD. You can test to see if GPSD is working properly using the `cgps` command.
    - Optional:
        - `fswebcam`: Useful for troubleshooting camera problems.
            - Predator does not depend on FSWebcam, but it can be a useful tool for capturing still images from connected cameras.


### ALPR Engine

If you intend to use any of Predator's license plate recognition capabilities, you'll need to install an ALPR engine. The two options are Phantom ALPR or OpenALPR.
- Phantom ALPR is a modified version of OpenALPR designed specifically for Predator. Phantom ALPR offers more in-depth integration, and is more fault tolerant.
    - If you want the best experience with Predator, and conflicts aren't a concern, Phantom ALPR is a great option.
    - You can download Phantom at <https://v0lttech.com/phantom.php>
- OpenALPR is the arguably industry standard for open source license plate recognition, and is widely used.
    - If you already have OpenALPR installed, and don't want to replace it, you can use it with Predator.

You can learn more about the installation process for each program in their respective documentation. After installing, you should be able to run the ALPR engine of your choice using the `alpr` command. If not, Predator won't be able to run the ALPR process, and will fail to analyze license plates.
