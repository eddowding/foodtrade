#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
import os
import sys
import time, datetime
import MySQLdb

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

# CLASS_PATH = 'C:/Users/Roshan Bhandari/Desktop/project repos/foodtrade/mainapp/classes'
# SETTINGS_PATH = 'C:/Users/Roshan Bhandari/Desktop/project repos/foodtrade/foodtrade'


sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)

from MongoConnection import MongoConnection
from TwitterError import TwitterError
from MySQLConnect import MySQLConnect
from settingslocal import *
from twython import Twython
from pygeocoder import Geocoder

class Friends():
    def __init__ (self):
        self.db_object = MongoConnection(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
        self.table_name = 'friends'
        self.db_object.create_table(self.table_name,'username')

    def get_twitter_obj(self, token, secret):
        return Twython(app_key = CONSUMER_KEY,app_secret = CONSUMER_SECRET,oauth_token = token,oauth_token_secret = secret)

    def get_friends(self, screen_name, next_cursor, friend_or_follower):
        mc = MySQLConnect()
        st = mc.get_token(screen_name)
        ACCESS_TOKEN = st[0]
        ACCESS_TOKEN_SECRET = st[1]
        user_twitter = self.get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        if friend_or_follower == 'friends':
            friends = user_twitter.get_friends_list(screen_name = screen_name, count=200, cursor = next_cursor)
            return friends
        else:
            followers = user_twitter.get_followers_list(screen_name = screen_name, count=200, cursor = next_cursor)
            return followers
    
    def process_friends_or_followers(self, eachUser, friend_or_follower):
        try:
            friends = self.get_friends(eachUser['username'], -1, friend_or_follower)
        except:
            return
        next_cursor = -1
        try:
            while(next_cursor !='0'):
                next_cursor = friends['next_cursor']
                for eachFriend in friends['users']:
                    '''Register this user'''
                    # self.register_friend(eachFriend, eachUser['username'])
                    self.register_as_unclaimed_user(eachFriend)                    
                    time.sleep(1)
                if next_cursor != 0:                    
                    friends = self.get_friends(eachUser['username'], next_cursor, friend_or_follower)
            return {'status':1}
        except:
            print 'landed in exception'
            return {'status':0, 'msg':'landed in exception'}

    def register_as_unclaimed_user(self,twitter_user):
        data = {
            'is_unknown_profile':'true',
            'recently_updated_by_super_user': 'false', 
            'sign_up_as': 'unclaimed',
            'type_user': [], 
            'name': twitter_user['name'],
            'email': '', 
            'description': twitter_user['description'],
            'username' : twitter_user['screen_name'],
            'screen_name': twitter_user['screen_name'],            
            'updates': [],
            'foods':[],
            'organisations':[],
            'subscribed':0,
            'newsletter_freq':'Never',            
            'followers_count':twitter_user['followers_count'],
            'friends_count':twitter_user['friends_count'],
        }
        try:
            data['profile_img'] = twitter_user['profile_image_url']
        except:
            data['profile_img'] = twitter_user['profile_img']
        try:
            data['profile_banner_url'] = twitter_user['profile_banner_url']
        except:
            data['profile_banner_url'] = ''

        from UserProfile import UserProfile
        userprofile = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
        check = userprofile.get_profile_by_username(twitter_user['screen_name'])

        if check == None:
            try:
                location_res = Geocoder.geocode(twitter_user['location'])
                data['twitter_address'] = twitter_user['location']
                data['address'] = str(location_res)
                data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude),float(location_res.latitude)]}
                data['zip_code'] = str(location_res.postal_code)
                data['address_geocoded']=True
            except:
                data['address'] = str('Antartica')
                data['twitter_address'] = twitter_user['location']
                data['latlng'] = {"type":"Point","coordinates":[float(-135.10000000000002) ,float(-82.86275189999999)]}
                data['zip_code'] = str('')
                data['address_geocoded']=False
                data['location_default_on_error'] = 'true'

            join_time = datetime.datetime.now()
            join_time = time.mktime(join_time.timetuple())
            data['join_time'] = int(join_time)            
            min_user_id = int(userprofile.get_minimum_id_of_user()[0]['minId']) -1
            data['useruid'] = min_user_id

            userprofile.update_profile_upsert({'screen_name':twitter_user['screen_name'],
                'username':twitter_user['screen_name']},data)
            # print twitter_user['screen_name'] + ' updated'
            return True
        else:
            new_data = {
            'followers_count':twitter_user['followers_count'],
            'friends_count':twitter_user['friends_count']}
            try:
                new_data['profile_img'] = twitter_user['profile_image_url']
            except:
                new_data['profile_img'] = twitter_user['profile_img']
            try:
                new_data['profile_banner_url'] = twitter_user['profile_banner_url']
            except:
                new_data['profile_banner_url'] = ''
            userprofile.update_profile_upsert({'screen_name':twitter_user['screen_name'],
                'username':twitter_user['screen_name']},new_data)
            # print twitter_user['screen_name'] + ' already exists'
            return False

    def register_friend(self, eachFriend, username=''):
        '''Register User to Friends Collection'''
        self.save_friend({'username':username, 'friends':eachFriend})
        return {'status':1}

    def register_friend_to_user(self, eachFriend, username=''):
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
            'updates': [],
            'foods':[],
            'organisations':[],
            'subscribed':0,
            'newsletter_freq':'Never'
        }
        try:
            data['profile_img'] = eachFriend['profile_image_url']
        except:
            data['profile_img'] = eachFriend['profile_img']
        from UserProfile import UserProfile
        userprofile = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
        check = userprofile.get_profile_by_username(eachFriend['screen_name'])

        if check ==None:
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
            
            min_user_id = int(userprofile.get_minimum_id_of_user()[0]['minId']) -1
            data['useruid'] = min_user_id

            userprofile.update_profile_upsert({'screen_name':eachFriend['screen_name'],'username':eachFriend['screen_name']},data)
            # print eachFriend['screen_name'] + " added"
            return True
        else:
            return False

    def register_all_friends(self):
        user_pages_count = int(self.db_object.get_count(self.table_name, {'friends.added_as_user':{'$exists':False}})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'friends.added_as_user':{'$exists':False}}, pageNumber = int(i+1))
            from UserProfile import UserProfile
            for eachUser in pag_users:
                user_profile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
                check = user_profile_obj.get_profile_by_username(eachUser['friends']['screen_name'])                                
                if check == None:                    
                    self.register_friend_to_user(eachUser['friends'])
                    self.update_friend(eachUser['friends']['screen_name'], eachUser['username'])
                else:                    
                    self.update_friend(eachUser['friends']['screen_name'], eachUser['username'])
            time.sleep(5)

    def update_friend(self, friend_name, username):
        # print friend_name + " updated"
        return self.db_object.update(self.table_name,{'username':username,'friends.screen_name':friend_name},{'friends.added_as_user':'true'})

    def get_friend(self, friend_name):
        return self.db_object.get_one(self.table_name,{'friends.screen_name':friend_name})

    def save_friend(self,doc):
        retval = self.db_object.update_upsert(self.table_name,{'username':doc['username'],'friends.screen_name':doc['friends']['screen_name']},doc)
        #print str(doc['username']) + "," + doc['friends']['screen_name']+ " saved"
        return retval