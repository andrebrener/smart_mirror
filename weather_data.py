import pyowm

def get_weather_info(key, city):
    owm = pyowm.OWM(key)

    observation = owm.weather_at_place(city)
    # observation = owm.weather_at_place('London,uk')
    w = observation.get_weather()

    weather_dict = {'status': w.get_status()}

    for key, val in w.get_temperature('celsius').items():
        if key != 'temp_kf':
            weather_dict[key] = val

    return weather_dict

if __name__ == '__main__':
   data_file = open('weather_api_key.txt', 'r')
   key = data_file.read().strip()
   city = 'Ciudad Autónoma de Buenos Aires,ar'

   weather = get_weather_info(key, city)
   print(weather)
