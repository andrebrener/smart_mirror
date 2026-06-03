# Smart Mirror

This application creates widgets to show in a mirror. The code is intended to run on a Raspberry Pi connected to a monitor behind a two-way mirror.
The code is written for and intended to be used with Python 3.

## Getting Started

### 1. Clone Repo

`git clone https://github.com/andrebrener/smart_mirror.git`

### 2. Install Packages Required

Go into the directory of the repo and run:
```pip install -r requirements.txt```

### 3. Get API Keys

The API keys must be saved with the names `weather_api_key.txt` and `football_api_key.txt` in the same directory.
- For weather data: [Open Weather Map](https://home.openweathermap.org/users/sign_up)
- For football data: [Football Data](https://www.football-data.org/)

### 4. Generate the data, then run

The clock and weather widgets read live data, but the **cryptocurrency** and **football** widgets read from pickle files (`prices_data.pkl` and `football_data.pkl`) produced by the data scripts. The data scripts live in the `widgets/` package — run them **as modules from the project root** (`python3 -m widgets.<name>`) so their imports resolve. Run them **before** (and periodically alongside) the UI, otherwise those two widgets stay empty:

```
python3 -m widgets.cryptocurrency_data
python3 -m widgets.football_results
python3 main.py
```

On a Raspberry Pi the two data scripts are intended to be run on a schedule with cron, e.g.:

```
*/10 * * * * cd /path/to/smart_mirror && python3 -m widgets.cryptocurrency_data
*/10 * * * * cd /path/to/smart_mirror && python3 -m widgets.football_results
```

## What Widgets are there?

- Date and time.
- Weather.
- Football games fixture.
- Cryptocurrency prices.

## Widgets & Customizations

### Date & Time
This will automatically get the time & date from the machine that runs the script.

### Weather
Define the city id in `constants.py`. City ids come from OpenWeatherMap's city list. That file (`city_list.json`, ~28 MB) is **not** committed to this repo; download the current `city.list.json.gz` from the [OpenWeatherMap bulk data page](https://bulk.openweathermap.org/sample/), unzip it to `city_list.json` in the project directory, and look up your city's `id` there.

### Football games fixture
Select the leagues and teams of the fixtures you would like to see. You can get the ids from the [API documentation](https://www.football-data.org/documentation/quickstart).
The chosen leagues and teams must be saved in csv files named `preferred_leagues.csv` and `preferred_teams.csv` respectively, following their structure.

### Cryptocurrency Prices
Define the list of coins in `constants.py` that you would like to see.

## Known Limitations

This project dates from 2017 and some external dependencies have since changed in ways that break the original code paths. These are documented rather than fixed here, because reviving them is a substantial rewrite:

- **Weather (pyowm):** `widgets/weather_data.py` uses the pyowm **v2** API (`pyowm.OWM(key).weather_at_id(...).get_weather()`), which was removed in pyowm v3. `requirements.txt` therefore pins `pyowm<3`. Migrating to pyowm v3 would require rewriting `get_weather_info`.
- **Football fixtures (football-data.org):** `widgets/football_results.py` calls the **v1** API over plain HTTP. v1 has been decommissioned; the current API is **v4** over HTTPS with a different JSON shape. The fixture pipeline needs a rewrite against v4 to work again.
- **Weather icons** are served from `http://i.imgur.com/...` over plain HTTP.

## License

No license file is currently included. Until one is added, the default copyright applies (all rights reserved).
