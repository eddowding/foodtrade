
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from TweetFeed import TweetFeed
from Tags import Tags
from mainapp.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation

consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'




class AjaxHandle():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    
    def post_tweet(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
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
        # uid = SocialAccount.objects.get(user__id=user_id).uid
        admin_twitter = Twython(
            app_key = consumer_key,
            app_secret = consumer_secret,
            oauth_token = admin_access_token,
            oauth_token_secret = admin_access_token_secret
            )
        message = request.POST.get('message')
        user_profile = UserProfile()
        if message != None and message != "":
            tweet = twitter.update_status(status = message)
            tweet_feed = TweetFeed()
            usr = SocialAccount.objects.get(uid = tweet['user']['id'])
            pic_url_list = []
            if tweet['entities'].get('media')!= None:
                for each in tweet['entities'].get('media'):
                    pic_url_list.append(each['media_url'])
            
            profile = user_profile.get_profile_by_id(str(usr.user.id))
            my_lat = profile['latitude']
            my_lon = profile['longitude']
            data = {'tweet_id': tweet['id'],
                    'parent_tweet_id': 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id'],
                    'status': tweet['text'],
                    'picture': pic_url_list,
                    'user':{
                    'username':tweet['user']['screen_name'],
                    'name': tweet['user']['name'],
                    'profile_img':tweet['user']['profile_image_url'],
                    'Description':tweet['user']['description'],
                    'place':tweet['user']['location'],
                    }
            }
            if my_lon == '' and my_lat == '':
                # get ip address
                ip_addr = get_client_ip(request)
                #get lat, long and address of user
                ip_location = get_addr_from_ip(ip_addr)
                data['location'] = {"type": "Point", "coordinates": [float(ip_location['longitude']), float(ip_location['latitude'])]},
            else:                
                data['location'] = {"type": "Point", "coordinates": [float(my_lon), float(my_lat)]}
            tweet_feed.insert_tweet(data)


            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")
            

    def add_connection(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.create_connection({'b_useruid': int(data['prof_id']), 'c_useruid': request.user.id});
            else:
                trade_conn.create_connection({'b_useruid': request.user.id, 'c_useruid': int(data['prof_id'])});
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def del_connection(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.delete_connection(b_useruid = int(data['prof_id']), c_useruid = request.user.id)
            else:
                trade_conn.delete_connection(b_useruid = request.user.id, c_useruid = int(data['prof_id']))
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def addfood(self, request):
        foo = Food()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.create_food(data)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deletefood(self, request):
        foo = Food()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.delete_food(useruid = data['useruid'], food_name = data['food_name']);
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def save_tags(self, request):
        if request.user.is_authenticated():
            tags = request.POST.get('tags')
            tags = "[{'node': 'Agricultural Suppliers', 'childrens': [{'node': 'Animal Feed'}, {'node': 'Compost'}, {'node': 'Livestock Breeder'}, {'node': 'Nursery'}, {'node': 'Seeds'}]}, {'node': 'Food service', 'childrens': [{'node': 'Art_gallery'}, {'node': 'Bar'}, {'node': 'Cafe'}, {'node': 'Catering Contractor'}, {'node': 'Food Stall'}, {'node': 'Home Cooking Service'}, {'node': 'Hostel'}, {'node': 'Hotel'}, {'node': 'Lodging'}, {'node': 'Museum'}, {'node': 'Pub'}, {'node': 'Public sector'}, {'node': 'Restaurant'}, {'node': 'School  University'}, {'node': 'Take Away Food Shops'}]}, {'node': 'Meal_delivery'}, {'node': 'Processing and Manufacture', 'childrens': [{'node': 'Drink'}, {'node': 'Food'}, {'node': 'Processing'}, {'node': 'Waste disposal'}]}, {'node': 'Production', 'childrens': [{'node': 'Arable Farm'}, {'node': 'Bee keeping'}, {'node': 'Box Scheme'}, {'node': 'Community Supported Agriculture (CSA)'}, {'node': 'Dairy'}, {'node': 'Fish'}, {'node': 'Forager'}, {'node': 'Horticulture'}, {'node': 'Livestock Farm'}, {'node': 'Market garden'}, {'node': 'Mixed farm'}, {'node': 'Orchard'}, {'node': 'Other'}, {'node': 'Smallholder'}, {'node': 'Vineyard'}]}, {'node': 'Real_estate_agency'}, {'node': 'Retail', 'childrens': [{'node': 'Baker'}, {'node': 'Butcher'}, {'node': 'Cheese Shop'}, {'node': 'Chocolatier'}, {'node': 'Confectioner'}, {'node': 'Convenience Store'}, {'node': 'Delicatessen'}, {'node': 'Farm Shop'}, {'node': 'Fishmonger'}, {'node': 'Fruitseller'}, {'node': 'Greengrocer'}, {'node': 'Health food'}, {'node': 'Market'}, {'node': 'Newsagent'}, {'node': 'Off licence'}, {'node': 'Supermarket'}]}, {'node': 'Rickmansworth'}, {'node': 'Wholesale and Distribution', 'childrens': [{'node': 'Cash and Carry'}, {'node': 'Community food group'}, {'node': 'Wholesale Market'}, {'node': 'Wholesaler'}, {'node': 'Wine Merchant'}]}]"
            json_tags = json.loads(tags)
            insert_val = {'parent':1, 'tags':json_tags}
            mytag = Tags()
            mytag.set_tags(insert_val)
            print mytag.get_tags()
            return HttpResponse("1")
        else:
            return HttpResponse('0')

    def addcustomer(self, request):
        customer = Customer()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            customer.create_customer(data)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def addmember(self, request):
        org = Organisation()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.create_member(data)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")
