# Credits

Predator is primarily developed by V0LT. However, this wouldn't be possible without the hard work of dozens of other projects. This document contains credits to all of the software and people Predator depends on to function.


## People

### Brandon Paroff

Brandon is responsible for helping to create and print the camera mounting brackets used during the development of Predator. You can find these files in the `assets` folder.


## Software

### OpenALPR

OpenALPR is the heart of Predator. OpenALPR is an open source tool for scanning images and reporting back a list of potential license plates, along with confidence levels. Predator uses OpenALPR as it's primarly computer-vision tool.

<https://www.openalpr.com/>


### FFMPEG

FFMPEG is one of the most powerful video processing tools currently available, and it's what gives Predator it's ability to quickly process large amounts of video. Predator uses FFMPEG to automatically break up videos into individual frames based on user preferences.

<https://ffmpeg.org/>


### ImageMagick

ImageMagick is one of the most popular command-line image manipulating tools, and is critical to Predator's ability to manipulate individual frames of video.

<https://imagemagick.org/index.php>


### FSWebcam

FSWebcam is a simple utility designed to make interacting with external cameras as easy as possible. FSWebcam is the utility Predator uses to access connected cameras in real-time mode.

<http://www.sanslogic.co.uk/fswebcam/>


### GPSD

GPSD is a Linux utility designed to allow programs to interact with GPS devices plugged into a system. Predator uses GPSD to get the current location, speed, and other information.

<https://gpsd.gitlab.io/gpsd/index.html>
