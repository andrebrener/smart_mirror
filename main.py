import io
import time

from tkinter import BOTTOM, Frame, Label, LEFT, RIGHT, Tk, Y
from datetime import date
from urllib.request import urlopen

import pandas as pd
import http.client

from PIL import Image, ImageTk
from weather_data import get_weather_info
from football_results import get_teams_fixture

league = 'Premier League'
match = 'Arsenal 2 - 0 Manchester United'

# Get Weather Data
data_file = open('weather_api_key.txt', 'r')
weather_key = data_file.read().strip()
city = 'Ciudad Autónoma de Buenos Aires,ar'
# weather = get_weather_info(weather_key, city)


# Get football data
data_file = open('football_api_key.txt', 'r')
football_key = data_file.read().strip()
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': football_key, 'X-Response-Control': 'full'}

leagues_df = pd.read_csv('preferred_leagues.csv')
teams_df = pd.read_csv('preferred_teams.csv')
team_names = teams_df['name'].unique()

# football_df = get_teams_fixture(connection, headers, leagues_df, team_names)

root = Tk()
root.configure(background='black')

# Build Frames
weather_frame = Frame(root, background='black')
time_frame = Frame(root, background='black')
football_frame = Frame(root, background='black')

# Generate Day
day1 = ''
calendar = Label(time_frame, fg='white', bg='black')
calendar.pack()


def update_day():
    global day1
    # get the current local time from the PC
    day2 = date.today().strftime('%a, %b %d')
    # if time string has changed, update it
    if day2 != day1:
        day1 = day2
        calendar.configure(text=day2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    calendar.after(5000, update_day)


update_day()

# Generate Time
time1 = ''
clock = Label(time_frame, fg='white', bg='black')
clock.pack()


def update_time():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.configure(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(1000, update_time)


update_time()

# Generate weather
weather_dict_1 = {'status': '', 'temp': '', 'temp_max': '', 'temp_min': ''}
url_1 = ''

status_label = Label(weather_frame, fg='white', bg='black')
temp_label = Label(weather_frame, fg='white', bg='black')
max_temp_label = Label(weather_frame, fg='white', bg='black')
min_temp_label = Label(weather_frame, fg='white', bg='black')
icon_label = Label(weather_frame, bg='black')
status_label.pack()
temp_label.pack()
max_temp_label.pack()
min_temp_label.pack()
icon_label.pack()


def update_weather():
    global weather_dict_1
    global url_1
    global weather_key
    global city
    # get the current local weather
    weather = get_weather_info(weather_key, city)
    if weather['status'].lower() == 'clear':
        url = 'http://i.imgur.com/o7gbio1.png'
    elif weather['status'].lower() == 'rain':
        url = 'http://i.imgur.com/V4UI3HB.png'
    elif weather['status'].lower() == 'cloud':
        url = 'http://i.imgur.com/vtM9cAF.png'

    weather_dict_2 = {
        'status': [weather['status'], status_label],
        'temp': [int(weather['temp']), temp_label],
        'temp_max': [int(weather['temp_max']), max_temp_label],
        'temp_min': [int(weather['temp_min']), min_temp_label],
    }
    # if weather has changed, update it
    for key, val in weather_dict_2.items():
        if val[0] != weather_dict_1[key]:
            val[1].configure(text=val[0])
    if url != url_1:
        url_1 = url
        image_bytes = urlopen(url).read()
        # internal data file
        data_stream = io.BytesIO(image_bytes)
        # open as a PIL image object
        pil_image = Image.open(data_stream)
        # data_stream the size of the image
        w, h = pil_image.size
        # convert PIL image object to Tkinter PhotoImage object
        tk_image = ImageTk.PhotoImage(pil_image)
        icon_label.configure(image=tk_image)
        icon_label.image = tk_image

    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    status_label.after(4 * 10 ^ 6, update_weather)


update_weather()


league_label = Label(football_frame, text=league, fg='white').pack()
match_label = Label(football_frame, text=match, fg='white').pack()

weather_frame.pack(side=LEFT, fill=Y)
time_frame.pack(side=RIGHT, fill=Y)
football_frame.pack(side=BOTTOM)

root.mainloop()
