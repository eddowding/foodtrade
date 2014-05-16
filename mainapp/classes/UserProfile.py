#!/usr/bin/env python
# encoding: utf-8

import re
from MongoConnection import MongoConnection
from bson.objectid import ObjectId
import time, datetime
from bson.code import Code
import os
import sys
from pygeocoder import Geocoder

CLASS_PATH = '/srv/www/live/foodtrade-env/foodtrade/mainapp/classes'
CRON_PATH = '/srv/www/live/foodtrade-env/foodtrade/CronJobs'
SETTINGS_PATH = '/srv/www/live/foodtrade-env/foodtrade/foodtrade'

# CLASS_PATH = 'C:/Users/Roshan Bhandari/Desktop/project repos/foodtrade/mainapp/classes'
# CRON_PATH = 'C:/Users/Roshan Bhandari/Desktop/project repos/foodtrade/CronJobs'
# SETTINGS_PATH = 'C:/Users/Roshan Bhandari/Desktop/project repos/foodtrade/foodtrade'

sys.path.insert(0, CLASS_PATH)
sys.path.insert(1,SETTINGS_PATH)
sys.path.insert(1,CRON_PATH)
from settingslocal import *
from MailchimpClass import MailChimp, MailChimpException

class UserProfile():
    def __init__ (self, host=REMOTE_SERVER_LITE, port=27017, db_name=REMOTE_MONGO_DBNAME, username=REMOTE_MONGO_USERNAME, password=REMOTE_MONGO_PASSWORD):        
        self.db_object = MongoConnection(host=host, port=port, db_name=db_name, username=username, password=password)
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name, 'useruid')

    def get_all_profiles(self, status):
        users = []
        if status == 'None':
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}})/15)+ 1
        else:
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':status})/15)+ 1
        for i in range(0,user_pages_count, 1):
            if status == 'None':
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}}, pageNumber = int(i+1))
            else:    
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':status}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)
        return users

    def register_all_profiles_to_mailchimp(self, status):
        users = []
        if status == 'None':
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}})/15)+ 1            
        else:
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':status})/15)+ 1
        for i in range(0,user_pages_count, 1):
            if status == 'None':
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}}, pageNumber = int(i+1))
            else:    
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':status}, pageNumber = int(i+1))
            for eachUser in pag_users:
                # import urllib2
                # m = urllib2.urlopen('http://ftstaging.cloudapp.net/mailchimp-migrate' + eachUser['username'] +'/')
                m = MailChimp()
                m.subscribe(eachUser)
                print eachUser['email'] + "subscribed"
        return users

    def get_all_users(self):
        users = []
        user_pages_count = int(self.db_object.get_count(self.table_name, {'is_unknown_profile':'false'})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'is_unknown_profile':'false'}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)                     
        return users

    def send_newsletter(self, substype):
        if substype == 'None':
            user_pages_count = int(self.db_object.get_count(self.table_name, 
              {'email':{'$ne':''},'newsletter_freq':{'$exists':False}})/15)+ 1
        else:  
            user_pages_count = int(self.db_object.get_count(self.table_name, 
              {'email':{'$ne':''},'newsletter_freq':{'$ne':'Never'},'newsletter_freq':str(substype)})/15)+ 1
        for i in range(0,user_pages_count, 1):
            if substype == 'None':
                pag_users = self.db_object.get_paginated_values(self.table_name,
                  {'email':{'$ne':''},'newsletter_freq':{'$exists':False}},pageNumber = int(i+1))
            else:              
                pag_users = self.db_object.get_paginated_values(self.table_name, 
                  {'email':{'$ne':''},'newsletter_freq':{'$ne':'Never'}, 'newsletter_freq':str(substype)},pageNumber = int(i+1))
            for eachUser in pag_users:
                if len(eachUser['email'])>0:
                    import urllib2
                    baseurl = "http://foodtrade.com/send-newsletter/" + str(substype.lower())+ "?username=" + str(eachUser['username']) + "&code=11foodtradeESRS22"
                    response = urllib2.urlopen(baseurl)
        return True

    def change_address(self, username, data):
        return self.db_object.update(self.table_name, {'username':username}, data)

    def geocode_and_update_address(self, username='', address=''):
        try:            
            data ={}
            location_res = Geocoder.geocode(address)
            data['address'] = str(location_res)
            data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude),float(location_res.latitude)]}
            data['zip_code'] = str(location_res.postal_code)
            self.db_object.update(self.table_name, {'screen_name':username,'username':username},data)
            return {'status':1}
        except:
            return {'status':0, 'message':'exception occured while geocoding'}

    def geocode_all_antartic_users(self):
        user_pages_count = int(self.db_object.get_count(self.table_name, {'address':'Antartica'})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'address':'Antartica'}, pageNumber = int(i+1))
            for eachUser in pag_users:
                self.geocode_and_update_address(eachUser['username'], eachUser['address'])
            time.sleep(5)
        return {'status':1}

    def get_minimum_id_of_user(self):
        return self.db_object.aggregrate_all(self.table_name, [ { '$group': { '_id':0, 'minId': { '$min': "$useruid"} } } ] )

    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': int(user_id)})

    def get_profile_by_profile_img(self, img):
        return self.db_object.get_one(self.table_name,{'profile_img': img})

    def get_profile_by_username(self, username):
        # return self.db_object.get_one(self.table_name,{'username': str(username)})
        return self.db_object.get_one(self.table_name,{'username': { "$regex" : re.compile("^"+str(username)+"$", re.IGNORECASE), "$options" : "-i" }})

    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'sign_up_as':type_usr})

    def get_all_friends_and_register_as_friend(self, start):
        maxtime = datetime.datetime.now() - datetime.timedelta(minutes=30)
        maxtime = int(time.mktime(maxtime.timetuple()))
        user_pages_count = int(self.db_object.get_count(self.table_name, {'join_time':{'$gt':start}, 'join_time':{'$lt':maxtime}, 'is_unknown_profile': 'false'}))
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'join_time':{'$gt':start}, 'join_time':{'$lt':maxtime}, 'is_unknown_profile': 'false'}, pageNumber = int(i+1))
            from friends import Friends                        
            for eachUser in pag_users:     
                friend_obj = Friends()
                friend_obj.process_friends_or_followers(eachUser, 'friends')
                friend_obj.process_friends_or_followers(eachUser, 'followers')
        return {'status':1}

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)

    def update_profile_fields(self, where, what):
        self.db_object.update(self.table_name, where, what)

    def subscribe(self, useruid):
        self.db_object.update(self.table_name, {"useruid":useruid}, {"subscribed":1})

    def update_profile(self, userid, description, address, type_usr, sign_up_as, phone, lat, lon, postal_code):
        return self.db_object.update(self.table_name,
             {'useruid':int(userid)},
             {'zip_code':str(postal_code),
             'description':str(description),
             'latlng.coordinates.1':float(lat),
             'latlng.coordinates.0':float(lon),
             'address':str(address),
             'type_user':type_usr,
             'sign_up_as':sign_up_as, 
             'phone_number':str(phone)}
             )

    def update_profile_by_username(self, username, description, address, type_usr, sign_up_as, phone, lat, lon, postal_code, name, is_superuser,
      company_num, website_url, facebook_page, deliverables, business_org_name, email, newsletter_freq, show_foods):

        data = {'zip_code':str(postal_code),
                 'description':description,
                 'latlng.coordinates.1':float(lat),
                 'latlng.coordinates.0':float(lon),
                 'address':str(address),
                 'type_user':type_usr,
                 'sign_up_as':sign_up_as, 
                 'phone_number':str(phone),
                 'name':name,
                 'company_num': company_num,
                 'website_url': website_url,
                 'facebook_page': facebook_page,
                 'deliverables': deliverables,
                 'business_org_name': business_org_name,
                 'email':email,
                 'newsletter_freq':newsletter_freq,
                 'show_foods': show_foods
                 }
        if not is_superuser: 
            return self.db_object.update(self.table_name,
                 {'username':username},
                 data)
        else:
            data['recently_updated_by_super_user'] = 'true'
            return self.db_object.update(self.table_name,
                 {'username':username},
                 data)

    def update_profile_upsert(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)

    def check_valid_email(self, username, email):
        user = self.db_object.get_one(self.table_name, {'username':username})
        new_email_user = self.db_object.get_one(self.table_name, {'email':email})
        if  new_email_user!= None:
            if user['email'] == email:
                return True
            return False
        else:
            return True

    def get_unclaimed_unedited_profile_count(self):
        return self.db_object.get_count(self.table_name, {'is_unknown_profile':'true', 'recently_updated_by_super_user':'false'})

    def get_unclaimed_edited_profile_count(self):
        return self.db_object.get_count(self.table_name, {'is_unknown_profile':'true', 'recently_updated_by_super_user':'true'})

    def get_unclaimed_profile_paginated(self, pagenum = 1, edit_value = 0):
        return self.db_object.get_paginated_values(self.table_name, 
            conditions = {'is_unknown_profile':'true','recently_updated_by_super_user':str(bool(edit_value)).lower()}, pageNumber = pagenum)

    def search_profiles(self):
        mapper = Code("""
            function () {
            
            var keyword = '"""+keyword+"""';
            keyword = keyword.toLowerCase();
            {"useruid": str(userid), "sign_up_as": sign_up_types[0],
                                          "type_user":str(','.join(type_user)),
                                            "zip_code": new_location[0], "address": new_location[3],
                                           "latitude": float(new_location[1]), "longitude": float(new_location[2]), 
                                           }
            
            var sign_up_as = this.sign_up_as.toLowerCase();
            var user_types = this.type_user.toLowerCase();
            var longitude = this.longitde;
            var latitude = this.latitude;


           
            var search_more = true;
            if(keyword == sign_up_as)
            {
                search_more = false;
            }

            var type_array = user_types.split();
            if(type_array.indexOf(keyword)!=-1)
            {
                search_more = false;
            }

            try
              {
               var user_name = this.username;

                        var name = this.name;

                        
                        var description = this.description;
                        if(user_name.indexOf(keyword) != -1 || name.indexOf(keyword) != -1 || description.indexOf(keyword) != -1 )
                        {
                            search_more = false;

                        }
              }
            catch(err)
              {
              
              }

            if(!search_more)
            {




              var lon1 = parseFloat("""+str(lon)+""");
               var lat1 = parseFloat("""+str(lat)+""");
               var lon2 = longitude;
               var lat2 = latitude;
               var R = 6371; // Radius of the earth in km
              var dLat = (lat2-lat1)* (Math.PI/180);  // deg2rad below
              var dLon = (lon2-lon1)* (Math.PI/180); 
              var a = 
                Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos((lat1)* (Math.PI/180)) * Math.cos((lat2)* (Math.PI/180)) * 
                Math.sin(dLon/2) * Math.sin(dLon/2)
                ; 
              var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
              var d = R * c; // Distance in km
              var ret_value =
              emit(this._id, d);
        }
                           


            }
            """)

        reducer = Code("""
            function (key, values) { 
            var  sum = 0
             for(var i=0;i<values.length;i++)
             { sum += 1;}
             return sum;
            }
            """)
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query, -1, 200)

    def calculate_trending_hashtags(self, start_time_stamp, end_time_stamp):
        query_str = """function () {for(var i = 0; i < this.updates.length; i++) {var current = this.updates[i];"""
        if start_time_stamp != "" and end_time_stamp != "":
            query_str = query_str + """if(current.deleted != 1 && current.time_stamp >= """ + str(time.mktime(start_time_stamp.timetuple())) + """ && current.time_stamp <= """ + str(time.mktime(end_time_stamp.timetuple())) + """ ){"""
        else:
            query_str = query_str + """if(current.deleted != 1){"""

        query_str = query_str + """
            items = current.status.split(' ');
            for(var j = 0; j < items.length; j++ ) {
                if(items[j].indexOf('#')==0){                        
                      var reg =  /\B#\w*[a-zA-Z]+\w*/g;
                      if (reg.test(items[j].toLowerCase())){
                        emit_text = items[j].toLowerCase();
                        emit_text.replace('?','');
                        emit(emit_text, 1);
                      }

                    }
                }
            }
            }}"""
        mapper = Code(query_str)
        reducer = Code("""
            function (key, values) { 
             var sum = 0;
             for (var i =0; i<values.length; i++){
                    sum = sum + parseInt(values[i]);
             }
             return parseInt(sum);
            }
            """)
        if start_time_stamp !="" and end_time_stamp !="":
            result = self.db_object.map_reduce(self.table_name, mapper, reducer,{}, result_table_name = 'trendingthisweek')[0:10]
        else:
            result = self.db_object.map_reduce(self.table_name, mapper, reducer,{},result_table_name = 'trendingalltime')[0:10]
        return result

'''
Please do not remove the code below. It is necessary during 
registering user to mailchimp by cron.
'''        
# us = UserProfile()
# us.register_all_profiles_to_mailchimp('Never')
'''ends'''