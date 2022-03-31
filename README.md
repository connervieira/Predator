# Predator

**Copyright 2022 V0LT - Conner Vieira**

A vision system primarily designed for license plate reading and general object recognition in both pre-recorded and real-time video.

![Predator LPRS header](./assets/images/branding/PredatorHeaderLight.svg)


## Disclaimer

While Predator is designed to be stable and reliable, you should not depend on it for safety or security critical tasks. See the SECURITY.md document for more information.


## Description

Predator is an advanced multipurpose platform focused on license plate reading and object recognition. Predator can analyze pre-recorded video from dashcams, security cameras, or other devices, as well as real-time video streams from live vehicle-mounted cameras and static webcams. In addition to video analysis, Predator is also capable of acting as a standard dash-cam or security camera, eliminating the need to install multiple devices for a single usage situation. When installed in a vehicle Predator can seamlessly detect objects and license plates as you drive, sending you alerts automatically based on customizable criteria. When installed as a stationary security camera, Predator can run in the background, sending information to webhooks, or using audio alerts to indicate important events.

Predator's license plate recognition is heavily based on OpenALPR, which is arguably the gold standard for license plate recognition in the open source software community. While OpenALPR provides a rock solid foundation, Predator adds dozens of powerful features that drastically amplify it's abilities. Through extensive customizability, Predator gives you the power to dial in the performance and accuracy of your camera system without ever needing an internet connection or central database. Regardless of what you're looking to accomplish, Predator gives you the means to get there.

Predator goes above just a computer vision platform. Making use of other data sources, like GPS devices, Predator can seamlessly provide alerts for potential points of interest, like speed cameras and red-light cameras. Once again, due to the sheer number of customizability options, all of Predator's alerting and monitoring functionality can be easily configured, disabled, or activated based on what you're looking to accomplish.


## General Features

### Lightweight

The Predator interface uses very little resources, allowing the majority of your processing power to remain available for license plate recognition, object detection, and database analysis.

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

### Database Alerts

While Predator's powerful real-time video analysis can provide useful information to the driver, Predator also supports offline database alerts for known locations of speed cameras and red-light cameras. Using a connected GPS, Predator can alert the driver when alerting a known point of interest.

### Documented

Predator's extreme customizability can be a bit overwhelming to new users. For this reason, Predator is extensively documented, and comes bundled with step-by-step guides on how to download it, install it, configure it, and run it.


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
