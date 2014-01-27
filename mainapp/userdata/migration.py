import json
from gen_extra_data2 import generate
from unique_name import unique_name
from user_types import get_unique_types, get_unique_foods
import uuid
import random
import csv
import time
from TweetFeed import TweetFeed,TradeConnection, UserProfile, UserProfile1, Food, Customer, Organisation
from pymongo import Connection

tweet_id = 10000
# c = Connection()
# c.drop_database('foodtrade')
def gen_unique_sentence(no_words):
    f = open("american-english", 'r')
    words = f.read().split("\n")
    random.shuffle(words)
    return " ".join(words[0:no_words-1])

def gen_unique_address():
    rand_no = int(random.randrange(0, 41000))
    
    data = [str(rand_no), str("{0:.5f}".format(random.uniform(-1, 1) * 90)), str("{0:.5f}".format(random.uniform(-1, 1) * 180)), "location "+ str(rand_no)]
    return data #lat 1 lon -2 


def gen_auth_user(user_pk, username):
    '''Status: Completed'''
    auth_user = {"model":"auth.user", "pk": user_pk, "fields": {"username": username, "email":"sujitmhj@gmail.com"}} #first model- make pk, username as unique
    return auth_user



def gen_socialaccount(social_pk, user_pk, user, name, description):
    '''Status: Complete'''
    extra_data = generate([description, name, user])

    socialaccount_fields = {"user": user_pk, "provider":"1",
                            "last_login": "2013-11-22 11:11:11",
                            "date_joined": "2013-11-22 11:11:11",
                             "uid": user, 
                             "extra_data": extra_data
                            } # make user from above, uid unique, extra_data is complex 

    socialaccount_socialaccount = {"model":"socialaccount.socialaccount","pk": social_pk, "fields": socialaccount_fields} #second model
    social_pk += 1
    return socialaccount_socialaccount

def gen_tradeconnection_userprofile(third_pk, userid, user, name, description, new_location):
    '''Status: Need to generate location, lat and long'''

    sign_up_types = ["Individual", "Business", "Organisation"]
    random.shuffle(sign_up_types)
    if sign_up_types[0] == "Business":

        type_user = get_unique_types()
        foods = get_unique_foods()
    else:
        type_user = []
        foods = []
    global tweet_id


    latlng = {"type" : "Point", "coordinates" : [float(new_location[2]),float(new_location[1])] } #copy coordinated from above lat-lon of user.
       
    tradeconnection_userprofile_fields = {"username":user, 'screen_name':user, "description": description, "name":name, "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png", "useruid": userid, "sign_up_as": sign_up_types[0],
                                          "type_user":type_user,
                                            "zip_code": new_location[0], "address": new_location[3],
                                           "latlng":latlng, "foods":foods, "organisations":[]
                                           }
                                          #userid from above, sign_up_as is string = Individual, or Food Business or Organization,
                                          # zip ode random, lat and lon from zip code.
    
    
    tradeconnection_userprofile_fields["updates"] = []

    rand_no = int(random.randrange(1,3))
    tweet_feed = TweetFeed()
    for i in range(rand_no):
        # Generates Tweet Feeds
        status = gen_unique_sentence(15)
        tradeconnection_tweets_fields_user = {"username":user, "place":new_location[3],
                                              "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
                                              "name":name,  "description":description}


        tradeconnection_tweets_fields_location = {"type" : "Point", "coordinates" : [float(new_location[2]),float(new_location[1])] } #copy coordinated from above lat-lon of user.
        current_time = int(time.time())
        time_before = current_time - 20*24*3600

        tweet_time = int(random.randrange(time_before, current_time))
        parent_tweet_id = 0
        rand_no = int(random.randrange(0, 100))
        previous_tweet_id = tweet_id-1000
        if previous_tweet_id <0:
            previous_tweet_id =0
        if rand_no>90:
            parent_tweet_id = int(random.randrange(previous_tweet_id,tweet_id))

        tradeconnection_tweets_fields = {"status":status, "parent_tweet_id":parent_tweet_id,  "deleted":0, 
                                         "tweet_id":tweet_id, "time_stamp":tweet_time}


        
        tradeconnection_userprofile_fields["updates"].append(tradeconnection_tweets_fields)
        tweet_id = tweet_id +1
   

    # userprofile.create_profile(tradeconnection_userprofile_fields)

    # tweet_feed.update_data(userid)




def main(total_data, tweets_per_user):
    user_pk = 2
    social_pk = 1
    third_pk = 1
    fourth_pk = 1

    my_entry = []
    with open('../fixtures/my_json.json', 'a') as fp:
        # fp.write('[')
        for i in range(total_data-1):
            username = unique_name[user_pk-2].replace(" ", "")
            name = unique_name[user_pk - 2]
            description = gen_unique_sentence(10)

            auth_user = gen_auth_user(user_pk, username)
            user_pk += 1

            socialaccount_socialaccount = gen_socialaccount(social_pk, user_pk-1, username, name, description)
            social_pk += 1

            new_location = gen_unique_address()
            

            tradeconnection_userprofile = gen_tradeconnection_userprofile(third_pk, user_pk-1, username, name, description, new_location)
            third_pk += 1
            
            my_range = range(tweets_per_user[0], tweets_per_user[1])
            random.shuffle(my_range)
            # for i in my_range:
            #   tradeconnection_tweets = gen_fourth_pk(fourth_pk, username, name, new_location)
            #   fourth_pk += 1
            #   entry.append(tradeconnection_tweets)
            # my_entry.extend(entry)
        
        #     fp.write(json.dumps(auth_user)+',')
        #     fp.write(json.dumps(socialaccount_socialaccount))
        #     if i!=total_data-2:
        #         fp.write(',')
        # fp.write(']')


# main(499, [1, 10]  ) # first fields is the total no of users and second is tweets_per_user with [min, max]/

def changes():

    up = UserProfile()
    up.flag_profile()

    up1 = UserProfile1()
    up1_a = up1.get_all_profiles()

    for userprofile in up1_a:
        data = {'sign_up_as': str(userprofile['sign_up_as']),
            'type_user': userprofile['type_user'], 
            'zip_code': str(userprofile['zip_code']),
            'latlng' : userprofile['latlng'],
            'address': userprofile["address"],
            'name': userprofile['name'],
            'email': "", 
            'description':userprofile['description'],
            'username' : userprofile["username"],
            'screen_name': userprofile['username'],
            'profile_img': userprofile['profile_img'],
            'updates': userprofile['updates'],
            'foods':userprofile['foods'],
            'organisations':userprofile['organisations']
            }
    up.update(int(userprofile['useruid']), data)

changes()