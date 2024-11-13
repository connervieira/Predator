# Auto Install

Here you can learn about the auto-install script for the Predator ecosystem, and the requirements for using it.


## Disclaimer

**This script should only be run on systems dedicated to the usage of Predator.** This script erases and overwrites files without prompting the user. Do not use this script on a system with files you don't want to lose. Ideally, this script should only be used on a clean OS install.

This script **is not** designed to be run on your normal, every-day computer. Rather, it is designed to quickly deploy Predator on a dedicated system. In other words, if you want to install Predator on your main computer for sake of testing, experimentation, or development, you should not use this script. If you instead want to install the Predator ecosystem on a computer dedicated to ALPR, dash-cam recording, or other Predator functionality, this script can be an extremely conveinent way to do so.

Predator, Cortex, and Optic assume that your username is "pi" by default. If the primary user on your system has a different username, you'll have to manually reconfigure each component after the installation script finishes.


## Support

This script should work on practically any Debian/Ubuntu based operating system, including Raspberry Pi OS, Pop!\_OS, and Mint.

It has been successfully tested on the following platforms:
- Raspberry Pi 5 (4GB) - Raspberry Pi OS Lite (64bit)
- LibreComputer AML-S905X-CC-V2 - Raspbian 12 (64bit)


## Components

The auto-install script will install the following components:
- Predator (<https://v0lttech.com/predator.php>)
- Phantom ALPR (<https://v0lttech.com/phantom.php>)
- Optic (<https://v0lttech.com/optic.php>)
- Cortex (<https://v0lttech.com/cortex.php>)

## Usage

To use the auto-install script, simply authenticate as root, then execute the latest version of the script. This can be done with the following commands:

1. `sudo su`
2. `curl https://v0lttech.com/predator/autodeploy/autoinstall.sh | bash`
