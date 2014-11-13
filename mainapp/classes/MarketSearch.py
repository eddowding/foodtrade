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

from FullSearch import GeneralSearch

    

class MarketSearch(GeneralSearch):
    def get_result(self):
        query_string = []

        agg_pipeline = []
        or_conditions = []
        # Check if keyword is not empty
        if self.want != "all":
            want_like = re.compile(self.want + '+', re.IGNORECASE)
            want_re = {"$regex": want_like, '$options': '-i'}
            query_string .append({'updates':{"$elemMatch":{'status':want_re,"deleted":0}}})


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            keyword_re = {"$regex": keyword_like, '$options': '-i'}
            query_string .append({'updates':{"$elemMatch":{'status':keyword_re,"deleted":0}}})
        if self.user_type != "all":
            sign_up_as = "Business" if self.user_type == "Companies" else "Individual"
            print sign_up_as
            query_string.append({"sign_up_as":sign_up_as})

        if len(self.biz_type_filters) > 0:
            query_string.append({"type_user":{"$all":self.biz_type_filters}})
        
        # Check organisation filter
        if len(self.org_filters) > 0:
            query_string.append({"organisations":{"$all":self.org_filters}})


        query_string.append({"$nor":[{"$exists": False},{"updates": { "$size": 0 }}]})
        time_stamp = int(time.time()) - 300*24*3600
        # query_string.append({'updates':{"$elemMatch":{'time_stamp':{"$gt":int(time_stamp)},"deleted":0}}})



        geo_search = {"near": [float(self.lng), float(self.lat)],
                                   "distanceField": "distance",
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,
                                    "spherical":True,
                                    "limit":5000,
                                }

        

        pipeline = []

        final_query = {"$and":query_string}

        if len(query_string)>0:
            geo_search['query'] = final_query


        geo_search['maxDistance'] = self.max_distance
        
        geo_near = {
                        "$geoNear": geo_search
                      }


        # pipeline.append(geo_near)
 
        pipeline.append({"$project":{"username":1, "description":1,"type_user":1, "address":1,"sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0,"profile_banner_url":1}})
        pipeline.append({"$unwind":"$updates"})
        
        and_query = []
        if self.keyword !="":
            and_query.append({"updates.status":keyword_re})
        if self.want!="all":
            and_query.append({"updates.status":want_re})

        and_query.append({'updates.time_stamp':{"$gt":time_stamp},"updates.deleted":0})

        if len(and_query) == 0:
            and_query = [{"updates.deleted":0}]

        pipeline.append({"$match":{"$and":and_query}})

        pipeline.append({"$sort": SON([("updates.time_stamp", -1)])})
        pipeline.append({"$limit":self.result_limit})
        agg = self.db.aggregate(pipeline)['result']
        for result in agg:
            result['updates']['status_raw'] = result['updates']['status']
            result['updates']['status'] = self.recognise_name(result['updates']['status'])
        return {"result":agg, "total":200,"center":[float(self.lng), float(self.lat)]}


    def replies_count(self,parent_tweet_id):
        query_string = {'updates':{"$elemMatch":{'parent_tweet_id':parent_tweet_id,"deleted":0}}}
        pipeline = []
        pipeline.append({"$match":query_string})
        pipeline.append({"$project":{"updates":1, "_id":0}})
        pipeline.append({"$unwind":"$updates"})
        pipeline.append({"$match":{"updates.parent_tweet_id":parent_tweet_id}})

        pipeline.append({"$group": { "_id": "same", "count": { "$sum":1} }})
        agg = self.db.aggregate(pipeline)
        result = self.db.aggregate(pipeline)['result']

        if len(result)>0:
            return result[0]['count']
        return 0





    def get_single_tweet(self,tweet_id):
        query_string = {'updates':{"$elemMatch":{'tweet_id':tweet_id,"deleted":0}}}
        pipeline = []
        pipeline.append({"$match":query_string})
        pipeline.append({"$project":{"username":1, "description":1,"address":1,"type_user":1, "sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0}})
        pipeline.append({"$unwind":"$updates"})
        pipeline.append({"$match":{"updates.tweet_id":tweet_id}})
        result = self.db.aggregate(pipeline)['result']
        parameter = {"status":"error"}

        if len(result)>0:
            distance = self.calc_distance(result[0]['latlng']['coordinates'][1],result[0]['latlng']['coordinates'][0])
            result[0]['distance'] = '%.1f' % distance
            result[0]['updates']['status'] = self.recognise_name(result[0]['updates']['status'])
            if distance<50 or self.user['subscribed'] == 1:
                parameter['status'] = "ok"
                result[0]['replies_count'] = self.replies_count(tweet_id)

                parameter['result'] = result[0]
        return parameter

    def get_filters(self,ftype):
        query_string = []
        if ftype == "biz":
            filter_type = "type_user"
        else:
            filter_type = "organisations"
        


        # Check if keyword is not empty
        if self.want != "all":
            want_like = re.compile(self.want + '+', re.IGNORECASE)
            want_re = {"$regex": want_like, '$options': '-i'}
            query_string .append({'updates':{"$elemMatch":{'status':want_re,"deleted":0}}})


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            keyword_re = {"$regex": keyword_like, '$options': '-i'}
            query_string .append({'updates':{"$elemMatch":{'status':keyword_re,"deleted":0}}})
        if self.user_type != "all":
            sign_up_as = "Business" if self.user_type == "Companies" else "Individual"
            query_string.append({"sign_up_as":sign_up_as})



        query_string.append({"$nor":[{"$exists": False},{"updates": { "$size": 0 }}]})
        pipeline = []
        geo_search = {"near": [float(self.lng), float(self.lat)],
                                    "distanceField": "distance",
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,
                                    "spherical":True,
                                    "limit":50,
        }

        



        if len(query_string)>0:
            geo_search['query'] = query_string


        geo_search['maxDistance'] = self.max_distance
        
        geo_near = {
                        "$geoNear": geo_search
                      }


        pipeline.append(geo_near)


        pipeline.append({"$project":{"updates":1,filter_type:1,"_id":0}})
        pipeline.append({"$unwind":"$updates"})
        and_query = [{"updates.deleted":0}]

        if self.keyword !="":
            and_query.append({"updates.status":keyword_re})
        if self.want!="all":
            and_query.append({"updates.status":want_re})

        pipeline.append({"$match":{"$and":and_query}})

        pipeline.append({"$project":{filter_type:1,"_id":0}})

        pipeline.append({"$unwind":"$"+filter_type})

        pipeline.append({"$group": { "_id": "$"+filter_type, "count": { "$sum":1} }})
        pipeline.append({"$sort": SON([("count", -1), ("_id", -1)])})
        agg = self.db.aggregate(pipeline)

        pipeline.append({"$limit":self.result_limit})
        return self.db.aggregate(pipeline)['result']
        
    

    def get_market_filters(self):
        org_filter = self.get_filters("org")
        biz_filter = self.get_filters('biz')

        return {"result":{"org":org_filter,"biz":biz_filter}, "total":200,"center":[float(self.lng), float(self.lat)]}
