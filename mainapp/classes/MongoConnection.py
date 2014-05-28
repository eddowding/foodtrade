#!/usr/bin/env python
# encoding: utf-8
# Create your views here.
from pymongo import MongoClient
import pymongo
from pymongo import Connection
import json
from bson import BSON
from bson import json_util


class MongoConnection():
    def __init__ (self, host="localhost",port=27017, db_name='indexer', conn_type="local", username='ftroot', password='ftroot'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.conn_type = conn_type
        self.username = username
        self.password = password
        self.conn = None
        self.db = None

    def create_connection(self):
        self.conn = Connection(self.host, self.port)
        self.db = self.conn[self.db_name]
        self.db.authenticate(self.username, self.password)

    def close_connection(self):
        self.conn.close()


    def ensure_index(self, table_name, index=None):
        self.create_connection()
        db[table_name].ensure_index([(index,pymongo.GEOSPHERE)])
        db.close()
    
    def create_table(self, table_name, index=None):
        self.create_connection()
        self.db[table_name].create_index( [(index, pymongo.DESCENDING)] )
        self.close_connection()


    def get_one(self,table_name,conditions={}):
        self.create_connection()
        single_doc = self.db[table_name].find_one(conditions)
        json_doc = json.dumps(single_doc,default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")        
        self.close_connection()
        return json.loads(json_doc)

    def get_all(self,table_name,conditions={}, sort_index ='_id', limit=100):
        self.create_connection()
        all_doc = self.db[table_name].find(conditions).sort(sort_index, pymongo.DESCENDING).limit(limit)
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(str(json_doc))


    def insert_one(self, table_name, value):
        self.create_connection()
        self.db[table_name].insert(value)
        self.close_connection()

    def update_push(self, table_name, where, what):
        #print where, what
        self.create_connection()
        self.db[table_name].update(where,{"$push":what},upsert=False)
        self.close_connection()

    def update(self, table_name, where, what):
        #print where, what
        self.create_connection()
        self.db[table_name].update(where,{"$set":what},upsert=False)
        self.close_connection()

    def update_multi(self, table_name, where, what):
        self.create_connection()
        self.db[table_name].update(where,{"$set":what},upsert=False, multi=True)
        self.close_connection()

    def update_upsert(self, table_name, where, what):
        self.create_connection()
        self.db[table_name].update(where,{"$set":what},upsert=True)        
        self.close_connection()

    def map_reduce(self, table_name, mapper, reducer, query, result_table_name):
        self.create_connection()
        myresult = self.db[table_name].map_reduce(mapper, reducer, result_table_name, query)
        self.close_connection()
        return myresult

    def map_reduce_search(self, table_name, mapper, reducer,query, sort_by, sort = -1, limit = 20):
        if sort_by == "distance":
            sort_direction = pymongo.ASCENDING
        else:
            sort_direction = pymongo.DESCENDING
        self.create_connection()
        myresult = self.db[table_name].map_reduce(mapper,reducer,'results', query)
        results = self.db['results'].find().sort("value."+sort_by, sort_direction).limit(limit)
        json_doc = json.dumps(list(results),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(str(json_doc))

    def aggregrate_all(self,table_name,conditions={}):
        self.create_connection()
        all_doc = self.db[table_name].aggregate(conditions)['result']
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(str(json_doc))
        
    def group(self,table_name,key, condition, initial, reducer):
        self.create_connection()
        all_doc = self.db[table_name].group(key=key, condition=condition, initial=initial, reduce=reducer)
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(str(json_doc))

    def get_distinct(self,table_name, distinct_val, query):
        self.create_connection()
        all_doc = self.db[table_name].find(query).distinct(distinct_val)
        count = len(all_doc)        
        parameter = {}
        parameter['count'] = count
        parameter['results'] = all_doc
        self.close_connection()
        return parameter
        
    def get_all_vals(self,table_name,conditions={}, sort_index ='_id'):
        self.create_connection()
        all_doc = self.db[table_name].find(conditions).sort(sort_index, pymongo.DESCENDING)
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(json_doc)

    def get_paginated_values(self, table_name, conditions ={}, sort_index ='_id', pageNumber = 1):
        self.create_connection()
        all_doc = self.db[table_name].find(conditions).sort(sort_index, pymongo.DESCENDING).skip((pageNumber-1)*15).limit(15)
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        self.close_connection()
        return json.loads(json_doc)        

    def get_count(self, table_name,conditions={}, sort_index='_id'):
        self.create_connection()
        count = self.db[table_name].find(conditions).count()
        self.close_connection()
        return count
