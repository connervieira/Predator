# Installation

This document contains detailed instructions on how to install Predator.


## Quick Install Guide

If you're already familiar with Predator, and you just want a quick set-up guide, you can use the following steps to set everything up. For more detailed instructions, skip to the 'Full Install Guide' later in the document.

1. Install Linux packages: `sudo apt-get install ffmpeg mpg321 gpsd gpsd-clients imagemagick fswebcam libhdf5-dev build-essential`
2. Install Python packages: `pip3 install pytz validators requests gps gpsd-py3 opencv-python cvlib tensorflow keras silence-tensorflow psutil rns lxmf gpiozero`
    - If you see an "externally managed environment" error while installing Python packages, consider one of the following solutions:
        - If you're installing Predator on a system dedicated to it's use (such as a computer installed in a vehicle), you can override this warning and force install the packages (at the risk of breaking your install) using by adding the `--break-system-packages` flag to the installation command.
            - It's worth mentioning that during testing, using the `--break-system-packages` flag while installing Predator has never caused any noticable system issues on any common Debian-based Linux distribution (Ubuntu, Mint, Raspberry Pi OS, etc.). However, you should still exercise caution when using it, especially if you aren't using a fresh Python installation.
        - If you're focused on developing or modifying Predator, try creating a virtual environment for sake of consistency. This method is very reliable, but will often cause issues if you intend to integrate Predator with external interfaces in production (like V0LT Optic or V0LT Cortex), since these interfaces are unable to run Predator as part of a virtual environment.
            - You can create a virtual environment by navigating to the Predator directory, and running the following command: `python3 -m venv .venv`
            - After creating the virtual environment, activate it by running the `source .venv/bin/activate` command.
            - Next, install all required Python packages.
            - Finally, run Predator. In the future, you'll need to re-activate the virtual environment every time you run Predator.
        - The most time consuming solution is to install the required packages through your default package manager. Most packages will just be named after the original Python package, with "python3-" appended to the beginning. For example, the `gpiozero` package can be installed with the `sudo apt install python3-gpiozero` command. However, some packages may not follow this naming scheme, and you might need to manually search for them.
3. Install an ALPR engine, like [Phantom](https://v0lttech.com/phantom.php).
4. Configure Predator, as described in the [CONFIGURE.md](CONFIGURE.md) file.


## Full Install Guide

This is the installation process for Predator and all of its dependencies. This process is written assuming you're running a distribution of GNU/Linux, but it is generally possible to get Predator to function on MacOS and BSD-based operating systems as well.

### Dependencies

- Python packages: `pip3 install pytz validators requests gps geopy gpsd-py3 opencv-python cvlib tensorflow keras silence-tensorflow psutil`
    - Required:
        - `pytz`: Required to manage timezones.
    - Highly recommended:
        - `validators` and `requests`: Required to network functionality, like push notifications, status light interfacing, remove alert lists, and more.
    - Recommended:
        - `gps`, `geopy`, and `gpsd-py3`: Required to enable GPS features.
            - These packages are not required for reading GPX files, and are only necessary for interacting with live GPS devices.
        - `opencv-python`, `cvlib`, `tensorflow`, `keras`, `silence-tensorflow`: Required for object recognition features and dash-cam video capture.
            - These packages are not required for basic license plate recognition.
    - Optional:
        - `psutil`: Required to process disk usage information in management mode and dash-cam mode.
        - `lxmf`, `rns`: Required to send offline parking notifications over the Reticulum stack.
        - `gpiozero`: Required to trigger events using GPIO inputs.
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

If you intend to use any of Predator's license plate recognition capabilities, you'll need to install an ALPR engine. The two options are 'Phantom ALPR' or 'OpenALPR'.
- Phantom ALPR is a modified version of OpenALPR designed specifically for Predator. Phantom ALPR offers more in-depth integration, and is more fault tolerant.
    - If you want the best experience with Predator, and conflicts aren't a concern, Phantom ALPR is a great option.
    - You can download Phantom at <https://v0lttech.com/phantom.php>
- OpenALPR is the arguably industry standard for open source license plate recognition, and is widely used.
    - If you already have OpenALPR installed, and don't want to replace it, you can use it with Predator.

You can learn more about the installation process for each program in their respective documentation. After installing, you should be able to run the ALPR engine of your choice using the `alpr` command. If not, Predator won't be able to run the ALPR process, and will fail to analyze license plates.
