from bson.son import SON
from bson.objectid import ObjectId
from MongoConnection import MongoConnection
import json
import operator
import datetime,time

class UserProfile():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')
        self.db_object.ensure_index(self.table_name,'latlng')

  
    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': user_id})


    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'sign_up_as':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)
    def update(self, where, what):
        return self.db_object.update(self.table_name, where, what)

    def agg(self,query):
        return self.db_object.aggregrate_all(self.table_name,query)

    def find (self, query):
        return self.db_object.get_all(table_name=self.table_name,conditions=query, sort_index ='username', limit=20)




class UserUpdates():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userupdates'
        self.db_object.create_table(self.table_name,'useruid')
        self.db_object.ensure_index(self.table_name,'latlng')

  
    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': user_id})


    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'sign_up_as':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)
    def update(self, where, what):
        return self.db_object.update(self.table_name, where, what)

    def agg(self,query):
        return self.db_object.aggregrate_all(self.table_name,query)

    def find (self, query):
        return self.db_object.get_all(table_name=self.table_name,conditions=query, sort_index ='_id', limit=1) #00000)



def main():
    up = UserProfile()
    all_up = up.find({"username":"sujitmhj"})
    print all_up
    for each in all_up:
        print each

# main()

import re


class Search():
    """docstring for UserConnections"""
    def __init__(self, keyword="", lon = "", lat ="", place = "", foods="", business="", organisation="",sort="", search_global=False,news="notfornews"):
        keyword = keyword.encode('utf-8')
        self.keyword = str(keyword.strip())
        self.lon = lon
        self.lat = lat
        self.place = place
        self.foods = foods
        self.business = business
        self.organisation = organisation
        self.sort = sort
        self.search_global = search_global
        self.news = news

    def search(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}


            search_variables = ["sign_up_as","business_org_name", "name", "description", "username", "nick_name"]
            
            
            for search_item in search_variables:
                or_conditions.append({search_item:reg_expression})
            # Searches keyword as food
            food_attributes = ["food_name","description","food_tags"]

            for fd_attr in food_attributes:

                or_conditions.append({'foods':{"$elemMatch":{fd_attr:reg_expression}}})



            # search by business type
            or_conditions.append({'type_user':reg_expression})
        


            # Only for profile Search
            # status_query ={'':{"$elemMatch":{'status':reg_expression}}}




        # if(self.lon != "" and self.lat != ""):
        #     query_string['latlng'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":1609340}} #{ "$near" : [ float(self.lon), float(self.lat)] , "$maxDistance": 160.934 } #('$near', {'lat': float(self.lat), 'long': float(self.lon)}), ('$maxDistance', 160.934)]) 
            # query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}


        and_query =[]



        # Limit distance within 200 miles
        # if not self.search_global:
        #     and_query.append({"distance":{"$lte":1609.34}})


        pre_condition = {"sign_up_as":{"$ne":"unclaimed"}}

        and_query.append(pre_condition)

   

        # check food filters
        foods_match = []
        for fd in self.foods:
            foods_match.append({ "$elemMatch" : { "food_name": fd}})
        if len(self.foods) > 0:
            and_query.append({"foods": {"$all":foods_match}})
        
        # Check business filter
        if len(self.business) > 0:
            and_query.append({"type_user":{"$all":self.business}})
        
        # Check organisation filter
        if len(self.organisation) > 0:
            and_query.append({"organisations":{"$all":self.organisation}})

        if len(and_query)>0:
            query_string["$and"] = and_query
        if self.keyword !="":
            query_string["$or"] = or_conditions


        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(self.lon), float(self.lat)] },
            "$maxDistance" : 160000
          }}
          
        up = UserProfile()
        return up.find(query_string)


        

handle = Search(keyword="", lon = "-0.12548719999995228", lat ="51.508515", place = "", foods="", business="", organisation="",sort="", search_global=False,news="notfornews")
print len(handle.search())
# db.userprofile.find().forEach( function(doc){
#     var docpy = doc;
#     for(var i = 0;i<doc.updates.length;i++)
#     {
#         docpy.update = doc.updates[i];
#         delete docpy._id;
#         db.userupdates.insert(docpy);
#     }
#     });