#! /usr/bin/env python3

#########################################################
# XBAR / SWIFTBAR METADATA #
#########################################################

# <xbar.title>Climate Clock</xbar.title>
# <xbar.version>v1.2</xbar.version>
# <xbar.author>Niklas Bogensperger</xbar.author>
# <xbar.author.github>niklasbogensperger</xbar.author.github>
# <xbar.desc>Climate clock deadline from climateclock.world in the menu bar</xbar.desc>
# <xbar.dependencies>python, pendulum, requests</xbar.dependencies>
# <xbar.abouturl>https://github.com/niklasbogensperger/climate-clock-menu-bar</xbar.abouturl>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>


import json
import os

import pendulum
import requests

#########################################################
# CONFIGURATION #
#########################################################

# CUSTOMIZE AT LEAST THIS VARIABLE BEFORE RUNNING
# file to use for the cache (name can be changed); file should not yet exist and path should be absolute
# when saving to SwiftBar scripts folder: keep leading dot (.) in filename to skip registering the file as another SwiftBar plugin
CACHE_FILE = "/absolute/path/to/folder/of/choice/.climate_clock_timestamp.json"

# whether to use long or short labels (e.g. "ʏʀꜱ" vs. "ʏ")
LABELS_LONG = False
# whether to display minutes and seconds as well (set refresh rate of script to 1s (or a bit less))
MINUTES_SECONDS = False

# change in the event of the API URL changing
# (likely would require changes in code as well)
API_URL = "https://api.climateclock.world/v2/clock.json"

#########################################################


def query_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error querying API: {e}")
        return None

    try:
        data = response.json()
        deadline = data['data']['modules']['carbon_deadline_1']['timestamp']
        return deadline
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
    except KeyError as e:
        print(f"Error extracting deadline from response: {e}")
        return None


def read_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as file:
                cache_data = json.load(file)
                timestamp = cache_data.get('timestamp')
                deadline = cache_data.get('deadline')
                return timestamp, deadline
    except (IOError, json.JSONDecodeError, KeyError) as e:
        print(f"Error during cache read: {e}")
        return None


def write_cache(timestamp, deadline):
    try:
        with open(CACHE_FILE, 'w') as file:
            cache_data = {'timestamp': timestamp, 'deadline': deadline}
            json.dump(cache_data, file)
            return True
    except IOError as e:
        print(f"Error during cache write: {e}")
        return False


def get_or_update_deadline():
    cache_data = read_cache()
    if cache_data is not None:
        timestamp, deadline = cache_data
        # only query the API if the cache is older than a day
        if pendulum.now() - pendulum.parse(timestamp) < pendulum.duration(hours=24):
            return deadline
    else:
        deadline = None

    new_deadline = query_api()
    if new_deadline is not None:
        write_cache(pendulum.now().isoformat(), new_deadline)
        return new_deadline

    # always (try to) return cached value as a fallback should there be an error during updating
    return deadline


def calculate_countdown(deadline_str):
    now = pendulum.now()
    deadline = pendulum.parse(deadline_str)
    difference = deadline.diff(now)

    years = difference.years
    hours = difference.hours
    minutes = difference.minutes
    seconds = difference.remaining_seconds

    # need to this to get the remaining months and days only in days
    date_only_days_remaining = now.add(years=years, hours=hours, minutes=minutes, seconds=seconds)
    days = deadline.diff(date_only_days_remaining).in_days()

    return {
        'years': years,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'deadline': deadline.to_datetime_string()
    }


def title_string(countdown):
    years = countdown["years"]
    days = countdown["days"]
    hours = countdown["hours"]
    minutes = countdown["minutes"]
    seconds = countdown["seconds"]

    y_label, d_label, h_label = " ʏ", " ᴅ", " ʜ"
    if LABELS_LONG:
        y_label, d_label, h_label = " ʏʀꜱ", " ᴅᴀʏꜱ", " ʜʀꜱ"

    if MINUTES_SECONDS:
        return f"{years}{y_label} {days}{d_label} {hours:02}:{minutes:02}:{seconds:02}"
    return f"{years}{y_label} {days}{d_label} {hours:02}{h_label}"


deadline = get_or_update_deadline()
if deadline is not None:
    countdown = calculate_countdown(deadline)
    print(f"{title_string(countdown)} | color=pink")
    print('---')
    print("Deadline to limit global warming to 1.5°C: | disabled=true")
    print(f"{countdown['deadline']} | disabled=true color=red")
    print('---')
    print("climateclock.world | href='https://climateclock.world'")
    print("#ActInTime | disabled=true font='SF Mono'")
