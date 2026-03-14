# This is a stand-alone helper script to help identify the GPIO pin numbers on a FT232H USB GPIO module. It opens inputs on all pins specified in `PINS`, and prints any state changes.
# This can be used to confirm the pin IDs that your physical controls/triggers are connected to.

PINS = [
    "C0",
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
    "C6",
    "C7"
]

import time
import os
os.environ.setdefault('BLINKA_FT232H', '1')

import board
import digitalio


# Initialize all pins as inputs:
buttons = {}
for pin in PINS
    buttons[pin] = digitalio.DigitalInOut(getattr(board, pin))
    buttons[pin].direction = digitalio.Direction.INPUT

# Endlessly monitor for pin state changes.
last_state = {}
while True:
    current_state = {}
    for pin in PINS:
        current_state = buttons[pin].value

    if (current_state != last_state): # Check to see if the state changed this frame.
        print(current_state)
    last_state = current_state
