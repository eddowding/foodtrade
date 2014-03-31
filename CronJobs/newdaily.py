#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from UserProfile import UserProfile
import settingslocal   

def send_newsletter(substype):
    substype = substype.capitalize()
    user_profile_obj = UserProfile(host='localhost', port=27017,db_name='foodtrade', username=settingslocal.REMOTE_MONGO_USERNAME, password=settingslocal.REMOTE_MONGO_PASSWORD)

    if substype == 'Daily':
        user_profile_obj.send_newsletter('Daily')
        #pass

    elif substype == 'Weekly' or substype == 'None':
        pass
        #users = user_profile_obj.get_all_profiles(substype)
    elif substype == 'Monthly':
        pass
        #users = user_profile_obj.get_all_profiles('Monthly')
    # count = 0
    # for eachUser in users:
    #     if len(eachUser['email'])>0:
    #         import urllib2
    #         baseurl = "http://foodtrade.com/send-newsletter/" + str(substype.lower())+ "?username=" + str(eachUser['username']) + "&code=11foodtradeESRS22"
    #         response = urllib2.urlopen(baseurl)


def trending_hash_tags():
    start_time = datetime.date.today() - datetime.timedelta(7)
    end_time = datetime.date.today()
    user_profile_obj = UserProfile(host='localhost', port=27017,db_name='foodtrade', username=settingslocal.REMOTE_MONGO_USERNAME, password=settingslocal.REMOTE_MONGO_PASSWORD)
    # user_profile_obj = UserProfile(host=settingslocal.LOCAL_SERVER, port=27017,db_name='foodtrade', username=settingslocal.REMOTE_MONGO_USERNAME, password=settingslocal.REMOTE_MONGO_USERNAME)
    user_profile_obj.calculate_trending_hashtags(start_time, end_time)
    user_profile_obj.calculate_trending_hashtags("", "")
    return {'status':1}