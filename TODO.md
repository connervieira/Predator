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
- [ ] Add frames to queue before writing to disk.


## Hypothetical

Features in this section may be added in the future, but are not actively planned.

- [ ] Add more stamp options to dash-cam mode.
    - [ ] Add custom relay status stamps through GPIO.
    - [ ] Add dash-cam operation mode stamp.
- [ ] Add individual resolution configuration for dashcam capture devices.
- [ ] Add status light interfacing to dashcam mode.
- [ ] Add remote motion detection alerts for dashcam mode via Reticulum.
