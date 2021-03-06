#!/usr/bin/env python
# encoding: utf-8
import re

# from TweetFeed import TweetFeed, UserProfile

from bson.son import SON
from bson.objectid import ObjectId
from MongoConnection import MongoConnection
import json
import operator
import datetime,time
from TweetFeed import TradeConnection
from TweetFeed import UserProfile as UserDetails

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
        "subscribed": "$subscribed",
        "video_url":'$video_url',
        "banner_url":'$profile_banner_url'
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

    def get_tweets_by_user_id(self, user_id):
        query_string = {}
        agg_pipeline = []
        or_conditions = []

        up = UserDetails()
        usr_pr = up.get_profile_by_id(user_id)
        search_user = {"useruid":user_id}
        if usr_pr['sign_up_as'] == "Organisation":

            if usr_pr.get('business_org_name')!=None:
                myname = usr_pr.get('business_org_name') if (usr_pr['sign_up_as'] == 'Business' or usr_pr['sign_up_as'] == 'Organisation') \
                and usr_pr.get('business_org_name')!='' else usr_pr['name']
            else:
                myname = usr_pr['name']
            search_org = {"organisations":{"$all":[myname]}}
            query_string = {"$or":[search_user,search_org]}
        else:
            query_string = search_user


        geo_near = {
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    # "maxDistance": 160.934,
                                    "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":50,
                                    "distanceMultiplier":6371
                                }
                      }
        agg_pipeline.append(geo_near)

        # agg_pipeline.append({ '$match':query_string})

        agg_pipeline.append({"$unwind": "$updates"})


        query_string2 = {"updates.deleted":{"$ne":1},"updates.parent_tweet_id":"0"}
        agg_pipeline.append({ '$match':query_string2})
       
        # agg_pipeline.append({ '$match':{"updates":{"$size":0}}})
        sort_text = "updates.time_stamp"
        sort_order = -1
       

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

        group_fields = {}
        group_fields["_id"] = "all"

        group_fields["businesses"] = { "$push": "$type_user"}

        group_fields["update_count"] = {"$sum": 1}

        result_type = "updates.status"
        
        
        group_fields["results"] = self.get_result_fields(result_type)
        
        agg_pipeline.append({"$group": group_fields})
        

        
        agg_pipeline.append({ "$limit" : 10 })

        

        up = UserProfile()
        statuses = up.agg(agg_pipeline)

        result_profiles = []
        if len(statuses)>0:
            return statuses[0]
        else:
            return {"foods":[], "businesses":[], "organisations":[],"results":[], "update_count":0}


   
    def supplier_updates(self, user_id,request_type):
        query_string = {}
        agg_pipeline = []
        or_conditions = []

        trade_con = TradeConnection()
        if request_type == "suppliers":
            conns = trade_con.get_connection_by_business(user_id)
            dict_name = "c_useruid"
        if request_type == "stockists":
            conns = trade_con.get_connection_by_customer(user_id)
            dict_name = "b_useruid"
      
        

        con_ids = []
        if request_type == "suppliers" or request_type == "stockists":
            for con in conns:
                con_ids.append(con[dict_name])


        if request_type == "favourites":
            up = UserDetails()
            user_details = up.get_profile_by_id(user_id)
            try:
                favourites = user_details['favourites']
            except:
                favourites = []
            con_ids = favourites

        and_query = []

        if len(con_ids) == 0:
            return {"foods":[], "businesses":[], "organisations":[],"results":[], "individual_counter":0, "business_counter":0, "organisation_counter":0, "update_counter":0}


        query_string = {"useruid":{"$in":con_ids}}

        geo_near = {
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    # "maxDistance": 160.934,
                                    "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":20,
                                    "distanceMultiplier":6371
                                }
                      }
        agg_pipeline.append(geo_near)

        # agg_pipeline.append({ '$match':query_string})

        agg_pipeline.append({"$unwind": "$updates"})


        query_string2 = {"updates.deleted":{"$ne":1},"updates.parent_tweet_id":"0"}
        agg_pipeline.append({ '$match':query_string2})
       
        # agg_pipeline.append({ '$match':{"updates":{"$size":0}}})
        sort_text = "updates.time_stamp"
        sort_order = -1
       

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

        group_fields = {}
        group_fields["_id"] = "all"
        group_fields["foods"] = { "$push": "$foods" }
        group_fields["businesses"] = { "$push": "$type_user"}
        group_fields["organisations"] = { "$push": "$organisations"}
        group_fields["individual_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Individual"]}, 1, 0]}}
        group_fields["business_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Business"]}, 1, 0]}}
        group_fields["organisation_count"] = {"$sum":{"$cond": [{"$eq": ['$sign_up_as', "Organisation"]}, 1, 0]}}
        group_fields["update_count"] = {"$sum": 1}

        result_type = "updates.status"
        
        
        group_fields["results"] = self.get_result_fields(result_type)
        
        agg_pipeline.append({"$group": group_fields})
        

        
        agg_pipeline.append({ "$limit" : 30 })

        

        up = UserProfile()
        statuses = up.agg(agg_pipeline)

        result_profiles = []
        profile_counts = {"Individual":0, "Business":0, "Organisation":0}
      
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



    def search_all(self):
        statuses = self.get_search_type(0)
        profiles = self.get_search_type(1)

        result_profiles = []
        profile_counts = {"Individual":0, "Business":0, "Organisation":0}
        if len(profiles)>0:
            for prf in profiles[0]['results']:
                if profile_counts[prf['sign_up_as']] < 20:
                    result_profiles.append(prf)
                    profile_counts[prf['sign_up_as']] = profile_counts[prf['sign_up_as']] +1

                if len(result_profiles) > 60:
                    break

            profiles[0]['results'] = result_profiles

        if len(profiles)>0:
            if len(statuses)>0:               
                profiles[0]["foods"].extend(statuses[0]["foods"])
                profiles[0]["businesses"].extend(statuses[0]["businesses"])
                profiles[0]["organisations"].extend(statuses[0]["organisations"])
                # if not self.search_global:
                    # profiles[0]["results"] = profiles[0]["results"][:15]
                profiles[0]["results"].extend(statuses[0]["results"][:20])
                # else:
                #     profiles[0]["results"].extend(statuses[0]["results"])
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

    def get_search_type(self, search_type):
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
        

            # Only for Status
            if search_type==0:
                or_conditions.append({'updates.status':reg_expression})
                status_query ={'updates':{"$elemMatch":{'status':reg_expression}}}
                or_conditions.append(status_query)


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

        if search_type == 0:
            check_update = {'updates.0': {"$exists": True}}
            and_query.append(check_update)


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


        geo_search = {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    # "maxDistance": 0.425260398681,
                                    "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,
                                    "spherical":True,
                                    "limit":30,
                                    "distanceMultiplier":6371
                                }

        if not self.search_global :
            geo_search['maxDistance'] = 0.01511379689
        geo_near = {
                        "$geoNear": geo_search
                      }



        agg_pipeline.append(geo_near)

        if len(and_query)>0 or self.keyword != "":
            agg_pipeline.append({ '$match':query_string})

        # for profile search
        # if search_type==1:
        #     only_business_org = [{"sign_up_as":{"$ne":"unclaimed"}}]
        #     agg_pipeline.append({ '$match': {"$and": only_business_org}})


        if search_type == 0:
            agg_pipeline.append({"$unwind": "$updates"})


        if search_type == 0:
            new_q_string = dict(query_string)
            new_and = and_query[:]
            new_and.remove(check_update)
            new_and.append({"updates.deleted":{"$ne":1},"updates.parent_tweet_id":"0"})
            new_q_string["$and"] = new_and
            agg_pipeline.append({ '$match':new_q_string})
        
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
        

        
        agg_pipeline.append({ "$limit" : 30 })

        

        up = UserProfile()
        return up.agg(agg_pipeline)
        
        # print json.dumps(len(up.find(query_string)))
        # print json.dumps(up.find(query_string))

# sh = Search(keyword="sujit", lon = 85.3363578, lat=27.7059892, place = "", foods=[], business=['Compost','Animal Feed'], organisation=[],sort="")
# print sh.search_all()



    def get_tweet_by_parent(self, parent_tweet_id):
        agg_pipeline = []


        parent_tweet_query = {"sign_up_as":{"$ne":"unclaimed"}, 'updates':{"$elemMatch":{'parent_tweet_id':parent_tweet_id}}}

        geo_near = {
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    # "maxDistance": 160.934,
                                    "query": parent_tweet_query,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":10,
                                    "distanceMultiplier":6371
                                }
                      }
        agg_pipeline.append(geo_near)
        # query_string = {'updates':{"$elemMatch":{'parent_tweet_id':parent_tweet_id}}}
        # agg_pipeline.append({ '$match':query_string})

        agg_pipeline.append({"$unwind": "$updates"})


        agg_pipeline.append({ '$match':{"updates.deleted":{"$ne":1}, "updates.parent_tweet_id":parent_tweet_id}})

       
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
        agg_pipeline.append({ "$limit" : 30 })
        up = UserProfile()
        return up.agg(agg_pipeline)

    def get_single_tweet(self, tweet_id):
        agg_pipeline = []
        query_string = {'updates':{"$elemMatch":{'tweet_id':tweet_id}}}
        geo_near = {
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    "maxDistance": 160.934,
                                    "query": query_string,
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":1,
                                    "distanceMultiplier":6371
                                  }
                      }
        agg_pipeline.append(geo_near)
        agg_pipeline.append({"$unwind": "$updates"})
        agg_pipeline.append({ '$match':{"updates.deleted":{"$ne":1}, "updates.tweet_id":tweet_id}})
        sort_text = "updates.time_stamp"
        sort_order = -1

        agg_pipeline.append({"$sort": SON([(sort_text, sort_order), ("time_stamp", -1)])})

 

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

                childrens = self.get_all_children(result['tweetuid'])

                if childrens != None:
                    for child in childrens:
                        child['mentions'] = mentions + " " + child['mentions']
                    total_results.extend(childrens)
            return total_results
        except:
            return None
