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
    def get_result_fields(self,type_result):
        if type_result == "description":
            result_type = "$useruid"
        else:
            result_type = "$username"
        return { "$push": {
        "user":{"name":"$name", 
        "address":"$address",
        "profile_img":"$profile_img",
        "description":"$description",
        "username":"$username"},
        "useruid":"$useruid",
        "type_user":"$type_user",
        "parent_tweetuid":"$parent_tweetuid",
        "status":"$"+type_result,
        "distance":"$distance",
        "location":"$latlng",
        "organisations":"$organisations",
        "foods":"$foods",
        "sign_up_as":"$sign_up_as",
        "time_stamp":"$updates.time_stamp",
        "result_type":result_type
        }}


    def item_counter(self, item_list):
        counter = {}
        try:
            for it in item_list:
                try:
                    counter[it] = counter[it] + 1
                except:
                    
                    counter[it] = 1
             
        except:
            counter = {}
            for item in item_list:
                for it in item:
                    try:
                        counter[it] = counter[it] + 1
                    except:
                        try:
                            counter[it] = 1
                        except:
                            pass

    
            

        
        sorted_counter = sorted(counter.iteritems(), key=operator.itemgetter(1),reverse=True)
        return [{"uid":value,"value":label} for value, label in sorted_counter]
 

    def search_all(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []
        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}


            search_variables = ["sign_up_as", "name", "description", "username", "nick_name"]
            
            
            for search_item in search_variables:
                or_conditions.append({search_item:reg_expression})
            status_query ={'updates':{"$elemMatch":{'status':reg_expression}}}

            # Searches keyword as food
            or_conditions.append({'foods':reg_expression})


            or_conditions.append({'businesses':reg_expression})

            or_conditions.append(status_query)
            or_conditions.append({'updates.status':reg_expression})
            query_string['$or'] = or_conditions

        # if(self.lon != "" and self.lat != ""):
        #     query_string['latlng'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":1609340}} #{ "$near" : [ float(self.lon), float(self.lat)] , "$maxDistance": 160.934 } #('$near', {'lat': float(self.lat), 'long': float(self.lon)}), ('$maxDistance', 160.934)]) 
            # query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass

        and_query =[]
        up = UserProfile()


        # Limit distance within 200 miles
        and_query.append({"distance":{"$lte":321.868}})


        # check food filters
        if len(self.foods) > 0:
            and_query.append({"foods": {"$all":self.foods}})
        
        # Check business filter
        if len(self.business) > 0:
            and_query.append({"type_user":{"$all":self.business}})
        
        # Check organisation filter
        if len(self.organisation) > 0:
            and_query.append({"organisations":{"$all":self.organisation}})


        query_string["$and"] = and_query
 

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

       
        agg_pipeline.append({ '$match':{"updates":{"$size":0}}})
        if self.sort == "time":
            sort_text = "updates.time_stamp"
            sort_order = -1
        else:
            sort_text = "distance"
            sort_order = 1
        

        # print sort_text

        
        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

        next_index = 4
        if len(or_conditions) > 0:
            next_index = 5
            agg_pipeline.append({ '$match':{"$or":or_conditions}})


        group_fields = {}
        group_fields["_id"] = "all"
        group_fields["foods"] = { "$push": "$foods" }
        group_fields["businesses"] = { "$push": "$type_user" }
        group_fields["organisations"] = { "$push": "$organisations"}

        group_fields["results"] = self.get_result_fields("description")
        
        agg_pipeline.append({"$group": group_fields})
        
        agg_pipeline.append({ "$limit" : 20 })

        
        
        profiles = up.agg(agg_pipeline)
        agg_pipeline[2] = {"$unwind": "$updates"}

        group_fields["results"] = self.get_result_fields("updates.status")
        # agg_pipeline[next_index] = {"$group":group_fields}
        statuses = up.agg(agg_pipeline)

        if len(profiles)>0:
            if len(statuses)>0:
               
                profiles[0]["foods"].extend(statuses[0]["foods"])
                profiles[0]["businesses"].extend(statuses[0]["businesses"])
                profiles[0]["organisations"].extend(statuses[0]["organisations"])
                profiles[0]["results"].extend(statuses[0]["results"])
        else:
            profiles = statuses

        
        if len(profiles)>0:

            results = profiles[0]
        else:
            return {"foods":[], "businesses":[], "organisations":[],"results":[]}


        foods_list = results["foods"]

        foods_counter = self.item_counter(foods_list)
        results["foods"] = foods_counter

        businesses_list = results["businesses"]
        businesses_counter = self.item_counter(businesses_list)
        results["businesses"] = businesses_counter

        organisations_list = results["organisations"]
        organisations_counter = self.item_counter(organisations_list)
        results["organisations"] = organisations_counter
        # print len(results['results'])
        # print json.dumps(results)
        # print results
        return results
        # print json.dumps(len(up.find(query_string)))
        # print json.dumps(up.find(query_string))

# sh = Search(keyword="sujit", lon = 85.3363578, lat=27.7059892, place = "", foods=[], business=['Compost','Animal Feed'], organisation=[],sort="")
# print sh.search_all()


        


