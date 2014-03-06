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
from mainapp.classes.TweetFeed import TradeConnection, UserProfile, Food, Customer, Organisation, Team, RecommendFood, Notification, Friends, Spam, InviteId, Invites, UnapprovedFood, ApprovedFoodTags
from AjaxSearch import AjaxSearch
from pygeocoder import Geocoder
from mainapp.profilepage import get_connections, get_all_foods, get_organisations
from mainapp.views import get_twitter_obj
import datetime, time
from bson.objectid import ObjectId
from mainapp.views import calculate_time_ago
from django.contrib.auth.models import User
from mainapp.bitly import construct_invite_tweet, shorten_url
# from validate_email import validate_email
# consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
# consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
# admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'


class AjaxHandle(AjaxSearch):
    """docstring for AjaxHandle"""
    def __init__(self):
        pass
        
    def create_fake_profile(self, invitee_name, username):
        '''
            This function checks if the invited user is already a member or not.Then
            If it is already a member it bypasses that and if not then it creates a 
            membership in the site in such a way that his/her profile can be edited 
            by admin and the flag is_unknown_profile is raised in the userinfo 
            collection.
        '''
        user_profile_obj = UserProfile()
        registered_user = user_profile_obj.get_profile_by_username(invitee_name)


        min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1

        if registered_user == None or len(registered_user) == 0:
            friend_obj = Friends()
            invited_friend = friend_obj.get_friend_from_screen_name(invitee_name.replace('@',''), username)
            data = {
                'is_unknown_profile': 'true',
                'recently_updated_by_super_user': 'false',
                'address' : invited_friend['friends']['location'],
                'email' : '',
                'description' : invited_friend['friends']['description'],
                'foods': [],
                'name' : invited_friend['friends']['name'],
                'phone_number' : '',
                'profile_img':invited_friend['friends']['profile_image_url'],
                'sign_up_as': 'unclaimed',
                'type_user':[],
                'updates': [],
                'screen_name': invited_friend['friends']['screen_name'],
                'Organisations':[],
                'useruid': min_user_id,
                'username':invited_friend['friends']['screen_name'],
                'subscribed':0,
                'newsletter_freq':'Weekly'
            }
            try:
                location_res = Geocoder.geocode(invited_friend['friends']['location'])
                data['latlng'] = {"type":"Point","coordinates":[float(location_res.longitude) ,float(location_res.latitude)]}
                data['zip_code'] = str(location_res.postal_code)
            except:
                lat, lon, addr,postal_code = 51.5072 , -0.1275, "3 Whitehall, London SW1A 2EL, UK", "SW1 A 2EL"
                data['address'] = addr
                data['latlng'] = {"type":"Point","coordinates" : [float(lon),float(lat)]}
                data['location_default_on_error'] = 'true'
            user_profile_obj.create_profile(data)
            return {'status':1}
        else:
            return {'status':0}

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
        parent_tweet_id = request.POST.get("parentid",0)

        only_foodtrade = request.POST.get('foodtrade_only',"false")

        prof_url = " http://"+request.META['HTTP_HOST']+"/profile/"+request.user.username

        if parent_tweet_id != 0:
            tf_obj = TweetFeed()
            tf_user = tf_obj.get_user_by_tweet(str(parent_tweet_id))
            parent_username = tf_user['username']
            prof_url = " http://"+request.META['HTTP_HOST']+"/"+str(parent_username)+"/post/"+str(parent_tweet_id)
        url = shorten_url(prof_url)

        if message != None and message != "":
            '''For invitation message only.'''
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
                                    'message':str(message)}
                            '''Save the invited ones to invites collection'''
                            invite_obj.save_invites(doc)
                            
                            ''' Creating the unused profile of each Invited. '''
                            self.create_fake_profile(str(eachInvitee), request.user.username)

                        '''Change the used status flag of the invite ID generated.'''
                        invite_id_obj.change_used_status(request.user.id, request.POST['invite_id'])

                        '''Generate new invite ID.'''
                        new_invite_id = invite_id_obj.get_unused_id(request.user.id)

                        '''Construct New Invite URL.'''
                        new_invite_tweet = construct_invite_tweet(request, new_invite_id)
                        return HttpResponse(json.dumps({'status':'1', 
                            'new_invite_id':new_invite_id['uid']['id'], 
                            'new_invite_tweet':new_invite_tweet}))
                return HttpResponse(json.dumps({'status':1}))
            else:
                pic_url_list = []
                if only_foodtrade == "false":
                    tweet = user_twitter.update_status(status = message+url, in_reply_to_status_id=parent_tweet_id)
                    tweet_id = str(tweet['id'])
                    if tweet['entities'].get('media')!= None:
                        for each in tweet['entities'].get('media'):
                            pic_url_list.append(each['media_url'])
                else:
                    import uuid
                    tweet_id = uuid.uuid4()

            tweet_feed = TweetFeed()
            data = {'tweet_id': str(tweet_id),
                    'parent_tweet_id': str(parent_tweet_id),
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
                    if buyer['username'] != str(request.user.username):
                        notification_obj.save_notification({
                                'notification_to':buyer['username'], 
                                'notification_message':'@' + str(request.user.username) + ' added you as buyer. You can add contacts, connect and share your business products.', 
                                'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                                'notification_type':'Added Buyer',
                                'notification_view_status':'false',
                                'notification_archived_status':'false',
                                'notifying_user':str(request.user.username)
                                })
                    else:
                        pass
                except:
                    pass
            else:
                trade_conn.create_connection({'b_useruid': request.user.id, 'c_useruid': int(data['prof_id'])})
                try:
                    cust = user_profile_obj.get_profile_by_id(int(data['prof_id']))
                    if cust['username'] != str(request.user.username):
                        notification_obj.save_notification({
                                'notification_to':cust['username'],
                                'notification_message':'@' + str(cust['username']) + ' said he sells products to you. You can add contacts, connect and share your business products.', 
                                'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                                'notification_type':'Added Seller',
                                'notification_view_status':'false',
                                'notification_archived_status':'false',
                                'notifying_user':str(request.user.username)
                                })                
                    else:
                        pass
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
        else:
            return HttpResponse("{'status':0}")

    def third_party_add_org(self, request):
        org = Organisation()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.create_member(data)
            parameters = {}
            parameters['organisations'] = get_organisations(int(data['memberuid']))
            parameters['profile_id'], parameters['user_id'] = int(data['memberuid']), request.user.id

            notification_obj = Notification()
            user_profile_obj = UserProfile()
            try:
                mem = user_profile_obj.get_profile_by_id(int(data['memberuid']))
                org  = user_profile_obj.get_profile_by_id(int(data['orguid']))
                if org['username'] != str(mem['username']):
                    notification_obj.save_notification({
                            'notification_to':org['username'], 
                            'notification_message':'@' + str(mem['username']) + ' added himself as the member of your Organisation. You can connect with him and increase value of your Organisation', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added member',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(mem['username'])
                            })
                else:
                    pass
            except:
                pass
            return render_to_response('ajax_org.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def third_party_delete_org(self, request):
        org = Organisation()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            org.delete_member(orguid = data['orguid'], member_id = data['memberuid'])
            
            parameters = {}
            parameters['organisations'] = get_organisations(int(data['memberuid']))
            parameters['profile_id'], parameters['user_id'] = int(data['memberuid']), request.user.id
            return render_to_response('ajax_org.html', parameters, context_instance=RequestContext(request))
        else:
            return HttpResponse("{'status':0}")

    def addfood(self, request):
        foo = Food()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.create_food(data)
            notice_obj = Notification()
            user_profile_obj = UserProfile()
            
            created_by = user_profile_obj.get_profile_by_id(int(request.user.id))
            created_on  = user_profile_obj.get_profile_by_id(int(data['useruid']))
            if created_on['username'] != created_by['username']:
                notice_obj.save_notification({
                        'notification_to':created_on['username'], 
                        'notification_message':'@' + str(created_by['username']) + ' added ' + str(data['food_name'] + ' on your profile.'), 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Added Food',
                        'food_name':data['food_name'],
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(created_by['username'])
                        })
            else:
                pass

            parameters = {}
            parameters['all_foods'] = get_all_foods(int(data['useruid']), request.user.id)
            parameters['profile_id'], parameters['user_id'] = int(data['useruid']), request.user.id
            return render_to_response('ajax_food.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def addnewfood(self, request):
        foo = UnapprovedFood()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.create_food(data)
            print 'new food ', data['food_name'], ' created !!'
            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def deletefood(self, request):
        foo = Food()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.delete_food(useruid = data['useruid'], food_name = data['food_name']);
            parameters = {}
            parameters['all_foods'] = get_all_foods(int(data['useruid']), request.user.id)
            parameters['profile_id'], parameters['user_id'] = int(data['useruid']), request.user.id
            return render_to_response('ajax_food.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")    

    def delete_unapproved_food(self, request):
        foo = UnapprovedFood()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            foo.delete_food(food_name = data['food_name']);
            
            twt = TweetFeed()
            twt.update_data(data['useruid'])

            return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")            

    def trash_unapproved_food(self, request):
        foo = UnapprovedFood()
        foods = Food()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            # delete from unapproved
            foo.delete_food(food_name = data['food_name']);
            print 'unapproved food ', data['food_name'], ' deleted'
            all_foods = foods.get_foods_by_food_name(data['food_name'])
            # delete all foods with this name
            for each in all_foods:
                foods.delete_food(food_name = each['food_name'], useruid = each['useruid']);
                print each['useruid'] , ' user food ', each['food_name'], ' deleted'
            return HttpResponse("{'status':1}")
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
                if seller['username'] != cust['username']:
                    notification_obj.save_notification({
                            'notification_to':seller['username'], 
                            'notification_message':'@' + str(cust['username']) + ' said, he is your customer. You can connect to him and increase your business value.', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added Customer',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(cust['username'])
                            })
                else:
                    pass
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
                if org['username'] != mem['username']:
                    notification_obj.save_notification({
                            'notification_to':org['username'], 
                            'notification_message':'@' + str(mem['username']) + ' added himself as the member of your Organisation. You can connect with him and increase value of your Organisation', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added member',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(mem['username'])
                            })
                else:
                    pass
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
                if org['username'] != mem['username']:
                    notification_obj.save_notification({
                            'notification_to':org['username'], 
                            'notification_message':'@' + str(mem['username']) + ' said he/she works in your Organisation.', 
                            'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                            'notification_type':'Added Team',
                            'notification_view_status':'false',
                            'notification_archived_status':'false',
                            'notifying_user':str(mem['username'])
                            })
                else:
                    pass
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

    def approve_tag(self, request):
        foo = ApprovedFoodTags()
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            myfood = foo.get_food_by_name(str(data['food_name']))
            print 'new tag ', data['tags'], ' approved !!'
            if myfood == None:
                foo.create_food(data)
            else:
                if data['status'] == 'add':
                    data['tags'] +=','+myfood['tags']
                else:
                    tags_list = myfood['tags'].split(',')
                    if data['tags'] in tags_list:
                        tags_list.remove(data['tags'])
                        data['tags'] = ','.join(tags_list)
                foo.update_food(data['food_name'], data['tags'])
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
            if email.send_mail(subject, template_content = [{'name':'main', 'content':body}], to=[{'email':receiver_email}]):
                return HttpResponse("{'status':1}")
        return HttpResponse("{'status':0}")

    def vouch_for_food(self, request):
        recomm = RecommendFood()
        #print request.POST.get('data')
        data = request.POST.get('data')
        print 'vouch data', type(data), data
        data = eval(request.POST.get('data'))
        if data !=None and data !="":
            if data['action'] == 'add':
                recomm.create_recomm(data)

                notification_obj = Notification()
                user_profile_obj = UserProfile()
                try:
                    busss  = user_profile_obj.get_profile_by_id(int(data['business_id']))
                    rec  = user_profile_obj.get_profile_by_id(int(data['recommender_id']))
                    if busss['username'] != rec['username']:
                        notification_obj.save_notification({
                                'notification_to':busss['username'], 
                                'notification_message':'@' + str(rec['username']) + ' vouched for your food ' + str(data['food_name']) + '.', 
                                'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                                'notification_type':'Vouched Food',
                                'notification_view_status':'false',
                                'notification_archived_status':'false',
                                'notifying_user':str(rec['username'])
                                })            
                    else:
                        pass
                except:
                    pass
            else:
                recomm.delete_recomm(data['business_id'], data['food_name'], data['recommender_id'])

            parameters = {}
            parameters['all_foods'] = get_all_foods(int(data['business_id']), request.user.id)
            parameters['profile_id'], parameters['user_id'] = int(data['business_id']), request.user.id
            return render_to_response('ajax_food.html', parameters, context_instance=RequestContext(request))
            # return HttpResponse("{'status':1}")
        else:
            return HttpResponse("{'status':0}")

    def getnotification(self, request):
        username = request.user.username
        notification_obj  = Notification()
        return notification_obj.get_notification(username)

    def change_notification_status(self, request):
    	'''Changes the status of Notification'''
        if request.method == 'POST' and request.user.is_authenticated:
            notification_obj = Notification()
            return notification_obj.change_notification_status(request.user.username)
        else:
            return HttpResponse(json.dumps({'status':'0'}))

    def validate_logged_in(self,request):
    	'''Validates if the user is logged in or not.'''
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'status':'1'}))
        return HttpResponse(json.dumps({'status':'0'}))

    def get_friends_paginated(self,request):
    	'''Returns a list of pagiated friends'''
        if request.method == 'POST' and request.user.is_authenticated:
            page_num = request.POST['pgnum']
            friends_obj = Friends()
            return HttpResponse(json.dumps(friends_obj.get_paginated_friends(request.user.username, page_num)))
        else:
            return HttpResponse(json.dumps({'status':'0'}))
    def search_friend(self, request):
    	'''This function is used to search friends from the invite page'''
        if request.method == 'POST' and request.user.is_authenticated:
            query = request.POST['query']
            friends_obj = Friends()
            result = friends_obj.search_friends(request.user.username, query)
            return HttpResponse(json.dumps({'result':result, 'result_count':len(result)}))
        else:
            return HttpResponse(json.dumps({'status':'0'}))

    def activity_handle(self,request):
    	'''This function is used for tasks on the dropdown in activity page.'''
        if request.user.is_authenticated and request.method == 'POST':
            task = request.POST['task']
            change_id = request.POST['changeID']
            user = request.user.username
            tweet_feed_obj = TweetFeed()

            if task == 'spam':
            	'''Marking spam.'''
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
            	'''Deleting a Tweet'''
                #print change_id
                if request.user.is_superuser or request.user.is_authenticated:
                    tweet_feed_obj.delete_tweet(request.user.id,str(change_id))
                return HttpResponse(json.dumps({'status':'1', 'activity':'deleteTweet', '_id':change_id}))

            if task == 'follow':
            	'''Marking follower'''
                friend_obj = Friends()
                fid = friend_obj.get_friend_id(request.user.username, change_id)
                data = tweet_feed_obj.follow_user(fid, request.user.username, request.user.id)
                return HttpResponse(json.dumps(data))

            if task == 'buyFrom' or task == 'sellTo':
                tc_object = TradeConnection()
                if task == 'sellTo':
                    '''If adds as sells to'''
                    b_id = int(change_id)
                    c_id = int(request.user.id)

                elif task == 'buyFrom':
                    '''Marks buys from'''
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
                '''If marks as Member'''
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
        '''This function is used to archive a notification.'''
        notification_id = request.POST['notification_id']
        notifying_user_name = request.POST['notifying_user_name']
        if request.user.is_authenticated:
            notification_obj = Notification()
            result = notification_obj.change_notification_archived_status(notification_id)
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized for this action.'}))
    
    def get_notices_paginated(self, request):
    	'''This function returns the paginated list of notifications.'''
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
        '''This function changes the notification status from read to unread.'''
        if request.user.is_authenticated:
            notice_obj = Notification()
            notification_id = request.POST['notification_id']
            this_not = notice_obj.get_notification_by_id(notification_id)
            notice_obj.change_notification_view_status(notification_id)            
            if this_not['notification_view_status'] == 'false':
                return HttpResponse(json.dumps({'status':1, 
                	'notification_id':notification_id, 
                	'message':'Successfully changed status','already':'false'}))
            else:
                return HttpResponse(json.dumps({'status':1, 
                	'notification_id':notification_id, 
                	'message':'Successfully changed status', 'already':'true'})) 
        else:
            return HttpResponse(json.dumps({'status':0, 
            	'activity':'notification status change', 
            	'message':'You are not authorized to perform this action.'}))

    def un_archive_notification(self, request):
        '''This function un-archives a notification.'''
        if request.user.is_authenticated:
            notice_obj = Notification()
            notification_id = request.POST['notification_id']
            notice_obj.un_archive_notification(notification_id)            
            return HttpResponse(json.dumps({'status':1, 
            	'notification_id':notification_id, 
            	'message':'Successfully changed status'}))
        else:
            return HttpResponse(json.dumps({'status':0, 
            	'activity':'notification status change', 
            	'message':'You are not authorized to perform this action.'}))

    def get_notification_counts(self, request):
        '''This function returns the Notification(Inbox) Count.'''
        if request.user.username:
            notice_obj = Notification()
            notices = notice_obj.get_notification_counts(request.user.username)
            return HttpResponse(json.dumps(notices))
        else:
            return HttpResponse(json.dumps({'status':0, 
            	'message':'You are not authorized to perform this action.'}))

    def get_unclaimed_paginated(self, request):
        '''This function returns unclaimed profiles paginated.'''
        print request.POST
        parameters = {}  
        user_profile_obj = UserProfile()  
        tags = Tags()
        parameters['all_tags'] = tags.get_tags()
        if request.user.is_authenticated() and request.user.is_superuser:
            unclaimed_profiles = user_profile_obj.get_unclaimed_profile_paginated(int(request.POST['current_page']))
            parameters['unclaimed_profiles'] = unclaimed_profiles
            return HttpResponse(json.dumps(parameters))
        else:
            return HttpResponse(json.dumps({'status':0, 
                'message':'You are not authorized to perform this action.'}))

    def unclaimed_profiles_bulk_update(self, request):
        if request.user.is_authenticated and request.user.is_superuser and request.method =="POST":
            #print request.POST
            uname = request.POST['uname'].split(',')
            data = eval(request.POST['data'])
            for eachUser in uname:
                try:
                    sua = data[eachUser]['sign_up_as']
                    formatted_address = data[eachUser]['address']
                    name = data[eachUser]['name']
                    
                    type_user = data[eachUser]['type'].split(',')
                    n_type_user = []
                    for eachType in type_user:
                        if eachType == '':
                            n_type_user.append(eachType)
                    try:
                        add_res = Geocoder.geocode(str(formatted_address))
                    except:
                        add_res = Geocoder.geocode(str("London, UK"))

                    print sua, formatted_address, name, type_user, add_res

                    user_profile_obj = UserProfile()
                    user_profile_obj.update_profile_fields({'username':eachUser},
                        {'latlng.coordinates':list([float(add_res[0].longitude),float(add_res[0].latitude)]),
                        'address':str(formatted_address),
                        'sign_up_as':str(sua),
                        'type_user':type_user,
                        'zip_code': str(add_res[0].postal_code),
                        'name':str(name),
                        'recently_updated_by_super_user':'true'})
                except:
                    continue
            return HttpResponse(json.dumps({'users':uname, 'status':'1'}))
        else:
            return HttpResponse(json.dumps({'status':0, 
                'message':'You are not authorized to perform this action.'}))

    def check_email_address(self, request):
        if request.user.is_authenticated:
            user_profile_obj = UserProfile()
            email = request.POST.get('email')
            if request.user.is_superuser:
                username = request.POST.get('username')
            else:
                username = request.user.username
            if user_profile_obj.check_valid_email(username, email):
                return HttpResponse(json.dumps({'status':1, 'valid':'yes'}))
            else:
                return HttpResponse(json.dumps({'status':1, 'valid':'no'}))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized to perform this action.'}))

    def search_users(self, request):
        if request.user.is_authenticated:
            q = request.POST.get('q')
            user_id = request.user.id
            tweet_feed_obj = TweetFeed()
            results = tweet_feed_obj.search_tweeter_users(user_id, q)
            return HttpResponse(json.dumps({'results':results}))
        else:
            return HttpResponse(json.dumps({'status':0, 'message':'You are not authorized to perform this action.'}))        

