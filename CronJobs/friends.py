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

class Friends():
    def __init__ (self):
        self.db_object = MongoConnection(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, 
        conn_type='remote', username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
        self.table_name = 'friends'
        self.db_object.create_table(self.table_name,'username')

    def register_all_friends(self):
        user_pages_count = int(self.db_object.get_count(self.table_name, {'friends.added_as_user':{'$exists':False}})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'friends.added_as_user':{'$exists':False}}, pageNumber = int(i+1))
            for eachUser in pag_users:
                user_profile_obj = UserProfile(host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, 
    conn_type='remote', username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD)
                check = user_profile_obj.get_profile_by_username(eachUser['friends']['screen_name'])                                
                if check == None:
                    register_user_to_mongo(eachUser['friends'])
                    self.update_friend(eachUser['friends']['screen_name'], eachUser['username'])
                else:                    
                    self.update_friend(eachUser['friends']['screen_name'], eachUser['username'])

    def update_friend(self, friend_name, username):
        self.db_object.update(self.table_name,{'username':username,'friends.screen_name':friend_name}, 
            {'friends.added_as_user':'true'})

    def save_friend(self,doc):
        return self.db_object.update_upsert(self.table_name,{'username':doc['username'],'friends.screen_name':doc['friends']['screen_name']},doc)
