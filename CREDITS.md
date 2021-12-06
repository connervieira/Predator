# Credits

This document contains credits to all of the software Predator depends on to function.


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


### GNU AWK

AWK is a GNU utility for manipulating text. Predator uses AWK to handle data output by OpenALPR during image processing.

<https://www.gnu.org/software/gawk/>
