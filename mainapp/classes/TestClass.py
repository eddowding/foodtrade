from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util

from twython import Twython
import json
from pymongo import Connection
import re



import json
class TweetFeed():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tweets_test'
        # self.db_object.create_table(self.table_name,'parent_tweet_id')
        # self.db_object.ensure_index(self.table_name,'location')


    def insert_tweet(self, value):
        value['deleted'] = 0
        value['time_stamp'] = int(time.time())
        self.db_object.insert_one(self.table_name,value)

    def get_tweet_by_id(self,tweet_id):
        return self.db_object.get_one(self.table_name,{'tweet_id':tweet_id, 'deleted':0})

    def find(self,query):
        return self.db_object.get_one(self.table_name,query)


tf = TweetFeed()

updates = ["this is test", "Good morning Nepal", "this is a status"]

insert_val = {"name":"sujit"}
insert_val["updates"] = updates
tf.insert_tweet(insert_val)

keyword = "nepal"
keyword_like = re.compile(keyword + '+', re.IGNORECASE)
query_string = {'updates':{"$elemMatch":{"$regex": keyword_like, '$options': '-i'}}}

print tf.find(query_string)
