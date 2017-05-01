import io
import time
import pickle

from tkinter import BOTTOM, Frame, Label, LEFT, RIGHT, Tk, Y, E
from datetime import date
from urllib.request import urlopen

import pandas as pd
import http.client

from PIL import Image, ImageTk
from weather_data import get_weather_info
from football_results import get_football_data


def update_time():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.configure(text=time2)

    clock.after(900, update_time)


def update_day():
    global day1
    global date1
    # get the current local time from the PC
    day2 = date.today().strftime('%A')
    date_2 = date.today().strftime('%d %b, %Y')
    # if time string has changed, update it
    if day2 != day1:
        day1 = day2
        calendar.configure(text=day2)
        date_label.configure(text=date_2)

    calendar.after(900, update_day)


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
    else:
        url = 'http://i.imgur.com/vtM9cAF.png'

    weather_dict_2 = {
        'status': [weather['status'], status_label],
        'temp': [weather['temp'], temp_label],
        'temp_max': [weather['temp_max'], max_temp_label],
        'temp_min': [weather['temp_min'], min_temp_label],
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

    status_label.after(10 ^ 7, update_weather)


def update_fixture():
    global connection
    global headers
    global leagues
    global team_names

    with open('football_data.pkl', 'rb') as f:
        games_list = pickle.load(f)
    # games_list = get_football_data(connection, headers, leagues, team_names)
    for i, game in enumerate(games_list):
        for n, element in enumerate(game):
            Label(
                football_frame,
                text=element,
                fg='white',
                bg='black',
                font=("Helvetica")).grid(
                    row=i, column=n)

    football_frame.after(2000, update_fixture)


if __name__ == '__main__':

    root = Tk()
    root.configure(background='black')
    # Build Frames
    weather_frame = Frame(root, background='black')
    time_frame = Frame(root, background='black')
    football_frame = Frame(root, background='black')

    # Get Data from APIs

    # Get Football Data
    data_file = open('football_api_key.txt', 'r')
    football_key = data_file.read().strip()
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': football_key, 'X-Response-Control': 'full'}

    leagues = pd.read_csv('preferred_leagues.csv')
    teams = pd.read_csv('preferred_teams.csv')
    team_names = teams['name'].unique()

    # Get Weather Data
    data_file = open('weather_api_key.txt', 'r')
    weather_key = data_file.read().strip()
    city = 'Ciudad Autónoma de Buenos Aires,ar'

    # Generate Data

    # Generate Time
    time1 = ''
    clock = Label(time_frame, fg='white', bg='black', font=("Helvetica", 100))
    clock.pack()

    # Generate Day
    day1 = ''
    date_1 = ''
    calendar = Label(
        time_frame, fg='white', bg='black', font=("Helvetica", 60))
    date_label = Label(
        time_frame, fg='white', bg='black', font=("Helvetica", 60))
    calendar.pack()
    date_label.pack()

    # Generate weather
    weather_dict_1 = {'status': '', 'temp': '', 'temp_max': '', 'temp_min': ''}
    url_1 = ''

    status_label = Label(
        weather_frame, fg='white', bg='black', font=("Helvetica", 55))
    temp_label = Label(
        weather_frame, fg='white', bg='black', font=("Helvetica", 170))
    max_temp_label = Label(weather_frame, fg='white', bg='black',
            font=("Helvetica", 50))
    min_temp_label = Label(weather_frame, fg='white', bg='black',
            font=("Helvetica", 50))
    icon_label = Label(weather_frame, bg='black')
    status_label.grid(row=3, column=1)
    temp_label.grid(row=1, column=2, columnspan=2)
    max_temp_label.grid(row=3, column=2, sticky=E)
    min_temp_label.grid(row=3, column=3, sticky=E)
    icon_label.grid(row=1, column=1)

    # Update Data
    update_time()
    update_day()
    update_weather()
    update_fixture()

    # Pack Frames
    weather_frame.pack(side=LEFT, fill=Y)
    time_frame.pack(side=RIGHT, fill=Y)
    football_frame.pack(side=BOTTOM)
    football_frame.place(relx=.27, rely=.55)

    root.attributes("-fullscreen", True)
    root.mainloop()
