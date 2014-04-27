#!/usr/bin/env python
# encoding: utf-8
from MongoConnection import MongoConnection

from bson.objectid import ObjectId
# import time
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util
from pymongo import Connection
from django.conf import settings
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''
import json, time, datetime


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

    def get_twitter_followers_and_number(self,user_id, find_username, find_userid):
        st = SocialToken.objects.get(account__user__id=user_id)
        ACCESS_TOKEN = st.token
        ACCESS_TOKEN_SECRET = st.token_secret        
        user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        result = user_twitter.show_user(user_id=find_userid, screen_name=find_username)

        self.db_object.update_upsert(self.table_name, )

       