# Documentation

This document contains the information you need to know to set up and use Predator


## Installation

This is the installation process for Predator and all of it's dependencies.

1. Install OpenALPR
    - Since Predator is a front-end for OpenALPR, you'll need to install it for it to work properly.
    - You can learn about the OpenALPR installation process at <https://github.com/openalpr/openalpr>
    - After installing, you should be able to run OpenALPR using the `alpr` command.
2. Install FFMPEG
    - Predator uses FFMPEG to process videos.
    - You can install FFMPEG using the following command on a Debian based Linux machine:
    - `sudo apt-get install ffmpeg`
3. Install ImageMagick
    - Predator uses ImageMagick to manipulate frames of video.
    - You can learn about the ImageMagick installation process at <https://imagemagick.org/script/download.php>
4. Download Predator.
    - Predator can be downloaded either from the V0LT website, or from it's GitHub page. The download straight from the V0LT website is recommended for sake of stability and completeness, but you're free to use GitHub as well if you're OK with using a less stable version of Predator.
    - V0LT website: <https://v0lttech.com/predator.php>
    - GitHub page: <https://v0lttech.com/predator.php>
        - `git clone https://github.com/connervieira/Predator`
5. Extract Predator
    - After downloading Predator, regardless of where you get it from, extract it from the compressed archive (if necessary), and place it somewhere on your filesystem.


## Configuration

After installing Predator, you'll need to do some quick configuration to be able to use it properly.

1. Open the Predator configuration
    - Open the `main.py` file in the Predator folder using your text editor of choice.
    - Navigate to the top of the document, and locate the 'CONFIGURATION START' section.
2. Set the location of the `crop_image` script
    - The `crop_image` script is the script used by Predator to crop down individual frames of video.
    - The script is located in the Predator folder, along side the `main.py` file.
    - Simply set the `crop_script_path` to an absolute path pointing to the script.
    - For example: `crop_script_path = "/home/user/Downloads/Predator/crop_image"`
3. Configure the margin that will be cropped out of the frames.
    - Since the majority of camera setups (especially dashcams) will see far more than just license plates, it's important to crop images down to increase the likelihood of detecting license plates.
    - Determine how much Predator will crop out of each image by modifying the appropriate variables.
    - For example, setting `top_margin = "500"` will cause Predator to crop out the top 500 pixels of each frame.


## Usage

After configuring Predator, you can try it out for the first time!

1. Run Predator
    - To run Predator, simply navigate to it's folder, then run `main.py` using the `python3` command.
        - `python3 main.py`
    - After Predator starts, you should see a large banner reading 'PREDATOR LPRS'
2. Set preferences
    - Next Predator will prompt you to set your preferences for this session.
    - First, you'll be asked to set the root project folder. Simple create an empty folder, then place your video(s) into it. Specify the absolute path to this folder here.
        - Example: `/home/cvieira/Downloads/MyProjectFolder`
    - Next, you'll be asked to enter the file name of the video you want to analyze. This video should be placed in the root project directory you just specified.
        - Example: `MyVideo.mp4`
    - Finally, you'll be asked how many second you want to wait between frames for analysis. Since it would be inefficient to process every single frame of video, this value is used to only take frames every N seconds. You can think of this value as "only process a frame every N seconds of video"
    - Example: `2` will take a frame to process every 2 seconds of video. This would break up a 10 second video into 5 frames.
3. Run Predator
    - After finishing setting up your preferences, Predator will begin running automatically.
    - You should note that while Predator is running it's analysis, you'll notice a folder named 'frames' appear in the project folder. Individual frames will begin to appear in this folder as Predator runs. Do not modify or delete these, since Predator will repeatedly access and modify these during the course of it's analysis. After analysis completes, you can safely delete these files.
4. Manipulate results
    - After Predator finishes running, you'll be prompted to "Press enter to continue". After pressing enter, you'll see the analysis menu.
    - This menu has 4 options.
        0. Quit
            - Enter '0' into the selection to quit Predator.
        1. View data
            - Enter '1' into the selection to open up further options for viewing the data collected by Predator.
        2. Export data
            - Enter '2' into the selection to open up further options for exporting the data collected by Predator.
        3. Manage raw analysis data
            - Enter '3' into the selection to view or export the raw data collected by Predator, before sanitization and validations takes place. In other words, this data is every single plate detected by Predator, regardless of whether it matches the formatting guidelines.
