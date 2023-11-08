# Integration

This document explains how external local programs can interface with Predator.


## Collection

Predator uses various files to share information with external programs. External programs can read these files to collect information from Predator.

### Status

Basic status information is shared with external programs in the form of 'heartbeats'. Each time a processing cycle is completed, a timestamp is added to the `heartbeat.json` file, located in the interface directory. Old entries in this file are trimmed after a certain threshold, as defined in the configuration. These timestamps are analogous to a real heartbeat, in that they signal to external services that Predator is alive and actively running. The frequency of heartbeats is dependent on the processing speed of the device Predator is running on, but the interval is usually less than 5 to 10 seconds, even on low-power devices.

Example file contents:

```json
[
    1677690941.7604642,
    1677690942.3249989,
    1677690943.4345562,
    1677690944.6840843,
    1677690946.1587856
]
```


### Plates

Information about the license plates detected by Predator is saved to the `plates.json` file. Each time a processing cycle is completed, an entry in this file is added, using the current Unix timestamp as the key. If no plates were detected, this entry will be empty. When one or more plates are detected, a dictionary will be added for each detected plate, containing all of the guesses for that plate with confidence levels. The key for each plate will be the most likely guess.

This file is unrelated to the normal license plate log file, and disregards the `realtime>saving>license_plates>` configuration values.

Example file contents:

```json
{
    "1677861070.712512": {
    },
    "1677861072.284712": {
        "KVH8151": {
            "KVH8151": 92.113914,
            "KVH81S1": 83.792648,
            "KVH8I51": 82.17038,
            "KVH811": 80.023598
        },
        "ISO5122": {
            "ISO5122": 97.697231,
            "IS05122": 94.220752,
            "IS05I22": 82.465191
        }
    }, 
    "1677861074.512752": {
        "KVH8I53": {
            "KVH8I53": 91.512873,
            "KVH81S": 81.511251
        }
    }
}
```


### Errors

Every time an error is encountered and displayed on screen, and identical error message is added to the `errors.json` file. This file contains a JSON dictionary, where each error uses the time it occurred as a key. The contents of this file are not automatically cleared. The message is stored under the "msg" field in the JSON dictionary. The "type" field will be a string set to either "error" or "warn", depending on the type of message.

Example file contents:

```JSON
{
    "1677890942.18778": {
        "msg": "The local ignore list file does not exist. The local ignore list is disabled.",
        "type": "error"
    },
    "1677890942.217734": {
        "msg": "Invalid configuration option: ['config>developer>ignore_list>local_file']",
        "type": "error"
    }
}
```


## Triggers

In addition to the files for sharing information from Predator to external programs, external programs can use create specific files to trigger certain events in Predator.

### Dashcam Saving

When an important event happens while driving, a user may want to save a specific dashcam video segment to a separate folder so that it doesn't get accidentally deleted. This is referred to as "locking" or "saving" a dashcam video.

Dashcam saving can be triggered by create the file specified by the `dashcam>saving>trigger` configuration value inside the interface directory. When this file is created, Predator will save the current dashcam video to the configured directory, then delete the trigger file. The trigger file does not need to contain any information. Only its existence is required to trigger Predator.
