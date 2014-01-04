import re

from TweetFeed import TweetFeed



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
            query_string['status'] = {"$regex": keyword_like, '$options': '-i'}

        if(self.lon != "" and self.lat != ""):
            query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":160934}}
        # print query_string
        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.search_tweets(query_string)
        return search_results
