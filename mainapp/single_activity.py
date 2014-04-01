from django.shortcuts import render_to_response
from django.template import RequestContext
from classes.TweetFeed import TweetFeed, UserProfile
from classes.DataConnector import UserInfo
from classes.Search import Search
from activity import set_time_date
from django.core.context_processors import csrf
from geolocation import get_addr_from_ip
import json
import pprint
from django.http import Http404
from mainapp.profilepage import get_banner_url

def get_post_parameters(request, tweet_id):
    parameters={}

    user_profile_obj = UserProfile()
    parameters.update(csrf(request))
    if request.user.is_authenticated():
        user_id = request.user.id
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

    search_handle = Search(lon = default_lon, lat =default_lat)
    try:
        single_tweet = search_handle.get_single_tweet(str(tweet_id))
        a = single_tweet[0]
    except:
        raise Http404
    keyword = ''
    single_tweet = set_time_date(single_tweet[0],keyword)
    results = search_handle.get_direct_children(str(tweet_id))

    # send banner url
    parameters['banner_url'] = get_banner_url(single_tweet['user']['username'])
    if results!= None:
        for i in range(len(results)):
            results[i] = set_time_date(results[i],keyword)
            mentions = "@" + single_tweet['user']['username']+ " " + "@" + results[i]['user']['username'] 
            results[i]['mentions'] = mentions

            if results[i]["result_type"] == results[i]["user"]["username"]:
                tweet_id = results[i]["tweetuid"]
                replies = search_handle.get_all_children([tweet_id])
                if replies == None:
                    continue
                replies = sorted(replies, key=lambda k: k['time_stamp']) 
                for j in range(len(replies)):
                    replies[j] = set_time_date(replies[j],keyword)
                    replies[j]['mentions'] = mentions + " " + replies[j]['mentions']
                results[i]['replies'] = replies
    single_tweet['user']['profile_img'] = single_tweet['user']['profile_img'].replace("normal","bigger")
    try:
        single_tweet['user']['business_org_name'] = str(single_tweet['user']['business_org_name'])
    except:
        pass
    parameters['results'] = results
    parameters['json_data'] = json.dumps(results)
    parameters['parent_tweet'] = single_tweet
    addr = single_tweet['user']['address'].split(',')
    parameters['tweet_country'] = addr[len(addr)-1].strip()
    parameters['parent_json'] = json.dumps(single_tweet)
    parameters['s_userinfo'] = UserInfo(single_tweet['useruid'])

    return parameters



def home(request, username, tweet_id):    
    return render_to_response('activity_single.html',get_post_parameters(request,tweet_id),context_instance=RequestContext(request))