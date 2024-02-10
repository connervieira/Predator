# Hardware

Predator is primarily a software utility. However, it goes without saying that Predator is only useful if it has hardware capable of effectively collecting and processing video and image information. This document describes hardware information related to Predator, including parts lists.

To learn more about paid hardware/software support for Predator, see [../APEX.md](../APEX.md).


## Recommendations

This section contains recommendations for those looking to build a hardware device that runs Predator.

- The processing device should be fully capable of running Linux.
    - Having a device that can easily run Linux will make installing and setting up Predator drastically easier, as you'll spend less time troubleshooting compatibility issues, and more time actually assembling and configuring your device.
        - More specifically, something running a Debian-based distribution will work best. This includes operating systems like Ubuntu, Raspberry Pi OS, Pop!_OS, and several others.
- Camera color accuracy is practically irrelevant when it comes to Predator's ability to recognize license plates.
    - Even gray-scale cameras should have no problems recognizing license plates.
- Consider the context of the situation you want to use Predator in, and consider how to align your camera and it's lens.
- Consider motion blur when setting up your camera.
    - Ensure your camera is mounted somewhere stable enough that it can take clear images of the vehicles you're scanning, even while they are in motion.


## Guidelines

As a general rule, these are the parts you'll need in a Predator device:

- Camera
    - Required (for real-time and dash-cam mode)
        - Without a camera, Predator will have no way of using real-time mode or dash-cam mode, and only pre-recorded mode will be usable.
- Processing
    - Required
        - Needless to say, Predator can't be run without a processing device.
    - This device could be anything from a high end workstation to a single-board-computer, like a Raspberry Pi.
- Networking
    - Recommended
        - Predator is fully functional without being connected to a network. However, having access to a local area network can allow Predator to be remotely controlled through a web interface like [Optic](https://v0lttech.com/optic.php) or [Cortex](https://v0lttech.com/cortex.php).
            - This is the way most installs are controlled, due to limited space to install displays in most cars. A remote control web interface allows nearly any smartphone, tablet, or laptop to become Predator's display.
        - Access to the internet will allow Predator to download remote alert databases and use remote push notifications.
- Mounting Hardware
    - Recommended
        - Without mounting hardware, your Predator device will be significantly harder to mount in your build.
- Input Device
    - Optional
        - Without an input device, the only way to configure Predator will be remotely.
        - If your installation scenario makes an input device inconvenient or difficult to install, considering using a web interface like [Optic](https://v0lttech.com/optic.php) or [Cortex](https://v0lttech.com/cortex.php).
- Display
    - Optional
        - Without a display, Predator can only realistically run in headless mode, and it will be significantly harder to debug.
        - Once again, remote access via a web interface like [Optic](https://v0lttech.com/optic.php) could completely replace a directly connected display.
- Speaker
    - Optional
        - A speaker allows Predator to play notification noises. Without a speaker, Predator will be able to function, but it won't be able to easily notify the user when a plate is detected.
    - Any speaker can be used, including an existing sound system in a car. As long as Linux can play an audio output to it, it should work fine.
- GPS
    - Optional
        - Predator doesn't need a GPS to function. However, certain features won't be operational without it.
- Clock
    - Optional
        - Since most single-board computers (like the Raspberry Pi) don't have a real time clock (RTC), they will lose track of time without access to the internet. Adding a real time clock ensures your system's time remains accurate.
        - Predator should generally work fine with inaccurate time, but you may find it inconvenient, especially when interpreting log files and dash-cam video files.


## Builds

This section contains part recommendations. Please keep in mind that these parts are not guaranteed to work, and you shouldn't blindly purchase things in these lists.

Each build in this section has a nick-name to keep it distinct from the other builds. These nick-names align with the pre-built Predator Apex models on the V0LT website at <https://v0lttech.com/predator/predatorapex.php>


### Predator Scorpion

- Link: <https://v0lttech.com/predator/predatorscorpion.php>
- Description: Predator Scorpion is designed for general use in vehicles, security systems, and other low-power applications that require medium to long distance scanning.
- Advantages:
    - All of the parts are physically small, and can be easily fit in tight places, like the interior of a vehicle.
    - The entire system is lightweight, making it easy to move around.
    - Each device is very low power usage, so it should be easy to install using existing infrastructure in your car, building, or other system.
- Disadvantages:
    - This hardware configuration severely struggles to successfully read license plates on fast moving vehicles due to the low shutter speed of the camera.
- Price: ~$140
- Parts:
    - Camera: ELP-USB500W02M-SFV(5-50)
        - Price: ~$80
        - Resolution: 2592x1944
        - Frame Rate: 15FPS
            - Reduced Resolution Frame Rate: 30FPS
        - Lens: 5-50mm (10X optical zoom)
    - Processing: Raspberry Pi 4 B
        - Price: ~$40
        - Memory: 2GB
        - CPU: 4 Core, 1.5GHz ARM CPU 
    - Miscellaneous:
        - Necessary Cables
        - Storage
            - SD card for OS, flash-drive for images, etc.
        - Mounting Hardware
            - Screws, adhesives, brackets, etc.
            - Necessary to hold the camera in a stable position.
