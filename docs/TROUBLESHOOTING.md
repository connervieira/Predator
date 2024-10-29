# Troubleshooting

This document lists specific problems that you may encounter, and suggested solutions.

All of these solutions assume you have already completed the full installation/configuration process.


## Dash-cam

### The audio recording process works for the first segment, but then occasionally fails for subsequent segments.

Try increasing the `dashcam>capture>audio>start_delay` value. It's likely the audio capture device is not being fully released by the previous segment before it tries to be accessed by the new segment.


### The audio is not synced up with the video (the audio is longer or shorter than the video).

Ensure that the video recording is running at a consistent frame-rate (and therefore, is a consistent length of time). For example, if your video flucuates between 32 and 37 FPS, try capping it at 30FPS to ensure a consistent frame-rate. This can be done with the `dashcam>capture>video>devices>DEVICE_NAME>frame_rate>max` configuration value.
