# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from classes.TweetFeed import TweetFeed, UserProfile
from classes.Search import Search
from classes.Search2 import Search2
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId
from geolocation import get_addr_from_ip
import time
from classes.DataConnector import UserInfo

from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt

from djstripe.models import Customer
import pprint
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property





def get_time(time_val):
    time_elapsed = int(time.time()) - time_val         
    if time_elapsed<60:
        time_text = str(time_elapsed) + ' seconds'
    elif time_elapsed < 3600:
        minutes = time_elapsed/60
        time_text = str(minutes) + ' minutes'
    elif time_elapsed < 3600*24:
        hours = time_elapsed/3600
        time_text = str(hours) + ' hours'
    elif time_elapsed < 3600*24*365:
        days = time_elapsed/3600/24
        time_text = str(days) + ' days'
    else:
        years = time_elapsed/3600/24/365
        time_text = str(years) + ' years'
    return time_text


def set_time_date(single_result,keyword):
    distance_text = ""


    # try:
    lonlat_distance = single_result['distance'] * 0.621371 #distance(my_lon, my_lat, single_result['location']['coordinates'][0],single_result['location']['coordinates'][1])
    
    lonlat_distance = '%.1f' % lonlat_distance
    result_class = single_result["sign_up_as"].lower()
    try: 
        for fd in single_result["foods"]:
            if fd.lower() == keyword or fd in foods:
                result_class = result_class + " produce"
                break
    except:
        pass
    try:
        if single_result["result_type"] == single_result["user"]["username"]:
            if keyword in single_result['status']:
                result_class = result_class + " updates"



        else:
            result_class = result_class + " profile"
    except:
        pass

    single_result["result_class"] = result_class





    # if lonlat_distance>1:
    #     distance_text = str(lonlat_distance) +" Km"
    # else:
    #     distance_text = str(lonlat_distance*1000) + " m"
    distance_text = str(lonlat_distance) + " miles"
    if single_result['location']['coordinates'][0] == -135.10000000000002 and single_result['location']['coordinates'][1] == -82.86275189999999:
        distance_text = "NA"
        single_result['user']['address'] = "NA"
    try:
        single_result['time_elapsed'] = get_time(single_result['time_stamp'])

    except:
       time_text = ""

    single_result['distance_text'] = distance_text
    return single_result

def get_search_parameters(request):
    parameters = {}

    default_location = ""
    no_of_results = 5

    if request.user.is_authenticated():
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))

        default_lon = float(user_profile['latlng']['coordinates'][0])
        default_lat = float(user_profile['latlng']['coordinates'][1])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        default_location = user_profile['zip_code']



        no_of_results = 10
        subscribed = True

        customer, created = Customer.get_or_create(request.user)
        if created:
            subscribed = False

        if not customer.has_active_subscription():
            subscribed = False

        if subscribed:
            no_of_results = 30


    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]

        else:
            ip = request.META.get('REMOTE_ADDR')
        location_info = get_addr_from_ip(ip)
        subscribed = False
        default_lon = float(location_info['longitude'])
        default_lat = float(location_info['latitude'])

    keyword = request.GET.get('q',request.POST.get('q',""))
    keyword = keyword.strip()
    sort = request.GET.get('sort',request.POST.get('sort',"time"))
    my_lon = request.GET.get('lon',request.POST.get('lon',""))
    my_lat = request.GET.get('lat',request.POST.get('lat',"") ) 
    location = request.GET.get('location',default_location)
    biz_request = request.GET.get('b',"")
    food_request = request.GET.get('f',"")
    organisation_request = request.GET.get('o',"")


    no_of_results = 30

    if len(biz_request)>0:
        businesses = [biz_request]
    else:
        businesses = json.loads(request.POST.get('businesses',"[]"))

    if len(food_request)>0:
        foods = [food_request]
    else:
        foods = json.loads(request.POST.get('foods',"[]"))

    if len(organisation_request)>0:
        organisations = [organisation_request]
    else:
        organisations = json.loads(request.POST.get('organisations',"[]"))



    if my_lon == "" or my_lat=="":
        my_lon = default_lon
        my_lat = default_lat

    else:
        my_lat = float(my_lat)
        my_lon = float(my_lon)

    keyword = keyword.lower()

    search_global = subscribed



    if request.user.is_superuser:
        search_global = True
    search_handle = Search(keyword=keyword, lon = my_lon, lat =my_lat, place = location, foods=foods, business=businesses, organisation=organisations, sort=sort, search_global=search_global)
    search_results = search_handle.search_all()
    results =search_results['results'][:no_of_results-1]
    results =search_results['results']
    if request.user.is_superuser:
        results =search_results['results']

    for i in range(len(results)):
        results[i] = set_time_date(results[i],keyword)
        results[i]['mentions'] = "@" + results[i]['user']['username'] 
        user_loc = results[i]['location']


        if results[i]["result_type"] == results[i]["user"]["username"]:
            tweet_id = results[i]["tweetuid"]
            replies = search_handle.get_all_children(tweet_id)
            if replies == None:
                continue
            replies = sorted(replies, key=lambda k: k['time_stamp']) 
            for j in range(len(replies)):
                replies[j] = set_time_date(replies[j],keyword)
                replies[j]['mentions'] = "@" + results[i]['user']['username'] + " " + replies[j]['mentions']
        
            results[i]['replies'] = replies

    for i in range(len(results)):
        from mainapp.profilepage import get_banner_url
        from mainapp.profilepage import get_video_html
        banner_url = get_banner_url(username=results[i]['user']['username'],logged_useruid=request.user.id)
        results[i]['user']['banner_url'] = banner_url
        user_prof = UserProfile()
        try:
            video_url = user_prof.get_profile_by_username(results[i]['user']['username'])['video_url']
            video_html = get_video_html(video_url)
        except:
            video_url = ''
            video_html = ''
        results[i]['user']['intro_video'] =  video_html
    
            
    parameters['results'] = results

    # print len(results)
    parameters['json_data'] = json.dumps(results)
    parameters['results_business_count'] = search_results["business_counter"]
    parameters['results_individual_count'] = search_results["individual_counter"]
    parameters['results_organisation_count'] = search_results["organisation_counter"]
    parameters['results_updates_count'] = search_results["update_counter"]


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

    business_filters_temp = []
    for f in business_filters:        

        if f["uid"]=="":
            continue
        else:
            business_filters_count = business_filters_count + f['value']
        if (f["uid"] == biz_request or f["uid"].lower() == keyword) and f["uid"]!="":
            f["prev"] = True


        business_filters_temp.append(f)
    business_filters = business_filters_temp




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
    return parameters




    

@csrf_exempt
def home(request): 
    # print request['subscribed']
    return render_to_response('activity.html',get_search_parameters(request) ,context_instance=RequestContext(request))


@csrf_exempt
def activity_suppliers(request,request_type): 
    parameters = {}

    if request.user.is_authenticated():
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))

        default_lon = float(user_profile['latlng']['coordinates'][0])
        default_lat = float(user_profile['latlng']['coordinates'][1])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        default_location = user_profile['zip_code']



        no_of_results = 10
        subscribed = True

        customer, created = Customer.get_or_create(request.user)
        if created:
            subscribed = False

        if not customer.has_active_subscription():
            subscribed = False

        if subscribed:
            no_of_results = 30


    else:
        return HttpResponseRedirect("/activity")

    request_types = ['suppliers','stockists','favourites']

    if request_type not in request_types:
        return HttpResponseRedirect("/activity")

    my_lon = default_lon
    my_lat = default_lat



    search_global = subscribed

    keyword = ""

    if request.user.is_superuser:
        search_global = True
    search_handle = Search(lon = my_lon, lat =my_lat)
    search_results = search_handle.supplier_updates(user_id, request_type)
    results =search_results['results'][:no_of_results-1]
    results =search_results['results']
    if request.user.is_superuser:
        results =search_results['results']

    for i in range(len(results)):
        results[i] = set_time_date(results[i],"")
        results[i]['mentions'] = "@" + results[i]['user']['username'] 
        user_loc = results[i]['location']


        if results[i]["result_type"] == results[i]["user"]["username"]:
            tweet_id = results[i]["tweetuid"]
            replies = search_handle.get_all_children(tweet_id)
            if replies == None:
                continue
            replies = sorted(replies, key=lambda k: k['time_stamp']) 
            for j in range(len(replies)):
                replies[j] = set_time_date(replies[j],keyword)
                replies[j]['mentions'] = "@" + results[i]['user']['username'] + " " + replies[j]['mentions']
        
            results[i]['replies'] = replies

    for i in range(len(results)):
        from mainapp.profilepage import get_banner_url
        from mainapp.profilepage import get_video_html
        banner_url = get_banner_url(username=results[i]['user']['username'],logged_useruid=request.user.id)
        results[i]['user']['banner_url'] = banner_url
        user_prof = UserProfile()
        try:
            video_url = user_prof.get_profile_by_username(results[i]['user']['username'])['video_url']
            video_html = get_video_html(video_url)
        except:
            video_url = ''
            video_html = ''
        results[i]['user']['intro_video'] =  video_html
    
            
    parameters['results'] = results

    # print len(results)
    parameters['json_data'] = json.dumps(results)
    parameters['results_business_count'] = search_results["business_counter"]
    parameters['results_individual_count'] = search_results["individual_counter"]
    parameters['results_organisation_count'] = search_results["organisation_counter"]
    parameters['results_updates_count'] = search_results["update_counter"]


    parameters['search'] = {'query':"", 'place':"", 'lon':my_lon, 'lat':my_lat}

    # For food Filters
    food_filters = search_results["foods"]
    food_filters_count = 0
    for f in food_filters:
      
        if f["uid"]=="":
            food_filters.remove(f)
        else:
            food_filters_count = food_filters_count + f['value']
    parameters['foods_filter'] = json.dumps(food_filters)
    parameters['food_count'] = int(food_filters_count)


    # For business Filter
    business_filters = search_results["businesses"]
    business_filters_count = 0

    business_filters_temp = []
    for f in business_filters:        

        if f["uid"]=="":
            continue
        else:
            business_filters_count = business_filters_count + f['value']
        


        business_filters_temp.append(f)
    business_filters = business_filters_temp




    parameters['business_filter'] = json.dumps(business_filters)
    parameters['business_count'] = int(business_filters_count)


    # For organisation Filter
    organisation_filters = search_results["organisations"]
    organisation_filters_count = 0
    for f in organisation_filters:
      
        if f["uid"]=="":
            organisation_filters.remove(f)
        else:
            organisation_filters_count = organisation_filters_count + f['value']
    parameters['organisation_filter'] = json.dumps(organisation_filters)
    parameters['organisation_count'] = int(organisation_filters_count)

    return render_to_response('supplier_updates.html',parameters ,context_instance=RequestContext(request))