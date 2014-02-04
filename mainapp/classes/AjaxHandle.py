# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
from django.template import RequestContext
from django.conf import settings
import json
from mainapp.classes.TweetFeed import TweetFeed
from mainapp.classes.Email import Email
from Tags import Tags
from Foods import AdminFoods
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood, Notification, Friends, Spam, InviteId, Invites
from AjaxSearch import AjaxSearch
from pygeocoder import Geocoder
from mainapp.profilepage import get_connections, get_all_foods
from mainapp.views import get_twitter_obj
import datetime, time
from bson.objectid import ObjectId
from mainapp.views import calculate_time_ago
from django.contrib.auth.models import User
from mainapp.bitly import construct_invite_tweet, shorten_url

# consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
# consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET =''

# admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
# admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'


class AjaxHandle(AjaxSearch):
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
    
    def post_tweet(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')

        user_id = request.user.id
        st = SocialToken.objects.get(account__user__id=user_id)

        ACCESS_TOKEN = st.token
        ACCESS_TOKEN_SECRET = st.token_secret
        
        user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        bot_twitter = get_twitter_obj(settings.BOT_ACCESS_TOKEN, settings.BOT_ACCESS_TOKEN_SECRET)
        message = request.POST.get('message')
        noappend = request.POST.get('noappend')

        prof_url = " http://"+request.META['HTTP_HOST']+"/profile/"+request.user.username

        url = shorten_url(prof_url)

        if message != None and message != "":
            if noappend == 'noappend':
                tweet = user_twitter.update_status(status = message)
                if 'invite' in request.POST:
                    if request.POST['invite'] == 'true':
                        invite_id_obj = InviteId()
                        invite_obj = Invites()
                        invitees = request.POST['to'].split(',')
                        for eachInvitee in invitees:
                            doc = {
                                    'to_screenname':str(eachInvitee), 
                                    'from_username':str(request.user.username),
                                    'sent_time':str(time.mktime(datetime.datetime.now().timetuple())),
                                    'invite_id':ObjectId(str(request.POST['invite_id'])), 
                                    'message':str(str(message))}
                            invite_obj.save_invites(doc)
                        invite_id_obj.change_used_status(request.user.id, request.POST['invite_id'])
                        new_invite_id = invite_id_obj.get_unused_id(request.user.id)
                        new_invite_tweet = construct_invite_tweet(request, new_invite_id)
                        return HttpResponse(json.dumps({'status':'1', 
                            'new_invite_id':new_invite_id['uid']['id'], 
                            'new_invite_tweet':new_invite_tweet}))
                return HttpResponse(json.dumps({'status':1}))
            else:
                tweet = user_twitter.update_status(status = message+url, in_reply_to_status_id=)
            tweet_feed = TweetFeed()

            pic_url_list = []
            if tweet['entities'].get('media')!= None:
                for each in tweet['entities'].get('media'):
                    pic_url_list.append(each['media_url'])


            data = {'tweet_id': tweet['id'],
                    'parent_tweet_id': 0 if tweet['in_reply_to_status_id'] == None else tweet['in_reply_to_status_id'],
                    'status': message,
                    
                    'picture': pic_url_list,
                    
            }
           
            tweet_feed.insert_tweet(int(user_id),data)

            return HttpResponse(json.dumps({'status':1}))
        else:
            return HttpResponse(json.dumps({'status':1}))
            

    def post_tweet_admin(self, request):
        message = request.POST.get('message')
        if not request.user.is_authenticated():
            bot_twitter = get_twitter_obj(settings.BOT_ACCESS_TOKEN, settings.BOT_ACCESS_TOKEN_SECRET)
            if message != None and message != "":
                bot_twitter.update_status(status=message)
                return HttpResponse("{'status':1}")
        
        if request.user.is_authenticated():
            user_id = request.user.id
            st = SocialToken.objects.get(account__user__id=user_id)
            ACCESS_TOKEN = st.token
            ACCESS_TOKEN_SECRET = st.token_secret
            user_twitter = get_twitter_obj(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            if message != None and message != "":
                tweet = user_twitter.update_status(status = message)       
                return HttpResponse("{'status':1}")
        return HttpResponse("{'status':0}")

    def add_connection(self, request):
        trade_conn = TradeConnection()
        data = eval(request.POST.get('conn_data'))
        notification_obj = Notification()
        user_profile_obj = UserProfile()
        if data !=None and data !="":
            if data['status'] == 'buy_from':
                trade_conn.create_connection({'b_useruid': int(data['prof_id']), 'c_useruid': request.user.id})
                try:
                    buyer = user_profile_obj.get_profile_by_id(int(data['prof_id']))
                    notification_obj.save_notification({
                            'notification_to':buyer['username'], 
                            'notification_message':'@' + str(request.user.username) + ' added you as buyer. You can add contacts, connect and share your business products.', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added Buyer',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(request.user.username)
                            })
                except:
                    pass
            else:
                trade_conn.create_connection({'b_useruid': request.user.id, 'c_useruid': int(data['prof_id'])})
                try:
                    cust = user_profile_obj.get_profile_by_id(int(data['prof_id']))
                    notification_obj.save_notification({
                            'notification_to':cust['username'],
                            'notification_message':'@' + str(cust['username']) + ' said he sells products tp you. You can add contacts, connect and share your business products.', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added Seller',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(request.user.username)
                            })                
                except:
                    pass
            parameters = {}
            parameters['connections'], parameters['conn'] = get_connections(int(data['prof_id']))
            parameters['connections_str'] = str(json.dumps(parameters['connections']))
            parameters['profile_id'], parameters['user_id'] = int(data['prof_id']), request.user.id
            return render_to_response('conn_ajax.html', parameters)
        else:
            return HttpResponse("{'status':0}")

    def del_connection(self, request):
        trade_conn = TradeConnection()
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
        else:
            return HttpResponse("{'status':0}")

    def profile_user_delete_conn(self, request):
        trade_conn = TradeConnection()
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
            return HttpResponse("1")
        else:
            return HttpResponse('0')

    def save_adminfoods(self, request):
        if request.user.is_authenticated():
            tags = request.POST.get('tags')
            json_tags = json.loads(tags)
            insert_val = {'parent':1, 'adminfoods':json_tags}
            foods = AdminFoods()
            foods.set_tags(insert_val)
            # print foods.get_tags()
            return HttpResponse("1")
        else:
            return HttpResponse('0')

    def addcustomer(self, request):
        customer = Customer()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            customer.create_customer(data)

            notification_obj = Notification()
            user_profile_obj = UserProfile()
            try:
                cust = user_profile_obj.get_profile_by_id(int(data['customeruid']))
                seller  = user_profile_obj.get_profile_by_id(int(data['useruid']))
                notification_obj.save_notification({
                        'notification_to':seller['username'], 
                        'notification_message':'@' + str(cust['username']) + ' said, he is your customer. You can connect to him and increase your business value.', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Added Customer',
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(cust['username'])
                        })
            except:
                pass

            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deletecustomer(self, request):
        customer = Customer()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            customer.delete_customer(useruid = data['useruid'], customer_id = data['customeruid'])
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def addmember(self, request):
        org = Organisation()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.create_member(data)
            
            notification_obj = Notification()
            user_profile_obj = UserProfile()
            try:
                mem = user_profile_obj.get_profile_by_id(int(data['memberuid']))
                org  = user_profile_obj.get_profile_by_id(int(data['orguid']))
                # print org
                notification_obj.save_notification({
                        'notification_to':org['username'], 
                        'notification_message':'@' + str(mem['username']) + ' added himself as the member of your Organisation. You can connect with him and increase value of your Organisation', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Added member',
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(mem['username'])
                        })
            except:
                pass

            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deletemember(self, request):
        org = Organisation()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.delete_member(orguid = data['orguid'], member_id = data['memberuid'])
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def addteam(self, request):
        team = Team()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            team.create_member(data)

            notification_obj = Notification()
            user_profile_obj = UserProfile()
            mem = user_profile_obj.get_profile_by_id(int(data['memberuid']))
            org  = user_profile_obj.get_profile_by_id(int(data['orguid']))
            try:
                notification_obj.save_notification({
                        'notification_to':org['username'], 
                        'notification_message':'@' + str(mem['username']) + ' said he/she works inyour Organisation.', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Added Team',
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(mem['username'])
                        })
            except:
                pass
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deleteteam(self, request):
        team = Team()
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

            notification_obj = Notification()
            user_profile_obj = UserProfile()
            try:
                busss  = user_profile_obj.get_profile_by_id(int(data['business_id']))
                rec  = user_profile_obj.get_profile_by_id(int(data['recommender_id']))
                notification_obj.save_notification({
                        'notification_to':busss['username'], 
                        'notification_message':'@' + str(rec['username']) + ' vouched for your food ' + str(data['food_name']) + '.', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Vouched Food',
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(rec['username'])
                        })            
            except:
                pass
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
                spam_obj = Spam()
                result = spam_obj.check_spam_by(change_id, int(request.user.id))
                try:
                    if(len(result) >0):
                        return HttpResponse(json.dumps({'status':0, 'activity':'spam', '_id':change_id, 
                            'message':'You have already marked it as spam.'}))
                    else:
                        spam_obj.mark_spam(int(request.user.id), change_id)
                        return HttpResponse(json.dumps({'status':1, 'activity':'spam', '_id':change_id, 
                            'message':'You marked this tweet as spam.'}))
                except:
                    spam_obj.mark_spam(int(request.user.id), change_id)
                    return HttpResponse(json.dumps({'status':1, 'activity':'spam', '_id':change_id, 
                        'message':'You marked this tweet as spam.'}))                    

            if task == 'delete':
                print change_id
                tweet_feed_obj.delete_tweet(request.user.id,int(change_id))
                return HttpResponse(json.dumps({'status':'1', 'activity':'deleteTweet', '_id':change_id}))

            if task == 'follow':
                friend_obj = Friends()
                fid = friend_obj.get_friend_id(request.user.username, change_id)
                data = tweet_feed_obj.follow_user(fid, request.user.username, request.user.id)
                return HttpResponse(json.dumps(data))

            if task == 'buyFrom' or task == 'sellTo':
                tc_object = TradeConnection()
                if task == 'buyFrom':
                    b_id = int(change_id)
                    c_id = int(request.user.id)

                elif task == 'sellTo':
                    b_id = int(request.user.id)
                    c_id = int(change_id)

                result = tc_object.search_connectedness(b_id,c_id)

                try:
                    if (len(result) > 0):
                        return HttpResponse (json.dumps({'status':0, 'activity':'buyFrom', '_id':change_id, 
                            'message':'You are already connected.'}))
                    else:
                        tc_object.create_connection({'c_useruid':c_id , 'b_useruid': b_id})
                        return HttpResponse (json.dumps({'status':1, 'activity':'buyFrom', '_id':change_id, 
                            'message':'You are connected.'}))
                except:
                    tc_object.create_connection({'c_useruid':c_id , 'b_useruid': b_id})
                    return HttpResponse (json.dumps({'status':1, 'activity':'buyFrom', '_id':change_id, 
                        'message':'You are connected.'}))

            if task == 'markMember':
                memberuid = int(request.user.id)
                orgid = int(change_id)
                org_obj = Organisation()
                result = org_obj.check_member(orgid, memberuid)
                try:
                    if(len(result)>0):
                        return HttpResponse(json.dumps({'status':0, 'activity':'markMember', '_id':change_id, 
                            'message':'You are already a member.'}))
                    else:        
                        org_obj.create_member({'memberuid': int(memberuid), 'orguid': int(orgid)})
                        return HttpResponse(json.dumps({'status':1, 'activity':'markMember', '_id':change_id, 
                            'message':'You are now a member.'}))
                except:
                    org_obj.create_member({'memberuid': int(memberuid), 'orguid': int(orgid)})
                    return HttpResponse(json.dumps({'status':1, 'activity':'markMember', '_id':change_id, 
                            'message':'You are now a member.'}))
        else:
            return HttpResponse(json.dumps({'status':'0', 'message':'You are not authorized for this request.'}))


    def archive_notification(self,request):
        #print request.POST
        notification_id = request.POST['notification_id']
        notifying_user_name = request.POST['notifying_user_name']
        if request.user.is_authenticated:
            notification_obj = Notification()
            result = notification_obj.change_notification_archived_status(notification_id)
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized for this action.'}))
    
    def get_notices_paginated(self, request):
        page_num = request.POST['pgnum']
        n_type = request.POST['n_type']

        if request.user.is_authenticated:
            parameters ={}
            user_name = request.user.username
            notices = Notification()
            my_notifications = notices.get_notification(user_name, page_number= int(page_num), n_type = n_type)

            parameters['archived_notification_count'] = my_notifications['archived_notification_count']
            parameters['all_notification_count'] = my_notifications['all_notification_count']
            parameters['unread_notification_count'] = my_notifications['unread_notification_count']
            
            myNotice = []
            for eachNotification in my_notifications['notifications']:
                processed_notice = {}
                user_profile_obj = UserProfile()
                notifying_user_profile = user_profile_obj.get_profile_by_username(eachNotification['notifying_user'])
                try:
                    if (notifying_user_profile['email'] != ''):
                        processed_notice['notifying_user_email'] = notifying_user_profile['email']
                except:
                    processed_notice['notifying_user_email'] = User.objects.get(username = eachNotification['notifying_user']).email
                try:                    
                    if (notifying_user_profile['screen_name'] != ''):
                        processed_notice['notifying_user_screenname'] = notifying_user_profile['screen_name']
                except:
                    processed_notice['notifying_user_screenname'] = SocialAccount.objects.get(user__id = request.user.id).extra_data['screen_name']
                processed_notice['my_email'] = User.objects.get(username = request.user.username).email
                processed_notice['notification_id'] = eachNotification['uid']['id']
                processed_notice['notifying_user'] = eachNotification['notifying_user']
                processed_notice['notification_message'] = eachNotification['notification_message'][0:50] + '....'
                processed_notice['notification_message_full'] = eachNotification['notification_message']
                processed_notice['time_elapsed'] = calculate_time_ago(eachNotification['notification_time'])
                processed_notice['notifying_user_profile'] = notifying_user_profile
                processed_notice['notification_view_status'] = eachNotification['notification_view_status']
                myNotice.append(processed_notice)


            parameters['notifications'] = myNotice
            return HttpResponse(json.dumps(parameters))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized for this action.'}))    

    def change_notification_view_status(self, request):
        if request.user.is_authenticated:
            notice_obj = Notification()
            notification_id = request.POST['notification_id']
            this_not = notice_obj.get_notification_by_id(notification_id)
            notice_obj.change_notification_view_status(notification_id)            
            if this_not['notification_view_status'] == 'false':
                return HttpResponse(json.dumps({'status':1, 'notification_id':notification_id, 'message':'Successfully changed status','already':'false'}))
            else:
                return HttpResponse(json.dumps({'status':1, 'notification_id':notification_id, 'message':'Successfully changed status', 'already':'true'})) 
        else:
            return HttpResponse(json.dumps({'status':0, 'activity':'notification status change', 'message':'You are not authorized to perform this action.'}))

    def un_archive_notification(self, request):
        if request.user.is_authenticated:
            notice_obj = Notification()
            notification_id = request.POST['notification_id']
            notice_obj.un_archive_notification(notification_id)            
            return HttpResponse(json.dumps({'status':1, 'notification_id':notification_id, 'message':'Successfully changed status'}))
        else:
            return HttpResponse(json.dumps({'status':0, 'activity':'notification status change', 'message':'You are not authorized to perform this action.'}))

    def get_notification_counts(self, request):
        if request.user.username:
            notice_obj = Notification()
            notices = notice_obj.get_notification_counts(request.user.username)
            return HttpResponse(json.dumps(notices))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized to perform this action.'}))
