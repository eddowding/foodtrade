

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from TweetFeed import TweetFeed
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
        return self.db_object.get_all_count(self.table_name,{"$or":[{'buyer':self.twitter_user_id},{'seller':self.twitter_user_id}]}, 'time_stamp')



        


class UserInfo():
    def __init__ (self,user_id):
        self.user_id = user.id
        twitter_user = SocialAccount.objects.get(user__id = user_id)
        self.full_name = twitter_user.extra_data.name
        self.username = twitter_user.extra_data.screen_name

        self.tweeter_user_id = twitter_user.extra_data.uid

        user_connection =  UserConnections(user_info['tweeter_user_id'])
        user.trade_connections = get_trade_connections(user_info['tweeter_user_id'])


    user_info 
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tweets'
        self.db_object.create_table(self.table_name,'parent_tweet_id')

    # def select_db(self, db_name):
    #   self.db = self.client[db_name]
    
    def get_tweet_by_id(self,tweet_id):
        return self.db_object.get_one(self.table_name,{'tweet_id':tweet_id, 'deleted':0})

    def get_tweet_by_parent_id(self, parent_tweet_id):
        return self.db_object.get_all(self.table_name,{'parent_tweet_id':parent_tweet_id, 'deleted':0}, 'time_stamp')

    def delete_tweet(self, tweet_id):
        self.db_object.update(self.table_name,{'_id':ObjectId(tweet_id)}, {'deleted':1})

    def get_tweet_by_user_id(self, user_id):
        return self.db_object.get_all(self.table_name,{'user_id':tweet_id, 'deleted':0}, 'time_stamp')


    def insert_tweet(self, value):
        value['deleted'] =0
        value['time_stamp'] = int(time.time())
        self.db_object.insert_one(self.table_name,value)



# tweet = TweetFeed()
# # print tweet.delete_tweet('52ad41d3df1d2d0f0e7e7da5')
# # tweet.insert_tweet({'parent_tweet_id':0, 'tweet_message':"nepal", 'time_stamp':datetime.now(), 'deleted':0})
# print tweet.get_tweet_by_parent_id(0)
# tweet_feed = TweetFeed()
# tweet_feed.insert_tweet({'parent_tweet_id': 2, 'user_id': 3, 'tweet_message': 'Hello there'})
# print tweet_feed.get_tweet_by_parent_id(2)




def get_user_data(request):

    user_info = {}
    if request.user.is_authenticated():

        return HttpResponseRedirect('/accounts/login/')
    user_id = request.user.id
    twitter_user = SocialAccount.objects.get(user__id = user_id)
    user_info['name_full'] = twitter_user.extra_data.name
    user_info['username'] = twitter_user.extra_data.screen_name
    user_info['tweeter_user_id'] = twitter_user.extra_data.uid
    user_connection =  UserConnections(user_info['tweeter_user_id'])
    user_info['trade_connections'] = get_trade_connections(user_info['tweeter_user_id'])
    user_info 


    user_id = request.user.id
    print user_id
    st = SocialToken.objects.get(account__user__id=user_id)
    access_token = st.token
    access_token_secret = st.token_secret