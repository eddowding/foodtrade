import re

from TweetFeed import TweetFeed, UserProfile

from bson.son import SON
from bson.objectid import ObjectId
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



    def search(self, search_by="Updates"):
        return self.search_updates()
        if search_by == "updates":
            pass
        else:
            return self.search_profiles()


    def search_profiles(self):

        tweet_search_object = UserProfile()
        search_results = tweet_search_object.get_search_results(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string,self.sort)
        full_search_results = []
        for rs in search_results:
            result_id = rs['uid']['id']
            result_id_obj=ObjectId(result_id)
            result_json = tweet_search_object.search_tweets({"_id":result_id_obj})[0]
            result_json['distance'] = rs['value']['distance']
            full_search_results.append(result_json)

        return full_search_results
        pass




        
    def search_updates(self):
        query_string = {}
        # if self.keyword !="":
        #     keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
        #     query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}},{'user.username':{"$regex": keyword_like, '$options': '-i'}},{'user.description':{"$regex": keyword_like, '$options': '-i'}}]
            
        if(self.lon != "" and self.lat != ""):
            query_string['location'] = { "$near" : [ float(self.lon), float(self.lat)] , "$maxDistance": 0 } #('$near', {'lat': float(self.lat), 'long': float(self.lon)}), ('$maxDistance', 160.934)]) 
            # query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass

        


# aggregate_query = [{
        #                 "$geoNear": {"near": [float(self.lon), float(self.lat)],
        #                             "distanceField": "distance",
        #                             "maxDistance": 160.934,
        #                             # "query": query_string,
        #                             # "includeLocs": "location.coordinates",
        #                             "uniqueDocs": True,  
        #                             "spherical":True,
        #                             "limit":20,
        #                             "distanceMultiplier":6371                          
        #                           }
        #               },
        #               { '$match':query_string},
        #               {"$sort": SON([("distance", 1), ("_id", -1)])}
        #               ]


        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.get_search_results(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string,self.sort)
        full_search_results = []
        for rs in search_results:
            result_id = rs['uid']['id']
            result_id_obj=ObjectId(result_id)
            result_json = tweet_search_object.search_tweets({"_id":result_id_obj})[0]
            result_json['distance'] = rs['value']['distance']
            full_search_results.append(result_json)

        return full_search_results
    def get_food_filters(self):
        query_string = {}
        # if self.keyword !="":
        #     keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
        #     query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}},{'user.username':{"$regex": keyword_like, '$options': '-i'}},{'user.description':{"$regex": keyword_like, '$options': '-i'}}]
            
        if(self.lon != "" and self.lat != ""):
            query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass

        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.get_all_foods(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string)
       


        # search_results = tweet_search_object.aggregrate(aggregate_query)
        # search_results = tweet_search_object.search_tweets(query_string)
        return search_results

    def get_business_filters(self):
        query_string = {}
        # if self.keyword !="":
        #     keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
        #     query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}},{'user.username':{"$regex": keyword_like, '$options': '-i'}},{'user.description':{"$regex": keyword_like, '$options': '-i'}}]
            
        if(self.lon != "" and self.lat != ""):
            query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass

        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.get_all_businesses(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string)
       


        # search_results = tweet_search_object.aggregrate(aggregate_query)
        # search_results = tweet_search_object.search_tweets(query_string)
        return search_results


    def get_organisation_filters(self):
        query_string = {}
        # if self.keyword !="":
        #     keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
        #     query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}},{'user.username':{"$regex": keyword_like, '$options': '-i'}},{'user.description':{"$regex": keyword_like, '$options': '-i'}}]
            
        if(self.lon != "" and self.lat != ""):
            query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160.934}}
            pass

        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.get_all_organisations(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string)
       


        # search_results = tweet_search_object.aggregrate(aggregate_query)
        # search_results = tweet_search_object.search_tweets(query_string)
        return search_results