# To-Do

This document quickly explains features that may be added to Predator in the future. This is an informal document, and it's typically used as a simple task tracker, not as change-log or official feature list.


## Planned

These are the features actively planned for Predator and are likely to be added within the near future.

- [X] Refine debug message function.
- [X] Add dashcam video saving.
- [X] Move object recognition logging configuration to the `saving` section.
- [X] Create documentation for interfacing with Predator.
- [X] Add automatic dashcam video segment clearing.
- [X] Add parking mode.
    - [X] Detect when the vehicle has been parked for a certain length of time.
    - [X] Detect motion to resume dashcam recording while parked.
- [X] Add GPS time verification.
- [X] Fix desynced video channels in dash-cam mode.
- [X] Add GPS demo mode.
- [X] Add configuration value to set maximum permitted framerate per capture device.
- [X] Add frames to queue before writing to disk.
- [X] Add the ability to disable dashcam capture devices from the configuration.
- [X] Fix dashcam saving when the first segment is saved.
- [X] Move status lighting configuration to general section.
- [X] Add individual resolution configuration for dashcam capture devices.
- [X] Add status light interfacing to dashcam mode.
- [X] Test dashcam saving with audio recording.
    - [X] Test when merging is enabled.
    - [X] Test when merging is disabled.
- [X] Test different output saving intervals.
- [X] Test background dash-cam recording.
- [X] Add remote motion detection alerts for dashcam mode via Reticulum.
- [X] Test configuration updates.
    - [X] Test config file reconciliation behavior.
    - [X] Test config behavior from sub-directories.
- [X] Add more dash-cam stamps.
    - [X] Add dash-cam operation mode stamp.
    - [X] Add custom relay status stamps through GPIO.
- [X] Add default config support for values that involve adding entries.
- [X] Improve the efficiency of the GPS stamp.
- [X] Check to see if old dashcam video files actually exist before deleting them.
- [X] Test GPS behavior.
- [X] Finish video framerate snapping.
- [X] Test the new ALPR system.
    - [X] Test pre-recorded mode.
    - [X] Test real-time mode.
    - [X] Test dash-cam mode.
- [X] Implement pre-recorded dash-cam side-car mode.
    - [X] Implement file generation.
    - [X] Convert plate corners to bounding box.
    - [X] Create file viewer.
- [X] Implement revised process exiting for real-time mode.
- [X] Finish alert documentation (ALERTS.md)
- [X] Fix frame counting for side-car mode.
- [X] Document `developer>frame_count_method` configuration value in `docs/CONFIGURE.md.
- [X] Validate multi-channel recording.
- [ ] Add sound effect for parking mode.


## Hypothetical

Features in this section may be added in the future, but are not actively planned.

