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
from mainapp.classes.TweetFeed import TweetFeed, Food, TradeConnection, Customer, TradeConnection, UserProfile, Organisation, Team, Notification, RecommendFood
from djstripe.models import Customer
from mainapp.classes.trends import TrendsThisWeek, TrendsAllTime


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
        b_conn_no = trade_conn.get_connection_no_by_business(self.user_id)
        c_conn_no = trade_conn.get_connection_no_by_customer(self.user_id)
        total_conn = b_conn_no + c_conn_no
        return b_conn_no, c_conn_no
        # return self.db_object.get_all_count(self.table_name,{"$or":[{'buyer':self.twitter_user_id},{'seller':self.twitter_user_id}]}, 'time_stamp')

    def get_food_connection_no(self):
        foo = Food()
        food_count = foo.get_food_count_by_userid(self.user_id)
        return food_count

    def get_organisation_connection_no(self):
        org = Organisation()
        organisations_Count = org.get_organisations_count_by_mem_id(self.user_id)
        return organisations_Count

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
        try:
            usr = User.objects.get(id=user_id)
            self.is_superuser = usr.is_superuser
        except:
            self.is_superuser = False

        user_profile = UserProfile()
        userprof = user_profile.get_profile_by_id(user_id)
        self.email = userprof['email']
        self.twitter_user = userprof['screen_name']
        self.lon = userprof['latlng']['coordinates'][0]
        self.lat = userprof['latlng']['coordinates'][1]

        # print self.lon
        # print self.lat
        self.user_type = userprof['sign_up_as']
        self.zip_code = userprof.get('zip_code')
        self.address = userprof['address']
        self.type = userprof['type_user']
        
        
        self.post_count = user_profile.get_post_count(user_id)

        try:
            self.country = userprof['address'].split(',')[len(userprof['address'].split(','))-1]
        except:
            self.country = ''
        try:
            self.facebook_page = userprof['facebook_page']
        except:
            self.facebook_page = ''

        try:
            self.webiste_url = userprof['webiste_url']
        except:
            self.webiste_url = ''
        try:
            self.company_num = userprof['company_num']
        except:
            self.facebook_page = ''
        try:
            self.deliverables = userprof['deliverables']
        except:
            self.deliverables = ''
        try:
            self.business_org_name = userprof['business_org_name']
        except:
            self.business_org_name = ''      

        self.email_registration = 0
        try:
            self.email_registration  = userprof['email_registration']
        except:
            pass
        
        user_connection =  UserConnections(user_id)
        if userprof.get('business_org_name')!=None:
            self.full_name= userprof.get('business_org_name') if (userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation') \
            and userprof.get('business_org_name')!='' else userprof['name']
        else :
            self.full_name = userprof['name']    
        # parameters['name'] = userprof['name']
        # self.full_name = userprof.get('business_org_name') if (userprof['sign_up_as'] == 'Business' or userprof['sign_up_as'] == 'Organisation') \
        # and  userprof.get('business_org_name')!='' else userprof['name']

        self.username = userprof['username']
        self.description = userprof['description']        
        self.profileimg = userprof['profile_img']
        b_conn_len, c_conn_len = user_connection.get_trade_connection_no()
        self.trade_connections_no = b_conn_len + c_conn_len
        self.b_conn_no = b_conn_len
        self.c_conn_no = c_conn_len
        self.food_no = user_connection.get_food_connection_no()
        self.nearby_businesses_no = user_connection.get_nearby_businesses_no(self.lon,self.lat)
        self.nearby_individuals_no = user_connection.get_nearby_individuals_no(self.lon,self.lat)
        self.organisation_connection_no = user_connection.get_organisation_connection_no()
        self.award_no = user_connection.get_award_no()


        '''Trends'''
        trends_this_week = TrendsThisWeek(host='localhost', port=27017,db_name='foodtrade', username='ftroot', password='ftroot')
        trends_all_time = TrendsAllTime(host='localhost', port=27017,db_name='foodtrade', username='ftroot', password='ftroot')
        self.hashtagsthis = trends_this_week.get_trends_this_week()
        self.hashtagsall = trends_all_time.get_trends_all_time()

        notification_obj = Notification()
        self.notification_count = notification_obj.get_notification_count(self.username)
        
        self.subscribed = True
        try:
            usr = User.objects.get(id=user_id)
            customer, created = Customer.get_or_create(usr)
            if created:
                self.subscribed = False

            if not customer.has_active_subscription():
                self.subscribed = False
        except:
            self.subscribed = False        