import re

# from TweetFeed import TweetFeed, UserProfile

from bson.son import SON
from bson.objectid import ObjectId
from MongoConnection import MongoConnection

import json
import operator


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
        return self.db_object.get_all(table_name=self.table_name,conditions=query, sort_index ='_id', limit=5000)


class Search():

    """docstring for UserConnections"""
    def __init__(self, keyword="", lon = "", lat ="", place = "", foods="", business="", organisation="",sort=""):
        self.keyword = str(keyword)
        self.lon = lon
        self.lat = lat
        self.place = place
        self.foods = foods
        self.business = business
        self.organisation = organisation
        self.sort = sort


    def item_counter(self, item_list):
        counter = {}
        for item in item_list:
            for it in item:
                try:
                    counter[it] = counter[it] + 1
                except:
                    counter[it] = 1
        
        sorted_counter = sorted(counter.iteritems(), key=operator.itemgetter(1),reverse=True)
        return [{value:label} for value, label in sorted_counter]
 

    def search_all(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []
        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}


            search_variables = ["sign_up_as", "name", "description", "username", "twitter_name"]
            
            
            for search_item in search_variables:
                or_conditions.append({search_item:reg_expression})
            status_query ={'updates':{"$elemMatch":{'status':reg_expression}}}
            or_conditions.append(status_query)
            or_conditions.append({'updates.status':reg_expression})
            query_string['$or'] = or_conditions




        # if(self.lon != "" and self.lat != ""):
        #     query_string['latlng'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":1609340}} #{ "$near" : [ float(self.lon), float(self.lat)] , "$maxDistance": 160.934 } #('$near', {'lat': float(self.lat), 'long': float(self.lon)}), ('$maxDistance', 160.934)]) 
            # query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass
        if len(self.foods) > 0:
            query_string['foods'] = {"$in":self.foods}
        if len(self.business) > 0:
            query_string['type_user'] = {"$in":self.business}
        if len(self.organisation) > 0:
            query_string['organisations'] = {"$in":self.organisation}

        up = UserProfile()
        # up.update({"username":"BobbyeRhym"}, {"updates":[]})

        geo_near = {
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    "maxDistance": 160.934,
                                    # "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":5000,
                                    "distanceMultiplier":6371                          
                                  }
                      }


        agg_pipeline.append(geo_near)
        agg_pipeline.append({ '$match':query_string})
        agg_pipeline.append({"$unwind": "$updates"})


        if len(or_conditions) > 0:
            agg_pipeline.append({ '$match':{"$or":or_conditions}})


        group_fields = {}
        group_fields["_id"] = "all"
        group_fields["foods"] = { "$push": "$foods" }
        group_fields["businesses"] = { "$push": "$type_user" }
        group_fields["organisations"] = { "$push": "$organisations"}

        group_fields["results"] = { "$push": {
        "user":{"name":"$name", 
        "address":"$address",
        "profile_img":"$profile_img",
        "description":"$description",
        "username":"$username"},
        "useruid":"$useruid",
        "type_user":"$type_user",
        "parent_tweetuid":"$parent_tweetuid",
        "status":"$updates.status",
        "distance_text":"$distance",
        "location":"$latlng",
        "organisations":"$organisations",
        "foods":"$foods",
        "sign_up_as":"$sign_up_as",
        "time_stamp":"$time_stamp",
        }}
        
        agg_pipeline.append({"$group": group_fields})
        agg_pipeline.append({"$sort": SON([("distance", 1), ("time_stamp", -1)])})
        results = up.agg(agg_pipeline)[0]
        foods_list = results["foods"]

        foods_counter = self.item_counter(foods_list)
        results["foods"] = foods_counter

        businesses_list = results["businesses"]
        businesses_counter = self.item_counter(businesses_list)
        results["businesses"] = businesses_counter


        organisations_list = results["organisations"]
        organisations_counter = self.item_counter(organisations_list)
        results["organisations"] = organisations_counter
        print len(results['results'])
        print json.dumps(results)
        # print json.dumps(len(up.find(query_string)))
        # print json.dumps(up.find(query_string))

sh = Search(keyword="tone", lon = 85.3363578, lat=27.7059892, place = "", foods=[], business=[], organisation=[],sort="")
sh.search_all()


        


