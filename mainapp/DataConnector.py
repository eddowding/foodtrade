# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from classes.TweetFeed import TweetFeed
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId

from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time

class UserConnections():

    """docstring for UserConnections"""
    def __init__(self, twitter_user_id):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'user_connections'
        self.db_object.create_table(self.table_name,'_id')
        self.twitter_user_id = twitter_user_id
        
    def insert_connection():
        pass

    def get_trade_connection_no():
        return 45
        # return self.db_object.get_all_count(self.table_name,{"$or":[{'buyer':self.twitter_user_id},{'seller':self.twitter_user_id}]}, 'time_stamp')
    def get_food_connection_no():
        return 65

    def get_organisation_connection_no():
        return 435
    def get_nearby_individuals_no():
        return 78

    def get_nearby_businesses_no():
        return 79



        


class UserInfo():
    def __init__ (self,user_id):
        self.user_id = user.id
        twitter_user = SocialAccount.objects.get(user__id = user_id)
        twitter_user_id = twitter_user.extra_data.uid
        user_connection =  UserConnections(twitter_user_id)

        self.full_name = twitter_user.extra_data.name
        self.username = twitter_user.extra_data.screen_name
        self.tweeter_user_id = twitter_user_id
        self.trade_connections_no = user_connection.get_trade_connection_no()
        self.food_no = user_connection.get_food_connection_no()
        self.nearby_businesses_no = user_connection.get_nearby_businesses_no()
        self.nearby_individuals_no = user_connection.get_nearby_individuals_no()
        self.organisation_connection_no = user_connection.get_organisation_connection_no()


