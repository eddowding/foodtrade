# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.geolocation import get_addr_from_ip
from mainapp.classes.TweetFeed import TweetFeed
from mainapp.classes.Email import Email
from Tags import Tags
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood
from Search import Search
import time
from mainapp.classes.DataConnector import UserInfo
consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'




class AjaxSearch():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    
    def ajax_search(self,request):
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

            


        keyword = request.POST.get('q',"")
        my_lon = request.POST.get('lon',"")
        my_lat = request.POST.get('lat',"")
        location = request.POST.get('location',"")
        if my_lon == "" or my_lat=="":
            my_lon = default_lon
            my_lat = default_lat

        else:
            my_lat = float(my_lat)
            my_lon = float(my_lon)

        organisations =request.POST.get('organisations',"")
        foods = request.POST.get('foods',"")
        businesses =request.POST.get('businesses',"")
        if organisations == "":
            organisations = []

        else:
            organisations = json.loads(organisations)
        if businesses == "":
            businesses = []
        else:
            businesses = json.loads(businesses)
        if foods == "":
            foods = []
        else:
            foods = json.loads(foods)


        search_handle = Search(keyword=keyword, lon = my_lon, lat =my_lat, place = location, foods=foods, business=businesses, organisation=organisations)
        results = search_handle.search()
        for i in range(len(results)):
            distance_text = ""
            # try:
            lonlat_distance = results[i]['distance'] * 0.621371 #distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
            # if lonlat_distance>1:
            #     distance_text = str(lonlat_distance) +" Km"
            # else:
            #     distance_text = str(lonlat_distance*1000) + " m"
            distance_text = str("{:10.2f}".format(lonlat_distance)) + " miles"
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
        return render_to_response('activity_ajax.html',parameters)