# climate-clock-menu-bar

SwiftBar/xbar plugin to see the climate clock deadline from [climateclock.world](https://climateclock.world/) in the menu bar


## Purpose

This script provides a countdown clock to the deadline set by [climateclock.world](https://climateclock.world/) (until which we need to limit global warming to 1.5°C) to the macOS menu bar using either of these two apps:
- [SwiftBar (recommended)](https://github.com/swiftbar/SwiftBar)
- [xbar](https://xbarapp.com/)

To minimize API calls and provide better performance, it keeps the current deadline in a cache file (see instructions below) and only queries the API once every 24h, as the value gets adjusted rarely.


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
2. Open it in a plain text editor or IDE of your choice
3. Set the configuration variables according to your liking (or leave the optional ones as the default); see also next section below
4. Copy/Move it to the SwiftBar/xbar script folder that you or the app chose
5. Make sure the file is executable: `chmod +x climate_clock.15m.py`


### 4. Configuration options

The (absolute) path to use for the cache file should be set with the `CACHE_FILE` variable. The default file name is `.climate_clock_timestamp.json`, but can be changed as well.<br />
**Note**: If you direct this file to the folder where you save your SwiftBar plugins, you should keep it hidden with the leading period in the filename. Otherwise, SwiftBar will think it is a plugin file as well and throw an error. (This behavior is not tested for xbar.)

In addition, you can easily tweak how the clock gets displayed in the menu bar:<br />
`LABELS_LONG` controls whether to use long or short labels, and `MINUTES_SECONDS` controls whether to show a full clock with minutes and seconds or just the hours with a label.<br />
**Note**: When using the `MINUTES_SECONDS` option, you should set the refresh rate of the script accordingly (in the filename itself, see [here](https://github.com/swiftbar/SwiftBar#plugin-naming)). 

Refer to the table below to see which format you prefer.

| `LABELS_LONG` | `MINUTES_SECONDS` | Output                  | Notes                                |
| ------------- | ----------------- | ----------------------- | ------------------------------------ |
| False         | False             | 0 ʏ 000 ᴅ 00 ʜ          | default                              |
| False         | True              | 0 ʏ 000 ᴅ 00:00:00      | adjust refresh rate (see note above) |
| True          | False             | 0 ʏʀꜱ 000 ᴅᴀʏꜱ 00 ʜʀꜱ   |                                      |
| True          | True              | 0 ʏʀꜱ 000 ᴅᴀʏꜱ 00:00:00 | adjust refresh rate (see note above) |


### 5. Miscellaneous tips/tricks and notes

- Hold the <kbd>⌥ Option</kbd> key while clicking on the menu bar entry to bring up SwiftBar options that are hidden by default (only applies to SwiftBar)
- Hold the <kbd>⌘ Command</kbd> key to drag the menu bar entry to the desired spot
