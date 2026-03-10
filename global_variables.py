def init():
    global predator_running
    predator_running = True

import threading
shutdown_event = threading.Event() # This event is called when Predator exits (in sync with global_vars.predator_running)
