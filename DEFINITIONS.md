# Definitions

This document contains definitions for several terms used in Predator.


## General

### ALPR

ALPR stands for 'automated license plate reading', and is the practice of automatically scanning, detecting, and reading vehicle license plates using a computer.


## Predator

### Mode

Predator uses the term 'mode' to describe the various ways it can operate. Each of Predator's modes have unique functionality designed to be used in a specific situation.

### Path

The term 'file path', 'directory path', or simply 'path' are used to refer to a location on a computer's file system. Predator uses 3 terms to refer to file paths, as defined here.

- Absolute
    - An "absolute" file path refers to a direct path on the file system, starting from the root of the filesystem.
    - Examples:
        - `/home/pi/Software/PredatorData/`
        - `/home/pi/Downloads/file.txt`
- Working Directory Relative
    - This type of path is defined relative to the current working (project) directory.
    - This kind of file path is typically used to define files that will change each time Predator runs, including analysis videos and a export information.
    - For example, a file path defined relative to the root project directory as `data/file.txt`, when the current root project directory is `/home/pi/Downloads/`, will translate to a complete file path of `/home/pi/Downloads/data/file.txt`
- Predator Directory Relative
    - This type of path is defined relative to the directory of Predator itself.
    - This kind of file path is typically used to define files that should be moved around with Predator, including configuration files and logs.
    - For example, a file path defined relative to the Predator directory as `config.json`, when Predator's directory is `/home/pi/Downloads/Predator`, will translate to a complete file path of `/home/pi/Downloads/Predator/config.json`

### Preference

A preference is a user setting defined when Predator launches. These settings are temporary, and are configured each time Predator boots.

### Configuration

A configuration value is a setting defined in Predator's configuration file. These settings are persistent, and don't change between restarts unless specifically modified.
