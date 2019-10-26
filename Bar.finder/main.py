import argparse
import folium
import json
import logging
import os
import requests
from dotenv import load_dotenv
from flask import Flask
from geopy import distance
from os import listdir

def get_distance_to_bar(bar):
    return bar['distance']

def get_bars_map():
    with open('index.html') as file:
        return file.read()

def get_my_location(own_location, yandex_token):
    url = 'https://geocode-maps.yandex.ru/1.x'
    payload = {
        'apikey': yandex_token,
        'format': 'json',
        'lang': 'ru_RU',
        'results': 1,
        'geocode': own_location,
    }
    response = requests.get(url, params=payload)
    if check_for_errors(response, own_location):
        response = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        my_location = tuple(reversed(response.split()))
        return my_location
    return None

def check_for_errors(response, location):
    if not response.ok:
        response = response.json()
        error = response['error']
        message = response['message']
        logging.error(f'Yandex stoped with "{error}" and message "{message}".')
        return None
    logging.info(f'All request parameters found. Status code {response.status_code}. >>>OK!')
    response = response.json()['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']
    if response == '0':
        logging.error(f'Yandex cannot find location "{location}".')
        return None
    logging.info(f'Found locations {response}. >>>OK!')
    return True

def get_database_file():
    filenames_list = listdir()
    database_file = None
    for filename in filenames_list:
        if filename.endswith('.json'):
            database_file = filename
            logging.info(f'Find JSON file {database_file}. >>>OK!')
    if not database_file:
        logging.error(f'''
         Can not find JSON database file.
         Please download and unpack this file to the same own folder (http://bit.ly/32KGz3l).
         After this run script again.
         ''')
        return None
    return database_file


def get_moscow_bars_data(database_file):
    with open(database_file, 'r', encoding='CP1251') as file:
        bars_data = json.load(file)
        return bars_data


def get_set_of_bars(my_location, bars_data):
    set_of_bars = []
    for bar in bars_data:
        bar_description = {}
        bar_title = bar['Name']
        bar_location = tuple(reversed(bar['geoData']['coordinates']))
        bar_latitude = bar_location[0]
        bar_longitude = bar_location[1]
        distance_to_bar = distance.distance(my_location, bar_location).km
        bar_description.update(
            {
                'title': bar_title,
                'longitude': bar_longitude,
                'latitude': bar_latitude,
                'distance': distance_to_bar
            }
        )
        set_of_bars.append(bar_description)
    return set_of_bars

def get_close_in_x_bars(set_of_bars, number_of_close_in_bars):
    close_in_bars = sorted(set_of_bars, key=get_distance_to_bar)
    close_in_x_bars = close_in_bars[:number_of_close_in_bars]
    return close_in_x_bars

def create_map_with_close_in_bars(my_map, close_in_x_bars):
    for bar in close_in_x_bars:
        bar_location = [bar['latitude'], bar['longitude']]
        folium.Marker(
            location = bar_location,
            popup=bar['title'],
            icon=folium.Icon(color='green'),
        ).add_to(my_map)
    return my_map

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find your BAR %)')
    parser.add_argument('-t', '--token', help='Add your own YANDEX Token')
    parser.add_argument('-l', '--location', help='Add your "own location" (with " ")')
    parser.add_argument('-sl', '--showlog', help='YES - to show log message')

    args = parser.parse_args()

    showlog = args.showlog
    if showlog:
        logging.basicConfig(level=logging.INFO)

    own_location = args.location
    if not own_location:
        logging.info('Get location from user input')
        own_location = input('Please input your location: ')

    yandex_token = args.token
    if not yandex_token:
        load_dotenv()
        logging.info('Get YANDEX token from .env file')
        yandex_token = os.getenv("YA_TOKEN")

    try:
        my_location = get_my_location(own_location, yandex_token)
    except requests.exceptions.ConnectionError:
        logging.error(f'Connection Error: Please check your Internet connection and try later.')
        exit()

    if not my_location:
        exit()

    database_file = get_database_file()
    if not database_file:
        exit()

    bars_data = get_moscow_bars_data(database_file)

    set_of_bars = get_set_of_bars(my_location, bars_data)

    number_of_close_in_bars = 5

    close_in_x_bars = get_close_in_x_bars(set_of_bars, number_of_close_in_bars)

    my_map = folium.Map(location=my_location, zoom_start=16)

    my_map = create_map_with_close_in_bars(my_map,close_in_x_bars)

    my_map.save('index.html')

    app = Flask(__name__)
    app.add_url_rule('/', 'My bars map', get_bars_map)
    app.run('0.0.0.0')