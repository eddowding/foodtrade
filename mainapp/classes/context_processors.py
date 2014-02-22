
from DataConnector import UserInfo
from djstripe.models import Customer
from mainapp.classes.TweetFeed import TweetFeed
def user_info(request):
    if request.user.is_authenticated():

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

            return {'userinfo' : user_info, "subscribed": subscribed, "can_tweet":can_tweet}
        except:
            return {'userinfo':""}
    return {}