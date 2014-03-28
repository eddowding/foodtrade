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
from settings_local import *
from twython import Twython
from pygeocoder import Geocoder
from friends import Friends
    
def get_twitter_obj(token, secret):
    return Twython(
        app_key = CONSUMER_KEY,
        app_secret = CONSUMER_SECRET,
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

def register_user_to_mongo(eachFriend, username=''):
    data = {
        'is_unknown_profile':'true',
        'recently_updated_by_super_user': 'false', 
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
        location_res = Geocoder.geocode(eachFriend['location'])
        data['address'] = str(location_res)
        data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude),float(location_res.latitude)]}
        data['zip_code'] = str(location_res.postal_code)
    except:
        data['address'] = str('Antartica')
        data['latlng'] = {"type":"Point","coordinates":[float(-135.10000000000002) ,float(-82.86275189999999)]}
        data['zip_code'] = str('')
        data['location_default_on_error'] = 'true'

    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    data['join_time'] = int(join_time)

    '''Register User to Mongo'''

    friend_obj = Friends()
    print data['screen_name'], "updating Friend"
    friend_obj.save_friend({'username':username, 'friends':eachFriend})
    userprofile = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, 
        conn_type='remote', username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
    min_user_id = int(userprofile.get_minimum_id_of_user()[0]['minId']) -1
    print min_user_id
    data['useruid'] = min_user_id
    check = userprofile.get_profile_by_username(eachFriend['screen_name'])
    if check ==None:
        userprofile.update_profile_upsert({'screen_name':eachFriend['screen_name'],'username':eachFriend['screen_name']},data)
        print data['screen_name']
    return True


def process_friends_or_followers(eachUser, friend_or_follower):
    try:
        friends = get_friends(eachUser['username'], -1, friend_or_follower)
    except:
        return
    next_cursor = -1
    try:
        while(next_cursor !='0'):
            next_cursor = friends['next_cursor']
            for eachFriend in friends['users']:
                '''Register this user'''
                register_user_to_mongo(eachFriend, eachUser['username'])
            if next_cursor != 0:
                friends = get_friends(eachUser['username'], next_cursor, friend_or_follower)
    except:
        twitter_err_obj = TwitterError()
        twitter_err_obj.save_error({'username':eachUser['username'],'error_type':'cron',
            'next_cursor':next_cursor, 'error_solve_stat':'false','user_type':friend_or_follower})


def create_users(arg):
    user_profile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, 
    username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
    if arg=='all':
        users = user_profile_obj.get_all_users()
    elif arg=='Antartica':
        users = user_profile_obj.get_all_antartic_users()
        for eachUser in users:
            friend_obj = Friends()
            fr = friend_obj.get_friend(eachUser['username'])
            data = {}
            try:
                fr_address = fr['friends']['location']
                print eachUser['screen_name'], fr_address
            except:
                continue
            if fr_address !='':
                try:
                    location_res = Geocoder.geocode(fr_address)
                except:
                    continue
                data['address'] = str(location_res)
                data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude),float(location_res.latitude)]}
                data['zip_code'] = str(location_res.postal_code)           
                user_profile_obj.change_address(eachUser['username'], data)
        return {'status':1}
    else:    
        '''get all newly registered users and process their friends and followers'''
        start_time = datetime.datetime.now() - datetime.timedelta(1)
        start_time = time.mktime(start_time.timetuple())
        start_time = int(start_time)

        user_profile_obj = UserProfile()
        users = user_profile_obj.get_all_profiles_by_time(start_time)

    for eachUser in users:        
        process_friends_or_followers(eachUser, 'friends')
        process_friends_or_followers(eachUser, 'followers')
        
# def solve_errors():
#     te = TwitterError()
#     twitter_errors = te.get_unsolved_error('cron')

#     '''Solve all previous errors'''
#     for eachError in twitter_errors:    
#         '''Make Profile for all the friends who have location'''
#         next_cursor = eachError['next_cursor']
#         if eachError['user_type'] =='friends':
#             users = get_friends(eachError['username'], int(eachError['next_cursor']), 'friends')
#         else:
#             users = get_friends(eachError['username'], int(eachError['next_cursor']), 'followers')
#         try:
#             while(next_cursor !='0'):
#                 next_cursor = users['next_cursor']
#                 for eachFriend in users['users']:
#                     '''Register this user'''
#                     register_user_to_mongo(eachFriend)
#                 if next_cursor != 0:
#                     if eachError['user_type'] =='friends':    
#                         users = get_friends(eachError['username'], next_cursor, 'friends')
#                     else:
#                         users = get_friends(eachError['username'], next_cursor, 'followers')
            
#             '''Normal Flow Update Error Status to Solved'''        
#             twitter_err_obj = TwitterError()
#             twitter_err_obj.save_error({'username':eachError['username'],'error_solve_stat':'false', 'error_type':'cron'}, 
#                 {'error_solve_stat':'true'})
#         except:
#             '''If error occurs save in errors'''
#             twitter_err_obj = TwitterError()
#             if eachError['user_type'] =='friends':
#                 twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
#                     'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'friends'})
#             else:
#                 twitter_err_obj.save_error({'username':eachError['username'],'error_type':'cron',
#                     'next_cursor_str':next_cursor, 'error_solve_stat':'false','user_type':'followers'})

create_users('new')
#create_users('Antartica')
#create_users('all')


