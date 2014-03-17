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


def register_user_to_mongo(eachFriend):
    user_profile_obj = UserProfile()
    min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1
    if eachFriend['location']=='':
        return

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
        location_res = Geocoder.geocode(eachFriend['location'])
        data['address'] = str(location_res)
        data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude) ,float(location_res.latitude)]}
        data['zip_code'] = str(location_res.postal_code)
    except:
        return

    join_time = datetime.datetime.now()
    join_time = time.mktime(join_time.timetuple())
    data['join_time'] = int(join_time)

    print data['screen_name']
    '''Register User to Mongo'''
    userprofile = UserProfile()
    userprofile.update_profile_upsert({'screen_name':eachFriend['screen_name'],
        'username':eachFriend['screen_name']},data)
    return True

class Friends():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'friends'
        self.db_object.create_table(self.table_name,'username')

    def register_all_friends(self):
        user_pages_count = int(self.db_object.get_count(self.table_name, {})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {}, pageNumber = int(i+1))
            for eachUser in pag_users:
                register_user_to_mongo(eachUser['friends'])

fr = Friends()        
fr.register_all_friends()