import io
import os
import time
import pickle

from tkinter import Frame, Label, Tk
from datetime import date
from urllib.request import urlopen

from PIL import Image, ImageTk
from constants import CITY_ID
from weather_data import get_weather_info

# Refresh intervals in milliseconds.
REFRESH_INTERVAL_MS = 10 * 60 * 1000  # 10 minutes


def update_time():
    global TIME
    # get the current local time from the PC
    current_time = time.strftime('%H:%M')
    # if time string has changed, update it
    if current_time != TIME:
        TIME = current_time
        clock.configure(text=current_time)

    clock.after(900, update_time)


def update_day():
    global day1
    # get the current local time from the PC
    day2 = date.today().strftime('%A')
    date_2 = date.today().strftime('%d %b, %Y')
    # if time string has changed, update it
    if day2 != day1:
        day1 = day2
        calendar.configure(text=day2)
        date_label.configure(text=date_2)

    calendar.after(900, update_day)


def update_prices():
    global PRICES

    if not os.path.exists('prices_data.pkl'):
        # The data is produced by cryptocurrency_data.py (run via cron).
        # Skip until it exists instead of crashing on first run.
        prices_frame.after(REFRESH_INTERVAL_MS, update_prices)
        return

    with open('prices_data.pkl', 'rb') as f:
        prices = pickle.load(f)

    if prices != PRICES:
        PRICES = prices
        # Reuse existing labels and only create new ones as needed, so the
        # update loop does not leak Label widgets on every refresh.
        for i, coin in enumerate(prices):
            for n, element in enumerate(coin):
                label = price_labels.get((i, n))
                if label is None:
                    label = Label(
                        prices_frame,
                        fg='white',
                        bg='black',
                        font=("Helvetica", 30))
                    label.grid(row=i, column=n, sticky='w')
                    price_labels[(i, n)] = label
                label.configure(text=element)

    prices_frame.after(REFRESH_INTERVAL_MS, update_prices)


def update_weather():
    global WEATHER_DICT
    global WEATHER_URL
    global WEATHER_KEY
    global CITY_ID
    # get the current local weather
    weather = get_weather_info(WEATHER_KEY, CITY_ID)

    url_image = weather['url']

    current_weather = {
        'temp': [weather['temp'], temp_label]
    }
    # if weather has changed, update it
    for key, val in current_weather.items():
        if val[0] != WEATHER_DICT[key]:
            val[1].configure(text=val[0])
    if url_image != WEATHER_URL:
        WEATHER_URL = url_image
        image_bytes = urlopen(url_image).read()
        # internal data file
        data_stream = io.BytesIO(image_bytes)
        # open as a PIL image object
        pil_image = Image.open(data_stream)
        im_size = (200, 200)
        # convert PIL image object to Tkinter PhotoImage object
        pil_image = pil_image.resize(im_size, Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)
        icon_label.configure(image=tk_image)
        icon_label.image = tk_image

    temp_label.after(REFRESH_INTERVAL_MS, update_weather)


def update_fixture():
    global GAMES_LIST

    if not os.path.exists('football_data.pkl'):
        # The data is produced by football_results.py (run via cron).
        # Skip until it exists instead of crashing on first run.
        football_frame.after(REFRESH_INTERVAL_MS, update_fixture)
        return

    with open('football_data.pkl', 'rb') as f:
        games_list = pickle.load(f)
    if games_list != GAMES_LIST:
        GAMES_LIST = games_list
        # Reuse existing labels and only create new ones as needed, so the
        # update loop does not leak Label widgets on every refresh.
        for i, game in enumerate(games_list):
            for n, element in enumerate(game):
                label = fixture_labels.get((i, n))
                if label is None:
                    label = Label(
                        football_frame,
                        fg='white',
                        bg='black',
                        font=('Helvetica'))
                    label.grid(row=i, column=n)
                    fixture_labels[(i, n)] = label
                label.configure(text=element)

    football_frame.after(REFRESH_INTERVAL_MS, update_fixture)


if __name__ == '__main__':

    root = Tk()
    root.configure(background='black')
    # Build Frames
    top_left_frame = Frame(root, background='black')
    weather_frame = Frame(top_left_frame, background='black')
    prices_frame = Frame(top_left_frame, background='black')
    time_frame = Frame(root, background='black')
    football_frame = Frame(root, background='black')

    # Get Data from APIs

    # Get Weather Data
    data_file = open('weather_api_key.txt', 'r')
    WEATHER_KEY = data_file.read().strip()

    # Generate Data

    # Generate Pickle Global Data
    GAMES_LIST = []
    PRICES = []

    # Caches of Label widgets keyed by (row, column), so the price/fixture
    # update loops reuse widgets instead of creating new ones each refresh.
    price_labels = {}
    fixture_labels = {}

    # Generate Time
    TIME = ''
    clock = Label(time_frame, fg='white', bg='black', font=('Helvetica', 100))
    clock.pack()

    # Generate Day
    day1 = ''
    calendar = Label(
        time_frame, fg='white', bg='black', font=('Helvetica', 60))
    date_label = Label(
        time_frame, fg='white', bg='black', font=('Helvetica', 60))
    calendar.pack()
    date_label.pack()

    # Generate weather
    WEATHER_DICT = {'temp': ''}
    WEATHER_URL = ''

    temp_label = Label(
        weather_frame, fg='white', bg='black', font=('Helvetica', 170))

    icon_label = Label(weather_frame, bg='black')
    temp_label.grid(row=1, column=2, columnspan=2)
    icon_label.grid(row=1, column=1)

    # Update Data
    update_time()
    update_day()
    update_weather()
    update_fixture()
    update_prices()

    # Pack Frames

    weather_frame.grid(row=0, sticky='n', pady=30, padx=30)
    prices_frame.grid(row=1, sticky='sw', pady=20, padx=30)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    top_left_frame.grid(row=0, column=0, columnspan=2, sticky='nw')
    time_frame.grid(row=0, column=2, sticky='nsew', padx=30, pady=30)
    football_frame.grid(row=1, column=1, columnspan=1, sticky='ew', pady=20)

    root.attributes("-fullscreen", True)
    root.mainloop()
