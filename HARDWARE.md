# Hardware

Predator is primarily a software utility. However, it goes without saying that Predator is only useful if it has hardware capable of effectively collecting and processing video and image information. This document describes hardware information related to Predator, including parts lists.


## Recommendations

This section contains recommendations for those looking to build a hardware device that runs Predator.

- The processing device should be fully capable of running Linux.
    - Having a device that can easily run Linux will make installing and setting up Predator drastically easier, as you'll spend less time troubleshooting compatibility issues, and more time actually assembling and configuring your device.
        - More specifically, something running a Debian-based distribution will work best. This includes operating systems like Ubuntu, Raspberry Pi OS, Pop!_OS, and several others.
- Camera color accuracy is practically irrelevant when it comes to Predator's ability to recognize license plates.
    - Even gray-scale cameras should have no problems recognizing license plates.
- Consider the context of the situation you want to use Predator in, and consider how to align your camera and it's lens.
    - You should have your camera's lens zoomed in as far as reasonably possible.
        - For example, if you're installing Predator in a car, you may want to zoom in on the area in front of your car, where the license plate of the car in front of you is likely to be.
        - The more zoomed in your Predator system's camera is, the easier time it will have detecting license plates.
- Consider motion blur when setting up your camera.
    - As mentioned previously, zooming in as far as possible will increase Predator's ability to recognize plates at a distance. However, zooming in will also increase the effects of motion blur, since even tiny movements will shift the frame dramatically.
    - Ensure your camera is mounted somewhere stable enough that it can take clear images of the vehicles you're scanning, even while they are in motion.
- If processing speed is a concern, consider looking into a more custom solution.
    - During testing, a Raspberry Pi 3 was able to run through on processing cycle about every 10 seconds. That means Predator was able to take one frame, and scan it for license plates every 10 seconds. A Raspberry Pi 4 was able to do this same processing cycle in about 4 seconds. If you need something faster, you might want to consider a small-form-factor PC.


## Guidelines

As a general rule, these are the parts you'll need in a Predator device:

- Camera
    - Required (for real-time and dash-cam mode)
        - Without a camera, Predator will have no way of using real-time mode or dash-cam mode, and only pre-recorded mode will be usable.
- Processing
    - Required
        - Needless to say, Predator can't be run without a processing device.
    - This device could be anything from a high end workstation to a single-board-computer, like a Raspberry Pi.
- Input Device
    - Recommended
        - Without an input device, the only way to configure Predator will be remotely.
        - If your installation scenario makes an input device inconvenient or difficult to install, considering using wireless remote access via SSH.
- Display
    - Recommended
        - Without a display, Predator can only realistically run in headless mode, and it will be significantly harder to debug.
        - Once again, wireless remote access via SSH could entirely replace an external display, but this might not always be possible.
- Speaker
    - Recommended
        - A speaker allows Predator to play notification noises. Without a speaker, Predator will be able to function, but it won't be able to easily notify the user when a plate is detected.
    - Any speaker can be used, including an existing sound system in a car. As long as Linux can play an audio output to it, it should work fine.
- Mounting Hardware
    - Recommended
        - Without mounting hardware, your Predator device will be significantly harder to mount in your build.
- Networking
    - Optional
        - Predator is fully functional without being connected to a network. However, connecting to a network will allow Predator to download remote alert databases and use other optional features.
        - A typical installation will include a wireless adapter in order to allow Predator to download information from a wireless access point. However, a constant internet connection is unnecessary.
- GPS
    - Optional
        - Predator doesn't need a GPS to function. However, certain features won't be operational without it.


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
    - This processing device also takes several seconds to detect each license plate.
- Price Range: ~$100
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
