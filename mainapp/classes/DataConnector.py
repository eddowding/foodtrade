# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json

from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
from mainapp.TweetFeed import TradeConnection, Food, Organisation
class UserConnections():

    """docstring for UserConnections"""
    def __init__(self, user_id):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'user_connections'
        self.db_object.create_table(self.table_name,'_id')
        self.user_id = user_id
        
    def insert_connection(self):
        pass

    def get_trade_connection_no(self):
        trade_conn = TradeConnection()
        b_conn = trade_conn.get_connection_by_business(self.user_id)
        c_conn = trade_conn.get_connection_by_customer(self.user_id)
        total_conn = len(b_conn) + len(c_conn)
        return total_conn
        # return self.db_object.get_all_count(self.table_name,{"$or":[{'buyer':self.twitter_user_id},{'seller':self.twitter_user_id}]}, 'time_stamp')
    def get_food_connection_no(self):
        foo = Food()
        foods = foo.get_foods_by_userid(self.user_id)
        return len(foods)

    def get_organisation_connection_no(self):
        org = Organisation()
        organisations = org.get_organisations_by_mem_id(self.user_id)
        return len(organisations)

    def get_nearby_individuals_no(self):
        return 78

    def get_nearby_businesses_no(self):
        return 79



        


class UserInfo():
    def __init__ (self,user_id):
        self.user_id = user_id
        twitter_user = SocialAccount.objects.get(user__id = user_id)
        user_connection =  UserConnections(user_id)

        self.full_name = twitter_user.extra_data['name']
        self.username = twitter_user.extra_data['screen_name']
        self.profileimg = twitter_user.extra_data['profile_image_url_https']
        # print 'hello'+twitter_user.extra_data['profile_image_url_https']
        self.trade_connections_no = user_connection.get_trade_connection_no()
        self.food_no = user_connection.get_food_connection_no()
        self.nearby_businesses_no = user_connection.get_nearby_businesses_no()
        self.nearby_individuals_no = user_connection.get_nearby_individuals_no()
        self.organisation_connection_no = user_connection.get_organisation_connection_no()


