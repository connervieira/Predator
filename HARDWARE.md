# Hardware

Predator is primarily a software utility. However, it goes without saying that Predator is only useful if has hardware capable of collecting and processing video and image information. This document describes hardware information related to Predator, including parts list.


## Recommendations

This section contains recommendations for those looking to build a hardware device that runs Predator.

- The processing device should be fully capable of running Linux.
    - Having a device that can easily run Linux will make installing and setting up Predator drastically easier, as you'll spend less time troubleshooting compatability issues, and more time actually assembling and configuring your device.
- Camera color accuracy is practically irrelevant when it comes to Predator's ability to recognize license plates.
    - Even grayscale cameras should have no problems recognizing license plates.
- Consider the context of the situation you want to use Predator in, and consider how to align your camera and it's lens.
    - You should have your camera's lens zoomed in as far as reasonably possible.
        - For example, if you're installing Predator in a car, you may want to zoom in on the area in front of your car, where the license plate of the car in front of you is likely to be.
- Consider motion blur when setting up your camera.
    - As mentioned previously, zooming in as far as possible will increase Predator's ability to recognize plates at a distance. However, zooming in will also increase the effects of motion blur, since even tiny movements will shift the frame dramatically.
    - Ensure your camera is mounted somewhere stable enough that it can take clear images of the vehicles you're scanning, even while they are in motion.


## Builds

This section contains part recommendations. Please keep in mind that these parts are not guaranteed to work, and you shouldn't blindly purchase things in these lists.

Each build in this section has a nick-name to keep it distinct from the other builds, but each part list may change over time as better part combinations are found. Don't rely on these nick-names as a way to uniquely identify a parts list.

### Predator Scorpion

- Description: Predator Scorpion is designed for general use in vehicles, security systems, and other low-power applications that require medium to long distance scanning.
- Advantages:
    - All of the parts are physically small, and can be easily fit in tight places, like the interior of a vehicle.
    - The entire system is lightweight, making it easy to move around.
    - Each device is very low power usage, so it should be easy to install using existing infrastructure in your car, building, or other system.
- Price Range: ~$100
- Parts:
    - Camera: ELP-USB500W02M-SFV(5-50)
        - Price: ~$70
        - Resolution: 2592x1944
        - Frame Rate: 15FPS
            - Reduced Resolution Frame Rate: 30FPS
        - Lens: 5-50mm (10X optical zoom)
    - Processing: Raspberry Pi 4 B
        - Price: ~$30
        - Memory: 2GB
        - CPU: 4 Core, 1.5GHz ARM CPU 
    - Miscellaneous:
        - Necessary Cables
        - Mounting Hardware
            - Screws, adhesive, etc.
            - Necessary to hold the camera in a stable position.
