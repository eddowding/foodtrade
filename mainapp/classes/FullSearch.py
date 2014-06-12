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


def get_request(request):
    search_request = {}
    search_request['keyword'] = request.POST.get("q",request.GET.get("q","")) 


    # location_res = Geocoder.geocode(self.location)
    # self.lon = float(location_res.longitude)
    # self.lat = float(location_res.latitude)



    ### Todo do task get logged in user's location and latlng info from db 
    default_location = "Bristol, London"
    default_lng = -2.321
    default_lat = 54.12

    ########################################################################
    search_request['location'] = request.POST.get("location",request.GET.get("location",default_location))

    search_request['lng'] = float(request.POST.get("lng",request.GET.get("lng",default_lng)))
    search_request['lat'] = float(request.POST.get("lat",request.GET.get("lat",default_lat)))
    search_request['search_for'] = request.POST.get("search",request.GET.get("search","food")) 
    search_request['indiv_biz'] = request.POST.get("only",request.GET.get("only","Business")) 
    search_request['biz_type_filters'] = request.POST.get("biz",request.GET.get("biz","[]")) 
    search_request['org_filters'] = request.POST.get("org",request.GET.get("org","[]")) 
    search_request['food_filters'] = request.POST.get("food",request.GET.get("food","[]")) 
    return search_request

    

class GeneralSearch():

    def __init__(self,request):
        db_object = MongoConnection("localhost",27017,'foodtrade')
        table_name = 'userprofile'
        db_object.create_table(table_name,'useruid')
        db_object.ensure_index(table_name,'latlng')

        db_object.create_table(table_name,'username')

        self.db = db_object.get_db()[table_name]



        params = get_request(request)

        self.keyword = params['keyword']
        self.search_for = params['search_for']
        self.location = params['location']

        self.lat = params['lat']
        self.lng = params['lng']
        self.indiv_biz = params['indiv_biz']
        self.org_filters = json.loads(params['org_filters'])
        self.biz_type_filters = json.loads(params['biz_type_filters'])
        self.food_filters = json.loads(params['food_filters'])
        self.radius = 160900000




    def get_result(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []


        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}

            if self.search_for != "food":
                search_variables = ["business_org_name", "name", "description", "username", "nick_name"]
            
                
                for search_item in search_variables:
                    or_conditions.append({search_item:reg_expression})
            # Searches keyword as food
            else:
                food_attributes = ["food_name","description","food_tags"]

                for fd_attr in food_attributes:

                    or_conditions.append({'foods':{"$elemMatch":{fd_attr:reg_expression}}})

            if self.search_for != "food":
                or_conditions.append({'type_user':reg_expression})
        
        and_query =[]

        pre_condition = {"sign_up_as":{"$ne":"unclaimed"}}

        and_query.append(pre_condition)


   

        # check food filters
        foods_match = []
        for fd in self.food_filters:
            foods_match.append({ "$elemMatch" : { "food_name": fd}})
        if len(self.food_filters) > 0:
            and_query.append({"foods": {"$all":foods_match}})
        
        # Check business filter
        if len(self.biz_type_filters) > 0:
            and_query.append({"type_user":{"$all":self.business}})
        
        # Check organisation filter
        if len(self.org_filters) > 0:
            and_query.append({"organisations":{"$all":self.orz_filters}})

        if len(and_query)>0:
            query_string["$and"] = and_query
        if self.keyword !="":
            query_string["$or"] = or_conditions


        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(self.lng), float(self.lat)] },
            "$maxDistance" : self.radius
          }}

        all_doc = self.db.find(query_string,{"latlng":1,"name":1,"user_type":1,"sign_up_as":1,"description":1,"profile_img":1,"foods":1,"username":1,"_id":0})
        total =  all_doc.count()
        first20 = all_doc.limit(20)
        result = [doc for doc in first20]
       
        for i in range(0,len(result)):
            distance= calc_distance(self.lat, 
                self.lng, 
                result[i]['latlng']['coordinates'][1],
                result[i]['latlng']['coordinates'][0])
            # print distance

            result[i]['distance']  = distance
        
        return_val = {"result":result, "total":total,"center":[float(self.lng), float(self.lat)]}

        return return_val

import math

def calc_distance(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6371000


    