import re

# from TweetFeed import TweetFeed, UserProfile

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
        return self.db_object.get_all(table_name=self.table_name,conditions=query, sort_index ='_id', limit=5000)

    def get_count(self,query):
        return self.db_object.get_count(table_name=self.table_name,conditions=query)
class Search2():
    """docstring for UserConnections"""
    def __init__(self, keyword="", lon = "", lat ="", place = "", foods="", business="", organisation="",sort="", search_global=False,news="notfornews"):
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
        
    def get_result_fields(self,type_result):
        if type_result == "description":
            result_type = "$useruid"
        else:
            result_type = "$username"

        return { "$push": {

        "user":{"name":"$name", 
        "business_org_name": "$business_org_name",
        "address":"$address",
        "profile_img":"$profile_img",
        "description":"$description",
        "username":"$username"},
        "useruid":"$useruid",
        "type_user":"$type_user",
        "tweet_id":"$updates.tweet_id",
        "parent_tweetuid":"$updates.parent_tweet_id",
        "status":"$"+type_result,
        "distance":"$distance",
        "location":"$latlng",
        "organisations":"$organisations",
        "foods":"$foods",
        "sign_up_as":"$sign_up_as",
        "zip_code":"$zip_code",
        "time_stamp":"$updates.time_stamp",
        "tweet_pictures":"$updates.picture",
        "result_type":result_type,
        "subscribed": "$subscribed"
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

    def merge_array(self, a, b):
        if len(a)>0:
            if len(b)>0:               
                a[0]["foods"].extend(b[0]["foods"])
                a[0]["businesses"].extend(b[0]["businesses"])
                a[0]["organisations"].extend(b[0]["organisations"])

                a[0]["results"].extend(b[0]["results"])
            return a
        else:
            return b


    def search_all(self):
        statuses = self.get_search_type(0,0)
        print statuses
        profile_individual = self.get_search_type(1,0)
        profile_business = self.get_search_type(1,1)
        profile_organisation = self.get_search_type(1,2)
        profiles = self.merge_array(profile_individual, profile_business)
        profiles = self.merge_array(profiles, profile_organisation)


        if len(profiles)>0:
            if len(statuses)>0:               
                profiles[0]["foods"].extend(statuses[0]["foods"])
                profiles[0]["businesses"].extend(statuses[0]["businesses"])
                profiles[0]["organisations"].extend(statuses[0]["organisations"])
                if not self.search_global:
                    profiles[0]["results"] = profiles[0]["results"][:15]
                    profiles[0]["results"].extend(statuses[0]["results"][:15])
                else:
                    profiles[0]["results"].extend(statuses[0]["results"])
            results = profiles[0]
        else:
            if len(statuses)>0:
                results = statuses[0]
            else:
                return {"foods":[], "businesses":[], "organisations":[],"results":[], "individual_counter":0, "business_counter":0, "organisation_counter":0, "update_counter":0}


        foods_list = results["foods"]
        foods_array = []


        for fds in foods_list:
            fd_list = []
            for fd in fds:
                try:
                    fd_list.append(fd['food_name'])
                except:
                    pass
            foods_array.append(fd_list)


        foods_counter = self.item_counter(foods_array)
        results["foods"] = foods_counter
        businesses_list = results["businesses"]
        businesses_counter = self.item_counter(businesses_list)
        results["businesses"] = businesses_counter
        organisations_list = results["organisations"]
        organisations_counter = self.item_counter(organisations_list)
        results["organisations"] = organisations_counter
        try:
            results["individual_counter"] = profiles[0]["individual_count"]
            results["business_counter"] = profiles[0]["business_count"]
            results["organisation_counter"] = profiles[0]["organisation_count"]
        except:
            results["individual_counter"] = 0
            results["business_counter"] = 0
            results["organisation_counter"] = 0
        try:
            results["update_counter"] = statuses[0]["update_count"]
        except:
            results["update_counter"] = 0
        return results

    def get_search_type(self, search_type, profile = 0):
        query_string = {}
        agg_pipeline = []
        or_conditions = []


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}


            search_variables = ["sign_up_as", "name", "description", "username", "nick_name"]
            
            
            for search_item in search_variables:
                or_conditions.append({search_item:reg_expression})
            # Searches keyword as food
            food_attributes = ["food_name","description","food_tags"]

            for fd_attr in food_attributes:

                or_conditions.append({'foods':{"$elemMatch":{fd_attr:reg_expression}}})

            # search by business type
            or_conditions.append({'type_user':reg_expression})

            
            # Only for Status
            if search_type==0:
                or_conditions.append({'updates.status':reg_expression})
                status_query ={'updates':{"$elemMatch":{'status':reg_expression}}}
                or_conditions.append(status_query)


        

        and_query =[]
        profile_types = ['Individual','Business','Organisation']
        if search_type == 0:
            pre_condition = {"sign_up_as":{"$ne":"unclaimed"}}
        elif search_type == 1:
            pre_condition = {"sign_up_as":profile_types[profile]}


        and_query.append(pre_condition)
        if search_type == 0:
            and_query.append({'updates.1': {"$exists": True}})

        # Limit distance within 200 miles
        # if not self.search_global:
        #     and_query.append({"distance":{"$lte":1609.34}})


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




        geo_near_query = {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    # "maxDistance": 0.025260398681,
                                    "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,
                                    "spherical":True,
                                    "limit":20,
                                    "distanceMultiplier":6371
                                }


        geo_near = {
                        "$geoNear": geo_near_query
                    }


        agg_pipeline.append(geo_near)

        # if len(and_query)>0 or self.keyword != "":
        #     agg_pipeline.append({ '$match':query_string})

        # for profile search
        # if search_type==1:
        #     only_business_org = [{"sign_up_as":{"$ne":"unclaimed"}}]
        #     agg_pipeline.append({ '$match': {"$and": only_business_org}})


        if search_type == 0:
            agg_pipeline.append({"$unwind": "$updates"})


        if search_type == 0:
            if self.keyword != "":
                agg_pipeline.append({ '$match':{"updates.status":reg_expression, "updates.deleted":{"$ne":1},"updates.parent_tweet_id":"0"}})
            else:
                agg_pipeline.append({ '$match':{"updates.deleted":{"$ne":1},"updates.parent_tweet_id":"0"}})
        
        start_time = int(time.time()) - 7*24*3600
        end_time = int(time.time()) 
        if search_type == 0 and self.news != "notfornews":
            if  self.news == "old" or self.news == "none":
                start_time = int(time.time()) - 14*24*3600
                end_time = int(time.time()) - 7*24*3600
            elif  self.news == "daily":
                start_time = int(time.time()) - 1*24*3600
                end_time = int(time.time())
            elif  self.news == "weekly":
                start_time = int(time.time()) - 7*24*3600
                end_time = int(time.time()) 
            elif  self.news == "monthly":
                start_time = int(time.time()) - 30*24*3600
                end_time = int(time.time())             
            agg_pipeline.append({ '$match':{"updates.time_stamp": {"$lte":end_time,"$gte":start_time} }})

        # agg_pipeline.append({ '$match':{"updates":{"$size":0}}})
        if self.sort == "time":
            sort_text = "updates.time_stamp"
            sort_order = -1
        else:
            sort_text = "distance"
            sort_order = 1
        
        if search_type == 1:
            sort_text = "distance"
            sort_order = 1

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})
        agg_pipeline.append({ "$limit" : 20 })

        group_fields = {}
        group_fields["_id"] = "all"
        group_fields["foods"] = { "$push": "$foods" }
        group_fields["businesses"] = { "$push": "$type_user"}
        group_fields["organisations"] = { "$push": "$organisations"}
        group_fields["individual_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Individual"]}, 1, 0]}}
        group_fields["business_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Business"]}, 1, 0]}}
        group_fields["organisation_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Organisation"]}, 1, 0]}}
        group_fields["update_count"] = {"$sum": 1}

        if search_type == 0:
            result_type = "updates.status"
        else:
            result_type = "description"
        
        group_fields["results"] = self.get_result_fields(result_type)
        
        agg_pipeline.append({"$group": group_fields})
        

        
        

        

        up = UserProfile()
        return up.agg(agg_pipeline)
        
        # print json.dumps(len(up.find(query_string)))
        # print json.dumps(up.find(query_string))

# sh = Search(keyword="sujit", lon = 85.3363578, lat=27.7059892, place = "", foods=[], business=['Compost','Animal Feed'], organisation=[],sort="")
# print sh.search_all()



    def get_tweet_by_parent(self, parent_tweet_id):
        
        agg_pipeline = []


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
        query_string = {'updates':{"$elemMatch":{'parent_tweet_id':{"$in":parent_tweet_id}}}}
        agg_pipeline.append({ '$match':query_string})

        agg_pipeline.append({"$unwind": "$updates"})


        agg_pipeline.append({ '$match':{"updates.deleted":{"$ne":1}, "updates.parent_tweet_id":{"$in":parent_tweet_id}}})

       
        # agg_pipeline.append({ '$match':{"updates":{"$size":0}}})

        sort_text = "updates.time_stamp"
        sort_order = -1

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

        if search_type == 0:
            agg_pipeline.append({"$limit":20})

        # next_index = 5
        # if len(or_conditions) > 0:
        #     next_index = 6
        #     agg_pipeline.append({ '$match':{"$or":or_conditions}})


        group_fields = {}
        group_fields["_id"] = "all"
        group_fields["foods"] = { "$push": "$foods.foods_match" }
        group_fields["businesses"] = { "$push": "$type_user"}
        group_fields["organisations"] = { "$push": "$organisations"}
        group_fields["individual_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Individual"]}, 1, 0]}}
        group_fields["business_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Business"]}, 1, 0]}}
        group_fields["organisation_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Organisation"]}, 1, 0]}}
        group_fields["update_count"] = {"$sum": 1}

        result_type = "updates.status"
        group_fields["results"] = self.get_result_fields(result_type)
        
        agg_pipeline.append({"$group": group_fields})
            

        up = UserProfile()
        return up.agg(agg_pipeline)







    def get_single_tweet(self, tweet_id):
        
        agg_pipeline = []


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
        query_string = {'updates':{"$elemMatch":{'tweet_id':tweet_id}}}
        agg_pipeline.append({ '$match':query_string})

        agg_pipeline.append({"$unwind": "$updates"})


        agg_pipeline.append({ '$match':{"updates.deleted":{"$ne":1}, "updates.tweet_id":tweet_id}})

       
        # agg_pipeline.append({ '$match':{"updates":{"$size":0}}})

        sort_text = "updates.time_stamp"
        sort_order = -1

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

        # next_index = 5
        # if len(or_conditions) > 0:
        #     next_index = 6
        #     agg_pipeline.append({ '$match':{"$or":or_conditions}})


        group_fields = {}
        group_fields["_id"] = "all"
   
        result_type = "updates.status"
   
        
        group_fields["results"] = self.get_result_fields(result_type)
        
        agg_pipeline.append({"$group": group_fields})
        

        

        up = UserProfile()
        return up.agg(agg_pipeline)[0]['results']



    def get_direct_children(self, root_id):
        try:
            results = self.get_tweet_by_parent(root_id)[0]['results']
            return results
        except:
            return None



    def get_all_children(self,root_id):
    
        try:
            results = self.get_tweet_by_parent(root_id)[0]['results']
            # return results
            total_results = results
            tweet_ids = []
            for result in results:
                mentions = '@'+result['user']['username']
                result['mentions'] = mentions
                # tweet_ids.append(result['tweetuid'])

                childrens = self.get_all_children([result['tweetuid']])

                if childrens != None:
                    for child in childrens:
                        child['mentions'] = mentions + " " + child['mentions']
                    total_results.extend(childrens)
            return total_results
        except:
            return None
