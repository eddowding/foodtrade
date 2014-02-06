# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from django.conf import settings
from mainapp.classes.TweetFeed import TweetFeed, UserProfile, Friends, TwitterError, Invites, InviteId, Notification
from mainapp.classes.Tags import Tags
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
from django.contrib.auth.models import User
from mainapp.bitly import construct_invite_tweet
from django.contrib.auth.decorators import user_passes_test

next_cursor = -1
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''

def calculate_time_ago(calc_time):
    time_elapsed = int(time.time()) - calc_time
    if time_elapsed<60:
        time_text = str(time_elapsed) + 'seconds'
    elif time_elapsed < 3600:
        minutes = time_elapsed/60
        time_text = str(int(minutes)) + 'minutes'
    elif time_elapsed < 3600*24:
        hours = time_elapsed/3600
        time_text = str(int(hours)) + 'hours'
    elif time_elapsed < 3600*24*365:
        days = time_elapsed/3600/24
        time_text = str(int(days)) + 'days'
    else:
        years = time_elapsed/3600/24/365
        time_text = str(int(years)) + 'years'
    return time_text

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
            text = "@" + tweet['user']['screen_name'] + " Thanks! Please confirm your post by clicking this http://fresh.foodtrade.com/?" + tweet['id_str'] + " You'll only have to do this once."
            # try:
            #     bot_twitter.update_status(status = text, in_reply_to_status_id = tweet['id'])
            # except:
            #     pass

    if len(tweet_list)!=0:
        max_id.max_tweet_id = max(tweet_list)
        max_id.save()
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
    page_num = 1
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
                            friends_obj.save_friends({'username':request.user.username,
                                'friends':eachFriend})
                        if next_cursor != 0:
                            friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)
                except:
                    # print "Inside use case 1 exception"
                    twitter_err_obj.save_error({'username':request.user.username, 
                        'next_cursor_str':next_cursor, 'error_solve_stat':'false'})
                # print "Inside use case 1 get values"
                friends = friends_obj.get_paginated_friends(request.user.username, page_num)
                friend_count = friends_obj.get_friends_count(request.user.username)
            else:
                # print "Inside use case 1 else"
                friends = friends_obj.get_paginated_friends(request.user.username, page_num)
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
                        friends_obj.save_friends({'username':request.user.username,
                            'friends':eachFriend})
                    if next_cursor != 0:
                        friends = tweetfeed_obj.get_friends(request.user.id, next_cursor)
            except:
                # print "Inside use case 2 exception"
                twitter_err_obj = TwitterError()
                twitter_err_obj.save_error({'username':request.user.username, 
                    'next_cursor_str':next_cursor, 'error_solve_stat':'false'})
            #print "Inside use case 2 get friends"
            friends = friends_obj.get_paginated_friends(request.user.username, page_num)
            friend_count = friends_obj.get_friends_count(request.user.username)
    friend_list = []

    for eachFriend in friends:
        invites_obj = Invites()
        my_name = request.user.username
        if invites_obj.check_invited(eachFriend['friends']['screen_name'], my_name) == False:
            friend_list.append({'friends':{'screen_name':eachFriend['friends']['screen_name'],
                'name':eachFriend['friends']['name'], 'profile_image_url':eachFriend['friends']['profile_image_url']}})
    
    page_count = int(friend_count/15)+1
    while (len(friend_list) == 0 and page_num <=page_count):
        page_num = page_num + 1
        friends = friends_obj.get_paginated_friends(request.user.username, page_num)
        for eachFriend in friends:
            invites_obj = Invites()
            my_name = request.user.username
            if invites_obj.check_invited(eachFriend['friends']['screen_name'], my_name) == False:
                friend_list.append({'friends':{'screen_name':eachFriend['friends']['screen_name'],
                    'name':eachFriend['friends']['name'], 'profile_image_url':eachFriend['friends']['profile_image_url']}})

    parameters['friend'] = friend_list
    parameters['page_count'] = page_count

    user_profile_obj = UserProfile()
    userprofile = user_profile_obj.get_profile_by_id(request.user.id)
    parameters['userprofile'] = userprofile

    invites_obj = InviteId()
    invite_id = invites_obj.get_unused_id(request.user.id)

    invite_tweet = construct_invite_tweet(request, invite_id)
    parameters['invite_id'] = invite_id['uid']['id']
    parameters ['invite_tweet'] = invite_tweet
    return render_to_response('invites.html', parameters, context_instance=RequestContext(request))



def handle_invitation_hit(request, invite_id):
    request.session['invite_id'] = str(invite_id)
    return HttpResponseRedirect('/')

def notifications(request):
    parameters = {}

    if request.user.is_authenticated():        
        user_id = request.user.id
        user_profile_obj = UserProfile()
        user_profile = user_profile_obj.get_profile_by_id(str(user_id))
        user_info = UserInfo(user_id)
        parameters['userinfo'] = user_info
        parameters['user_id'] = request.user.id

        user_profile_obj = UserProfile()
        userprofile = user_profile_obj.get_profile_by_id(request.user.id)
        parameters['userprofile'] = userprofile
    else:
        return HttpResponseRedirect('/')

    user_name = request.user.username
    user_email = request.user.email

    notices = Notification()
    my_notifications = notices.get_notification(user_name, page_number=1, n_type = 'all')
    parameters['archived_notification_count'] = my_notifications['archived_notification_count']
    parameters['all_notification_count'] = my_notifications['all_notification_count']
    parameters['unread_notification_count'] = my_notifications['unread_notification_count']
    parameters['email'] = user_email
    parameters['screen_name'] = SocialAccount.objects.get(user__id = user_id).extra_data['screen_name']

    myNotice = []
    for eachNotification in my_notifications['notifications']:
        processed_notice = {}
        user_profile_obj = UserProfile()
        notifying_user_profile = user_profile_obj.get_profile_by_username(eachNotification['notifying_user'])
        try:
            if (notifying_user_profile['email'] != ''):
                processed_notice['notifying_user_email'] = notifying_user_profile['email']
        except:
            user = User.objects.get(username = eachNotification['notifying_user'])
            # print eachNotification
            processed_notice['notifying_user_email'] = user.email
        try:
            if (notifying_user_profile['screen_name'] != ''):
                processed_notice['notifying_user_screenname'] = notifying_user_profile['screen_name']
        except:
            processed_notice['notifying_user_screenname'] = account = SocialAccount.objects.get(user__id = request.user.id).extra_data['screen_name']
        processed_notice['notification_id'] = eachNotification['uid']['id']
        processed_notice['notifying_user'] = eachNotification['notifying_user']
        processed_notice['notification_message'] = eachNotification['notification_message'][0:50] + '....'
        processed_notice['notification_message_full'] = eachNotification['notification_message']
        processed_notice['time_elapsed'] = calculate_time_ago(eachNotification['notification_time'])
        processed_notice['notifying_user_profile'] = notifying_user_profile
        processed_notice['notification_view_status'] = eachNotification['notification_view_status']
        myNotice.append(processed_notice)
    parameters['notifications'] = myNotice
    return render_to_response('notice.html', parameters, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def unclaimed_profiles(request):
    parameters = {}    
    tags = Tags()
    parameters['all_tags'] = tags.get_tags()
    if request.user.is_authenticated():
        user_id = request.user.id
        user_info = UserInfo(user_id)
        user_profile_obj = UserProfile()
        userprofile = user_profile_obj.get_profile_by_id(user_id)
        parameters['userprofile'] = UserProfile
        parameters['userinfo'] = user_info
    else:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        if request.GET.get('page') == None:
            page_num =1
        else:
            page_num = int(request.GET['page'])

        user_profile_obj = UserProfile()
        unclaimed_profiles = user_profile_obj.get_unclaimed_profile_paginated(page_num)
        parameters['unclaimed_profiles'] = unclaimed_profiles
        parameters['unclaimed_profiles_json'] = json.dumps(unclaimed_profiles)
        parameters['page'] = page_num
        
    return render_to_response('unclaimed1.html', parameters, context_instance=RequestContext(request))