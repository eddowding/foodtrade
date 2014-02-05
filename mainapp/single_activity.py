from django.shortcuts import render_to_response
from django.template import RequestContext
from classes.TweetFeed import TweetFeed, UserProfile
from classes.DataConnector import UserInfo

def home(request, username, tweet_id):
    parameters={}
    user_profile_obj = UserProfile()
    post_profile = user_profile.get_profile_by_username(str(username))
    
    if request.user.is_authenticated():
        # parameters['user'] = request.user
        user_id = request.user.id
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        
        # default_lon = float(user_profile['latlng']['coordinates'][0])
        # default_lat = float(user_profile['latlng']['coordinates'][1])
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        # default_location = user_profile['zip_code']

    return render_to_response('activity_single.html',parameters ,context_instance=RequestContext(request))