# Predator
# reticulum.py
# This script handles communication with remote nodes over the Reticulum network stack. To learn more about Reticulum (a third party, open source project), visit https://reticulum.network/

# Copyright (C) 2026 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.




# This script contains functions for interacting with services over the Reticulum network protocol.



import os # Required to interact with certain operating system functions

import config # `config.py`
load_config = config.load_config
config = load_config()


import LXMF
import RNS
import time
import utils
display_message = utils.display_message
debug_message = utils.debug_message


rns = RNS.Reticulum() # Initialize Reticulum.
lxmf_router = LXMF.LXMRouter(storagepath="/tmp/predatorlxmf")

if (os.path.exists(config["dashcam"]["notifications"]["reticulum"]["identity_file"]) == False):
    new_identity = RNS.Identity()
    new_identity.to_file(config["dashcam"]["notifications"]["reticulum"]["identity_file"])

debug_message("Loading Reticulum identity file")
identity = RNS.Identity().from_file(config["dashcam"]["notifications"]["reticulum"]["identity_file"])

debug_message("Announcing Reticulum source")
source = lxmf_router.register_delivery_identity(identity, display_name="Predator")
lxmf_router.announce(source.hash) # Announce this instance.
last_announce = time.time()

def lxmf_send_message(message, destination):
    global lxmf_router
    global config

    if (time.time() - last_announce > 30*60):
        debug_message("Announcing Reticulum source")
        lxmf_router.announce(source.hash) # Announce this instance.

    debug_message("Identifying Reticulum destination")
    recipient_hash = bytes.fromhex(destination)
    if not RNS.Transport.has_path(recipient_hash): # Check to see if the destination is currently unknown.
        RNS.Transport.request_path(recipient_hash)
        start_time = time.time()
        while not RNS.Transport.has_path(recipient_hash): # Wait until the destination is known.
            if (time.time() - start_time > 10): # Check to see if the request has been stuck for more than a certain number of seconds.
                display_message("Failed to determine Reticulum destination.", 2)
                break
            time.sleep(0.1)
    recipient_identity = RNS.Identity.recall(recipient_hash)
    dest = RNS.Destination(recipient_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, "lxmf", "delivery") # Establish the LXMF destination.

    debug_message("Sending Reticulum message")
    lxmf_request = LXMF.LXMessage(dest, source, message, "Predator", desired_method=LXMF.LXMessage.DIRECT)
    lxmf_router.handle_outbound(lxmf_request)
    time.sleep(0.01) # Pause for a brief destinationmoment to let the outbound request be processed by Reticulum.
