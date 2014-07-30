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
from TweetFeed import UserProfile
import math
from mainapp.geolocation import get_addr_from_ip
from mainapp.classes.Foods import AdminFoods
from mainapp.classes.TweetFeed import UserProfile

class GeneralSearch():

    def __init__(self,request):
        db_object = MongoConnection("localhost",27017,'foodtrade')
        table_name = 'userprofile'
        db_object.create_table(table_name,'useruid')
        db_object.ensure_index(table_name,'latlng')
        db_object.create_table(table_name,'foods.food_name')
        db_object.create_table(table_name,'updates.status')
        db_object.create_table(table_name,'username')
        self.db = db_object.get_db()[table_name]

        params = self.get_request(request)
        self.keyword = params['keyword']
        self.search_for = params['search_for']
        self.location = params['location']

        self.lat = params['lat']
        self.lng = params['lng']

        self.want = params['want']
        self.user_type = params['usertype']
        self.org_filters = json.loads(params['org'])
        self.biz_type_filters = json.loads(params['biz'])
        self.food_filters = json.loads(params['food_filters'])
        self.distance_limit = 300
        self.result_limit = 20
        

        

        if request.user.is_authenticated():

            self.user = params['up']
            try:
                

                ## make all super user subscribed permission
                if request.user.is_superuser:
                    self.user['subscribed'] = 1

                if self.user['subscribed'] == 1:
                    self.result_limit = 20
                    self.distance_limit = 50
            except:
                pass

        self.radius = self.distance_limit*1609.34
        self.max_distance = self.distance_limit/3963.1676


    def get_request(self,request):
        search_request = {}
        search_request['keyword'] = request.POST.get("q",request.GET.get("q","")) 
        if request.user.is_authenticated():


            up_object = UserProfile()
            up = up_object.get_profile_by_id(request.user.id)

            default_location = up['address']
            default_lng = up['latlng']['coordinates'][0]
            default_lat = up['latlng']['coordinates'][1]

            search_request['up'] = up
        
        else:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]

            else:
                ip = request.META.get('REMOTE_ADDR')
            location_info = get_addr_from_ip(ip)
            default_lng = float(location_info['longitude'])
            default_lat = float(location_info['latitude'])
            default_location = "unknown"

        search_request['location'] = request.POST.get("location",request.GET.get("location",default_location))

        search_request['lng'] = float(request.POST.get("lng",request.GET.get("lng",default_lng)))
        search_request['lat'] = float(request.POST.get("lat",request.GET.get("lat",default_lat)))

        search_request['want'] = request.POST.get("want",request.GET.get("want","all"))
        search_request['search_for'] = request.POST.get("search_type",request.GET.get("search_type","produce")) 
        search_request['usertype'] = request.POST.get("usertype",request.GET.get("usertype","all")) 
        search_request['biz'] = request.POST.get("biz",request.GET.get("biz","[]"))

        search_request['org'] = request.POST.get("org",request.GET.get("org","[]"))

        print "after_loads",type(search_request['org'])
        search_request['food_filters'] = request.POST.get("food",request.GET.get("food","[]")) 
        return search_request


    def get_latest_updates(self, time_stamp=None):
        query_string = {}
        agg_pipeline = []
        or_conditions = []

        
        pipeline = []
        pre_match = {}
        if time_stamp!=None:
            pre_match = {'updates':{"$elemMatch":{'time_stamp':{"$gt":int(time_stamp)},"deleted":0}}}
            post_match = {'updates.time_stamp':{"$gt":int(time_stamp)},"updates.deleted":0}
        else:
            time_stamp = int(time.time()) - 30*24*3600
            pre_match = {'updates':{"$elemMatch":{'time_stamp':{"$gt":int(time_stamp)},"deleted":0}}}
            post_match = {'updates.time_stamp':{"$gt":int(time_stamp)},"updates.deleted":0}



        if self.user['sign_up_as'] == "Individual":
            pre_match['sign_up_as'] = "Individual"
        else:
            pre_match['sign_up_as'] = {"$ne":"Individual"}
        
        pipeline.append({"$match":pre_match})
        pipeline.append({"$project":{"username":1,"name":1,"updates":1,"profile_img":1,"_id":0}})
        





        pipeline.append({"$unwind":"$updates"})

        if time_stamp!=None:
            pipeline.append({"$match":post_match})

        pipeline.append({"$sort": SON([("updates.time_stamp", -1)])})
        pipeline.append({"$limit":10})
        final_result = self.db.aggregate(pipeline)['result']
        params= {}
        for result in final_result:
            result['updates']['status'] = self.recognise_name(result['updates']['status'])

        params['result'] = final_result
        params['status'] = "ok"
        if len(final_result) > 0:
            params['time'] = final_result[0]['updates']['time_stamp']
        return params

    def get_query_string(self):
        query_string = {}
        agg_pipeline = []
        or_conditions = []


        # Check if keyword is not empty
        if self.keyword !="":
            keyword_like = re.compile(self.keyword + '+', re.IGNORECASE)
            reg_expression = {"$regex": keyword_like, '$options': '-i'}


        #### Profile Search ######
            if self.search_for != "produce":
                search_variables = ["business_org_name", "name", "description", "username", "nick_name"]
            
                
                for search_item in search_variables:
                    or_conditions.append({search_item:reg_expression})

                or_conditions.append({"type_user":reg_expression})
        ####### Searches keyword as food

            else:
                food_attributes = ["food_name","description","food_tags"]
                we_buy = 3
                if self.want!="all":
                    if self.want == "Sell":
                        we_buy = 1
                    if self.want == "Buy":
                        we_buy = 0

                print "help", we_buy
                for fd_attr in food_attributes:

                    or_conditions.append({'foods':{"$elemMatch":{fd_attr:reg_expression, "webuy":{"$ne":we_buy}}}})
        
        and_query =[]

        pre_condition = {"sign_up_as":{"$ne":"unclaimed"}}

        and_query.append(pre_condition)

   




        if self.user_type != "all":
            sign_up_as = "Business" if self.user_type == "Companies" else "Individual"
            
            and_query.append({"sign_up_as":sign_up_as})
        

        if len(self.biz_type_filters) > 0:
            and_query.append({"type_user":{"$all":self.biz_type_filters}})
        
        # Check organisation filter
        if len(self.org_filters) > 0:
            and_query.append({"organisations":{"$all":self.org_filters}})




        # ######################### Food filters ################
        # foods_match = []
        # for fd in self.food_filters:
        #     foods_match.append({ "$elemMatch" : { "food_name": fd}})

        # if len(self.food_filters) > 0:
        #     and_query.append({"foods": {"$all":foods_match}})
        
   



        if len(and_query)>0:
            query_string["$and"] = and_query
        if self.keyword !="":
            query_string["$or"] = or_conditions
        return query_string

    def get_result(self):
        query_string = self.get_query_string()


        # pipeline = []
        # pipeline.append({"$match":query_string})
        # pipeline.append({"$project":{"foods":1,"_id":0}})
        # pipeline.append({"$unwind":"$foods"})
        # pipeline.append({"$project":{"name":"$foods.food_name", "count":"$foods.food_name"}})

        # pipeline.append({"$group": { "_id": "$name", "count": { "$sum":1} }})
        # pipeline.append({"$sort": SON([("count", -1), ("_id", -1)])})
        # agg = self.db.aggregate(pipeline)
        

        query_string["latlng"]= {"$near": {
            "$geometry" : { "type" : "Point" , "coordinates": [float(self.lng), float(self.lat)] },
            "$maxDistance" : self.radius
          }}

        all_doc = self.db.find(query_string,{"latlng":1,"name":1,"type_user":1,"address":1,"foods":1,"sign_up_as":1,"description":1,"profile_img":1,"foods":1,"username":1,"_id":0})
        total =  all_doc.count()
        first20 = all_doc.limit(self.result_limit)
        result = [doc for doc in first20]
        for i in range(0,len(result)):
            distance= self.calc_distance(
                result[i]['latlng']['coordinates'][1],
                result[i]['latlng']['coordinates'][0])
            webuy_count = 0
            wesell_count = 0
            webuy_matches = []
            wesell_matches = []
            for fd in result[i]['foods']:
                if self.keyword.lower() in fd['food_name'].lower() and self.search_for == "produce" and self.keyword != "":
                    matched = True
                else:
                    matched = False
                try:
                    if fd['webuy']==0:
                        wesell_count = wesell_count +1
                        if matched:
                            wesell_matches.append(fd['food_name'])

                        if (self.search_for != "produce" or self.keyword == "") and wesell_count == 1:
                            wesell_matches.append(fd['food_name'])

                    else:
                        webuy_count = webuy_count + 1
                        if matched:
                            webuy_matches.append(fd['food_name'])
                        if (self.search_for != "produce" or self.keyword == "") and webuy_count == 1:
                            webuy_matches.append(fd['food_name'])
                else:
                    continue
                    



            result[i]['foods'] = {"webuy_count":webuy_count, "webuy_matches":webuy_matches, "wesell_count":wesell_count,"wesell_matches":wesell_matches}

            result[i]['distance']  = '%.1f' % distance
        
        return_val = {"result":result, "total":total,"center":[float(self.lng), float(self.lat)]}


        
        return return_val

    def recognise_name(self,value):
        value = value.encode('utf-8').strip()
        result = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)', value, re.M|re.I)
        tags = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z_]+[A-Za-z0-9]+)', value, re.M|re.I)
        links = re.findall("((http:|https:)//[^ \<]*[^ \<\.])",value)
        if links:
            for each_link in links:
                value = value.replace(str(each_link[0]), '<a href="'+str(each_link[0])+'" target="_blank">'+ str(each_link[0]) + '</a>')
        if tags:
            for each_tag in tags:
                value = value.replace("#"+each_tag, '<a href="/activity/?q=%23'+each_tag+'&tab=market&stype=produce&pwant=all">#'+each_tag+'</a>')
        if result:
            user_prof = UserProfile()
            for each in result:
                try:
                    # usr = User.objects.get(username = str(each))
                    usr_pr = user_prof.get_profile_by_username(each)
                    if usr_pr['sign_up_as'] != 'unclaimed':
                        value = value.replace("@"+each, '<a href="/'+each+'/">@'+each+'</a>')
                except:
                    pass


        admin_foods = AdminFoods()
        master_foods = admin_foods.get_tags()
        #create master list of foods
        final_master = []
        for each in master_foods:
            if each.get('childrens')!=None:
                final_master.extend([str(i['node']).lower() for i in each['childrens']])
            else:
                final_master.extend([str(each['node']).lower()])

        val_list = value.split()
        for each in val_list:
            if each.lower() in final_master:
                value = value.replace(each, '<a href="/activity/?f='+each.title()+'">'+each+'</a>')
        return value



    def calc_distance(self,lat2, lon2):
        try:
            lat1 = self.user['latlng']['coordinates'][1]
            lon1 = self.user['latlng']['coordinates'][0]
        except:
            lat1 = self.lat
            lon1 = self.lng
        from math import sin, cos, sqrt, atan2, radians

        R = 3963.1676


        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)




        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance


    