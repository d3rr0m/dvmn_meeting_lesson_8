import json
from folium import Map, Marker
from geopy import distance
from dotenv import dotenv_values
from flask import Flask

from fetch_coordinates import fetch_coordinates


YANDEX_API_KEY = dotenv_values('.env')['YANDEX_API_KEY']
HTML_FILENAME = 'index.html'


def save_map_to_disk(map: Map):
    map.save(HTML_FILENAME)


def gen_map(place, coffee_shops):
    map = Map(location=place, zoom_start=13)

    for coffee_shop in coffee_shops:
        Marker(
            [coffee_shop['latitude'],
             coffee_shop['longitude']],
            tooltip=coffee_shop['name']
            ).add_to(map)

    save_map_to_disk(map)


def get_distance_to_cafe(cafe):
    return cafe['distance']


def main():
    place = input('Введите ваше местопорожение: ')
    place_longitude, place_latitude = fetch_coordinates(YANDEX_API_KEY, place)
    print(f'Ваши координаты: {place_longitude, place_latitude}')

    with open('coffee.json', 'r') as file:
        content = file.read()
        coffee_shops = json.loads(content)

    coffee_shops_with_distance = [{
        'name': cafe['Name'],
        'longitude': cafe['Longitude_WGS84'],
        'latitude': cafe['Latitude_WGS84'],
        'distance': distance.distance(
            (place_latitude, place_longitude),
            (cafe['Latitude_WGS84'], cafe['Longitude_WGS84'])).km,
        }
        for cafe in coffee_shops]

    sorted_coffee_shops = sorted(
        coffee_shops_with_distance,
        key=get_distance_to_cafe,
        )
    five_nearest_coffee_shops = sorted_coffee_shops[:5]

    gen_map([place_latitude, place_longitude], five_nearest_coffee_shops)
    run_site()


def get_site():
    with open(HTML_FILENAME, 'r') as file:
        return file.read()


def run_site():
    app = Flask(__name__)
    app.add_url_rule('/', 'coffee shops near your location', get_site)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
