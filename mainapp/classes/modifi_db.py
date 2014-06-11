from bson.son import SON
from bson.objectid import ObjectId
from MongoConnection import MongoConnection
import json
import operator
import datetime,time
from pygeocoder import Geocoder
import re
from bson import json_util
from bson.json_util import loads
class general_search():
    def __init__(self,request):

        db_object = MongoConnection("localhost",27017,'foodtrade')
        table_name = 'userprofile'
        db_object.create_table(table_name,'useruid')
        db_object.ensure_index(table_name,'latlng')

        db_object.create_table(table_name,'username')

        self.db = db_object.get_db()[table_name]

        self.keyword = ""
        self.search_for = "food"
        self.location = "Bristol, UK"
        self.lon = 87
        self.lat = 27
        # location_res = Geocoder.geocode(self.location)
        # self.lon = float(location_res.longitude)
        # self.lat = float(location_res.latitude)
        self.indiv_biz = []
        self.orz_filters = []
        self.biz_type_filters = []
        self.food_filters = []
        self.radius = 160900000

    def get_result(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}

            if self.search_for != "food":
                search_variables = ["business_org_name", "name", "description", "username", "nick_name"]
            
                
                for search_item in search_variables:
                    or_conditions.append({search_item:reg_expression})
            # Searches keyword as food
            else:
                food_attributes = ["food_name","description","food_tags"]

                for fd_attr in food_attributes:

                    or_conditions.append({'foods':{"$elemMatch":{fd_attr:reg_expression}}})



            # search by business type"
            if self.search_for != "food":
                or_conditions.append({'type_user':reg_expression})
        
        and_query =[]

        pre_condition = {"sign_up_as":{"$ne":"unclaimed"}}

        and_query.append(pre_condition)

   

        # check food filters
        foods_match = []
        for fd in self.food_filters:
            foods_match.append({ "$elemMatch" : { "food_name": fd}})
        if len(self.food_filters) > 0:
            and_query.append({"foods": {"$all":foods_match}})
        
        # Check business filter
        if len(self.biz_type_filters) > 0:
            and_query.append({"type_user":{"$all":self.business}})
        
        # Check organisation filter
        if len(self.orz_filters) > 0:
            and_query.append({"organisations":{"$all":self.orz_filters}})

        if len(and_query)>0:
            query_string["$and"] = and_query
        if self.keyword !="":
            query_string["$or"] = or_conditions


        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(self.lon), float(self.lat)] },
            "$maxDistance" : self.radius
          }}
# - profile_img
# - username
# - name
# - type
# - description
# - foods
        all_doc = self.db.find(query_string,{"latlng":1,"name":1,"user_type":1,"description":1,"profile_img":1,"foods":1,"username":1,"_id":0})
        total =  all_doc.count()
        first20 = all_doc.limit(20)
        result = [doc for doc in first20]
       
        for i in range(0,len(result)):
            distance= calc_distance(self.lat, 
                self.lon, 
                result[i]['latlng']['coordinates'][1],
                result[i]['latlng']['coordinates'][0])
            # print distance

            result[i]['distance']  = distance
        


        return result[0]

import math

def calc_distance(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6371000


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

gs = general_search("res")
print gs.get_result()


class UserUpdates():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userupdates'
        self.db_object.create_table(self.table_name,'useruid')
        self.db_object.create_table(self.table_name,'update.time')
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



    def get_latest_updates(self,lon, lat):
        query_string = {}
        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(lon), float(lat)] },
            "$maxDistance" : 160000
          }}
        return self.db_object.get_all_custom(table_name=self.table_name,fields={"update.time_stamp":1},conditions=query_string, sort_index ='update.time_stamp', limit=5)
        

    def get_latest_after(self,lon, lat,time_stamp):
        query_string = {}
        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(lon), float(lat)] },
            "$maxDistance" : 160000
          }}
        query_string["update.time_stamp"] = {"$gt":time_stamp}
        return self.db_object.get_all_custom(table_name=self.table_name,conditions=query_string, sort_index ='update.time_stamp', limit=5)
        
# uu = UserUpdates()
# print uu.get_latest_updates(lon = "-0.12548719999995228", lat ="51.508515")
# print uu.get_latest_after(lon = "-0.12548719999995228", lat ="51.508515",time_stamp = 1400590225)




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


        

# handle = Search(keyword="", lon = "-0.12548719999995228", lat ="51.508515", place = "", foods="", business="", organisation="",sort="", search_global=False,news="notfornews")
# print len(handle.search


# db.userprofile.find().forEach( function(doc){
#     var docpy = doc;
#     for(var i = 0;i<doc.updates.length;i++)
#     {
#         docpy.update = doc.updates[i];
#         delete docpy._id;
#         db.userupdates.insert(docpy);
#     }
#     });


# db.userprofile.find().forEach( function(doc){
    
#     for(var i = 0;i<doc.foods.length;i++)
#     {
#         var food = doc.foods[i];
#         food.latlng = doc.latlng;

#         db.userfoods.insert(food);
#     }
#     });



