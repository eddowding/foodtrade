from django import forms
from django.contrib.auth.models import User
from mainapp.classes.TweetFeed import UserProfile, Notification, Invites, InviteAccept
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
from classes.Tags import Tags
from pygeocoder import Geocoder
import datetime,time

class SignupForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Username',
     'class' : 'form-control'})) 
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'Email',
     'class' : 'form-control'}))
    sign_up_as = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Sign up as',
     'class' : 'form-control'}))

    address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': u'Please select an address.',
     'class' : 'form-control', 'value':'London,UK'}))

    type_user = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    lat = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    lng = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        self.request =request
        super(SignupForm, self).__init__(*args, **kwargs)

    def save(self, user):
        lat = float(self.cleaned_data['lat'])
        lon = float(self.cleaned_data['lng'])
        invite_id = ''
        try:
            invite_id = self.request.session['invite_id']
        except:
            invite_id = ''
        try:
            addr = Geocoder.reverse_geocode(float(lat),float(lon))

            address = str(addr)
            postal_code = str(addr.postal_code) 
        
        except:
            results = Geocoder.geocode('London, UK')
            address = str(results)
            lat, lon  = float(results.latitude), float(results.longitude)
            postal_code = str(results.postal_code)

        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        print self.request
        print invite_id, "Roshan Bhandari"

        data = {'useruid': int(user.id), 'sign_up_as': str(self.cleaned_data['sign_up_as']),
        		'type_user': str(self.cleaned_data['type_user']).split(","), 
                'zip_code': str(postal_code),
                'latlng' : {"type" : "Point", "coordinates" : [float(lon),float(lat)] },
        		'address': address,
                'name': social_account.extra_data['name'],
                'description': social_account.extra_data['description'],
                'username' : user.username,
                'twitter_name': social_account.extra_data['screen_name'],
                'profile_img': social_account.extra_data['profile_image_url'],
                'updates': [],
                'foods':[],
                'organisations':[]
        }

        userprofile.create_profile(data)

        if invite_id != '':
            invititation_to = user.username
            screen_name = social_account.extra_data['screen_name']
            invite_accept_obj = InviteAccept()
            invites_obj = Invites()
            print screen_name, invite_id
            result = invites_obj.check_invited_by_invite_id(str(screen_name), str(invite_id))
            print result
            try:
                if(len(result)>0):
                    invited_by = result['from_username']
                    invite_accept_obj.insert_invite_accept(invite_id, invited_by, invititation_to)
                    
                    notification_obj = Notification()
                    invites_obj = Invites()
                     
                    notification_obj.save_notification({
                        'notification_to':str(invited_by), 
                        'notification_message':'@' + str(screen_name) + ' has accepted your invitation and joined FoodTrade. You can connect and add him to your contacts.', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Invitation Accept',
                        'notification_view_status':'false',
                        'notification_archived_status':'false',
                        'notifying_user':str(screen_name)
                        })

                    now = datetime.datetime.now()
                    notification_time  = time.mktime(now.timetuple())

                    invitees_for_this_user = invites_obj.check_invitees(screen_name)
                    if(len(invitees_for_this_user)>0):
                        for eachInvitees in invitees_for_this_user:
                            notification_obj.save_notification({
                        'notification_to':eachInvitees['from_username'], 
                        'notification_message':'@' + str(screen_name) + ' joined FoodTrade. You can add to your contacts and connect.', 
                        'notification_time':time.mktime(datetime.datetime.now().timetuple()),
                        'notification_type':'Joined FoodTrade',
                        'notification_view_status':'false',
                        'notification_arcived_status':'false',
                        'notifying_user':str(screen_name)
                        })
            except:
                return HttpResponseRedirect('/activity/')
        return HttpResponseRedirect('/activity/')                
