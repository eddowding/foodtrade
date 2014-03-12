from MongoConnection import MongoConnection
from bson.objectid import ObjectId
from bson.code import Code
from bson import BSON
from bson import json_util
from django.contrib.auth.models import User
import json
import pprint


class KPIStats():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'_id')

    def user_count(self):
        self.table_name = 'userprofile'
        individual_count = self.db_object.get_count(self.table_name, {'sign_up_as': 'Individual'})
        business_count = self.db_object.get_count(self.table_name, {'sign_up_as': 'Business'})
        organisation_count = self.db_object.get_count(self.table_name, {'sign_up_as': 'Organisation'})
        return {'individual_count': individual_count,'business_count': business_count,'organisation_count': organisation_count}

    def activity_count(self):
        self.table_name = 'userprofile'
        agg_pipeline = []
        agg_pipeline.append({"$unwind": "$updates"})
        agg_pipeline.append({ '$match':{"updates.deleted": 0,"updates.parent_tweet_id":"0"}})
        mongo = MongoConnection("localhost",27017,'foodtrade')
        results = mongo.aggregrate_all(self.table_name, agg_pipeline)
        return len(results)

    def replies_count(self):
        self.table_name = 'userprofile'
        agg_pipeline = []
        agg_pipeline.append({"$unwind": "$updates"})
        agg_pipeline.append({ '$match':{"updates.deleted": 0,"updates.parent_tweet_id":{"$ne":"0"}}})
        mongo = MongoConnection("localhost",27017,'foodtrade')
        results_replies = mongo.aggregrate_all(self.table_name, agg_pipeline)
        return len(results_replies)

    def avg_conn_per_business(self):
        total_connections = self.total_connections()
        user_count = self.user_count()
        return round(float(total_connections)/float(user_count['business_count']), 2)

    def total_connections(self):
        self.table_name = 'tradeconnection'
        return self.db_object.get_count(self.table_name, {'deleted': 0})
