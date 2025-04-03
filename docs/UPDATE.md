# Installation

This document explains how to update Predator from one version to another.


## Checking Dependencies

After downloading the new version of Predator, you should check its documentation files to see if any dependencies have been changed since the version you're currently running. Predator's dependencies can typically be found in the `docs/INSTALL.md` file, though older versions may have the dependencies listed in the `DOCUMENTATION.md` file.


## Updating Configuration

This is the most technical step in updating Predator. There are a few different ways to go about moving your configuration to a different version of Predator.

### Automatic (Recommended)

Predator versions 12.0 and later can automatically reconcile differences between the existing configuration file and the default configuration from the new version. To use this feature, simply update Predator, leaving your existing `config.json` file in place. On first start-up, Predator will compare the active configuration file with the version's default, and reconcile differences. Values that only exist in the active configuration will be removed. Values that only exist in the default configuration file will be added to the active configuration. Modified values will remain unchanged.

### Refresh

The most reliable way to update your configuration is to simply replace it with the default `assets/support/configdefault.json` file from the new version of Predator, and manually copy over the important values from your old configuration file. This method makes it much less likely that you'll accidentally use an incompatible configuration file. However, this will require you to fully re-configure Predator from scratch.

## Troubleshooting

If you run into problems, and want to completely reset Predator and start fresh, you can do so with the following steps:

1. Erase the contents of the working directory (as defined in `config.json` under `general>working_directory`).
2. Erase the contents of the interface directory (as defined in `config.json` under `general>interface_directory`).
3. Replace the `config.json` file with the default `assets/support/configdefault.json` file that comes with the new version of Predator.
