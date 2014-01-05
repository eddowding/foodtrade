from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
import pymongo
class Tags():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tags'
    
    def get_tags(self):
        try:
            return self.db_object.get_one(self.table_name,{})['tags']
        except:
            return []

    def set_tags(self,tags):
        try:
            val = self.db_object.get_one(self.table_name,{})['tags']
            return self.db_object.update(self.table_name,{'parent':1}, {'tags':tags['tags']})
        except:
            return self.db_object.insert_one(self.table_name,tags)
        




