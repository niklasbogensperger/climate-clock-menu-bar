# openconnect-menu-bar

SwiftBar/xbar plugin to see the climate clock deadline from [climateclock.world](https://climateclock.world/) in the menu bar


## Purpose

This script provides a countdown clock to the deadline set by [climateclock.world](https://climateclock.world/) (until which we need to limit global warming to 1.5°C) to the macOS menu bar using either of these two apps:
- [SwiftBar (recommended)](https://github.com/swiftbar/SwiftBar)
- [xbar](https://xbarapp.com/)


## Screenshot

![Screenshot](./screenshot.png)


## Setup

### 1. Install the latest SwiftBar or xbar release

- [SwiftBar (recommended)](https://github.com/swiftbar/SwiftBar)
- [xbar](https://xbarapp.com/)


### 2. Ensure you have Python3 and the required packages installed

Install python3 e.g. with the [homebrew package manager](https://brew.sh):
```shell
brew install python3
```

Furthermore, the following two packages are needed from PyPi:
- pendulum
- requests

Install them e.g. via pip (your setup may differ):
```shell
pip3 install --user pendulum requests
```


### 3. Download the "climate_clock.15m.py" script

1. [Download](https://github.com/niklasbogensperger/climate-clock-menu-bar/blob/main/climate_clock.15m.py) the file
2. Copy/Move it to the SwiftBar/xbar script folder that you or the app chose
3. Make sure the file is executable: `chmod +x climate_clock.15m.py`


### 4. Miscellaneous tips/tricks and notes

- Hold the <kbd>⌥ Option</kbd> key while clicking on the menu bar entry to bring up SwiftBar options that are hidden by default (only applies to SwiftBar)
- Hold the <kbd>⌘ Command</kbd> key to drag the menu bar entry to the desired spot
