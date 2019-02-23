import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

token = config.get('API','G_KEY')

def get_nearby(lat,long):
    latlong = lat + ',' + long

    result = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius=500&type=bus_station&key={}'.format(latlong,token))
    result_json = result.json()["results"]

    nearby_list = []
    for item in result_json:
        itemlat = item["geometry"]['location']['lat']
        itemlng = item["geometry"]['location']['lng']
        name = item["name"]
        nearby_list.append((itemlat,itemlng,name))

    return nearby_list

