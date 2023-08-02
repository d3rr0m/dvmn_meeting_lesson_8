import json
from dotenv import dotenv_values
import requests


YANDEX_API_KEY = dotenv_values('.env')['YANDEX_API_KEY']


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


def main():
    with open('coffee.json', 'r') as file:
        city = input('Input your city: ')
        longitude, altitude = fetch_coordinates(YANDEX_API_KEY, city)
        print(f'Ваши координаты: {longitude}, {altitude}')
        content = file.read()
        coffe_shops = json.loads(content)
        #for cafe in coffe_shops:
            #print(cafe['Name'], cafe['Longitude_WGS84'], cafe['Latitude_WGS84'])


if __name__ == '__main__':
    main()
