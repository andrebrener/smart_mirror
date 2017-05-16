import pyowm

images_dict = {
    'clear': 'http://i.imgur.com/PaFjwVA.jpg',
    'rain': 'http://i.imgur.com/77EPHDJ.jpg',
    'snow': 'http://i.imgur.com/FB19CJM.jpg',
    'drizzle': 'http://i.imgur.com/FB19CJM.jpg',
    'thunderstorm': 'http://i.imgur.com/DNxm5nn.jpg',
    'clouds': 'http://i.imgur.com/EMHPJx9.jpg',
    'dust': 'http://i.imgur.com/EMHPJx9.jpg',
    'fog': 'http://i.imgur.com/EMHPJx9.jpg',
    'smoke': 'http://i.imgur.com/EMHPJx9.jpg'
}


def get_weather_info(key, city_id):
    owm = pyowm.OWM(key)

    observation = owm.weather_at_id(city_id)
    # observation = owm.weather_at_place('London,uk')
    w = observation.get_weather()

    weather_dict = {'status': w.get_status()}

    for key, val in w.get_temperature('celsius').items():
        if key != 'temp_kf':
            weather_dict[key] = '{}°'.format(int(val))

    weather_dict['url'] = images_dict[weather_dict['status'].lower()]

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
