import pyowm


def get_weather_info(key, city_id):
    owm = pyowm.OWM(key)

    observation = owm.weather_at_id(city_id)
    # observation = owm.weather_at_place('London,uk')
    w = observation.get_weather()

    weather_dict = {'status': w.get_status()}

    for key, val in w.get_temperature('celsius').items():
        if key != 'temp_kf':
            weather_dict[key] = '{} °'.format(int(val))

    return weather_dict


if __name__ == '__main__':
    import json
    import random

    data_file = open('weather_api_key.txt', 'r')
    key = data_file.read().strip()

    with open('city_list.json') as d:
        data = json.load(d)

    ids_list = [data[i]['id'] for i in range(len(data))]

    rnd_list = random.sample(ids_list, 300)

    status_list = []

    for id in rnd_list:
        weather = get_weather_info(key, id)
        status_list.append(weather['status'])

    unique_status = set(status_list)

    print(unique_status)


    
