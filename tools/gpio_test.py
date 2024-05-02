# V0LT Predator
# GPIO Test

import os # Required to interact with certain operating system functions
import json # Required to process JSON data
import time

from gpiozero import Button
from signal import pause

def on_press():
    print("BUTTON PRESSED")

def watch_button(pin, event=on_press):
    print("Watching pin " + str(pin))
    button = Button(pin)

    time_pressed = 0
    last_triggered = 0
    while True:
        if (button.is_pressed and time_pressed == 0): # Check to see if the button was just pressed.
            print("Pressed")
            time_pressed = time.time()
        elif (button.is_pressed and time.time() - time_pressed < 1): # Check to see if the button is being held, but the time threshold hasn't been reached.
            print("Holding")
        elif (button.is_pressed and time.time() - time_pressed >= 1): # Check to see if the button is being held, and the time threshold has been reached.
            if (time.time() - last_triggered > 1):
                print("Triggered")
                event()
            last_triggered = time.time()
        elif (button.is_pressed == False):
            time_pressed = 0

        time.sleep(0.1)

watch_button(17)
