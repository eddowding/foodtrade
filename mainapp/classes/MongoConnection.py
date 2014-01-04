from pymongo import MongoClient
import pymongo
from pymongo import Connection
import json
from bson import BSON
from bson import json_util

class MongoConnection():
    def __init__ (self, host="localhost",port=27017, db_name='indexer'):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[db_name]

    def ensure_index(self, table_name, index=None):
        self.db[table_name].ensure_index([(index,pymongo.GEOSPHERE)])
    
    def create_table(self, table_name, index=None):
        self.db[table_name].create_index( [(index, pymongo.DESCENDING), ('unique',True)] )


    def get_one(self,table_name,conditions={}):
        single_doc = self.db[table_name].find_one(conditions)
        json_doc = json.dumps(single_doc,default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(json_doc)

    def get_all(self,table_name,conditions={}, sort_index ='_id'):
        all_doc = self.db[table_name].find(conditions).sort(sort_index, pymongo.DESCENDING).limit(8)
        json_doc = json.dumps(list(all_doc),default=json_util.default)
        json_doc = json_doc.replace("$oid", "id")
        json_doc = json_doc.replace("_id", "uid")
        return json.loads(str(json_doc))


    def insert_one(self, table_name, value):
        self.db[table_name].insert(value)

    def update(self, table_name, where, what):
        self.db[table_name].update(where,{"$set":what},upsert=False)

    def update_upsert(self, table_name, where, what):
        self.db[table_name].update(where,{"$set":what},upsert=True)


# mydb = MongoConnection()
# # mydb.select_db('indexer')
# print mydb.get_all('urlfilter',{'word':'intramurals'})

    