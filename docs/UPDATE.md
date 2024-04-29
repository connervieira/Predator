# Installation

This document explains how to update Predator from one version to another.


## Checking Dependencies

After downloading the new version of Predator, you should check its documentation files to see if any dependencies have been changed since the version you're currently running. Predator's dependencies can typically be found in the `docs/INSTALL.md` file, though older versions may have the dependencies listed in the `DOCUMENTATION.md` file.


## Updating Configuration

This is the most technical step in updating Predator. There are a few different ways to go about moving your configuration to a different version of Predator.

### Automatic (Recommended)

### Refresh

The most reliable way to update your configuration is to simply replace it with the default `assets/support/configdefault.json` file from the new version of Predator, and manually copy over the important values from your old configuration file. This method makes it much less likely that you'll accidentally use an incompatible configuration file.

### Brute Force

If you've made extensive changes to your configuration file, and don't want to manually re-configure the new version, you can try directly copying your current `config.json` file over the one from the new version. Predator's configuration file often changes dramatically from version to version, so this will almost certainly require some adjustments to your configuration file to make to make it compatible.

When you first run Predator using your original configuration file, you will likely see several errors about missing or invalid configuration values. You should take note of the invalid configuration values, and use the information found in the [docs/CONFIGURE.md](docs/CONFIGURE.md) file to modify the `config.json` file to correct the invalid values. It is likely that some values listed as invalid will be completely missing from your original configuration file. In this case, you may want to copy them from the default configuration file that came with the new version of Predator.


## Troubleshooting

If you run into problems, and want to completely reset Predator and start fresh, you can do so with the following steps:

1. Erase the contents of the working directory (as defined in `config.json` under `general>working_directory`).
2. Erase the contents of the interface directory (as defined in `config.json` under `general>interface_directory`).
3. Replace the `config.json` file with the default `config.json` file that comes with the new version of Predator.
