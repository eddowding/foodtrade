# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
from django.template import RequestContext
import json
from mainapp.classes.TweetFeed import TweetFeed
from mainapp.classes.Email import Email
from Tags import Tags
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood, Notification, Friends
from AjaxSearch import AjaxSearch
from pygeocoder import Geocoder
from mainapp.profilepage import get_connections, get_all_foods


consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'



class AjaxHandle(AjaxSearch):
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
        noappend = request.POST.get('noappend')


        url = " http://"+request.META['HTTP_HOST']+"/profile/"+request.user.username

        user_profile = UserProfile()
        if message != None and message != "":
            if noappend == 'noappend':
                tweet = twitter.update_status(status = message)
            else:
                tweet = twitter.update_status(status = message+url)
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
                    'status': message,
                    "useruid": str(user_id),
                    "foods": [], 
                    'organisations':[], 
                    "type_user":[],
                    "sign_up_as": profile['sign_up_as'],
                    'picture': pic_url_list,
                    'user':{
                    'username':tweet['user']['screen_name'],
                    'name': tweet['user']['name'],
                    'profile_img':tweet['user']['profile_image_url'],
                    'description':tweet['user']['description'],
                    'location':tweet['user']['location'],
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
            tweet_feed.update_data(user_id)
            return HttpResponse(json.dumps({'status':1}))
        else:
            return HttpResponse(json.dumps({'status':1}))
            

    def post_tweet_admin(self, request):
        message = request.POST.get('message')
        if not request.user.is_authenticated():
            admin_twitter = Twython(
            app_key = consumer_key,
            app_secret = consumer_secret,
            oauth_token = admin_access_token,
            oauth_token_secret = admin_access_token_secret
            )
            if message != None and message != "":
                admin_twitter.update_status(status=message)

                return HttpResponse("{'status':1}")
            
        # uid = SocialAccount.objects.get(user__id=user_id).uid
        
        if request.user.is_authenticated():
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
            if message != None and message != "":
                tweet = twitter.update_status(status = message)       
                return HttpResponse("{'status':1}")
        return HttpResponse("{'status':0}")

    def add_connection(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.create_connection({'b_useruid': int(data['prof_id']), 'c_useruid': request.user.id})
            else:
                trade_conn.create_connection({'b_useruid': request.user.id, 'c_useruid': int(data['prof_id'])})
            parameters = {}
            parameters['connections'], parameters['conn'] = get_connections(int(data['prof_id']))
            parameters['connections_str'] = str(json.dumps(parameters['connections']))
            parameters['profile_id'], parameters['user_id'] = int(data['prof_id']), request.user.id
            return render_to_response('conn_ajax.html', parameters)
            # return HttpResponse("{'status':1}")
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
            parameters = {}
            parameters['connections'], parameters['conn'] = get_connections(int(data['prof_id']))
            parameters['connections_str'] = json.dumps(parameters['connections'])
            parameters['profile_id'], parameters['user_id'] = int(data['prof_id']), request.user.id
            return render_to_response('conn_ajax.html', parameters)            
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def profile_user_delete_conn(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.delete_connection(b_useruid = int(data['prof_id']), c_useruid = int(data['conn_id']))
            else:
                trade_conn.delete_connection(b_useruid = int(data['conn_id']), c_useruid = int(data['prof_id']))
            parameters = {}
            parameters['connections'], parameters['conn'] = get_connections(int(data['prof_id']))
            parameters['connections_str'] = json.dumps(parameters['connections'])
            parameters['profile_id'], parameters['user_id'] = int(data['prof_id']), request.user.id
            return render_to_response('conn_ajax.html', parameters)            
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def third_party_conn(self, request):
        trade_conn = TradeConnection()
        print request.POST.get('conn_data')
        data = eval(request.POST.get('conn_data'))
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.create_connection({'b_useruid': int(data['prof_id']), 'c_useruid': int(data['buss_id'])})
            elif data['status'] == 'sell_to':
                trade_conn.create_connection({'b_useruid': int(data['buss_id']), 'c_useruid': int(data['prof_id'])})

            # add parameters
            parameters = {}
            parameters['connections'], parameters['conn'] = get_connections(int(data['prof_id']))
            parameters['connections_str'] = json.dumps(parameters['connections'])
            parameters['profile_id'], parameters['user_id'] = int(data['prof_id']), request.user.id
            return render_to_response('conn_ajax.html', parameters)
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def addfood(self, request):
        foo = Food()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.create_food(data)
            parameters = {}
            parameters['all_foods'] = get_all_foods(int(data['useruid']))
            parameters['profile_id'], parameters['user_id'] = int(data['useruid']), request.user.id
            return render_to_response('ajax_food.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deletefood(self, request):
        foo = Food()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.delete_food(useruid = data['useruid'], food_name = data['food_name']);
            parameters = {}
            parameters['all_foods'] = get_all_foods(int(data['useruid']))
            parameters['profile_id'], parameters['user_id'] = int(data['useruid']), request.user.id
            return render_to_response('ajax_food.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def save_tags(self, request):
        if request.user.is_authenticated():
            tags = request.POST.get('tags')
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

    def deletecustomer(self, request):
        customer = Customer()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            customer.delete_customer(useruid = data['useruid'], customer_id = data['customeruid'])
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

    def deletemember(self, request):
        org = Organisation()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.delete_member(orguid = data['orguid'], member_id = data['memberuid'])
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def addteam(self, request):
        team = Team()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            team.create_member(data)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deleteteam(self, request):
        team = Team()
        print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            team.delete_member(orguid = data['orguid'], member_id = data['memberuid'])
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def send_email(self, request):        
        sender_name = request.POST.get('name')
        receiver_email = request.POST.get('receiver')
        sender_email = request.POST.get('sender')
        message = request.POST.get('message')
        subject = sender_name + " has contacted you"
        if sender_name!="" and receiver_email != "" and sender_email != "" and message != "":
            body = "Hi!" +'\r\n\r\n' + message +'\r\n\r\n'+sender_name +'\r\n' +sender_email
            email = Email()
            if email.send_mail(receiver_email, subject, body):
                return HttpResponse("{'status':1}")
        
        return HttpResponse("{'status':0}")

    def vouch_for_food(self, request):
        recomm = RecommendFood()
        #print request.POST.get('data')
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            recomm.create_recomm(data)
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def getnotification(self, request):
        username = request.user.username
        notification_obj  = Notification()
        return notification_obj.get_notification(username)

    def change_notification_status(self, request):
        if request.method == 'POST' and request.user.is_authenticated:
            notification_obj = Notification()
            return notification_obj.change_notification_status(request.user.username)
        else:
            return HttpResponse(json.dumps({'status':'0'}))

    def validate_logged_in(self,request):
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'status':'1'}))
        return HttpResponse(json.dumps({'status':'0'}))

    def get_friends_paginated(self,request):
        if request.method == 'POST' and request.user.is_authenticated:
            page_num = request.POST['pgnum']
            friends_obj = Friends()
            return HttpResponse(json.dumps(friends_obj.get_paginated_friends(request.user.username, page_num)))
        else:
            return HttpResponse(json.dumps({'status':'0'}))
    def search_friend(self, request):
        if request.method == 'POST' and request.user.is_authenticated:
            query = request.POST['query']
            friends_obj = Friends()
            return HttpResponse(json.dumps(friends_obj.search_friends(request.user.username, query)))
        else:
            return HttpResponse(json.dumps({'status':'0'}))

    def check_valid_address(self, request):
        # print "Roshan Validate"
        if request.method == 'POST' and request.user.is_authenticated:
            # print "Inside"
            address = request.POST['address']
            if Geocoder.geocode(address).valid_address:
                return HttpResponse(json.dumps({'valid':'true'}))
            else:
                return HttpResponse(json.dumps({'valid':'false'}))
        else:
            return HttpResponse(json.dumps({'status':'0'}))

    def activity_handle(self,request):
        if request.user.is_authenticated and request.method == 'POST':
            task = request.POST['task']
            change_id = request.POST['changeID']
            user = request.user.username
            tweet_feed_obj = TweetFeed()
            if task == 'spam':
                print task

            if task == 'delete':
                tweet_feed_obj.delete_tweet(change_id)
                return HttpResponse(json.dumps({'status':'1', 'activity':'deleteTweet', '_id':change_id}))

            if task == 'follow':
                friend_obj = Friends()
                fid = friend_obj.get_friend_id(request.user.username, change_id)
                data = tweet_feed_obj.follow_user(fid, request.user.username, request.user.id)
                return HttpResponse(json.dumps(data))
            if task == 'buyFrom':
                # print request.user.id, change_id
                tc_object = TradeConnection()
                result = tc_object.search_connectedness(int(change_id), int(request.user.id))
                try:
                    if (len(result) > 0):
                        return HttpResponse (json.dumps({'status':0, 'activity':'buyFrom', '_id':change_id, 'message':'You are already connected.'}))
                    else:
                        tc_object.create_connection({'c_useruid':int(request.user.id) , 'b_useruid': int(change_id)})
                        return HttpResponse (json.dumps({'status':1, 'activity':'buyFrom', '_id':change_id, 'message':'You are connected.'}))
                except:
                    tc_object.create_connection({'c_useruid':int(request.user.id) , 'b_useruid': int(change_id)})
                    return HttpResponse (json.dumps({'status':1, 'activity':'buyFrom', '_id':change_id, 'message':'You are connected.'}))

            if task == 'sellTo':                
                tc_object = TradeConnection()
                result = tc_object.search_connectedness(int(request.user.id), int(change_id))
                try:
                    if (len(result) > 0):
                        return HttpResponse (json.dumps({'status':0, 'activity':'sellTo', '_id':change_id, 'message':'You are already connected.'}))
                    else:
                        tc_object.create_connection({'c_useruid':int(change_id) , 'b_useruid': int(request.user.id)})
                        return HttpResponse (json.dumps({'status':1, 'activity':'sellTo', '_id':change_id, 'message':'You are connected.'}))
                except:
                    tc_object.create_connection({'c_useruid':int(change_id) , 'b_useruid': int(request.user.id)})
                    return HttpResponse (json.dumps({'status':1, 'activity':'sellTo', '_id':change_id, 'message':'You are connected.'}))
        else:
            return HttpResponse(json.dumps({'status':'0'}))


