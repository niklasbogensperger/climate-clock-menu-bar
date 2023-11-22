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


import subprocess

import pendulum
import requests

#########################################################
# CONFIGURATION #
#########################################################

LABELS_LONG = False
MINUTES_SECONDS = False

#########################################################


def get_carbon_deadline_timestamp_requests():
    url = "https://api.climateclock.world/v2/clock.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        timestamp = data['data']['modules']['carbon_deadline_1']['timestamp']
        return timestamp
    else:
        print(f"Error: {response.status_code}")
        return None


def get_carbon_deadline_timestamp_shell():
    command = "curl https://api.climateclock.world/v2/clock.json | jq '.data.modules.carbon_deadline_1.timestamp'"

    try:
        result = subprocess.check_output(command, shell=True, text=True).strip().replace('"', '')
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


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


deadline = get_carbon_deadline_timestamp_requests()
if deadline is not None:
    countdown = calculate_countdown(deadline)
    print(f"{title_string(countdown)} | color=pink")
    print('---')
    print("Deadline to limit global warming to 1.5°C: | disabled=true")
    print(f"{countdown['deadline']} | disabled=true color=red")
    print('---')
    print("climateclock.world | href='https://climateclock.world'")
    print("#ActInTime | disabled=true font='SF Mono'")
