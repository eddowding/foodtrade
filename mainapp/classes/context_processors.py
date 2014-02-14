
from DataConnector import UserInfo
from djstripe.models import Customer
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
            return {'userinfo' : user_info, "subscribed": subscribed}
        except:
            return {'userinfo':""}
    return {}