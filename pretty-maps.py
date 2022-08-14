
# Prettymaps
from prettymaps import *
# Vsketch
import vsketch
# OSMNX
import osmnx as ox
#json
import json
#datetime
import datetime
from datetime import date
#tweepy
import tweepy
# Matplotlib-related
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
from descartes import PolygonPatch
# Shapely
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union
#import env
from dotenv import load_dotenv
import os

# Credentials
load_dotenv('.env')

def create_pretty_map():
    city_latitude, city_longitude, city_name, city_country = get_city_detail()
    print(city_latitude, city_longitude, city_name, city_country)
    fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)
    layers = plot(
        (city_latitude, city_longitude), radius = 2000,
        ax = ax,
        layers = {
                'perimeter': {},
                'streets': {
                    'custom_filter': '["highway"~"motorway|trunk|primary|secondary|tertiary|residential|service|unclassified|pedestrian|footway"]',
                    'width': {
                        'motorway': 2.5,
                        'trunk': 2.5,
                        'primary': 2.25,
                        'secondary': 2,
                        'tertiary': 1.75,
                        'residential': 1.5,
                        'service': 1,
                        'unclassified': 1,
                        'pedestrian': 1,
                        'footway': 0.5,
                    }
                },
                'water': {'tags': {'natural': ['water', 'bay']}},
                #'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': False},
                #'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
                #'forest': {'tags': {'landuse': 'forest'}},
                #'parking': {'tags': {'amenity': 'parking', 'highway': 'pedestrian', 'man_made': 'pier'}}
            },
            drawing_kwargs = {
                'background': {'fc': '#FFF', 'ec': '#dadbc1', 'zorder': -1},
                'perimeter': {'fc': '#0D0208', 'ec': '#FFF', 'lw': 0, 'zorder': 0},
                'water': {'fc': '#2b5770', 'ec': '#2F3737', 'lw': 1, 'zorder': 2},
                'streets': {'fc': '#22b455', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
                #'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
                #'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
                #'parking': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
                #'building': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
            },

            osm_credit = {'color': '#2F3737'}
    )

    ax.text(
        0.5, 0.5, 
        ' '*3 + city_name + ', ' + city_country + ' '*3, 
        horizontalalignment='center',
        verticalalignment='center', 
        transform=ax.transAxes,
        color = '#FFF',
        backgroundcolor='#101820',
        zorder = 6, 
        fontproperties = fm.FontProperties(fname = 'Orbitron.ttf', size = 30)
    )
    plt.savefig(city_name + '.jpeg')
    #upload_to_twitter(city_name, city_country)

def upload_to_twitter(city_name, city_country):
    #tweepy V2
    #api = tweepy.Client(bearer_token='', consumer_key=consumer_key, consumer_secret=consumer_secret, 
                        #access_token=access_token, access_token_secret=access_token_secret)

    #Connect to api using tweepy V1(only v1 api works as on 10/04/2022)
    auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
    auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
    api = tweepy.API(auth, wait_on_rate_limit = True)

    # Upload image
    media = api.media_upload(city_name + '.jpeg')
    api.update_status(city_name + ', ' + city_country, media_ids = [media.media_id_string])
    

def get_city_detail():
    standard_date = date(2022, 8, 14)
    with open('world_cities.json', encoding="utf8") as data_file:   
        data = json.load(data_file)
        for v in data:
            if(v['uniqueID'] == (datetime.datetime.now().date() - standard_date).days):
                return v['lat'], v['lng'], v['city'], v['country']

def main():
    create_pretty_map()

if __name__ == "__main__":
    main()


  