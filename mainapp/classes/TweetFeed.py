from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
import pymongo
class TweetFeed():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tweets'
        # self.db_object.create_table(self.tab/le_name,'location')
        self.db_object.ensure_index(self.table_name,'location')
        # self.db_object.ensure_index(self.table_name,'location')

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

    def search_tweets(self, query):
        return self.db_object.get_all(self.table_name, query, 'time_stamp')

    def insert_tweet(self, value):
        value['deleted'] =0
    	value['time_stamp'] = int(time.time())
        self.db_object.insert_one(self.table_name,value)

    def get_tweet_by_user_ids(self, user_ids):
        return self.db_object.get_all(self.table_name,{"user_id": {"$in": user_ids},'deleted':0}, 'time_stamp')


    def aggregrate(self, conditions):
        return self.db_object.aggregrate_all(self.table_name,conditions)






# tweet = TweetFeed()
# # print tweet.delete_tweet('52ad41d3df1d2d0f0e7e7da5')
# # tweet.insert_tweet({'parent_tweet_id':0, 'tweet_message':"nepal", 'time_stamp':datetime.now(), 'deleted':0})
# print tweet.get_tweet_by_parent_id(0)
# tweet_feed = TweetFeed()
# tweet_feed.insert_tweet({'parent_tweet_id': 2, 'user_id': 3, 'tweet_message': 'Hello there'})
# print tweet_feed.get_tweet_by_parent_id(2)