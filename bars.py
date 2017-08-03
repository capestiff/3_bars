import json
from geopy.distance import vincenty
from config import JSON_PATH


def load_data(filepath):
    with open(filepath, 'r', encoding='cp1251') as file:
        json_data_list = json.loads(file.read())

    return json_data_list


def get_smallest_bar(json_data):
    list_of_smallest_bars = []
    smallest_bar = sorted(json_data, key=lambda key: key['SeatsCount'])[0]

    for bar_ in json_data:
        if bar_['SeatsCount'] == smallest_bar['SeatsCount']:
            list_of_smallest_bars.append(bar_)

    return list_of_smallest_bars


def get_biggest_bar(json_data):
    list_of_biggest_bars = []
    biggest_bar = sorted(json_data, key=lambda key: key['SeatsCount'])[-1]

    for bar_ in json_data:
        if bar_['SeatsCount'] == biggest_bar['SeatsCount']:
            list_of_biggest_bars.append(bar_)

    return list_of_biggest_bars


def get_closest_bar(bars_list_, longitude, latitude):
    my_gps_coords = (latitude, longitude)

    for bar_ in bars_list_:
        bar_gps_coords = (bar_['Latitude_WGS84'], bar_['Longitude_WGS84'])
        distance_between_two_points = vincenty(my_gps_coords, bar_gps_coords).km
        bar_['Distance'] = distance_between_two_points

    return sorted(bars_list_, key=lambda key: key['Distance'])[0]


if __name__ == '__main__':

    latitude = float(input('Введите широту: '))  # E.g.: 55.60
    longitude = float(input('Введите долготу: '))  # E.g.: 37.74

    bars_list = load_data(JSON_PATH)
    biggest_bars_list = get_biggest_bar(bars_list)
    smallest_bars_list = get_smallest_bar(bars_list)
    closest_bar = get_closest_bar(bars_list, longitude, latitude)

    print('\nСамый большой бар'.upper(), '({})'.format(len(biggest_bars_list)))
    for bar in biggest_bars_list:
        print('    {}: {} мест'.format(bar['Name'], bar['SeatsCount']))

    print('\nСамый маленький бар'.upper(), '({})'.format(len(smallest_bars_list)))
    for bar in smallest_bars_list:
        print('    {}: {} мест'.format(bar['Name'], bar['SeatsCount']))

    print('\nСамый близкий бар'.upper())
    print('    {}, {}, {} ({:.2f} км)'.format(closest_bar['Name'],
                                              closest_bar['District'],
                                              closest_bar['Address'],
                                              closest_bar['Distance']))
