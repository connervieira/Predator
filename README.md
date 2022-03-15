# Predator

A vision system primarily designed to read license plates in both pre-recorded and real-time video.

![Predator LPRS header](./assets/images/branding/PredatorHeaderLight.svg)


## Disclaimer

While Predator is reliable and resilient, you should not use it for safety critical tasks. Do not depend on Predator to autheticate cars at entry points, detect intruders, or monitor criminal activity unless you are fully prepared for it to fail.


## Description

Predator is a powerful camera and video processing tool designed to detect license plates in both real-time and in pre-recorded videos. Predator uses OpenALPR as it's back-end, and adds dozens of powerful features ontop of OpenALPR's already strong performance. Predator is designed to process large amounts of video efficiently on both high end hardware and affordable, low-power device, which makes it extremely versatile. It's designed to be highly customizable, allowing it to fit into any use case, ranging from a static video processing workstation, to a fully offline mobile real-time detection system.


## General Features

### Lightweight

Predator is a command line utility that uses very little resources, allowing the majority of your processing power to remain available for OpenALPR.

### Offline

Predator works entirely offline, and never needs to connect to the internet to function. Predator only ever makes network requests when the user actively asks it to download information from a network host.

### Free

Predator is completely free to use, and contains absolutely no ads or data mining of any kind.

### Open Source

Predator is free and open source from top to bottom, and is 'free software', meaning you can make changes and distribute them to others freely.

### Generic

By design, Predator doesn't require specialized hardware to run. While higher resolution cameras will obviously yield better results, any video format supported by FFMPEG will work with Predator.

### Easy

While being technically mindedly will certainly help, Predator doesn't require professional installation or setup to function. As long as you're reasonably experienced with the Linux command line, setting up Predator should be a piece of cake.

### Private

Since Predator is open source, self hosted, offline, and self contained, you can rest assured that it's completely private, and it doesn't collect any of the information you provide it.

### Multipurpose

Predator is deliberately designed to be multipurpose. It can operate both as an analysis tool for pre-recorded video, as well as a real-time monitoring program. Predator can even act as a standalone dashcam when license plate reading is unnecessary.

### Customizable

Predator is extremely customizable, making it easy to fit into any use case. Whether you want an intelligence security camera, or a powerful dashcam device, Predator can be adjusted to fit your needs.

### Mobile

Predator is designed to support low-energy-usage hardware such that it can be easily installed in a vehicle. A single USB port is enough to power an entire Predator system.

### Location Aware

Predator supports GPX files to allow for correlating license plates detected in pre-recorded video to their physical coordinates.

### Alerts

Predator supports customizable real-time alerts, allowing the user to be notified when a license plate matching one on a list is detected through audible sound alerts, visual cues, webhooks, and even push notifications!

### Safe

Predator is designed to be safe, regardless of the installation context. It's easy to configure Predator to completely hands free, ensuring that you don't have to look away from the road when Predator runs in a mobile context.

### Dash-cam

Predator comes with a dash-cam mode, allowing for customizable real-time recording without processing license plates. Dash-cam videos can later be processed by Predator in pre-recorded mode. Predator's dash-cam mode allows for multi-channel recording, making it easy to simultaneously record multiple angles using multiple cameras.

### Headless Ready

While Predator comes with a straight forward interface, it can be fully configured to run in headless mode, without any user interaction necessary. This makes it perfect for vehicle installations, where the driver wants Predator to automatically start when the vehicle turns on without any user input.

### Object Recognition

In addition to license plate scanning, Predator also supports general object recognition. It can collect a list of common objects and save them to a file, making it easy to find important events in recorded video.

## Screenshots

### Real-time Mode Alert

When operating in real-time mode, Predator can display alerts when it detects a plate found in a configured database.

![Alert hit sample image](./assets/images/screenshots/alerthit.png)

### Pre-recorded Mode Sample Image

While operating in pre-recorded mode, Predator can analyze any video, including dashcam video

![Dashcam sample image](./assets/images/screenshots/dashcamsample.png)

### Pre-recorded Sample Analysis

After scanning through an entire pre-recorded video based on user-configured preferences, Predator can display and export all of the plates it detected.

![Dashcam analysis output](./assets/images/screenshots/dashcamdetect.png)
