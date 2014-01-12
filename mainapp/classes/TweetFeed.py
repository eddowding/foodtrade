from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
from pygeocoder import Geocoder
from bson.code import Code
from bson import BSON
from bson import json_util

from twython import Twython
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
import json
from pymongo import Connection

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''


import json
class TweetFeed():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tweets'
        self.db_object.create_table(self.table_name,'parent_tweet_id')
        self.db_object.ensure_index(self.table_name,'location')
    
    def get_tweet_by_id(self,tweet_id):
        return self.db_object.get_one(self.table_name,{'tweet_id':tweet_id, 'deleted':0})

    def get_tweet_by_parent_id(self, parent_tweet_id):
        return self.db_object.get_all(self.table_name,{'parent_tweet_id':parent_tweet_id, 'deleted':0}, 'time_stamp')

    def delete_tweet(self, tweet_id):
        self.db_object.update(self.table_name,{'_id':ObjectId(tweet_id)}, {'deleted':1})

    def get_tweet_by_user_id(self, user_id):
        return self.db_object.get_all(self.table_name,{'user_id':tweet_id, 'deleted':0}, 'time_stamp')

    def search_tweets(self, query):
        return self.db_object.get_all(self.table_name, query, 'time_stamp')

    def insert_tweet(self, value):
        value['deleted'] =0
        value['time_stamp'] = int(time.time())
        self.db_object.insert_one(self.table_name,value)
        
    def get_tweet_by_user_ids(self, user_ids):
        return self.db_object.get_all(self.table_name,{"user_id": {"$in": user_ids},'deleted':0}, 'time_stamp')    

    def get_trending_hashtags(self, start_time_stamp, end_time_stamp):
        mapper = Code("""
            function () {
             items = this.status.split(' ');
             for(i=0;i<items.length;i++){ 
                if(items[i].indexOf('#')!=0){
                        emit(items[i], 1); 
                        }
                    }
            }
            """)

        reducer = Code("""
            function (key, values) { 
             var sum = 0;
             for (var i =0; i<values.length; i++){
                    sum = sum + parseInt(values[i]);
             }
             return sum;
            }
            """)
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query = { 'time_stamp':{'$gte': start_time_stamp,'$lte': end_time_stamp}})
        

    def aggregrate(self, conditions):
        return self.db_object.aggregrate_all(self.table_name,conditions)

    def get_near_people(self, query):
        return self.db_object.get_distinct(self.table_name,'user.username',query)['count']

    def get_search_results(self, keyword, lon, lat, food_filter, type_filter, organisation_filter, query):
        mapper = Code("""
            function () {
            if(this.foods)
            {
            var foods = this.foods;
            }
            else
            {
            var foods = [];
            }
            if(this.type_user)
            {
            var user_types = this.type_user;
            }
            else
            {
            var user_types = [];
            }
            
            
            var filtered = false;
            var food_filter = """+json.dumps(food_filter)+""";
            var type_filter = """+json.dumps(type_filter)+""";
            var organisation_filter = """+json.dumps(organisation_filter)+""";
            var food_filtered = true;
            var filtered = true;
            for(var i=0;i<food_filter.length;i++)
            {   
                if(foods.indexOf(food_filter[i])==-1)
                {

                    food_filtered = false;
                    break;
                   
                }
            }
            var business_filtered = true;
            for(var i=0;i<type_filter.length; i++)
            {
                if(user_types.indexOf(type_filter[i])==-1)
                {
                    business_filtered = false;
                    break;
                    
                }

            }

            var organisation_filtered = true;

            for(var i=0;i<organisation_filter.length;i++)
            {
                if(user_types.indexOf(organisation_filter[i])==-1)
                {
                   organisation_filtered = false;
                   break;
                }
            }
            if(organisation_filtered && business_filtered && food_filtered)
            {
                filtered = true;
            }
            var flag = true;
            var keyword = '"""+keyword+"""';

            if(keyword != '')
            {
                flag = false;
                var scope_string ='';
                if(this.sign_up_as == 'Business'){
                scope_string = foods.join();
                scope_string += user_types.join();
                }
                scope_string += this.user.username;
                scope_string += this.user.name;
                scope_string += this.sign_up_as;
                scope_string += this.status;
                scope_string += this.user.description;
                scope_string = scope_string.toLowerCase();
               
               if(scope_string.indexOf(keyword.toLowerCase()) !=-1)
               {
                     
                    flag = true;

                }
               }

               if(filtered && flag)
               {
               var lon1 = parseFloat("""+str(lon)+""");
               var lat1 = parseFloat("""+str(lat)+""");
               var lon2 = this.location.coordinates[0];
               var lat2 = this.location.coordinates[1];
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
              emit(this._id, d);
              }
                           


            }
            """)

        reducer = Code("""
            function (key, values) { 
             
             return values[0];
            }
            """)
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query, 1)
        

    def get_all_foods(self, keyword, lon, lat, food_filter, type_filter, organisation_filter, query):
        mapper = Code("""
            function () {
            var foods = this.foods;
            var user_types = this.type_user;
            var filtered = true;
            

            var flag = true;
            var keyword = '"""+keyword+"""';

            if(keyword != '')
            {
                flag = false;
                var scope_string ='';
                
                scope_string += this.user.username;
                scope_string += this.user.name;
                scope_string += this.sign_up_as;
                scope_string += this.status;
                scope_string += this.user.description;
                scope_string = scope_string.toLowerCase();
               
               if(scope_string.indexOf(keyword.toLowerCase()) !=-1)
               {
                     
                    flag = true;

                }
               }

               if(filtered && flag && foods)
               {
               for(var i =0; i<foods.length;i++)
               {
                    emit(foods[i], 1);
               }
               
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
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query, -1)

    def get_all_businesses(self, keyword, lon, lat, food_filter, type_filter, organisation_filter, query):
        mapper = Code("""
            function () {
            var foods = this.foods;
            var user_types = this.type_user;
            var filtered = true;
            

            var flag = true;
            var keyword = '"""+keyword+"""';

            if(keyword != '')
            {
                flag = false;
                var scope_string ='';
                
                scope_string += this.user.username;
                scope_string += this.user.name;
                scope_string += this.sign_up_as;
                scope_string += this.status;
                scope_string += this.user.description;
                scope_string = scope_string.toLowerCase();
               
               if(scope_string.indexOf(keyword.toLowerCase()) !=-1)
               {
                     
                    flag = true;

                }
               }

               if(filtered && flag && user_types)
               {
               for(var i =0; i<user_types.length;i++)
               {
                    emit(user_types[i], 1);
               }
               
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
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query, -1)


    # def get_all_foods(self, keyword, lon, lat, food_filter, type_filter, organisation_filter, query):
    #     mapper = Code("""
    #         function () {
    #         var foods = this.foods;
    #         var user_types = this.type_user;
    #         var filtered = true;
    #         var food_filter = """+json.dumps(food_filter)+""";
    #         var type_filter = """+json.dumps(type_filter)+""";
    #         var organisation_filter = """+json.dumps(organisation_filter)+""";
    #         for(var i=0;i<food_filter.length && filtered;i++)
    #         {
    #             if(foods.indexOf(food_filter[i])<0)
    #             {
    #                 filtered = false;
    #             }
    #         }
            
    #         for(var i=0;i<type_filter.length && filtered;i++)
    #         {
    #             if(user_types.indexOf(type_filter[i])<0)
    #             {
    #                 filtered = false;
    #             }
    #         }



    #         for(var i=0;i<organisation_filter.length && filtered;i++)
    #         {
    #             if(user_types.indexOf(organisation_filter[i])<0)
    #             {
    #                 filtered = false;
    #             }
    #         }

    #         var flag = true;
    #         var keyword = '"""+keyword+"""';

    #         if(keyword != '')
    #         {
    #             flag = false;
    #             var scope_string ='';
                
    #             scope_string += this.user.username;
    #             scope_string += this.user.name;
    #             scope_string += this.sign_up_as;
    #             scope_string += this.status;
    #             scope_string += this.user.description;
    #             scope_string = scope_string.toLowerCase();
               
    #            if(scope_string.indexOf(keyword.toLowerCase()) !=-1)
    #            {
                     
    #                 flag = true;

    #             }
    #            }

    #            if(filtered && flag && foods)
    #            {
    #            for(var i =0; i<foods.length;i++)
    #            {
    #                 emit(foods[i], 1);
    #            }
               
    #           }
                           


    #         }
    #         """)

    #     reducer = Code("""
    #         function (key, values) { 
    #         var  sum = 0
    #          for(var i=0;i<values.length;i++)
    #          { sum += 1;}
    #          return sum;
    #         }
    #         """)
    #     return self.db_object.map_reduce(self.table_name, mapper, reducer, query, 1)

    def update_tweets(self, username, first_name, last_name, description, zip_code):
        try:
            results = Geocoder.geocode(zip_code)
            lon = results[0].longitude
            lat = results[0].latitude
        except:
            results = Geocoder.geocode('sp5 1nr')
            lon = results[0].longitude
            lat = results[0].latitude

        return self.db_object.update(self.table_name,
            {'user.username':username}, 
            {
                'user.name':str(first_name + ' ' + last_name),
                'user.Description':description, 
                'location.coordinates':[lat, lon]
            })

        
    def get_friends(self, user_id, next_cursor):
        st = SocialToken.objects.get(account__user__id=user_id)
        access_token = st.token
        access_token_secret = st.token_secret        
        sa = SocialAccount.objects.get(user__id = user_id)
        screen_name = sa.extra_data['screen_name']
        twitter = Twython(
        app_key = consumer_key,
        app_secret = consumer_secret,
        oauth_token = access_token,
        oauth_token_secret = access_token_secret
        )
        friends = twitter.get_friends_list(screen_name = screen_name, count=200, cursor = next_cursor)
        return friends

    def get_followers(self, twitter_id):
        pass


class UserProfile():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')
  
    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': user_id})

    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'type':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)

    def update_profile(self, userid, zipcode, type_usr, sign_up_as, phone):
        print phone
        return self.db_object.update(self.table_name,
             {'useruid':str(userid)},
             {'zip_code':zipcode,'type_user':type_usr,'sign_up_as':sign_up_as, 'phone_number':str(phone)}
             )


class TradeConnection():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tradeconnection'
        self.db_object.create_table(self.table_name,'b_useruid')
    def get_connection_by_business(self,b_useruid):
        return self.db_object.get_all(self.table_name,{'b_useruid': b_useruid, 'deleted': 0})

    def get_connection_by_customer(self, c_useruid):
        return self.db_object.get_all(self.table_name,{'c_useruid':c_useruid, 'deleted': 0})

    def create_connection (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_connection(self, b_useruid, c_useruid):
        self.db_object.update(self.table_name,{'b_useruid': b_useruid, 'c_useruid': c_useruid}, {'deleted':1})

class Food():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'food'
        self.db_object.create_table(self.table_name,'food_name')
    def get_foods_by_userid(self,useruid):
        return self.db_object.get_all(self.table_name,{'useruid': useruid, 'deleted': 0})

    def get_all_foods(self, key, condition, initial, reducer):
        return self.db_object.group(self.table_name,key, condition, initial, reducer)


    def create_food (self, value):
        value['deleted'] =0
        # self.db_object.insert_one(self.table_name,value)
        self.db_object.update_upsert(self.table_name, {'food_name': value['food_name']}, {'deleted': 0, 'useruid': value['useruid']})

    def delete_food(self, useruid, food_name):
        self.db_object.update(self.table_name,{'useruid': useruid, 'food_name': food_name}, {'deleted':1})

class Customer():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'customer'
        self.db_object.create_table(self.table_name,'useruid')

    def get_customers_by_userid(self,useruid):
        return self.db_object.get_all(self.table_name,{'useruid': useruid, 'deleted': 0})

    def create_customer (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_customer(self, useruid, customer_id):
        self.db_object.update(self.table_name,{'useruid': useruid, 'customeruid': customer_id}, {'deleted':1})

class Organisation():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'organisation'
        self.db_object.create_table(self.table_name,'orguid')

    def get_members_by_orgid(self,orguid):
        return self.db_object.get_all(self.table_name,{'orguid': orguid, 'deleted': 0})

    def create_member (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_member(self, orguid, member_id):
        self.db_object.update(self.table_name,{'orguid': orguid, 'memberuid': member_id}, {'deleted':1})

    def get_organisations_by_mem_id(self, member_id):
        return self.db_object.get_all(self.table_name,{'memberuid': member_id, 'deleted': 0})

class Team():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'team'
        self.db_object.create_table(self.table_name,'orguid')

    def get_members_by_orgid(self,orguid):
        return self.db_object.get_all(self.table_name,{'orguid': orguid, 'deleted': 0})

    def create_member (self, value):
        value['deleted'] =0
        self.db_object.insert_one(self.table_name,value)

    def delete_member(self, orguid, member_id):
        self.db_object.update(self.table_name,{'orguid': orguid, 'memberuid': member_id}, {'deleted':1})

class RecommendFood():
    """docstring for Connection"""
    def __init__(self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'recommendfood'
        self.db_object.create_table(self.table_name,'food_name')


    def get_recomm(self,business_id, food_name):
        return self.db_object.get_all(self.table_name,{'food_name': food_name, 'business_id': business_id, 'deleted': 0})

    def create_recomm(self, value):
        value['deleted'] =0
        # self.db_object.insert_one(self.table_name,value)
        self.db_object.update_upsert(self.table_name, {'food_name': value['food_name'], 'business_id': value['business_id'], 'recommender_id': value['recommender_id']}, {'deleted': 0})

    def delete_recomm(self, business_id, food_name, recommender_id):
        self.db_object.update(self.table_name,{'business_id': business_id, 'food_name': food_name, 'recommender_id': recommender_id}, {'deleted':1})

class Friends():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'friends'
        self.db_object.create_table(self.table_name,'username')

    def save_friends(self,doc):
        return self.db_object.insert_one(self.table_name,doc)

    def get_friends(self, username):    
        all_doc = self.db_object.get_all_vals(self.table_name,{'username':str(username)})
        return all_doc

class Invites():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'invites'
        self.db_object.create_table(self.table_name,'username')

    def save_invites(self,doc):
        return self.db_object.insert_one(self.table_name,doc)

    def check_invitees(self, screen_name):
        return self.db_object.get_all(self.table_name, {'to':'@'+screen_name})

class Notification():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'notification'
        self.db_object.create_table(self.table_name,'to_username')

    def save_notification(self,doc):
        return self.db_object.insert_one(self.table_name,doc)

    def change_notification_status(self, notification_to):
        return self.db_object.update(self.table_name, 
            {'notification_to':notification_to}, 
            {'notification_view_status':'true'})

    def get_notification(self,username):
        notification_count = len(self.db_object.get_all_vals(self.table_name,
            {'notification_to':username, 'notification_view_status':'false'}))
        return HttpResponse(json.dumps({'notification_count':notification_count, 
            'notifications':self.db_object.get_all_vals(self.table_name,
            {'notification_to':username,'notification_view_status':'false'})}))


class TwitterError():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'twittererror'
        self.db_object.create_table(self.table_name,'screen_name')    

    def save_error(self, doc):
        return self.db_object.insert_one(self.table_name,doc)

    def get_error(self, screen_name):
        return self.db_object.get_all_vals(self.table_name,{'screen_name':screen_name, 'error_solve_stat':'false'})   

    def change_error_status(self, screen_name):
        return self.db_object.update(self.table_name, {'screen_name':screen_name}, {'error_solve_stat':'true'})
