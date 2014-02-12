# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from django.contrib.auth.models import User

from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time, datetime
from mainapp.classes.TweetFeed import TweetFeed, Food, TradeConnection, Customer, TradeConnection, UserProfile, Organisation, Team, Notification
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

    def get_nearby_individuals_no(self, lon, lat):
        query_string = {}
        
        query_string['latlng'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(lon), float(lat)]}, "$maxDistance":160934}}

        query_string['sign_up_as'] ='Individual'
       
        tweet_search_object = TweetFeed()
        count = tweet_search_object.get_near_people(query_string)

        return count

    def get_nearby_businesses_no(self, lon, lat):
        query_string = {}
        
        query_string['latlng'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(lon), float(lat)]}, "$maxDistance":160934}}

        query_string['sign_up_as'] ='Business'
       
        tweet_search_object = TweetFeed()
        count = tweet_search_object.get_near_people(query_string)

        return count

    def get_award_no(self):
        

        return 0

class UserInfo():
    def __init__ (self,user_id):
        self.user_id = user_id
        usr = User.objects.get(id=user_id)
        self.is_superuser = usr.is_superuser
        user_profile = UserProfile()
        userprof = user_profile.get_profile_by_id(user_id)
        self.email = userprof['email']
        self.twitter_user = userprof['screen_name']
        self.lon = userprof['latlng']['coordinates'][0]
        self.lat = userprof['latlng']['coordinates'][1]
        self.user_type = userprof['sign_up_as']
        self.zip_code = userprof['zip_code']
        self.address = userprof['address']
        self.type = userprof['type_user']

        user_connection =  UserConnections(user_id)

        self.full_name = userprof['name']
        self.username = userprof['screen_name']
        self.description = userprof['description']
        self.profileimg = userprof['profile_img']
        
        self.trade_connections_no = user_connection.get_trade_connection_no()
        self.food_no = user_connection.get_food_connection_no()
        self.nearby_businesses_no = user_connection.get_nearby_businesses_no(self.lon,self.lat)
        self.nearby_individuals_no = user_connection.get_nearby_individuals_no(self.lon,self.lat)
        self.organisation_connection_no = user_connection.get_organisation_connection_no()
        self.award_no = user_connection.get_award_no()

        start_time = datetime.date.today() - datetime.timedelta(7)
        end_time = datetime.date.today()
        t_feed_obj = TweetFeed()

        hashtags_this_week = t_feed_obj.get_trending_hashtags(start_time, end_time)
        self.hashtagsthis = hashtags_this_week

        hashtags_all_time = t_feed_obj.get_trending_hashtags("", "")
        self.hashtagsall = hashtags_all_time

        notification_obj = Notification()
        self.notification_count = notification_obj.get_notification_count(self.username)
