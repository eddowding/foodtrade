from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time

class TweetFeed():
    def __init__ (self):
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


userprofile = UserProfile()
print userprofile.get_profile_by_id(21)