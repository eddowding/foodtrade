# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

def home(request):
    parameters = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    parameters['user'] = request.user
    user_id = request.user.id
    st = SocialToken.objects.get(account__user__id=user_id)
    access_token = st.token
    access_token_secret = st.token_secret
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
    
    user_tweets = twitter.get_user_timeline(user_id=uid, count = 200,
                                        include_rts=True)
    tweet_list = []
    for tweet in user_tweets:
        # tweet_list.append(Twython.html_for_tweet(tweet))
        tweet_list.append(tweet)
    parameters['tweet_list'] = tweet_list
    return render_to_response('home.html', parameters)