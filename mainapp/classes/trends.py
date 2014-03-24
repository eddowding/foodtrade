#!/usr/bin/env python
# encoding: utf-8
import re
import pymongo
from MongoConnection import MongoConnection
from bson.objectid import ObjectId
import time, datetime
import json

class TrendsThisWeek():
    def __init__ (self, host="localhost", port=27017, db_name='foodtrade', username='', password=''):
        self.db = MongoConnection(host=host, port=port, db_name=db_name,username=username, password=password)
        self.table_name = 'trendingthisweek'
        self.db.create_table(self.table_name, '_id')

    def get_trends_this_week(self):
        results = self.db.get_all(self.table_name, sort_index ='value', limit=8)        
        return results

class TrendsAllTime():
    def __init__ (self, host="localhost", port=27017, db_name='foodtrade', username='', password=''):
        self.db = MongoConnection(host=host, port=port, db_name=db_name,username=username, password=password)
        self.table_name = 'trendingalltime'
        self.db.create_table(self.table_name, '_id')

    def get_trends_all_time(self):
        results = self.db.get_all(self.table_name,sort_index ='value', limit=8)
        return results