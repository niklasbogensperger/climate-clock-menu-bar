#! /usr/bin/env python3

#########################################################
# SWIFTBAR METADATA #
#########################################################

# <xbar.title>Climate Clock</xbar.title>
# <xbar.version>v2.1</xbar.version>
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

# whether to use long or short labels (e.g. "ʏʀꜱ" vs. "ʏ")
# default: False (short labels)
LABELS_LONG = False
# whether to display minutes and seconds as well (set refresh rate of script to 1s (or a bit less))
# default: False (do not display minutes/seconds)
MINUTES_SECONDS = False

# CHANGES USUALLY NOT NEEDED
# file to use for the cache
# default: SwiftBar cache directory for this plugin
CACHE_FILE = f"{os.getenv('SWIFTBAR_PLUGIN_CACHE_PATH')}/climate_clock_timestamp.json"
# API URL to query (any changes likely would require code modifications as well)
API_URL = "https://api.climateclock.world/v2/clock.json"

#########################################################


def query_api():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        error = f"Error querying API:\n↪︎ {e}"
        return None, error

    try:
        data = response.json()
        deadline = data['data']['modules']['carbon_deadline_1']['timestamp']
        return deadline, None
    except json.JSONDecodeError as e:
        error = f"Error decoding JSON response:\n↪︎ {e}"
        return None, error
    except KeyError as e:
        error = f"Error extracting deadline from response:\n↪︎ {e}"
        return None, error


def read_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as file:
                cache_data = json.load(file)
                timestamp = cache_data.get('timestamp')
                deadline = cache_data.get('deadline')
                return (timestamp, deadline), None
        else:
            raise FileNotFoundError("CACHE_FILE does not exist.")
    except (IOError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        error = f"Error during cache read:\n↪︎ {e}"
        return None, error


def write_cache(timestamp, deadline):
    try:
        with open(CACHE_FILE, 'w') as file:
            cache_data = {'timestamp': timestamp, 'deadline': deadline}
            json.dump(cache_data, file)
            return True, None
    except IOError as e:
        error = f"Error during cache write:\n↪︎ {e}"
        return False, error


def get_or_update_deadline():
    cache = read_cache()
    if cache[0] is not None:
        timestamp, deadline = cache[0]
        # only query the API if the cache is older than a day
        if pendulum.now() - pendulum.parse(timestamp) < pendulum.duration(hours=24):
            return deadline, None
    else:
        deadline = None
    error_cache = cache[1]

    new_deadline, error_api = query_api()
    errors = f"{error_cache if error_cache is not None else ''}\n{error_api if error_api is not None else ''}".strip()
    if new_deadline is not None:
        write_cache(pendulum.now().isoformat(), new_deadline)
        return new_deadline, errors

    # always (try to) return cached value as a fallback should there be an error during updating
    return deadline, errors


def calculate_countdown(deadline_str):
    now = pendulum.now()
    deadline = pendulum.parse(deadline_str)
    difference = deadline.diff(now)

    years = difference.years
    hours = difference.hours
    minutes = difference.minutes
    seconds = difference.remaining_seconds

    # need to do this to get the remaining months and days only in days
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

    # strings contain unicode "thin space" and "small capital letter" glyphs
    y_label, d_label, h_label = " ʏ", " ᴅ", " ʜ"
    if LABELS_LONG:
        y_label, d_label, h_label = " ʏʀꜱ", " ᴅᴀʏꜱ", " ʜʀꜱ"

    if MINUTES_SECONDS:
        return f"{years}{y_label} {days}{d_label} {hours:02}:{minutes:02}:{seconds:02}"
    return f"{years}{y_label} {days}{d_label} {hours:02}{h_label}"


deadline, errors = get_or_update_deadline()
if deadline is not None:
    countdown = calculate_countdown(deadline)
    print(f"{title_string(countdown)} | color=pink")
    print('---')
    print("Deadline to limit global warming to 1.5°C: | disabled=true")
    print(f"{countdown['deadline']} | disabled=true color=red")
    print('---')
    print("climateclock.world | href='https://climateclock.world'")
    print("#ActInTime | disabled=true font='SF Mono'")
else:
    print("climate clock | color=pink")
if errors:
    print('---')
    print("Last error(s): | disabled = true")
    print(f"{errors}| disabled = true")
