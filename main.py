import time

from tkinter import BOTTOM, Frame, Label, LEFT, RIGHT, Tk, Y
from datetime import date

import pandas as pd
import http.client

from weather_data import get_weather_info
from football_results import get_teams_fixture

league = 'Premier League'
match = 'Arsenal 2 - 0 Manchester United'

# Get Weather Data
data_file = open('weather_api_key.txt', 'r')
key = data_file.read().strip()
city = 'Ciudad Autónoma de Buenos Aires,ar'
weather = get_weather_info(key, city)

# Get football data
data_file = open('football_api_key.txt', 'r')
key = data_file.read().strip()
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': key, 'X-Response-Control': 'full'}

leagues_df = pd.read_csv('preferred_leagues.csv')
teams_df = pd.read_csv('preferred_teams.csv')
team_names = teams_df['name'].unique()

football_df = get_teams_fixture(connection, headers, leagues_df, team_names)

root = Tk()

# Build Frames
weather_frame = Frame(root)
time_frame = Frame(root)
football_frame = Frame(root)

# Generate Day
day1 = ''
calendar = Label(time_frame)
calendar.pack()


def change_day():
    global day1
    # get the current local time from the PC
    day2 = date.today().strftime('%a, %b %d')
    # if time string has changed, update it
    if day2 != day1:
        day1 = day2
        calendar.config(text=day2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    calendar.after(5000, change_day)


change_day()

# Generate Time
time1 = ''
clock = Label(time_frame)
clock.pack()


def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)


tick()

status_label = Label(weather_frame, text=weather['status']).pack()
cur_temp_label = Label(
    weather_frame,
    text='Current Temp: {}°C'.format(int(weather['temp']))).pack()
max_temp_label = Label(
    weather_frame,
    text='Max Temp: {}°C'.format(int(weather['temp_max']))).pack()
min_temp_label = Label(
    weather_frame,
    text='Min Temp: {}°C'.format(int(weather['temp_min']))).pack()

league_label = Label(football_frame, text=league).pack()
match_label = Label(football_frame, text=match).pack()

weather_frame.pack(side=LEFT, fill=Y)
time_frame.pack(side=RIGHT, fill=Y)
football_frame.pack(side=BOTTOM)

root.mainloop()
