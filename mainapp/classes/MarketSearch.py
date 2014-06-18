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
        query_string = self.get_query_string()
        pipeline = []
        pipeline.append({"$match":query_string})
        pipeline.append({"$project":{"username":1, "description":1,"type_user":1, "sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0}})
        pipeline.append({"$unwind":"$updates"})
        pipeline.append({"$match":{"updates.deleted":0}})
        pipeline.append({"$sort": SON([("updates.time_stamp", -1)])})
        pipeline.append({"$limit":20})
        agg = self.db.aggregate(pipeline)['result']
        return {"result":agg, "total":200,"center":[float(self.lng), float(self.lat)]}


        

    