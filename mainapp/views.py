# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from django.conf import settings
from mainapp.classes.TweetFeed import TweetFeed, UserProfile, Friends, TwitterError, Invites
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId
from geolocation import get_addr_from_ip
from django.template import RequestContext
import datetime
from django.core.context_processors import csrf
import time
from mainapp.classes.DataConnector import UserInfo
import pprint
next_cursor = -1

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''

def get_twitter_obj(token, secret):
    return Twython(
        app_key = settings.CONSUMER_KEY,
        app_secret = settings.CONSUMER_SECRET,
        oauth_token = token,
        oauth_token_secret = secret
        )

def home(request):
    parameters={}

    user_profile_obj = UserProfile()
    userprofile = user_profile_obj.get_profile_by_id(request.user.id)
    parameters['userprofile'] = UserProfile    
    
    parameters['user'] = request.user
    parameters['total_food_count'] = 2
    parameters['food'] = [{'name': 'Cauliflowers', 'tagcount': 7},{'name': 'Mutton', 'tagcount': 5}]
    parameters['total_business_count'] = 2
    parameters['business'] = [{'name': 'FoodSupply Pvt. Ltd.', 'tagcount': 7},{'name': 'Nina and Hager Meat Industry', 'tagcount': 5}]
    parameters['total_organization_count'] = 2
    parameters['organization'] = [{'name': 'Onion Export', 'tagcount': 7},{'name': 'Bajeko Sekuwa', 'tagcount': 5}]
    return render_to_response('index.html', parameters)

def singlebusiness(request):
    return render_to_response('singlebusiness.html',context_instance=RequestContext(request))

def tweets(request):
    parameters = {}
    HQ_twitter = get_twitter_obj(settings.HQ_ACCESS_TOKEN, settings.HQ_ACCESS_TOKEN_SECRET)
    bot_twitter = get_twitter_obj(settings.BOT_ACCESS_TOKEN, settings.BOT_ACCESS_TOKEN_SECRET)  
    try:
        max_id = MaxTweetId.objects.all()[0]
    except:
        max_id = MaxTweetId(max_tweet_id = 12345)
        max_id.save()
    max_tweet_id = int(max_id.max_tweet_id)
    print 'max_tweet_id', max_tweet_id
    mentions = HQ_twitter.get_mentions_timeline(count = 200, contributer_details = True, since_id = max_tweet_id)
    tweet_list = []
    tweet_feed = TweetFeed()
    user_profile = UserProfile()
    display_tweets = []    
    for tweet in mentions:
        try:
            usr = SocialAccount.objects.get(uid = tweet['user']['id'])
            pic_url_list = []
            if tweet['entities'].get('media')!= None:
                for each in tweet['entities'].get('media'):
                    pic_url_list.append(each['media_url'])
            
            profile = user_profile.get_profile_by_id(str(usr.user.id))
            my_lat = profile['latitude']
            my_lon = profile['longitude']
            data = {'tweet_id': tweet['id'],
                    'parent_tweet_id': 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id'],
                    'status': tweet['text'],
                    'picture': pic_url_list,
                    'user':{
                    'username':tweet['user']['screen_name'],
                    'name': tweet['user']['name'],
                    'profile_img':tweet['user']['profile_image_url'],
                    'Description':tweet['user']['description'],
                    'place':tweet['user']['location'],
                    }
            }
            if my_lon == '' and my_lat == '':
                # get ip address
                ip_addr = get_client_ip(request)
                #get lat, long and address of user
                ip_location = get_addr_from_ip(ip_addr)
                data['location'] = {"type": "Point", "coordinates": [float(ip_location['longitude']), float(ip_location['latitude'])]},
            else:                
                data['location'] = {"type": "Point", "coordinates": [float(my_lon), float(my_lat)]}
            tweet_list.append(tweet['id'])
            tweet_feed.insert_tweet(data)
            display_tweets.append(data)
        except:
            text = "@" + tweet['user']['screen_name'] + " Thanks! Please confirm your post by clicking this http://foodtradelite.cloudapp.net/?" + tweet['id_str'] + " You'll only have to do this once."
            print text
            try:
                bot_twitter.update_status(status = text, in_reply_to_status_id = tweet['id'])
            except:
                pass

    if len(tweet_list)!=0:
        max_id.max_tweet_id = max(tweet_list)
        max_id.save()
    print display_tweets
    parameters['tweet_list'] = display_tweets
    return render_to_response('home.html', parameters)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def trends(request):
    parameters = {}
    t_feed_obj = TweetFeed()

    if request.method == 'GET':
        start_time = datetime.date.today() - datetime.timedelta(7)
        end_time = datetime.date.today() 

    else:
        if request.POST['start_time'] != '':
            start_time = datetime.datetime.strptime(request.POST['start_time'], '%Y-%m-%d')
        else:
            start_time = datetime.date.today() - datetime.timedelta(7)
        if request.POST['end_time'] != '':
            end_time = datetime.datetime.strptime(request.POST['end_time'], '%Y-%m-%d')
        else:
            end_time = datetime.date.today() 
    

    start_time = time.mktime(start_time.timetuple())
    end_time = time.mktime(end_time.timetuple())
    results = t_feed_obj.get_trending_hashtags(start_time, end_time)
    new_results = []
    for sub in results:
        sub['value'] = int(sub['value'])
        new_results.append(sub)

    parameters['results'] = new_results[0:20]
    parameters.update(csrf(request))

    if request.user.is_authenticated():        
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        parameters['user_id'] = request.user.id

        user_profile_obj = UserProfile()
        userprofile = user_profile_obj.get_profile_by_id(request.user.id)
        parameters['userprofile'] = UserProfile

    return render_to_response('trends.html', parameters, context_instance=RequestContext(request))

def invite(request):
    parameters = {}
    tweetfeed_obj = TweetFeed()
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/') 

    if request.user.is_authenticated():        
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        parameters['user_id'] = request.user.id   

    if request.method == 'GET':
        friends_obj = Friends()
        friends_count = friends_obj.get_friends(request.user.username)
        if len(friends_count) > 0:
            twitter_err_obj = TwitterError()
            twitter_error = twitter_err_obj.get_error(request.user.username)
            twitter_err_obj.change_error_status(request.user.username)
            # print twitter_error
            if len(twitter_error) > 0:
                # print "Inside use case 1"
                try:
                    next_cursor = twitter_error[0]['next_cursor_str'] 
                    # print next_cursor     
                    friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)
                    count = 0
                    while(next_cursor !='0'):
                        # print "Inside use case 1 while loop"
                        next_cursor = friends['next_cursor_str']
                        friends_obj = Friends()
                        count = count + 1
                        for eachFriend in friends['users']:
                            friends_obj.save_friends({'username':request.user.username,'friends':eachFriend})
                        if next_cursor != 0:
                            friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)
                except:
                    # print "Inside use case 1 exception"
                    twitter_err_obj.save_error({'username':request.user.username, 
                        'next_cursor_str':next_cursor, 'error_solve_stat':'false'})
                # print "Inside use case 1 get values"
                friends = friends_obj.get_paginated_friends(request.user.username, 1)
                friend_count = friends_obj.get_friends_count(request.user.username)
            else:
                # print "Inside use case 1 else"
                friends = friends_obj.get_paginated_friends(request.user.username, 1)
                friend_count = friends_obj.get_friends_count(request.user.username)
        else:
            # print "Inside use case 2"
            next_cursor = -1
            friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)            
            count = 0 
            try:
                while (next_cursor != 0):
                    # print "Inside use case 1 while loop"
                    next_cursor = friends['next_cursor_str']
                    friends_obj = Friends()
                    count = count + 1
                    for eachFriend in friends['users']:
                        friends_obj.save_friends({'username':request.user.username,'friends':eachFriend})
                    if next_cursor != 0:
                        friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)
            except:
                # print "Inside use case 2 exception"
                twitter_err_obj = TwitterError()
                twitter_err_obj.save_error({'username':request.user.username, 
                    'next_cursor_str':next_cursor, 'error_solve_stat':'false'})
            #print "Inside use case 2 get friends"
            friends = friends_obj.get_paginated_friends(request.user.username, 1)
            friend_count = friends_obj.get_friends_count(request.user.username)
    friend_list = []
    for eachFriend in friends:
        invites_obj = Invites()
        if invites_obj.check_invited(eachFriend['friends']['screen_name']) == False:
            friend_list.append({'friends':{'screen_name':eachFriend['friends']['screen_name'],
                'name':eachFriend['friends']['name'], 'profile_image_url':eachFriend['friends']['profile_image_url']}})
    parameters['friend'] = friend_list
    parameters['page_count'] = int(friend_count/15)+1

    user_profile_obj = UserProfile()
    userprofile = user_profile_obj.get_profile_by_id(request.user.id)
    parameters['userprofile'] = UserProfile

    return render_to_response('invites.html', parameters, context_instance=RequestContext(request))