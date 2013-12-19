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
            keyword_like = re.compile(self.keyword + '+')
            query_string['status'] = {"$regex": keyword_like, '$options': '-i'}

        if(self.lon != "" and self.lat != ""):
            query_string['location'] = {"$near":{"$geometry":{"type":"Point", "coordinates":[float(self.lon), float(self.lat)]}, "$maxDistance":500000}}

        tweet_search_object = TweetFeed()
        search_results = tweet_search_object.search_tweets(query_string)
        print search_results



tweet_handler = TweetFeed()
tweet_doc = {
    'tweet_id':543654,
    'parent_tweet_id':0,
    'status':"I want to #sell 5 kg of #tomatoes",    
    'location':{"type": "Point", "coordinates": [102.0, 0.5]},
    'user':{
    'name': "David Villa",
    'Description':"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
    }
}
from pymongo import Connection
c = Connection()
c.drop_database('foodtrade')
tweet_handler.insert_tweet(tweet_doc)

search_handle = Search("#to", 102.0, 4.5, "nepal")
search_handle.search()

