# Documentation

This document contains the information you need to know to set up and use Predator.


## Installation

For installation instructions, see [docs/INSTALL.md](docs/INSTALL.md).

If you want to quickly deploy the entire Predator ecosystem automatically (including Phantom ALPR, Optic, and Cortex) on a system running a clean install of Debian, Raspbian, Ubuntu, or similar Linux distribution, you can do so by authenticating as root using the `sudo su` command, then running the following script: `curl https://v0lttech.com/predator/autodeploy/autoinstall.sh | bash`. **This script should only be run on systems dedicated to the usage of Predator**, since it will overwrite and erase files without consideration for other software. While the script will generally work just fine with other software (particularly programs written by V0LT, like Assassin and Parallax), you should not run it on a system with files you're unwilling to lose.


## Configuration

The steps for configuring Predator, as well as complete descriptions of all configuration values, can be found in the [docs/CONFIGURE.md](docs/CONFIGURE.md) document.


## Usage

To learn more about how to start and use Predator's various modes, see the [docs/USAGE.md](docs/USAGE.md) file.


## Hardware

Once you have the Predator software up and running, you may want to focus more on the hardware you plan to run it on. You can learn more about hardware requirements in the [docs/HARDWARE.md](docs/HARDWARE.md) file.


## Debugging

To learn how to use Predator's debug message feature to troubleshoot problems and improve processing speed, see the [docs/DEBUGGING.md](docs/DEBUGGING.md) file.


## Integration

Predator has several features that allow external programs to interface with it. To learn more about how to interface with Predator from external programs, see the [docs/INTEGRATION.md](docs/INTEGRATION.md) document.


## Updating

Updating between Predator versions may require certain steps to be repeated. To learn more about moving between Predator versions, see [docs/UPDATE.md](docs/UPDATE.md).
