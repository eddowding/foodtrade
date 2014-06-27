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

    

class ProfileSearch(GeneralSearch):




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
            query_string.append({"sign_up_as":sign_up_as})
        pipeline = []
        if len(query_string)>0:
            pipeline.append({"$match":{"$and":query_string}})


        pipeline.append({"$project":{"username":1, "description":1,"type_user":1, "sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0}})
        pipeline.append({"$unwind":"$updates"})
        and_query = [{"updates.deleted":0}]
        if self.keyword !="":
            and_query.append({"updates.status":keyword_re})
        if self.want!="all":
            and_query.append({"updates.status":want_re})
        pipeline.append({"$match":{"$and":and_query}})

        pipeline.append({"$sort": SON([("updates.time_stamp", -1)])})
        pipeline.append({"$limit":20})
        agg = self.db.aggregate(pipeline)['result']
        return {"result":agg, "total":200,"center":[float(self.lng), float(self.lat)]}


    def get_single_tweet(self,tweet_id):
        query_string = {'updates':{"$elemMatch":{'tweet_id':tweet_id,"deleted":0}}}
        pipeline = []
        pipeline.append({"$match":query_string})
        pipeline.append({"$project":{"username":1, "description":1,"type_user":1, "sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0}})
        pipeline.append({"$unwind":"$updates"})
        pipeline.append({"$match":{"updates.tweet_id":tweet_id}})
        result = self.db.aggregate(pipeline)['result']
        parameter = {"status":"error"}


        if(len(result)>0):
            distance = self.calc_distance(result[0]['latlng']['coordinates'][1],result[0]['latlng']['coordinates'][0])
            print distance
            if(distance<50):
                parameter['status'] = "ok"
                parameter['result'] = result[0]
        return parameter

    def get_filters(self,ftype):
        query_string = self.get_query_string()
        if ftype == "biz":
            filter_type = "type_user"
        else:
            filter_type = "organisations"
        pipeline = []


        geo_search = {"near": [float(self.lng), float(self.lat)],
                                    "distanceField": "distance",
                                    "includeLocs": "latlng",
                                    "uniqueDocs": True,
                                    "spherical":True,
                                    "limit":100,
        }

        



        if len(query_string)>0:
            geo_search['query'] = query_string


        geo_search['maxDistance'] = 0.425260398681
        
        geo_near = {
                        "$geoNear": geo_search
                      }


        pipeline.append(geo_near)



        pipeline.append({"$project":{"updates":1,filter_type:1,"_id":0}})
        

        pipeline.append({"$project":{filter_type:1,"_id":0}})

        pipeline.append({"$unwind":"$"+filter_type})

        pipeline.append({"$group": { "_id": "$"+filter_type, "count": { "$sum":1} }})
        pipeline.append({"$sort": SON([("count", -1), ("_id", -1)])})
        agg = self.db.aggregate(pipeline)

        pipeline.append({"$limit":100})
        return self.db.aggregate(pipeline)['result']
        
    

    def get_profile_filters(self):
        org_filter = self.get_filters("org")
        biz_filter = self.get_filters('biz')

        return {"result":{"org":org_filter,"biz":biz_filter}, "total":200,"center":[float(self.lng), float(self.lat)]}
