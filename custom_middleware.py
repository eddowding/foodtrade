import re
import time, datetime

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
import json 
from django import http
from mainapp.classes.TweetFeed import UserProfile
# from mainapp.classes.TweetFeed import Analytics
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.conf import settings
from django.utils.http import urlquote
from django.core import urlresolvers


try:
    import settings 
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
 
 
class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.        
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):
        '''Save Every Data in request for Analytical purpose'''




        host = request.get_host()
        old_url = [host, request.path]
        new_url = old_url[:]
        
        if (settings.REMOVE_WWW and old_url[0] and old_url[0].startswith('www.')):
            new_url[0] = old_url[0][4:]
        
        if new_url != old_url:
            try:
                urlresolvers.resolve(new_url[1])
            except urlresolvers.Resolver404:
                pass
            else:
                if new_url[0]:
                    newurl = "%s://%s%s" % (
                        request.is_secure() and 'https' or 'http',
                        new_url[0], urlquote(new_url[1]))
                else:
                    newurl = urlquote(new_url[1])
                if request.GET:
                    newurl += '?' + request.GET.urlencode()
                return http.HttpResponsePermanentRedirect(newurl)
        # return None


        # request_data  = json.dumps(str(request))
        # analytics_obj = Analytics()
        # request_time  = datetime.datetime.now()
        # request_time  = time.mktime(request_time.timetuple())
        # analytics_obj.save_data({'request_data':request_data, 'request_time':request_time})

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response 
        return None
 
    def process_response(self, request, response):
        # Avoid unnecessary work
        try:
            if request.user.is_authenticated() and "/accounts/twitter/login/callback/" in request.path:
                social_account = SocialAccount.objects.get(user__id = request.user.id)
                extra_data = social_account.extra_data
                image_desc = {'profile_img': extra_data['profile_image_url']}
                up = UserProfile()                
                up.update_profile_fields({"useruid":request.user.id}, image_desc)
        except:
            pass


        if response.has_header('Access-Control-Allow-Origin'):
            return response
 
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        return response