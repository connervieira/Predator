# Uninstalling

This document contains detailed instructions on how to uninstall Predator, and any traces it might leave.


## Erase Support Files

Predator only places support files in the working directory and interface directory (as specified in `config.json`). Erasing these directories should erase all files created by Predator that haven't been manually transferred to other folders.

If you use Phantom as your ALPR back-end, you may also want to erase the temporary image file found at `/dev/shm/phantom-webcam.jpg`. This file is automatically erased every time the system restarts.


## Uninstall Dependencies

Depending on your use case, you may want to uninstall the dependencies listed in [INSTALL.md](INSTALL.md).
