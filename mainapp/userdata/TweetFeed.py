from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util


class TweetFeed():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tweets'
        self.db_object.create_table(self.table_name,'parent_tweet_id')
        self.db_object.ensure_index(self.table_name,'location')
   	
    def get_tweet_by_id(self,tweet_id):
        return self.db_object.get_one(self.table_name,{'tweet_id':tweet_id, 'deleted':0})

    def get_tweet_by_parent_id(self, parent_tweet_id):
    	return self.db_object.get_all(self.table_name,{'parent_tweet_id':parent_tweet_id, 'deleted':0}, 'time_stamp')

    def delete_tweet(self, tweet_id):
    	self.db_object.update(self.table_name,{'_id':ObjectId(tweet_id)}, {'deleted':1})

    def get_tweet_by_user_id(self, user_id):
        return self.db_object.get_all(self.table_name,{'user_id':tweet_id, 'deleted':0}, 'time_stamp')

    def search_tweets(self, query):
        return self.db_object.get_all(self.table_name, query, 'time_stamp')

    def insert_tweet(self, value):
        self.db_object.insert_one(self.table_name,value)

    def get_tweet_by_user_ids(self, user_ids):
        return self.db_object.get_all(self.table_name,{"user_id": {"$in": user_ids},'deleted':0}, 'time_stamp')    

    def get_trending_hashtags(self, start_time_stamp, end_time_stamp):
        mapper = Code("""
            function () {
             items = this.status.split(' ');
             for(i=0;i<items.length;i++){ 
                if(items[i].indexOf('#')!=-1){
                        emit(items[i], 1); 
                        }
                    }
            }
            """)
        reducer = Code("""
            function (key, values) { 
             var sum = 0;
             for (var i =0; i<values.length; i++){
                    sum = sum + parseInt(values[i]);
             }
             return sum;
            }
            """)
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query = { 'time_stamp':{'$gte': start_time_stamp,'$lte': end_time_stamp}})
        

    def update_tweets(self, username, first_name, last_name, description, zip_code):
        try:
            results = Geocoder.geocode(zip_code)
            lon = results[0].longitude
            lat = results[0].latitude
        except:
            results = Geocoder.geocode('sp5 1nr')
            lon = results[0].longitude
            lat = results[0].latitude

        return self.db_object.update(self.table_name,
            {'user.username':username}, 
            {
                'user.name':str(first_name + ' ' + last_name),
                'user.Description':description, 
                'location.coordinates':[lat, lon]
            })

class UserProfile():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')
  
    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': user_id})

    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'type':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)

    def update_profile(self, userid, zipcode, type_usr, sign_up_as):
        return self.db_object.update(self.table_name,
            {'useruid':str(userid)}, {
                'zip_code':zipcode,
                'type_user':type_usr,
                'sign_up_as':sign_up_as
            })

class TradeConnection():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tradeconnection'
        self.db_object.create_table(self.table_name,'b_useruid')
    def get_connection_by_business(self,b_useruid):
        return self.db_object.get_all(self.table_name,{'b_useruid': b_useruid, 'deleted': 0})

    def get_connection_by_customer(self, c_useruid):
        return self.db_object.get_all(self.table_name,{'c_useruid':c_useruid, 'deleted': 0})

    def create_connection (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_connection(self, b_useruid, c_useruid):
        self.db_object.update(self.table_name,{'b_useruid': b_useruid, 'c_useruid': c_useruid}, {'deleted':1})

class Food():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'food'
        self.db_object.create_table(self.table_name,'useruid')
    def get_foods_by_userid(self,useruid):
        return self.db_object.get_all(self.table_name,{'useruid': useruid, 'deleted': 0})

    def create_food (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_food(self, useruid, food_name):
        self.db_object.update(self.table_name,{'useruid': useruid, 'food_name': food_name}, {'deleted':1})

class Customer():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'customer'
        self.db_object.create_table(self.table_name,'useruid')

    def get_customers_by_userid(self,useruid):
        return self.db_object.get_all(self.table_name,{'useruid': useruid, 'deleted': 0})

    def create_customer (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_customer(self, useruid, customer_id):
        self.db_object.update(self.table_name,{'useruid': useruid, 'customeruid': customer_id}, {'deleted':1})

class Organisation():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'organisation'
        self.db_object.create_table(self.table_name,'orguid')

    def get_members_by_orgid(self,orguid):
        return self.db_object.get_all(self.table_name,{'orguid': orguid, 'deleted': 0})

    def create_member (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_member(self, orguid, member_id):
        self.db_object.update(self.table_name,{'orguid': orguid, 'memberuid': member_id}, {'deleted':1})

    def get_organisations_by_mem_id(self, member_id):
        return self.db_object.get_all(self.table_name,{'memberuid': member_id, 'deleted': 0})

# trade_conn = TradeConnection()
# trade_conn.create_connection({'b_useruid': 23, 'c_useruid': 20})
# print trade_conn.get_connection_by_customer(23)
