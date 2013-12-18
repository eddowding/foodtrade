# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from TweetFeed import TweetFeed
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'



from django.template import RequestContext

def home(request):
    # parameters={}
    # parameters['user'] = request.user
    # parameters['total_food_count'] = 2
    # parameters['food'] = [{'name': 'Cauliflowers', 'tagcount': 7},{'name': 'Mutton', 'tagcount': 5}]
    # parameters['total_business_count'] = 2
    # parameters['business'] = [{'name': 'FoodSupply Pvt. Ltd.', 'tagcount': 7},{'name': 'Nina and Hager Meat Industry', 'tagcount': 5}]
    # parameters['total_organization_count'] = 2
    # parameters['organization'] = [{'name': 'Onion Export', 'tagcount': 7},{'name': 'Bajeko Sekuwa', 'tagcount': 5}]
    return render_to_response('thome.html',context_instance=RequestContext(request))

def tweets(request):
    parameters = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    parameters['user'] = request.user
    user_id = request.user.id
    print user_id
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
    print type(max_tweet_id), max_tweet_id
    mentions = admin_twitter.get_mentions_timeline(count = 200, contributer_details = True, since_id = max_tweet_id)
    print len(mentions)
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
            print "Inside except"
            text = "@" + tweet['user']['screen_name'] + " Thanks! Please confirm your post by clicking this link [link]. You'll only have to do this once."
            print text    
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

    return render_to_response('home.html', parameters)

