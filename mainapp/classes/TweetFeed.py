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
import re
from django.conf import settings
# from mainapp.views import get_twitter_obj
import json

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''


import json


def get_twitter_obj(token, secret):
    return Twython(
        app_key = settings.CONSUMER_KEY,
        app_secret = settings.CONSUMER_SECRET,
        oauth_token = token,
        oauth_token_secret = secret
        )


class TweetFeed():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')
        self.db_object.ensure_index(self.table_name,'latlng')
    
    def get_tweet_by_id(self,tweet_id):
        return self.db_object.get_one(self.table_name,{'tweet_id':tweet_id, 'deleted':0})

    def get_tweet_by_parent_id(self, parent_tweet_id):
        return self.db_object.get_all(self.table_name,{'parent_tweet_id':parent_tweet_id, 'deleted':0}, 'time_stamp')

    def delete_tweet(self, user_id,tweet_id):
        self.db_object.update( self.table_name, { "useruid":int(user_id), "updates.tweet_id": str(tweet_id) }, {"updates.$.deleted" : 1})

    def get_tweet_by_user_id(self, user_id):
        return self.db_object.get_one(self.table_name,{'useruid':int(user_id), 'updates':{"$elemMatch":{'deleted':0}}})

    def search_tweets(self, query):
        return self.db_object.get_all(self.table_name, query, 'time_stamp')

    def insert_tweet(self, user_id, tweet):
        tweet['deleted'] =0
        tweet['time_stamp'] = int(time.time())
        self.db_object.update_push(self.table_name,{"useruid":int(user_id)},{"updates":tweet})
        
    def get_tweet_by_user_ids(self, user_ids):
        return self.db_object.get_all(self.table_name,{"user_id": {"$in": user_ids},'deleted':0}, 'time_stamp')    

    def get_trending_hashtags(self, start_time_stamp, end_time_stamp):
        mapper = Code("""
            function () {
            for(var i = 0;i<this.updates.length;i++)

            {

            var current = this.updates[i];
            if(current.deleted != 1){
                     items = current.status.split(' ');
                     for(var j=0;j<items.length;j++){ 
                        if(items[j].indexOf('#')==0){
                                emit(items[j], 1); 
                                }
                            }
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
             return parseInt(sum);
            }
            """)
        if start_time_stamp=="" and end_time_stamp =="":
            result = self.db_object.map_reduce(self.table_name, mapper, reducer, query = {})[0:10]
        else:
            result = self.db_object.map_reduce(self.table_name, mapper, reducer, 
                query = { 'time_stamp':{'$gte': start_time_stamp,'$lte': end_time_stamp}})[0:10]
        #print result
        return result

    def aggregrate(self, conditions):
        return self.db_object.aggregrate_all(self.table_name,conditions)

    def update_data(self,user_id):
        food = Food()
        f_results = food.get_foods_by_userid(user_id)
        f_list = []
        for f in f_results:
            f_list.append(f['food_name'])
       
        orgn = Organisation()
        organisations = orgn.get_organisations_by_mem_id(user_id)
        org_list = []
        for org in organisations:
            twitter_user = SocialAccount.objects.get(user__id = org['orguid'])
            
            full_name = twitter_user.extra_data['name']
            org_list.append(full_name)

        self.db_object.update(self.table_name, {'useruid':int(user_id)}, {'foods':f_list,'organisations':org_list})
        

    def get_near_people(self, query):
        return self.db_object.get_distinct(self.table_name,'username',query)['count']

    

    def update_tweets(self, username, first_name, last_name, description, address, sign_up_as,  lat, lon,type_user=[]):
        results = address
        return self.db_object.update(self.table_name,
            {'user.username':username}, 
            {
                'user.name':str(first_name + ' ' + last_name),
                'user.description':description,
                'user.place' :str(results),
                # 'user.location' :str(results),
                'location.coordinates.0':float(lon),
                'location.coordinates.1':float(lat),
                'sign_up_as':str(sign_up_as),
                'type_user':type_user
            })

        
    def get_friends(self, user_id, next_cursor):
        st = SocialToken.objects.get(account__user__id=user_id)
        ACCESS_TOKEN = st.token
        ACCESS_TOKEN_SECRET = st.token_secret        
        sa = SocialAccount.objects.get(user__id = user_id)
        screen_name = sa.extra_data['screen_name']
        user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        friends = user_twitter.get_friends_list(screen_name = screen_name, count=200, cursor = next_cursor)
        return friends

    def get_followers(self, twitter_id):
        pass
        
    def get_user_tweets_latest(self, user_id):
        pass
    
    def follow_user(self, friend_id, my_username, my_id):
        st = SocialToken.objects.get(account__user__id=my_id)
        ACCESS_TOKEN = st.token
        ACCESS_TOKEN_SECRET = st.token_secret        
        user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        try:
            user_twitter.create_friendship(user_id = friend_id)
            return {'status':1, 'activity':'follow', '_id':my_id, 'message':'You have successfully followed.'}
        except:
            return {'status':0, 'activity':'follow', '_id':my_id, 'message':'Already Followed'}

class UserProfile():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'userprofile'
        self.db_object.create_table(self.table_name,'useruid')

    def get_all_profiles(self):
        return self.db_object.get_all_vals(self.table_name)
  
    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': int(user_id)})

    def get_profile_by_username(self, username):
        return self.db_object.get_one(self.table_name,{'username': str(username)})

    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'sign_up_as':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)

    def update_profile_fields(self, where, what):
        self.db_object.update(self.table_name, where, what)

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

    def update_profile_by_username(self, username, description, address, type_usr, sign_up_as, phone, lat, lon, postal_code, name):
        return self.db_object.update(self.table_name,
             {'username':username},
             {'zip_code':str(postal_code),
             'description':str(description),
             'latlng.coordinates.1':float(lat),
             'latlng.coordinates.0':float(lon),
             'address':str(address),
             'type_user':type_usr,
             'sign_up_as':sign_up_as, 
             'phone_number':str(phone),
             'name':name
             })        
    def update_profile_upsert(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)

    def get_unclaimed_profile_paginated(self, pagenum = 1):
        return self.db_object.get_paginated_values(self.table_name, 
            conditions = {'is_unknown_profile':'true'}, pageNumber = pagenum)

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
        # self.db_object.insert_one(self.table_name,value)
        self.db_object.update_upsert(self.table_name, 
            {'c_useruid': value['c_useruid'], 'b_useruid': value['b_useruid']}, {'deleted': 0})

    def delete_connection(self, b_useruid, c_useruid):
        self.db_object.update(self.table_name,{'b_useruid': b_useruid, 'c_useruid': c_useruid}, {'deleted':1})

    def search_connectedness(self, b_useruid, c_useruid):
        result = self.db_object.get_one(self.table_name, {'b_useruid': b_useruid, 'c_useruid': c_useruid,'deleted':0})
        return result

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
        self.db_object.update_upsert(self.table_name, {'food_name': value['food_name'], 
            'useruid': value['useruid']}, {'deleted': 0})
        twt = TweetFeed()
        twt.update_data(value['useruid'])

    def get_food_by_uid_food_name(self, food_name, user_id):
        return self.db_object.get_one(self.table_name, 
            {'useruid':user_id, 'food_name':food_name})

    def get_foods_by_food_name(self, food_name):
        return self.db_object.get_all(self.table_name, 
            {'food_name':food_name})

    def delete_food(self, useruid, food_name):
        self.db_object.update(self.table_name,{'useruid': useruid, 'food_name': food_name}, {'deleted':1})
        # also delete recommendations of the food
        table_name = 'recommendfood'
        self.db_object.create_table(table_name,'food_name')
        self.db_object.update_multi(table_name,{'business_id': useruid, 'food_name': food_name}, {'deleted':1})

    def update_food(self, data):
        self.db_object.update(self.table_name,{'food_name': data['food_name'], 'useruid': data['useruid'], 'deleted': 0},
         {'description':data['description'], 'food_tags': data['food_tags'], 'photo_url': data['photo_url']})


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
        # self.db_object.insert_one(self.table_name,value)
        self.db_object.update_upsert(self.table_name, {'customeruid': value['customeruid'], 'useruid': value['useruid']}, {'deleted': 0})

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
        value['deleted'] = 0
        self.db_object.update_upsert(self.table_name, {'memberuid': value['memberuid'], 'orguid': value['orguid']}, {'deleted': 0})        
        twt = TweetFeed()
        twt.update_data(value['memberuid'])

    def delete_member(self, orguid, member_id):
        self.db_object.update(self.table_name,{'orguid': orguid, 'memberuid': member_id}, {'deleted':1})

    def get_organisations_by_mem_id(self, member_id):
        return self.db_object.get_all(self.table_name,{'memberuid': member_id, 'deleted': 0})

    def check_member(self, org_id, mem_id):
        return self.db_object.get_one(self.table_name, {'orguid': int(org_id), 'memberuid':int(mem_id), 'deleted': 0})

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
        # self.db_object.insert_one(self.table_name,value)
        self.db_object.update_upsert(self.table_name, {'memberuid': value['memberuid'], 'orguid': value['orguid']}, {'deleted': 0})

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

    def get_paginated_friends(self, username, pagenum):
        friends = self.db_object.get_paginated_values(self.table_name,
            {'username':str(username)}, pageNumber = int(pagenum))
        friend_list = []
        for eachFriend in friends:
            invites_obj = Invites()
            if invites_obj.check_invited(eachFriend['friends']['screen_name'], username) == False:
                friend_list.append({'friends':{'screen_name':eachFriend['friends']['screen_name'],
                    'name':eachFriend['friends']['name'], 'profile_image_url':eachFriend['friends']['profile_image_url']}})        
        return friend_list

    def get_friends_count(self, username):
        return self.db_object.get_count(self.table_name,{'username':str(username)})

    def search_friends(self, username, query):
        friend = re.compile(str(query) + '+', re.IGNORECASE)
        result = self.db_object.get_paginated_values(self.table_name, 
            {'username':str(username), 
            '$or':[{'friends.name':{'$regex':friend}}, {'friends.screen_name':{'$regex':friend}}]})
        return result

    def get_friend_id(self, username, screen_name):
        #print username, screen_name, "Inside GET FRIEND ID"
        result = self.db_object.get_one(self.table_name,{'username':str(username),'friends.screen_name':str(screen_name)})
        #print result
        return result['friends']['id']

    def get_friend_from_screen_name(self, screen_name, username):
        result = self.db_object.get_one(self.table_name,
            {'friends.screen_name':screen_name, 'username':username})
        return result

class InviteId():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'inviteid'
        self.db_object.create_table(self.table_name,'username')

    def create_invites_id(self,doc):
        return self.db_object.insert_one(self.table_name,doc)

    def get_unused_id(self, user_id):
        try:
            if(len(self.db_object.get_one(self.table_name, {'used':'false', 'userid':user_id}))>0):
                return self.db_object.get_one(self.table_name, {'used':'false', 'userid':user_id})
            else:
                self.create_invites_id({'used':'false', 'userid':user_id})
                return self.db_object.get_one(self.table_name, {'used':'false', 'userid':user_id})
        except:
            self.create_invites_id({'used':'false', 'userid':user_id})
            return self.db_object.get_one(self.table_name, {'used':'false', 'userid':user_id})

    def change_used_status(self, user_id, invite_id):
        return self.db_object.update(self.table_name,{'_id':ObjectId(invite_id), 'userid':user_id}, {'used':'true'})

class Invites():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'invites'
        self.db_object.create_table(self.table_name,'username')

    def save_invites(self,doc):
        return self.db_object.update_upsert(self.table_name,
            {'to_screenname':doc['to_screenname'],'from_username':doc['from_username']},doc)

    def check_invitees(self, screen_name):
        return self.db_object.get_all(self.table_name, 
            {'to_screenname':str('@'+ str(screen_name))})

    def check_invited(self, screen_name, user_name):
        if len(self.db_object.get_all(self.table_name, {'to_screenname':str('@'+ str(screen_name)), 
            'from_username':str(user_name)})) > 0:
            return True
        return False

    def check_invited_by_invite_id(self, screen_name, invite_id):
        return self.db_object.get_one(self.table_name, {'to_screenname':str('@'+str(screen_name)), 
            'invite_id':ObjectId(invite_id)})

class InviteAccept():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'inviteAccept'
        self.db_object.create_table(self.table_name,'screen_name') 

    def insert_invite_accept(self, invite_id, invitation_by, invitation_to):
        result = self.db_object.insert_one(self.table_name, 
            {'invite_id':ObjectId(invite_id),'to_username':str('@'+str(invitation_to)), 'from_username':invitation_by,
            'accept_time': time.mktime(datetime.now().timetuple())})
        return result

class Notification():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'notification'
        self.db_object.create_table(self.table_name,'to_username')

    def save_notification(self,doc):
        return self.db_object.insert_one(self.table_name,doc)

    def get_notification_by_id(self, notification_id):
        return self.db_object.get_one(self.table_name, {'_id':ObjectId(str(notification_id))})

    def change_notification_view_status(self, notification_id):
        self.db_object.update_multi(self.table_name, 
            {'_id':ObjectId(notification_id)}, 
            {'notification_view_status':'true'})
        return HttpResponse(json.dumps({'status':1}))

    def change_notification_archived_status(self, notification_id):
        self.db_object.update_multi(self.table_name, 
            {'_id':ObjectId(str(notification_id))}, 
            {'notification_archived_status':'true'})
        return {'status':1, 'activity':'archive', 'notification_id':notification_id, 
            'message':'Message Archived successfully'}

    def get_notification(self,username, page_number = 1, n_type = 'unread'):
        all_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_archived_status':'false'})
        unread_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_view_status':'false'})
        archived_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_archived_status':'true'})
        if n_type == 'unread':
            return {'archived_notification_count':archived_notification_count, 
                    'all_notification_count':all_notification_count, 
                    'unread_notification_count':unread_notification_count, 
                    'notifications':self.db_object.get_paginated_values(self.table_name,
                    {'notification_to':username,
                    'notification_view_status':'false'},
                    sort_index ='notification_time', pageNumber = page_number)}

        elif n_type == 'archive':
            return {'archived_notification_count':archived_notification_count, 
                    'all_notification_count':all_notification_count, 
                    'unread_notification_count':unread_notification_count, 
                    'notifications':self.db_object.get_paginated_values(self.table_name,
                    {'notification_to':username,
                    'notification_archived_status':'true'},
                    sort_index ='notification_time', pageNumber = page_number)}

        elif n_type == 'all':
            return {'archived_notification_count':archived_notification_count, 
                    'all_notification_count':all_notification_count, 
                    'unread_notification_count':unread_notification_count, 
                    'notifications':self.db_object.get_paginated_values(self.table_name,
                    {'notification_to':username,
                    'notification_archived_status':'false'},
                    sort_index ='notification_time', pageNumber = page_number)}

    def get_notification_counts(self,username):
        all_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_archived_status':'false'})
        unread_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_view_status':'false'})
        archived_notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_archived_status':'true'})
        return {'all':all_notification_count, 'unread':unread_notification_count, 'archived':archived_notification_count}

    def get_notification_count(self, username):
        notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_view_status':'false'})
        return notification_count

    def get_archive_count(self, username):
        notification_count = self.db_object.get_count(self.table_name,
            {'notification_to':username, 'notification_archived_status':'true'})
        return notification_count    

    def un_archive_notification(self, notification_id):
        return self.db_object.update(self.table_name,
            {'_id':ObjectId(str(notification_id))}, {'notification_archived_status':'false'}) 

class TwitterError():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'twittererror'
        self.db_object.create_table(self.table_name,'screen_name')    

    def save_error(self, doc):
        return self.db_object.insert_one(self.table_name,doc)

    def get_error(self, screen_name):
        return self.db_object.get_all_vals(self.table_name,{'username':screen_name, 'error_solve_stat':'false'})   

    def change_error_status(self, screen_name):
        return self.db_object.update(self.table_name, {'username':screen_name}, {'error_solve_stat':'true'})

class Spam():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'spam'
        self.db_object.create_table(self.table_name,'screen_name') 

    def check_spam_by(self, tweet_id, user_id):
        result = self.db_object.get_one(self.table_name, {'tweet_id':ObjectId(tweet_id),'spam_by':user_id})
        return result

    def mark_spam(self, spam_by, tweet_id):
        return self.db_object.update_upsert(self.table_name, 
            {'tweet_id':ObjectId(tweet_id)}, {'spam_by':spam_by})  

