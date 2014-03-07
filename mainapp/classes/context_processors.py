from DataConnector import UserInfo
from djstripe.models import Customer
from mainapp.classes.TweetFeed import TweetFeed, InviteId
from mainapp.bitly import construct_invite_tweet, shorten_url

def user_info(request):
    if request.user.is_authenticated():

        '''Generate new invite ID.'''
        invite_id_obj = InviteId()                        
        invite_id = invite_id_obj.get_unused_id(request.user.id)

        '''Construct New Invite URL.'''
        invite_tweet = construct_invite_tweet(request, invite_id)

        subscribed = True
        customer, created = Customer.get_or_create(request.user)
        if created:
            subscribed = False

        if not customer.has_active_subscription():
            subscribed = False
        user_id = request.user.id

        try:

            user_info = UserInfo(user_id)
            ft = TweetFeed()
            has_tweet = ft.has_tweet_in_week(request.user.id)
            can_tweet = False

            if subscribed or (not has_tweet):
                can_tweet = True

            return {
                    'userinfo' : user_info, 
                    "subscribed": subscribed, 
                    "can_tweet":can_tweet, 
                    'invite_id':invite_id['uid']['id'], 
                    'invite_tweet':invite_tweet
                    }
        except:
            return {'userinfo':""}
    return {}