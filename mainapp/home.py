# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.classes.TweetFeed import TweetFeed, Invites, Notification, UserProfile, UnapprovedFood, ApprovedFoodTags, Food
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId
import datetime
import time
import json
from mainapp.classes.Foods import AdminFoods
from mainapp.classes.Tags import Tags
from mainapp.classes.MongoConnection import MongoConnection
from django.contrib.auth.decorators import user_passes_test
import pprint
from collections import Counter
from django.contrib.auth.models import User

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'

from classes.DataConnector import UserInfo
from django.template import RequestContext
from mainapp.classes.AjaxHandle import AjaxHandle
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ajax_request(request, func_name):
    #print func_name, request.POST
    ajax_handle = AjaxHandle()
    return_msg = getattr(ajax_handle,func_name)(request)
    if func_name == 'post_tweet' and 'invite' in request.POST and json.loads(return_msg.content)['status'] == 1:
        invite_obj = Invites()
        invitees = str(request.POST['to']).split(',')
        now = datetime.datetime.now()
        sent_time  = time.mktime(now.timetuple())
        for eachInvitee in invitees:
            invite_obj.save_invites({
                'from_username':request.user.username, 
                'to':eachInvitee, 
                'sent_time':sent_time
                })
    return return_msg


@user_passes_test(lambda u: u.is_superuser)
def admin_tags(request):
    parameters = {}
    if request.user.is_authenticated():
        user_id = request.user.id
        user_info = UserInfo(user_id)
        user_profile_obj = UserProfile()
        userprofile = user_profile_obj.get_profile_by_id(user_id)
        parameters['userprofile'] = UserProfile
        parameters['userinfo'] = user_info
        
    mytag = Tags()
    tags = mytag.get_tags()
    parameters['tags'] = json.dumps(tags)

    return render_to_response('admin_tags.html', parameters, context_instance=RequestContext(request))

def food_pipeline():
    aggregation_pipeline = []
    aggregation_pipeline.append({"$match":{'food_tags':{'$exists':True}}})
    aggregation_pipeline.append({"$match":{'food_tags': {'$ne': ''}}})
    aggregation_pipeline.append({
    "$group":
        {"_id": "$food_name", 
        "results":
        {'$push':{
        "food_tags":"$food_tags",
        "useruid": "$useruid"
        # "approved_food_tags": "$approved_food_tags"
        }
        }}
    })
    mongo = MongoConnection("localhost",27017,'foodtrade')
    results = mongo.aggregrate_all('food', aggregation_pipeline)
    return results

def fix_new_foods():
    # all items in food which are not in unapproved as well as admin foods
    new_foods = UnapprovedFood()
    admin_foods = AdminFoods()

    master_foods = admin_foods.get_tags()
    unapproved = new_foods.get_all_new_foods()
    unapproved = [str(i['food_name']) for i in unapproved]

    #create master list of foods
    final_master = []
    for each in master_foods:
        if each.get('childrens')!=None:
            final_master.extend([str(i['node']) for i in each['childrens']])
        else:
            final_master.extend([str(each['node'])])
        # if each.get('childrens') == None:
        #     final_master.extend([str(each['node'])])

    aggregation_pipeline = []
    aggregation_pipeline.append({"$match":{'deleted': 0}})
    aggregation_pipeline.append({
    "$group":
        {"_id": "$food_name"}
    })
    mongo = MongoConnection("localhost",27017,'foodtrade')
    food_results = mongo.aggregrate_all('food', aggregation_pipeline)
    
    for eachfood in food_results:
        if str(eachfood['uid']) not in final_master and str(eachfood['uid']) not in unapproved:
            new_foods.create_food({'food_name': eachfood['uid']})

@user_passes_test(lambda u: u.is_superuser)
def food_tags(request):
    parameters = {}
    fix_new_foods()
    if request.user.is_authenticated():
        # parameters['user'] = request.user
        user_id = request.user.id
       
        user_info = UserInfo(user_id)

        user_profile_obj = UserProfile()
        userprofile = user_profile_obj.get_profile_by_id(user_id)
        parameters['userprofile'] = UserProfile

        parameters['userinfo'] = user_info
        newfoo = UnapprovedFood()
        new_foods = newfoo.get_all_new_foods()
        parameters['unapproved_foods'] = new_foods

        # aggregate pipeline to display all tags of all foods
        results = food_pipeline()
        processed_results = []

        approved_tags = ApprovedFoodTags()
        all_approved = approved_tags.get_all_approved_foods()

        for each in results:
            mytags = {}
            for e in each['results']:
                t_list = e['food_tags'].split(',')
                app_tags = approved_tags.get_food_by_name(each['uid'])
                app_tags = app_tags['tags'].split(',') if app_tags!=None else []
                # app_tags = e.get('approved_food_tags').split(',') if e.get('approved_food_tags')!=None else False
                # if app_tags!=None:
                #     if Counter(t_list)==Counter(app_tags):
                #         continue
                for eachtts in t_list:
                    if app_tags!=None:
                        if eachtts not in app_tags:
                            if eachtts not in mytags.keys():
                                mytags[eachtts] = 'unapproved'
                        else:
                            mytags[eachtts] ='approved'
                    else:
                        if eachtts not in mytags.keys():
                            mytags[eachtts] = 'unapproved'

            processed_results.append({'food_name': each['uid'], 'results': mytags}) if mytags!={} else False
        parameters['tags_and_foods'] = processed_results

    foods = AdminFoods()
    tags = foods.get_tags()
    parameters['tags'] = json.dumps(tags)

    return render_to_response('food-tags.html', parameters, context_instance=RequestContext(request))

def home(request):
    parameters = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/activity/')
    return render_to_response('business.html',parameters,context_instance=RequestContext(request))

def tweets(request):
    parameters = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    parameters['user'] = request.user
    user_id = request.user.id
    # print user_id
    st = SocialToken.objects.get(account__user__id=user_id)
    access_token = st.token
    access_token_secret = st.token_secret
    twitter = Twython(
        app_key = consumer_key,
        app_secret = consumer_secret,
        oauth_token = access_token,
        oauth_token_secret = access_token_secret
    )
    # uid = SocialAccount.objects.get(user__id=user_id).uid
    admin_twitter = Twython(
        app_key = consumer_key,
        app_secret = consumer_secret,
        oauth_token = admin_access_token,
        oauth_token_secret = admin_access_token_secret
        )
    max_id = MaxTweetId.objects.all()[0]
    max_tweet_id = int(max_id.max_tweet_id)
    # print type(max_tweet_id), max_tweet_id
    mentions = admin_twitter.get_mentions_timeline(count = 200, contributer_details = True, since_id = max_tweet_id)
    # print len(mentions)
    tweet_list = []
    tweet_feed = TweetFeed()
    for tweet in mentions:
        try:
            usr = SocialAccount.objects.get(uid = tweet['user']['id'])
            pic_url_list = []
            if tweet['entities'].get('media')!= None:
                for each in tweet['entities'].get('media'):
                    pic_url_list.append(each['media_url'])
            data = {'tweet_id': tweet['id'],
                    'parent_tweet_id': 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id'],
                    'tweet_message': tweet['text'],
                    'picture': pic_url_list
            }
            tweet_list.append(tweet['id'])
            tweet_feed.insert_tweet(data)
        except:
            text = "@" + tweet['user']['screen_name'] + " Thanks! Please confirm your post by clicking this link [link]. You'll only have to do this once."
            try:
                admin_twitter.update_status(status = text)
            except:
                pass
    max_id.max_tweet_id = max(tweet_list)
    max_id.save()

    parameters['tweet_list'] = mentions
    user_profile_obj = UserProfile()
    userprofile = user_profile_obj.get_profile_by_id(user_id)
    parameters['userprofile'] = UserProfile
    return render_to_response('home.html', parameters)

@user_passes_test(lambda u: u.is_superuser)
def all_users(request):
    parameters = {}
    all_users = User.objects.all().order_by('-date_joined')
    final_list = []
    user_prof = UserProfile()
    for each in all_users:
        try:
            print each.username
            usr_pro = user_prof.get_profile_by_username(str(each.username))
            final_list.append({
                'date_joined': each.date_joined,
                'username': each.username,
                'sign_up_as': usr_pro['sign_up_as']
                })
        except:
            continue
    print final_list
    parameters['all_users'] = final_list
    return render_to_response('all_users.html', parameters, context_instance=RequestContext(request))
    # return render_to_response('all_users.html', parameters)