import json
import argparse
import math
from pathlib import Path
from decimal import Decimal, DecimalException


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("путь к файлу", help='программа считывает JSON-файл с data.mos.ru с данными о барах')
    args = parser.parse_args()
    return args.path_to_file


def load_data(filepath):
    with open(filepath, 'r', encoding='cp1251') as file:
        json_data_list = json.loads(file.read())

    return json_data_list


def get_smallest_bar(json_data):
    smallest_bar_ = min(json_data, key=lambda key: key['SeatsCount'])

    return smallest_bar_


def get_biggest_bar(json_data):
    biggest_bar_ = max(json_data, key=lambda key: key['SeatsCount'])

    return biggest_bar_


def get_closest_bar(bars_list_, longitude_, latitude_):
    my_gps_coords = {'latitude': Decimal(latitude_), 'longitude': Decimal(longitude_)}

    for bar_ in bars_list_:
        bar_gps_coords = {'latitude': bar_['Latitude_WGS84'], 'longitude': bar_['Longitude_WGS84']}
        bar_['Distance'] = get_distance_between_two_points_km(my_gps_coords, bar_gps_coords)

    return sorted(bars_list_, key=lambda key: key['Distance'])[0]


def get_distance_between_two_points_km(first_point_gps_coords, second_point_gps_coords):
    """
    Calculate central angle between two points via the haversine formula.
    More about at: https://en.wikipedia.org/wiki/Great-circle_distance
    """

    phita_1 = degrees_to_radians(first_point_gps_coords['latitude'])
    lambda_1 = degrees_to_radians(first_point_gps_coords['longitude'])
    phita_2 = degrees_to_radians(second_point_gps_coords['latitude'])
    lambda_2 = degrees_to_radians(second_point_gps_coords['longitude'])
    earth_radius = 6372.795  # in km

    # haversine formula
    central_angle = 2 * math.asin(math.sqrt(math.sin((phita_2 - phita_1)/2) ** 2 +
                                            math.cos(phita_1) * math.cos(phita_2) *
                                            math.sin((lambda_2 - lambda_1) / 2) ** 2))

    return Decimal(earth_radius * central_angle)  # distance in km


def degrees_to_radians(degrees):
    return Decimal(degrees) * Decimal(math.pi) / 180


def is_decimal(str_input):
    try:
        Decimal(str_input)
    except (DecimalException, TypeError):
        return False

    return True


def is_latitude(str_input):
    if is_decimal(str_input) and -90 <= Decimal(str_input) <= 90:
        return True
    else:
        print('Широта может быть в диапазоне -90 ... 90')
        return False


def is_longitude(str_input):
    if is_decimal(str_input) and -180 <= Decimal(str_input) <= 180:
        return True
    else:
        print('Долгота может быть в диапазоне -180 ... 180')
        return False


def is_good_json(str_input):
    if not str_input:
        return False
    elif Path(json_path).is_file() and json_path.lower().endswith('.json'):
        return True
    else:
        print('Проверьте правильность пути и имени файла')
        return False

if __name__ == '__main__':
    json_path, latitude, longitude = None, None, None

    while not is_good_json(json_path):
        json_path = input('Введите путь к JSON-файлу: ')
    while not is_latitude(latitude):
        latitude = input('Введите вашу широту: ')  # E.g.: 55.60
    while not is_longitude(longitude):
        longitude = input('Введите вашу долготу: ')  # E.g.: 37.74

    bars_list = load_data(json_path)
    biggest_bar = get_biggest_bar(bars_list)
    smallest_bar = get_smallest_bar(bars_list)
    closest_bar = get_closest_bar(bars_list, longitude, latitude)

    print('\nСамый большой бар'.upper())
    print('    {}: {} мест'.format(biggest_bar['Name'], biggest_bar['SeatsCount']))

    print('\nСамый маленький бар'.upper())
    print('    {}: {} мест'.format(smallest_bar['Name'], smallest_bar['SeatsCount']))

    print('\nСамый близкий бар'.upper())
    print('    {}, {}, {} ({:.2f} км)'.format(closest_bar['Name'],
                                              closest_bar['District'],
                                              closest_bar['Address'],
                                              closest_bar['Distance']))
