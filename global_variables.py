import os

def init():
    global PREDATOR_VERSION
    global PREDATOR_RUNNING
    global PREDATOR_ROOT_DIRECTORY
    global CONFIG_PATH

    PREDATOR_VERSION = "V12.0 (Pre-release)"
    PREDATOR_RUNNING = True
    PREDATOR_ROOT_DIRECTORY = str(os.path.dirname(os.path.realpath(__file__)))
    CONFIG_PATH = os.path.join(PREDATOR_ROOT_DIRECTORY, "config.json")

import threading
shutdown_event = threading.Event() # This event is called when Predator exits (in sync with global_vars.PREDATOR_RUNNING)
