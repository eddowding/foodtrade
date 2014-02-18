#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from django.conf import settings
from mainapp.classes.Email import Email
from mainapp.classes.TweetFeed import TweetFeed, UserProfile, Friends, TwitterError, Invites, InviteId, Notification, Analytics
from mainapp.classes.mailchimp import MailChimp, MailChimpException
from mainapp.classes.Tags import Tags
from search import *
from streaming import MyStreamer
from models import MaxTweetId
from geolocation import get_addr_from_ip
from django.template import RequestContext
import datetime
from django.core.context_processors import csrf
import time
from pygeocoder import Geocoder
from mainapp.classes.DataConnector import UserInfo
import pprint
from django.contrib.auth.models import User
from mainapp.bitly import construct_invite_tweet
from django.contrib.auth.decorators import user_passes_test
import HTMLParser
from mainapp.classes.Search import Search
from mainapp.classes.Email import Email


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
    user_profile = UserProfile()
    display_tweets = [] 

    for tweet in mentions:
        tweet_list.append(tweet['id'])
        try:
            user_profile = UserProfile()
            usr = user_profile.get_profile_by_username(tweet['user']['screen_name'])
            if usr['useruid'] == -1:
                continue

            pic_url_list = []
            if tweet['entities'].get('media')!= None:
                for each in tweet['entities'].get('media'):
                    pic_url_list.append(each['media_url'])
            h = HTMLParser.HTMLParser()
            tweet_id = str(tweet['id'])
            parent_tweet_id = 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id']
            tweet_feed = TweetFeed()
            data = {'tweet_id': str(tweet_id),
            'parent_tweet_id': str(parent_tweet_id),
            'status': h.unescape(tweet['text']),                    
            'picture': pic_url_list,
            }          
            tweet_feed.insert_tweet_by_username(usr['username'],data)

            
            display_tweets.append(data)
        except:
            tweet_id = str(tweet['id'])
            text = "@" + tweet['user']['screen_name'] + " Thanks! Please confirm your post by clicking this http://foodtrade.com/?tweetid=" + str(tweet_id) + " You'll only have to do this once."

            h = HTMLParser.HTMLParser()
            str_text = h.unescape(tweet['text']).encode('utf-8')
            str_text = str_text.replace("#signup","#join")
            str_text = str_text.replace("#register","#join")
            if "#join" in str_text:
                str_text = str_text.lower()
                str_text = str_text.strip()
                str_text = str_text.replace('@foodtradehq',"")
                str_text = str_text.strip()
                str_text = str_text.replace("#join","")
                str_text = str_text.strip()
                import re
                 
                regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

                user_emails = re.findall(regex, str_text)


                if len(user_emails)>0:
                    user_email = user_emails[0][0]
                    str_text = str_text.replace(user_email, "")
                    location = str_text.strip()
                    create_profile_from_mention(user_email, location, tweet)

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
    if request.GET.get('page')==None:
        page_num =1
    else:
        page_num = int(request.GET.get('page'))

    parameters = {}
    parameters['current_page_number'] = page_num

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
    parameters['friend_count'] = len(friend_list)

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
    # analytics_obj = Analytics()
    # analytics_obj.save({
    #     'site_visit_time':time.mktime(datetime.datetime.now().timetuple()),
    #     'invitation_id':str(invite_id),
    #     'Analytics Type':'Site Visit',
    #     'request_obj':str(request)
    #     })
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
            page_num = 1
            edit_value = 0
        else:
            page_num = int(request.GET['page'])
            edit_value = int(request.GET['edit'])
        if page_num <= 0:
            page_num = 1

        user_profile_obj = UserProfile()
        unclaimed_profiles = user_profile_obj.get_unclaimed_profile_paginated(page_num, edit_value)
        parameters['unclaimed_profiles'] = unclaimed_profiles
        parameters['edit_value'] = edit_value
        parameters['unedited_count'] = user_profile_obj.get_unclaimed_unedited_profile_count()
        parameters['edited_count'] = user_profile_obj.get_unclaimed_edited_profile_count()

        parameters['unclaimed_profiles_json'] = json.dumps(unclaimed_profiles)
        parameters['page_number'] = page_num
        
    return render_to_response('unclaimed.html', parameters, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)    
def transport_mailchimp(request):
    if request.user.is_authenticated:
        user_profile_obj = UserProfile()
        all_users = user_profile_obj.get_all_profiles()
        for eachUser in all_users:
            try:
                if eachUser['email'] == '':
                    continue
                m = MailChimp()
                m.subscribe(eachUser)
            except:
                mail_excep_obj = MailChimpException()
                mail_excep_obj.save_mailchimp_exception(eachUser)

def sms_receiver(request):
    # message = request.POST.get('message')
    body = request.GET.get('Body',"")
    msg_from = request.GET.get('From','')   
    from twilio.rest import TwilioRestClient 
 
    
    user_profile = UserProfile()

    try:
        usr = user_profile.get_profile_by_username(msg_from)
        # if usr['useruid'] == -1:
        #     continue



        pic_url_list = []
        if tweet['entities'].get('media')!= None:
            for each in tweet['entities'].get('media'):
                pic_url_list.append(each['media_url'])

        h = HTMLParser.HTMLParser()
        
        tweet_id = str(tweet['id'])
        parent_tweet_id = 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id']
        tweet_feed = TweetFeed()
        data = {'tweet_id': str(tweet_id),
        'parent_tweet_id': str(parent_tweet_id),
        'status': h.unescape(tweet['text']),                    
        'picture': pic_url_list,
        }          
        tweet_feed.insert_tweet_by_username(usr['username'],data)

        
        display_tweets.append(data)
    except:
        tweet_id = str(tweet['id'])
        
        h = HTMLParser.HTMLParser()
        str_text = body
        if "#join" in str_text:
            str_text = str_text.lower()
            str_text = str_text.strip()
            str_text = str_text.strip()
            str_text = str_text.replace("#join","")
            str_text = str_text.strip()
            import re
             
            regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                                "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                                "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

            user_emails = re.findall(regex, str_text)


            if len(user_emails)>0:
                user_email = user_emails[0][0]
                str_text = str_text.replace(user_email, "")
                location = str_text.strip()
                create_profile_from_mention(user_email, location, tweet)
                # put your own credentials here 
                ACCOUNT_SID = "ACc54d95fd16aa5e6e35dbe60d44f3cc94" 
                AUTH_TOKEN = "69e49be54014f34904e5c08715e0791e" 
                 
                client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
                 
                client.messages.create(
                    to=msg_from, 
                    from_="+442380000486", 
                    body="You have joined FoodTrade",  
                )



def send_newsletter(request, substype):
    user_profile_obj = UserProfile()
    if substype == 'subscribed':
        users = user_profile_obj.get_all_profiles('subscribed')
    elif substype == 'non':
        users = user_profile_obj.get_all_profiles('unsubscribed')
    for eachUser in users:
        search_handle = Search(lon = eachUser['latlng']['coordinates'][0], lat = eachUser['latlng']['coordinates'][1])
        search_results = search_handle.search_all()['results']
        temp_result = []
        no_of_results = 10
        for res in search_results:
            if res["result_type"] == res["user"]["username"]:
                temp_result.append(res)
            if len(temp_result) >= no_of_results:
                break

        results = temp_result
        tem_con = str(render_to_response('activity-email.html',{'results':results}, context_instance=RequestContext(request)))
        tem_con = tem_con.replace('Content-Type: text/html; charset=utf-8', '')
        m = Email()
        m.send_mail("Activity News Letter", [{'name':'main', 'content':tem_con}], [{'email':'brishi98@gmail.com'}])
        
    return HttpResponse(json.dumps({'status':'1'}))

def create_profile_from_mention(email, location, data):
    signup_data = {}
    try:
        location_res = Geocoder.geocode(location)
        latlng = {"type":"Point","coordinates":[float(location_res.longitude) ,float(location_res.latitude)]}
        user_address = location
        postal_code = location_res.postal_code
    except:
        try:
            location_res = Geocoder.geocode(data['user']['location'])
            lat, lon, addr,postal_code = location_res.latitude, location_res.longitude, location_res.postal_code
            latlng = {"type":"Point","coordinates" : [float(lon),float(lat)]}
            signup_data['location_default_on_error'] = 'true'
            user_address = data['user']['location']


        except:
            text = "We cannot recognise your location please try again with a postal code or from http://foodtrade.com"
            HQ_twitter = get_twitter_obj(settings.HQ_ACCESS_TOKEN, settings.HQ_ACCESS_TOKEN_SECRET)
            HQ_twitter.update_status(status = text, in_reply_to_status_id = data['id'])
            return 

    

    user_profile_obj = UserProfile()
    min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1

    signup_data = {
            'is_unknown_profile': 'false',
            'from_mentions': 'true',
            'address' : user_address,
            'latlng':latlng,
            'email' : email,
            'zip_code': str(postal_code),
            'description' : data['user']['description'],
            'foods': [],
            'name' : data['user']['name'],
            'phone_number' : '',
            'profile_img':data['user']['profile_image_url'],
            'sign_up_as': 'Individual',
            'type_user':[],
            'updates': [],
            'screen_name': data['user']['screen_name'],
            'Organisations':[],
            'useruid': min_user_id,
            'username':data['user']['screen_name']
        }
    
    user_profile_obj.create_profile(signup_data)

    return {'status':1}

