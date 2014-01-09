import json
from gen_extra_data2 import generate
from unique_name import unique_name
from user_types import get_unique_types, get_unique_foods
import uuid
import random
import csv
import time
from TweetFeed import TweetFeed,TradeConnection, UserProfile, Food, Customer, Organisation
from pymongo import Connection

tweet_id = 10000
c = Connection()
c.drop_database('foodtrade')
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
    if sign_up_types[0] == "Business":
        trade_connections = TradeConnection()
        for i in range(int(random.randrange(1,5))):
            rand_no = int(random.randrange(2,488))
            if rand_no != userid:
                ids = [rand_no, userid]
                random.shuffle(ids)
                con = { "deleted" : 0, "c_useruid" : ids[0], "b_useruid" : ids[1] }
                trade_connections.create_connection(con)

    tradeconnection_userprofile_fields = {"useruid": str(userid), "sign_up_as": sign_up_types[0],
                                          "type_user":str(','.join(type_user)),
                                            "zip_code": new_location[0], "address": new_location[3],
                                           "latitude": float(new_location[1]), "longitude": float(new_location[2]), 
                                           }
                                          #userid from above, sign_up_as is string = Individual, or Food Business or Organization,
                                          # zip ode random, lat and lon from zip code.
    userprofile = UserProfile()
    userprofile.create_profile(tradeconnection_userprofile_fields)


    rand_no = int(random.randrange(1,3))
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
            parent_tweet_id = item_no = int(random.randrange(previous_tweet_id,tweet_id))

        tradeconnection_tweets_fields = {"status":status, "useruid": str(userid), "sign_up_as": sign_up_types[0],
                                            "foods": foods, "type_user":type_user, "parent_tweet_id":parent_tweet_id,  "deleted":0, 
                                         "tweet_id":tweet_id, "user": tradeconnection_tweets_fields_user, "time_stamp":tweet_time,
                                          "location": tradeconnection_tweets_fields_location }  

        tweet_feed = TweetFeed()
        tweet_feed.insert_tweet(tradeconnection_tweets_fields)
        tweet_id = tweet_id +1




def main(total_data, tweets_per_user):
    user_pk = 2
    social_pk = 1
    third_pk = 1
    fourth_pk = 1

    my_entry = []
    with open('../fixtures/my_json.json', 'a') as fp:
        fp.write('[')
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
        
            fp.write(json.dumps(auth_user)+',')
            fp.write(json.dumps(socialaccount_socialaccount))
            if i!=total_data-2:
                fp.write(',')
        fp.write(']')


main(499, [1, 10]  ) # first fields is the total no of users and second is tweets_per_user with [min, max]