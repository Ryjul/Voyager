import re
import os
import requests
import sys
import time
import math
from bs4 import BeautifulSoup

# Scrape distance and epoch information and remove semicolon for processing.
trajectory_data_url = requests.get('https://voyager.jpl.nasa.gov/assets/javascripts/distance_data.js')
trajectory_data_url_string = str(trajectory_data_url.text)
trajectory_data_url_string_nosemicolons = trajectory_data_url_string.replace(';','')

# Get the numbers from the string.
trajectory_numbers_string = re.findall(r"[-+]?\d*\.\d+|\d+", trajectory_data_url_string_nosemicolons)

# Create a list of floats to be used in calculation.
trajectory_float_list = [float(entry) for entry in trajectory_numbers_string]

# Define Voyager trajectory variables.
epoch_0 = trajectory_float_list[1]
epoch_1 = trajectory_float_list[3]

dist_0_v1 = trajectory_float_list[6]
dist_1_v1 = trajectory_float_list[9]

dist_0_v2 = trajectory_float_list[12]
dist_1_v2 = trajectory_float_list[15]

dist_0_v1s = trajectory_float_list[18]
dist_1_v1s = trajectory_float_list[21]

dist_0_v2s = trajectory_float_list[24]
dist_1_v2s = trajectory_float_list[27]

current_speed_v1 = 16.9995
current_speed_v2 = 15.3741

speed_of_light = 299792.458

au_const = 149597870.691

voy1_launch_epoch = 242312160
voy2_launch_epoch = 240935340

days_per_year = 365
minutes_per_hour = 60
seconds_per_hour = 3600
seconds_per_minute = 60

# Clear the terminal.
clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

# Scrape Instrument Status Data with BeautifulSoup.
soup_page = 'https://voyager.jpl.nasa.gov/mission/status/'
html_content = requests.get(soup_page).text
soup = BeautifulSoup(html_content, "lxml")

status_list = []
rows = soup.find_all('tr')
for row in rows:
        cols = row.find_all('td')
        cols = [x.text.strip() for x in cols]
        status_list.append(cols)

# List of current instrument statuses.
statuses = (status_list[11:21])

# Make list of Voyager 1 instrument statuses.
v1_statuses = []
for i in statuses:
     v1_statuses.append(i[0])

v2_statuses = []
for i in statuses:
    v2_statuses.append(i[1])

# Function to calculate current epoch.
def calculate_current_epoch():
    return int(time.time())

# Function to calculate distances.
def calculate_current_dist(distance1 , distance2):
    return round((((int(time.time() - epoch_0 ) / (epoch_0 - epoch_1)) * (distance1 - distance2)) + distance2) , 1)

# Function to add commas to distances.
def current_dist_formatted(distance1 , distance2):
    return f'{round((((int(time.time() - epoch_0 ) / (epoch_0 - epoch_1)) * (distance1 - distance2)) + distance2) , 1):,}'

# Function to calculate AU distances.
def calculate_AU(distance1, distance2):
    return ((((int(time.time() - epoch_0 ) / (epoch_0 - epoch_1)) * (distance1 - distance2)) + distance2) / au_const)

# Function to format AU distances.
def AU_formatted(distance1, distance2):
    return format(((((int(time.time() - epoch_0 ) / (epoch_0 - epoch_1)) * (distance1 - distance2)) + distance2) / au_const) , '.12f')

def calculate_one_way_light(distance1, distance2):
    return format(((((int(time.time() - epoch_0 ) / (epoch_0 - epoch_1)) * (distance1 - distance2)) + distance2) / (speed_of_light * seconds_per_hour) ) , '.13f')

# Function to calculate mission years.
def calculate_years(launch_epoch):
    return int(math.floor((calculate_current_epoch() - launch_epoch) / (3600 * 24 * 365)))

# Function to calculate mission days.
def calculate_days(launch_epoch):
    return math.floor((((calculate_current_epoch() - launch_epoch) - (calculate_years(launch_epoch) * 3600 * 24 * 365))) / (3600 * 24))

# Format days for display.
def days_formatted(launch_epoch):
    return str(calculate_days(launch_epoch)).zfill(3)

# Function to calculate mission hours.
def calculate_hours(launch_epoch):
    return math.floor((((calculate_current_epoch() - launch_epoch) - (calculate_years(launch_epoch) * 3600 * 24 * 365) - (calculate_days(launch_epoch) * 3600 * 24)) / 3600))

# Format hours for display.
def hours_formatted(launch_epoch):
    return str(calculate_hours(launch_epoch)).zfill(2)

# Function to calculate mission minutes.
def calculate_minutes(launch_epoch):
    return math.floor((((calculate_current_epoch() - launch_epoch) - (calculate_years(launch_epoch) * 3600 * 24 * 365) - (calculate_days(launch_epoch) * 3600 * 24) - (calculate_hours(launch_epoch) * 3600)) / 60))

# Format minutes for display.
def minutes_formatted(launch_epoch):
    return str(calculate_minutes(launch_epoch)).zfill(2)

# Function to calculate mission seconds.
def calculate_seconds(launch_epoch):
    return math.floor(((calculate_current_epoch() - launch_epoch) - (calculate_years(launch_epoch) * 3600 * 24 * 365) - (calculate_days(launch_epoch) * 3600 * 24) - (calculate_hours(launch_epoch) * 3600) - (calculate_minutes(launch_epoch) * 60)))

# Format seconds for display.
def seconds_formatted(launch_epoch):
    return str(calculate_seconds(launch_epoch)).zfill(2)

# Main Loop.
while True:
    # Print Telemetry Data.
    clear()
    print('Live telemetry from the Voyager probes:' , '\n')
    print('Spacecraft:                                   Voyager 1                 Voyager 2' , '\n')
    print('Distance from Earth:                         ' , current_dist_formatted(dist_1_v1, dist_0_v1) ,'    km  ' , current_dist_formatted(dist_1_v2, dist_0_v2) , '    km') # Voyager 1 distance from Earth , Voyager 2 distance from Earth
    print('                                             ' , AU_formatted(dist_1_v1, dist_0_v1) ,'    AU  ' , AU_formatted(dist_1_v2, dist_0_v2) , '    AU') # Voyager 1 distance from Earth , Voyager 2 distance from Earth
    print('Distance from the sun:                       ' , current_dist_formatted(dist_1_v1s, dist_0_v1s) ,'    km  ' , current_dist_formatted(dist_1_v2s, dist_0_v2s) , '    km') # Voyager 1 distance from the sun , Voyager 2 distance from the sun
    print('                                             ' , AU_formatted(dist_1_v1s, dist_0_v1s) ,'    AU  ' , AU_formatted(dist_1_v2s, dist_0_v2s) , '    AU') # Voyager 1 distance from the sun , Voyager 2 distance from the sun
    print('One way communication time:                  ' , calculate_one_way_light(dist_1_v1, dist_0_v1) ,'     h  ' , calculate_one_way_light(dist_1_v2, dist_0_v2) , '     h') # Voyager 1 light travel time , Voyager 2 light travel time
    print('Elapsed mission time:                        ' , calculate_years(voy1_launch_epoch) , days_formatted(voy1_launch_epoch) , hours_formatted(voy1_launch_epoch) , minutes_formatted(voy1_launch_epoch) , seconds_formatted(voy1_launch_epoch) , '  ydhms  ' , calculate_years(voy2_launch_epoch) , days_formatted(voy2_launch_epoch) , hours_formatted(voy2_launch_epoch) , minutes_formatted(voy2_launch_epoch) , seconds_formatted(voy2_launch_epoch) , '  ydhms') # Voyager 1 and 2 elapsed mission time.
    print('Velocity (with respect to sun)               ' , current_speed_v1 , '           km/s  ' , current_speed_v2 , '           km/s' , '\n')

    print('Instrument status:' , '\n')
    print('Cosmic Ray Subsystem (CRS)                   ' , v1_statuses[0] , '                      ' , v2_statuses[0])
    print('Low-Energy Charged Particles (LECP)          ' , v1_statuses[1] , '                      ' , v2_statuses[1])
    print('Magnetometer (MAG)                           ' , v1_statuses[2] , '                      ' , v2_statuses[2])
    print('Plasma Wave Subsystem (MAG)                  ' , v1_statuses[3] , '                      ' , v2_statuses[3])
    print('Plasma Science (PLS)                         ' , v1_statuses[4] , '                     ' , v2_statuses[4])
    print('Imaging Science Subsystem (ISS)              ' , v1_statuses[5] , '                     ' , v2_statuses[5])
    print('IR Interferometer and Radiometer (IRIS)      ' , v1_statuses[6] , '                     ' , v2_statuses[6])
    print('Photopolarimeter Subsystem (PPS)             ' , v1_statuses[7] , '                     ' , v2_statuses[7])
    print('Planetary Radio Astronomy (PRA)              ' , v1_statuses[8] , '                     ' , v2_statuses[8])
    print('Ultraviolet Spectrometer (UVS)               ' , v1_statuses[9] , '                     ' , v2_statuses[9] , '\n')

    # Receiving data from JPL animation.
    print('Receiving data from JPL' , end = '\r')
    time.sleep(1)
    print('Receiving data from JPL.' , end = '\r')
    time.sleep(1)
    print('Receiving data from JPL..' , end = '\r')
    time.sleep(1)
    print('Receiving data from JPL...' , end = '\r')
    time.sleep(1)

