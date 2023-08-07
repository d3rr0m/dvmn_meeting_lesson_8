import json
import pprint
import folium
from geopy import distance
from dotenv import dotenv_values
import requests


YANDEX_API_KEY = dotenv_values('.env')['YANDEX_API_KEY']


def gen_map(place, coffee_shops):
    m = folium.Map(location=[place])
    m.save('index.html')


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


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

    sorted_coffee_shops = sorted(coffee_shops_with_distance, key=get_distance_to_cafe)
    five_nearest_coffee_shops = sorted_coffee_shops[:5]
    nearest_cafe = min(coffee_shops_with_distance, key=get_distance_to_cafe)
    #pprint.pprint(nearest_cafe, sort_dicts=False)


if __name__ == '__main__':
    main()
