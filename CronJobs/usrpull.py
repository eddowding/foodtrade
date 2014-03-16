#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime
import MySQLdb
APP_ROOT = os.path.realpath('..')
APP_ROOT = APP_ROOT.replace('\\','/')
CLASS_PATH = APP_ROOT + '/mainapp/classes'
SETTINGS_PATH = APP_ROOT + '/foodtrade'
sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from MongoConnection import MongoConnection
from TwitterError import TwitterError
from UserProfile import UserProfile
from MySQLConnect import MySQLConnect
import settings_local
from twython import Twython
from pygeocoder import Geocoder

def get_twitter_obj(token, secret):
    return Twython(
        app_key = settings_local.CONSUMER_KEY,
        app_secret = settings_local.CONSUMER_SECRET,
        oauth_token = token,
        oauth_token_secret = secret
        )

def get_friends(screen_name, next_cursor, friend_or_follower):
    mc = MySQLConnect()
    st = mc.get_token(screen_name)
    ACCESS_TOKEN = st[0]
    ACCESS_TOKEN_SECRET = st[1]
    user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    if friend_or_follower == 'friends':
        friends = user_twitter.get_friends_list(screen_name = screen_name, count=200, cursor = next_cursor)
        return friends
    else:
        followers = user_twitter.get_followers_list(screen_name = screen_name, count=200, cursor = next_cursor)
        return followers

def register_user_to_mongo(eachFriend):
    user_profile_obj = UserProfile()
    min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1
    data = {
        'is_unknown_profile':'true',
        'recently_updated_by_super_user': 'false', 
        'useruid': int(min_user_id),
        'sign_up_as': str('unclaimed'),
        'type_user': [], 
        'name': eachFriend['name'],
        'email': '', 
        'description': eachFriend['description'],
        'username' : eachFriend['screen_name'],
        'screen_name': eachFriend['screen_name'],
        'profile_img': eachFriend['profile_image_url'],
        'updates': [],
        'foods':[],
        'organisations':[],
        'subscribed':0,
        'newsletter_freq':'Never'
    }
    try:
        location_res = Geocoder.geocode(invited_friend['friends']['location'])
        data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude) ,float(location_res.latitude)]}
        data['zip_code'] = str(location_res.postal_code)
    except:
        return True

    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    data['join_time'] = int(join_time)
    print data['screen_name']
    '''Register User to Mongo'''
    userprofile = UserProfile()
    userprofile.update_profile_upsert({'screen_name':eachFriend['screen_name'],
        'username':eachFriend['screen_name']},data)
    return True


def process_friends_or_followers(eachUser, friend_or_follower):
    try:
        friends = get_friends(eachUser['username'], -1, friend_or_follower)
    except:
        return
    next_cursor = friend_or_follower,friends['next_cursor']
    try:
        while(next_cursor !='0'):
            next_cursor = friends['next_cursor']
            for eachFriend in friends['users']:
                '''Register this user'''
                if eachFriend['location']!='':
                    register_user_to_mongo(eachFriend)
                if next_cursor != 0:
                    users = get_friends(eachUser['username'], next_cursor, friend_or_follower)
    except:
        twitter_err_obj = TwitterError()
        twitter_err_obj.save_error({'username':eachUser['username'],'error_type':'cron',
            'next_cursor':next_cursor, 'error_solve_stat':'false','user_type':friend_or_follower})
        print "Inside Exception", next_cursor        

def create_users(arg):
    if arg=='all':
        user_profile_obj = UserProfile()
        users = user_profile_obj.get_all_users()
    else:    
        '''get all newly registered users and process their friends and followers'''
        start_time = datetime.datetime.now() - datetime.timedelta(1)
        start_time = time.mktime(start_time.timetuple())
        start_time = int(start_time)

        user_profile_obj = UserProfile()
        users = user_profile_obj.get_all_profiles_by_time(start_time)

    for eachUser in users:
        print eachUser['screen_name']
        process_friends_or_followers(eachUser, 'friends')
        process_friends_or_followers(eachUser, 'followers')
        
def solve_errors():
    te = TwitterError()
    twitter_errors = te.get_unsolved_error('cron')

    '''Solve all previous errors'''
    for eachError in twitter_errors:    
        '''Make Profile for all the friends who have location'''
        if eachError['user_type'] =='friends':
            users = get_friends(eachError['username'], eachError['next_cursor'], 'friends')
        else:
            users = get_friends(eachError['username'], eachError['next_cursor'], 'followers')
        try:
            while(next_cursor !='0'):
                next_cursor = users['next_cursor_str']
                for eachFriend in users['users']:
                    '''Register this user'''
                    if eachFriend['location']!='':
                        register_user_to_mongo(eachFriend)
                    if next_cursor != 0:
                        if eachError['user_type'] =='friends':    
                            users = get_friends(eachError['username'], next_cursor, 'friends')
                        else:
                            users = get_friends(eachError['username'], next_cursor, 'followers')
            '''Normal Flow Update Error Status to Solved'''        
            twitter_err_obj = TwitterError()
            twitter_err_obj.save_error({'username':eachError['username'],'error_solve_stat':'false', 'error_type':'cron'}, 
                {'error_solve_stat':'true'})
        except:
            '''If error occurs save in errors'''
            twitter_err_obj = TwitterError()
            if eachError['user_type'] =='friends':
                twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
                    'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'friends'})
            else:
                twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
                    'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'followers'})

create_users('all')                                
#solve_errors()

