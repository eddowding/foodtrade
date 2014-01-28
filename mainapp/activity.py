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

from django.template import RequestContext
from mainapp.classes.AjaxHandle import AjaxHandle
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    parameters = {}

    default_location = ""

    if request.user.is_authenticated():
        # parameters['user'] = request.user
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        
        default_lon = float(user_profile['latlng']['coordinates'][0])
        default_lat = float(user_profile['latlng']['coordinates'][1])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        default_location = user_profile['zip_code']



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
    sort = request.GET.get('sort',"time")
    my_lon = request.GET.get('lon',"")
    my_lat = request.GET.get('lat',"")
    location = request.GET.get('location',default_location)
    biz_request = request.GET.get('b',"")
    food_request = request.GET.get('f',"")
    organisation_request = request.GET.get('o',"")


    if len(biz_request)>0:
        businesses = [biz_request]
    else:
        businesses = []

    if len(food_request)>0:
        foods = [food_request]
    else:
        foods = []

    if len(organisation_request)>0:
        organisations = [organisation_request]
    else:
        organisations = []



    if my_lon == "" or my_lat=="":
        my_lon = default_lon
        my_lat = default_lat

    else:
        my_lat = float(my_lat)
        my_lon = float(my_lon)

    keyword = keyword.lower()
    search_handle = Search(keyword=keyword, lon = my_lon, lat =my_lat, place = location, foods=foods, business=businesses, organisation=organisations, sort=sort)
    search_results = search_handle.search_all()
    results =search_results['results'][:20]

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
    parameters['search'] = {'query':keyword, 'place':location, 'lon':my_lon, 'lat':my_lat}

    # For food Filters
    food_filters = search_results["foods"]
    food_filters_count = 0
    for f in food_filters:
        if (f["uid"] == food_request or f["uid"].lower() == keyword) and f["uid"]!="":
            f["prev"] = True
        if f["uid"]=="":
            food_filters.remove(f)
        else:
            food_filters_count = food_filters_count + f['value']
    parameters['foods_filter'] = json.dumps(food_filters)
    parameters['food_count'] = int(food_filters_count)


    # For business Filter
    business_filters = search_results["businesses"]
    business_filters_count = 0


    for f in business_filters:        

        if f["uid"]=="":
            business_filters.remove(f)
        else:
            business_filters_count = business_filters_count + f['value']
        if (f["uid"] == biz_request or f["uid"].lower() == keyword) and f["uid"]!="":
            f["prev"] = True



    parameters['business_filter'] = json.dumps(business_filters)
    parameters['business_count'] = int(business_filters_count)


    # For organisation Filter
    organisation_filters = search_results["organisations"]
    organisation_filters_count = 0
    for f in organisation_filters:
        if (f["uid"] == organisation_request or f["uid"].lower() == keyword) and f["uid"]!="":
            f["prev"] = True
        if f["uid"]=="":
            organisation_filters.remove(f)
        else:
            organisation_filters_count = organisation_filters_count + f['value']
    parameters['organisation_filter'] = json.dumps(organisation_filters)
    parameters['organisation_count'] = int(organisation_filters_count)


    return render_to_response('activity.html',parameters ,context_instance=RequestContext(request))

