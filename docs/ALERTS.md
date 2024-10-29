# Alerts

This document explains the format used by Predator alert databases.

## Overview

Predator is capable of loading alert lists from both local files and remote sources. Alert lists come in the form of a JSON dictionary.

Here is a break-down of each value in an alert database:

- `rule`: Each top-level key in the alert database should be a license plate rule that will trigger the alert.
    - `name`: This is an optional value that contains a human-friendly name for this alert.
    - `description`: This is an optional value that contains a brief human-friendly description of this alert.
    - `author`: This is an optional value that contains the author name associated with this alert.
    - `source`: This is an optional value that describes where the information for this alert was sourced from.
    - `vehicle`: This is an optional value that contains information about the vehicle this alert is associated with.
        - `color`: This is an optional sub-value for the vehicle color (all lowercase, human-friendly name).
        - `make`: This is an optional sub-value for the vehicle manufacturer.
        - `model`: This is an optional sub-value for the vehicle model.
        - `year`: This is an optional sub-value for the vehicle year. This value should be an integer.


## Examples

### Bare Minimum

This is an example of an alert database with the bare minimum information. This database will trigger alerts for the following plates: AAA1111, BBB2222, CCC3333.

```JSON
{
    "AAA1111": {},
    "BBB2222": {},
    "CCC3333": {}
}
```

### Full Information

This is an example of an alert database with all supported information included. This database will trigger alerts for the following plates: AAA1111, XYZ1234, ABC1234

```JSON
{
    "AAA1111": {
        "name": "Test Alert",
        "description": "A testing alert to verify Predator's alert functionality",
        "author": "V0LT",
        "source": "V0LT",
        "vehicle": {
            "color": "red",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2021
        }
    },
    "XYZ1234": {
        "name": "AMBER Alert",
        "description": "A testing alert that takes the form of an AMBER alert",
        "author": "V0LT",
        "source": "Ohio State Highway Patrol",
        "vehicle": {
            "color": "black",
            "make": "Subaru",
            "model": "Impreza",
            "year": 2016
        }
    },
    "ABC1234": {
        "name": "Test Alert",
        "description": "A testing alert to verify Predator's alert functionality",
        "author": "V0LT",
        "source": "V0LT",
        "vehicle": {
            "color": "blue",
            "make": "Honda",
            "model": "Accord",
            "year": 2011
        }
    }
}
```
