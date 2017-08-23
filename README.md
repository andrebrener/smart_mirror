# Smart Mirror

This application creates widgets to show in a mirror. The code is intended to run in a raspberry pi connected to a monitor behind a two way mirror.
The code is written and intended to use with Python 3.

## Getting Started

### 1. Clone Repo

`git clone https://github.com/andrebrener/football_data.git`

### 2. Install Packages Required

Go in the directory of the repo and run:
```pip install -r requirements.txt```

### 4. Get API Keys
The API keys must be saved with the names of `weather_api_key.txt` and `football_api_key.txt` in the same directory.
- For weather data: [Open Weather Map](https://home.openweathermap.org/users/sign_up)
- For football data: [Football Data](http://football-data.org/index)

### 3. Enjoy the repo :)

## What Widgets are there?

- Date and time.
- Weather.
- Football games fixture.
- Cryptocurrency prices.

## Widgets & Customizations

### Date & Time
This will automatically get the time & date from the machine that runs the script.

### Weather
Define the city id in `constants.py` with the id in [city_list.json](https://github.com/andrebrener/smart_mirror/blob/master/city_list.json).

### Football games fixture
Select the leagues and the teams of the fixtures you would like to see. You can get the ids from the [API documentation](http://football-data.org/documentation).
The chosen [leagues](https://github.com/andrebrener/smart_mirror/blob/master/preferred_leagues.csv) and [teams](https://github.com/andrebrener/smart_mirror/blob/master/preferred_teams.csv) must be saved in csv named `preferred_leagues.csv` and `preferred_teams.csv` respectively following their structure.

### Cryptocurrency Prices
Define the list of coins in `constants.py` that you would like to see.

