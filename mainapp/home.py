# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from mainapp.classes.TweetFeed import TweetFeed, Invites, Notification, UserProfile, UnapprovedFood
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId
import datetime
import time
import json
from mainapp.classes.Foods import AdminFoods
from mainapp.classes.Tags import Tags

from django.contrib.auth.decorators import user_passes_test

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

@user_passes_test(lambda u: u.is_superuser)
def food_tags(request):
    parameters = {}
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

    foods = AdminFoods()
    tags = foods.get_tags()
    parameters['tags'] = json.dumps(tags)

    return render_to_response('food-tags.html', parameters, context_instance=RequestContext(request))

def home(request):
    parameters = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect('/activity/')
    return render_to_response('front.html',parameters,context_instance=RequestContext(request))

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

    ''' kaam chhaina '''
        # print json.dumps(data, sort_keys = True, indent = 4)
        # tweet_list.append(Twython.html_for_tweet(tweet))
        # tweet_list.append(tweet)
    # print tweet_list
    # print json.dumps(mentions[0], sort_keys = True, indent = 4)
    # parameters['tweet_list'] = mentions
    # final_list = []
    # # since_id should be mentions[0]['id']
    # for each in mentions:
    #     final_list.append({'created_at': each['created_at'],
    #         'tweet_id': each['id'],
    #         'parent_tweet_id': each['in_reply_to_status_id'],
    #         'tweet_message': each['text'],
    #         'twitter_uid': each['user']['id']
    #         })
    # tweet_feed = TweetFeed()
    # # tweet_feed.insert_tweet({'parent_tweet_id': 2, 'user_id': 3, 'tweet_message': 'Hello there'})
    # print tweet_feed.get_tweet_by_parent_id(2)

    # search_results = twitter.search(q="#nepal")
    # print search_results
    # print json.dumps(search_results, sort_keys = True, indent = 4)
    # search_results = search_general(twitter, hashtags = ['#Nepal'])
    # search_results = twitter.search(q = '@SantoshGhimire ')
    # print json.dumps(search_results, sort_keys = True, indent = 4)
    # for result in search_results:
    #     print result['text']
    #     # print json.dumps(result, sort_keys = True, indent = 4)
    # print len(search_results['statuses'])
    # search_results = []
    parameters['tweet_list'] = mentions
    user_profile_obj = UserProfile()
    userprofile = user_profile_obj.get_profile_by_id(user_id)
    parameters['userprofile'] = UserProfile
    return render_to_response('home.html', parameters)

