
from DataConnector import UserInfo

def user_info(request):
    if request.user.is_authenticated():
        user_id = request.user.id
        try:
            user_info = UserInfo(user_id)
            return {'userinfo' : user_info }
        except:
            return {'userinfo':""}
    return {}