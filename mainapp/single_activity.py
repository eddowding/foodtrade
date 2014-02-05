from django.shortcuts import render_to_response
from django.template import RequestContext
from classes.TweetFeed import TweetFeed, UserProfile
from classes.DataConnector import UserInfo
from classes.Search import Search
from activity import set_time_date
from django.core.context_processors import csrf

def home(request, username, tweet_id):
    parameters={}
    user_profile_obj = UserProfile()
    post_profile = user_profile_obj.get_profile_by_username(str(username))
    parameters.update(csrf(request))
    if request.user.is_authenticated():
        # parameters['user'] = request.user
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
    single_tweet = search_handle.get_single_tweet(str(tweet_id))
    keyword = ''
    single_tweet = set_time_date(single_tweet[0],keyword)
    results = search_handle.get_direct_children([str(tweet_id)])
    if results!= None:
        for i in range(len(results)):
            results[i] = set_time_date(results[i],keyword)
            mentions = "@" + username+ " " + "@" + results[i]['user']['username'] 
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
                # print results[i]['replies']
                results[i]['replies'] = replies

    parameters['results'] = results
    parameters['parent_tweet'] = single_tweet
    return render_to_response('activity_single.html',parameters ,context_instance=RequestContext(request))