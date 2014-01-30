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
            
            default_lon = float(user_profile['latlng']['coordinates'][0])
            default_lat = float(user_profile['latlng']['coordinates'][1])
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
        sort = request.POST.get('sort',"distance")
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


        search_handle = Search(keyword=keyword, lon = my_lon, lat =my_lat, place = location, foods=foods, business=businesses, organisation=organisations,sort=sort)
        search_results = search_handle.search_all()
        results =search_results['results'][:40]

        for i in range(len(results)):
            distance_text = ""

            # try:
            lonlat_distance = results[i]['distance'] * 0.621371 #distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
            
            lonlat_distance = '%.1f' % lonlat_distance
            result_class = results[i]["sign_up_as"].lower() 
            for fd in results[i]:
                if fd.lower() == keyword or fd in foods:
                    result_class = result_class + " produce"
                    break
            if results[i]["result_type"] == results[i]["user"]["username"]:
                if keyword in results[i]['status']:
                    result_class = result_class + " updates"

            else:
                result_class = result_class + " profile"

            results[i]["result_class"] = result_class





            # if lonlat_distance>1:
            #     distance_text = str(lonlat_distance) +" Km"
            # else:
            #     distance_text = str(lonlat_distance*1000) + " m"
            distance_text = str(lonlat_distance) + " miles"
            try:
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

            except:
               time_text = ""

            results[i]['distance_text'] = distance_text
            results[i]['time_elapsed'] = time_text


        
        parameters['results'] = results
        parameters['json_data'] = json.dumps(results)
        



        ret_val = {}
        ret_val["updates"] = str(render_to_response('activity_updates.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["biz"] = str(render_to_response('activity_biz.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val["org"] = str(render_to_response('activity_org.html',parameters)).replace("Content-Type: text/html; charset=utf-8","")
        ret_val['results_business_count'] = search_results["business_counter"]
        ret_val['results_organisation_count'] = search_results["organisation_counter"]
        ret_val['results_updates_count'] = search_results["update_counter"]
        return HttpResponse(json.dumps(ret_val))
