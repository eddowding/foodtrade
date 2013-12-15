# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from TweetFeed import TweetFeed
from search import search_general

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

def home(request):
    parameters={}
    parameters['user'] = request.user
    parameters['total_food_count'] = 2
    parameters['food'] = [{'name': 'Cauliflowers', 'tagcount': 7},{'name': 'Mutton', 'tagcount': 5}]
    parameters['total_business_count'] = 2
    parameters['business'] = [{'name': 'FoodSupply Pvt. Ltd.', 'tagcount': 7},{'name': 'Nina and Hager Meat Industry', 'tagcount': 5}]
    parameters['total_organization_count'] = 2
    parameters['organization'] = [{'name': 'Onion Export', 'tagcount': 7},{'name': 'Bajeko Sekuwa', 'tagcount': 5}]
    return render_to_response('index.html', parameters)

def tweets(request):
    parameters = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    parameters['user'] = request.user
    user_id = request.user.id
    st = SocialToken.objects.get(account__user__id=user_id)
    access_token = st.token
    access_token_secret = st.token_secret
    print access_token
    print access_token_secret
    twitter = Twython(
        app_key = consumer_key,
        app_secret = consumer_secret,
        oauth_token = access_token,
        oauth_token_secret = access_token_secret
    )
    uid = SocialAccount.objects.get(user__id=user_id).uid
    # tweet = 'Hello !!'
    # twitter.update_status(status = tweet)
    # twitter.get_home_timeline()
    
    # user_tweets = twitter.get_user_timeline(user_id=uid, count = 200,
    #                                     include_rts=True)
    mentions = twitter.get_mentions_timeline(count = 200, contributer_details = True)
    # tweet_list = []
    # for tweet in mentions:
    #     tweet_list.append(Twython.html_for_tweet(tweet))
        # tweet_list.append(tweet)
    # print json.dumps(mentions[0:2], sort_keys = True, indent = 4)
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
    search_results = twitter.search(q = '@SantoshGhimire ')
    # print json.dumps(search_results, sort_keys = True, indent = 4)
    for result in search_results:
        print result['text']
        # print json.dumps(result, sort_keys = True, indent = 4)
    print len(search_results['statuses'])
    parameters['tweet_list'] = search_results
    return render_to_response('home.html', parameters)
