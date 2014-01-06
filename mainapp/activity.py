# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from classes.TweetFeed import TweetFeed, UserProfile
from classes.Search import Search
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId
from geolocation import get_addr_from_ip
import time
from classes.DataConnector import UserInfo

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
    parameters = {}

    if request.user.is_authenticated():
        # parameters['user'] = request.user
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        
        default_lon = float(user_profile['longitude'])
        default_lat = float(user_profile['latitude'])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info



    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            location_info = get_addr_from_ip(ip)
            default_lon = float(location_info['longitude'])
            default_lat = float(location_info['latitude'])
        


    keyword = request.GET.get('q',"")
    my_lon = request.GET.get('lon',"")
    my_lat = request.GET.get('lat',"")
    location = request.GET.get('location',"")
    if my_lon == "" or my_lat=="":
        my_lon = default_lon
        my_lat = default_lat

    else:
        my_lat = float(my_lat)
        my_lon = float(my_lon)



    search_handle = Search(keyword, my_lon, my_lat, "nepal")
    results = search_handle.search()
    for i in range(len(results)):
        print results[i]
        distance_text = ""
        # try:
        lonlat_distance = results[i]['distance'] * 0.621371 #distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
        # if lonlat_distance>1:
        #     distance_text = str(lonlat_distance) +" Km"
        # else:
        #     distance_text = str(lonlat_distance*1000) + " m"
        distance_text = str("{:10.2f}".format(lonlat_distance)) + " miles"
        print lonlat_distance
        time_elapsed = int(time.time()) - results[i]['time_stamp']
        if time_elapsed<60:
            time_text = str(time_elapsed) + 'seconds'
        elif time_elapsed < 3600:
            minutes = time_elapsed/60
            time_text = str(minutes) + 'minutes'
        elif time_elapsed < 3600*24:
            hours = time_elapsed/3600
            time_text = str(hours) + 'hours'
        elif time_elapsed < 3600*24*365:
            days = time_elapsed/3600/24
            time_text = str(days) + 'days'
        else:
            years = time_elapsed/3600/24/365
            time_text = str(years) + 'years'

        # except:
        #    pass

        results[i]['distance_text'] = distance_text
        results[i]['time_elapsed'] = time_text


    
    parameters['results'] = results
    parameters['json_data'] = json.dumps(results)
    parameters['search'] = {'query':keyword, 'place':location, 'lon':my_lon, 'lat':my_lat}





    return render_to_response('activity.html',parameters ,context_instance=RequestContext(request))

