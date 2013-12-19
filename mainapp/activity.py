# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from classes.TweetFeed import TweetFeed
from classes.Search import Search
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId


consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'

from math import radians, cos, sin, asin, sqrt
def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


from django.template import RequestContext


from mainapp.classes.AjaxHandle import AjaxHandle


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def home(request):
    keyword = request.GET.get('q',"")
    my_lon = float(request.GET.get('lon',85.33333330000005))
    my_lat = float(request.GET.get('lat',27.7))
    location = request.GET.get('location',"")
    if my_lon == "" or my_lat=="":
        my_lon = 85.33333330000005
        my_lat = 27.7



    tweet_doc = {
        'tweet_id':543654,
        'parent_tweet_id':0,
        'status':" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.",    
        'location':{"type": "Point", "coordinates": [float(my_lon), float(my_lat)]},
        'user':{
        'username':"david",
        'name': "David Villa",
        'profile_img':"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
        'Description':"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod",
        'place':"78 Example Street, Test Town"
        }
    }
    from pymongo import Connection
    c = Connection()
    c.drop_database('foodtrade')
    tweet_handler = TweetFeed() 
    tweet_handler.insert_tweet(tweet_doc)

    search_handle = Search(keyword, my_lon, my_lat, "nepal")
    results = search_handle.search()

    for i in range(len(results)):
        
        distance_text = ""
        # try:
        lonlat_distance = distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
        if lonlat_distance>1:
            distance_text = str(lonlat_distance) +" Km"
        else:
            distance_text = str(lonlat_distance*1000) + " m"
        # except:
            pass

        results[i]['distance_text'] = distance_text


    parameters = {}
    parameters['results'] = results
    parameters['search'] = {'query':keyword, 'place':location, 'lon':my_lon, 'lat':my_lat}





    return render_to_response('activity.html',parameters ,context_instance=RequestContext(request))

