# V0LT Predator
# This script is a helper used to relay the state of GPIO inputs to another device running Predator, over a network.

# ======== Configuration ========
pins_to_monitor = [17, 19] # GPIO pin IDs to monitor
port = 5000 # Network port to transmit pin states.
# ====== End Configuration ======

import os
import json
import socket
from gpiozero import Button


# This will hold the state of each pin
state = {pin: False for pin in pins_to_monitor}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', port))
server_socket.listen(1) # Listen for one connection.

connection, address = server_socket.accept() # Accept a connection
print(f"Connection from {address}")

def update_and_send_state(pin, pressed):
    state[pin] = pressed
    send_state()

def send_state():
    state_json = json.dumps(state)
    connection.sendall(state_json.encode())


for pin in pins_to_monitor:
    button = Button(pin)
    button.when_pressed = lambda pin=pin: update_and_send_state(pin, True)
    button.when_released = lambda pin=pin: update_and_send_state(pin, False)

try:
    print("Running (Press Ctrl+C) to exit")
    while True:
        pass # Keep the server running
except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    connection.close()
    server_socket.close()
