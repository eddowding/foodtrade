# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.geolocation import get_addr_from_ip
from mainapp.classes.TweetFeed import TweetFeed
from mainapp.classes.Email import Email
from Tags import Tags
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood
from Search import Search
import time
from mainapp.classes.DataConnector import UserInfo
from mainapp.single_activity import get_post_parameters
from mainapp.activity import get_search_parameters

from MongoConnection import MongoConnection

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'




class ConnectionMap():
    """docstring for AjaxHandle"""
    def __init__(self,request):
        ids_string = request.POST.get('ids')
        # ids_string_list = ids_string.split(',')
        # self.ids = []
        # for i in ids_string_list:
        #     self.ids.append(int(i))
        self.ids = json.loads(ids_string)



    def get_connection_network(self):
        db_object = MongoConnection("localhost",27017,'foodtrade')
        table_name = 'tradeconnection'
        # db_object.create_table(table_name,'useruid')
        # db_object.ensure_index(table_name,'latlng')
        # db_object.create_table(table_name,'foods.food_name')
        # db_object.create_table(table_name,'updates.status')
        # db_object.create_table(table_name,'username')
        self.db = db_object.get_db()[table_name]
        self.db1 = db_object.get_db()["userprofile"]



        # pipeline = []
        pipeline1 ={"$match":{"deleted":0,"$or":[{"b_useruid":{"$in":self.ids}},{"b_useruid":{"$in":self.ids}}]}}

        pipeline2 = {"$project":{"b_useruid":1, "c_useruid":1,"_id":0}}
        pipeline = [pipeline1, pipeline2]
        # pipeline = [pipeline1]
        # pipeline.append({"$limit":20})
        results = self.db.aggregate(pipeline)['result']
 
        # return

        unique_user_ids = []
        for usr in results:
            b_user = int(usr['b_useruid'])
            c_user = int(usr['c_useruid'])
            if b_user not in unique_user_ids:
                unique_user_ids.append(int(b_user))

            if c_user not in unique_user_ids:
                unique_user_ids.append(int(c_user))

        if len(unique_user_ids)==0:
            return HttpResponse("no result")
        print len(unique_user_ids)
        pipeline = []
        pipeline1 ={"$match":{"useruid":{"$in":unique_user_ids}}}
        pipeline2 = {"$project":{"useruid":1,"username":1, "description":1,"type_user":1, "sign_up_as":1,"latlng":1,"name":1,"updates":1,"profile_img":1,"_id":0}}
        pipeline = [pipeline1, pipeline2]

        results1 = self.db1.aggregate(pipeline)['result']
        user_dict = {}
        for result in results1:
            user_dict["user_"+str(int(result['useruid']))] = result

        ret_val = {"connections":results,"users":user_dict}
            
        return HttpResponse(json.dumps(ret_val))
        


