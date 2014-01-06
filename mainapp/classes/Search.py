import re

from mainapp.classes.TweetFeed import TweetFeed

from bson.son import SON

class Search():

    """docstring for UserConnections"""
    def __init__(self, keyword="", lon = "", lat ="", place = "", foods="-1", business="-1", organisation="-1"):
        self.keyword = str(keyword)
        self.lon = lon
        self.lat = lat
        self.place = place
        self.foods = foods
        self.business = business
        self.organisation = organisation



    def search(self):
        query_string = {}
        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            query_string['$or'] = [{'status':{"$regex": keyword_like, '$options': '-i'}},{'user.name':{"$regex": keyword_like, '$options': '-i'}}]
            
        if(self.lon != "" and self.lat != ""):
            # query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160934}}
            pass
        # print query_string
        if(self.foods!="-1"):
            pass
        if(self.business!="-1"):
            pass
        if(self.organisation!="-1"):
            pass


        aggregate_query = [{
                        "$geoNear": {"near": [float(self.lon), float(self.lat)],
                                    "distanceField": "distance",
                                    "maxDistance": 160.934,
                                    # "query": query_string,
                                    # "includeLocs": "location.coordinates",
                                    "uniqueDocs": True,  
                                    "spherical":True,
                                    "limit":20,
                                    "distanceMultiplier":6371                          
                                  }
                      },
                      { '$match':query_string},
                      {"$sort": SON([("distance", 1), ("_id", -1)])}
                      ]
        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.aggregrate(aggregate_query)
        # search_results = tweet_search_object.search_tweets(query_string)
        return search_results
