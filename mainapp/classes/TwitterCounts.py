#!/usr/bin/env python
# encoding: utf-8
from MongoConnection import MongoConnection
from bson.objectid import ObjectId
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util
from pymongo import Connection
from django.conf import settings
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
from twython import Twython
import json, time, datetime

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''


def get_twitter_obj(token, secret):
    return Twython(
        app_key = settings.CONSUMER_KEY,
        app_secret = settings.CONSUMER_SECRET,
        oauth_token = token,
        oauth_token_secret = secret
        )

class TwitterCounts():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'twittercounts'

    def get_twitter_followers_and_number(self,user_id, find_username):
        try:
            st = SocialToken.objects.get(account__user__id=user_id)    
            ACCESS_TOKEN = st.token
            ACCESS_TOKEN_SECRET = st.token_secret
            user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        except:
            pass

        from mainapp.classes.TweetFeed import Friends 
        friend_obj = Friends()
        friend = friend_obj.get_one({'friends.screen_name':find_username})

        try:
            result = user_twitter.show_user(screen_name=find_username)
            self.db_object.update_upsert(self.table_name,{'screen_name':find_username, 'data':result}, 
                {'screen_name':find_username,'data':result})
            return_values = {'followers_count':result['followers_count'], 'friends_count':result['friends_count'], 'banner_url':result['profile_banner_url'] +'/web_retina'}
            return return_values
        except:
            result = self.db_object.get_one(self.table_name,{'screen_name':find_username})    
            try:
                return_values = {'followers_count':result['data']['followers_count'], 'friends_count':result['data']['friends_count'], 'banner_url':result['data']['profile_banner_url'] + '/web_retina'}
            except:
                return_values = {'followers_count':result['data']['followers_count'], 'friends_count':result['data']['friends_count'], 'banner_url':'none'}
            return return_values




       