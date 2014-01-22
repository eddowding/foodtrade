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
        
        default_lon = float(user_profile['longitude'])
        default_lat = float(user_profile['latitude'])
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
    sort = request.GET.get('sort',"distance")
    my_lon = request.GET.get('lon',"")
    my_lat = request.GET.get('lat',"")
    location = request.GET.get('location',default_location)
    if my_lon == "" or my_lat=="":
        my_lon = default_lon
        my_lat = default_lat

    else:
        my_lat = float(my_lat)
        my_lon = float(my_lon)

    organisations =request.GET.get('organisations',"")
    foods = request.GET.get('foods',"")
    businesses =request.GET.get('businesses',"")
    if organisations == "":
        organisations = []
    if businesses == "":
        businesses = []
    if foods == "":
        foods = []


    search_handle = Search(keyword=keyword, lon = my_lon, lat =my_lat, place = location, foods=foods, business=businesses, organisation=organisations, sort=sort)
    results = search_handle.search()
    for i in range(len(results)):
        distance_text = ""
        # try:
        lonlat_distance = results[i]['distance'] * 0.621371 #distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
        
        lonlat_distance = '%.1f' % lonlat_distance
        # if lonlat_distance>1:
        #     distance_text = str(lonlat_distance) +" Km"
        # else:
        #     distance_text = str(lonlat_distance*1000) + " m"
        distance_text = str(lonlat_distance) + " miles"
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

    # For food Filters
    food_filters = search_handle.get_food_filters()
    food_filters_count = 0
    for f in food_filters:
        food_filters_count = food_filters_count + f['value']
    parameters['foods_filter'] = json.dumps(food_filters)
    parameters['food_count'] = int(food_filters_count)


    # For business Filter
    business_filters = search_handle.get_business_filters()
    business_filters_count = 0
    for f in business_filters:
        business_filters_count = business_filters_count + f['value']
    parameters['business_filter'] = json.dumps(business_filters)
    parameters['business_count'] = int(business_filters_count)


    # For organisation Filter
    organisation_filters = search_handle.get_organisation_filters()
    organisation_filters_count = 0
    for f in organisation_filters:
        organisation_filters_count = organisation_filters_count + f['value']
    parameters['organisation_filter'] = json.dumps(organisation_filters)
    parameters['organisation_count'] = int(organisation_filters_count)



    return render_to_response('activity.html',parameters ,context_instance=RequestContext(request))

