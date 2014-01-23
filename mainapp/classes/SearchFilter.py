import re
from bson.code import Code
from TweetFeed import TweetFeed, Food

from bson.son import SON
from bson.objectid import ObjectId
class SearchFilter():

    """docstring for UserConnections"""
    def __init__(self):
        pass



    def get_all_foods(self):
        
        query_string = {}
        # if self.keyword !="":
        #     keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
        #     query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}},{'user.username':{"$regex": keyword_like, '$options': '-i'}},{'user.description':{"$regex": keyword_like, '$options': '-i'}}]
            
        # if(self.lon != "" and self.lat != ""):
        #     query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160934}}
        #     pass
        


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
        reducer = Code("""
                       function(obj, prev){
                         prev.count ++;
  
                       }                """)
        from bson.son import SON
        food_object = Food()
        results = food_object.get_all_foods(key={"food_name":1}, condition={}, initial={"count": 0}, reducer=reducer)

        # aggregate_query = [
        #         {"$unwind": "$food_name"},
        #      {"$group": {"_id": "$food_name", "count": {"$sum": 2}}},
        #      {"$sort": SON([("count", -1), ("_id", -1)])}
        #  ]
        # food_object = Food()
        # results = food_object.get_all_foods(aggregate_query)
        print results

        # print results
        # search_results = tweet_search_object.get_search_results(self.keyword, self.lon, self.lat, self.foods, self.business, self.organisation,query_string)
        # full_search_results = []
        # for rs in search_results:
        #     result_id = rs['uid']['id']
        #     result_id_obj=ObjectId(result_id)
        #     result_json = tweet_search_object.search_tweets({"_id":result_id_obj})[0]
        #     result_json['distance'] = rs['value']
        #     full_search_results.append(result_json)


        # # search_results = tweet_search_object.aggregrate(aggregate_query)
        # # search_results = tweet_search_object.search_tweets(query_string)
        # return full_search_results


obj = SearchFilter()
obj.get_all_foods()