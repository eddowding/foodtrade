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
     'class' : 'form-control', 'value':''}))

    type_user = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    lat = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    lng = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    # formatted_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
    #  'class' : 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        self.request =request
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'

    def save(self, user):
        try:
            addr = self.cleaned_data['address']
            lat = self.cleaned_data['lat']
            lon = self.cleaned_data['lng']
            # print lat, lon, len(lat), len(lon)
            if len(lat) == 0 and len(lon) == 0:
                addr_geo = Geocoder.geocode(addr.strip())
                lat = float(addr_geo.latitude)
                lon = float(addr_geo.longitude)
                postal_code = str(addr_geo.postal_code)
                # print addr, lat, lon, postal_code, "inside try if"
            else:
                result = Geocoder.reverse_geocode(float(lat),float(lon))
                postal_code = str(result.postal_code)
                # print addr, lat, lon, postal_code, "inside try else"

        except:
            lat, lon, addr,postal_code = 51.5072 , -0.1275, "3 Whitehall, London SW1A 2EL, UK", "SW1 A 2EL"
            # print addr, lat, lon, postal_code, "inside exception"
        
        invite_id = ''
        try:
            invite_id = self.request.session['invite_id']
        except:
            invite_id = ''

        address = addr 

        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        data = {'useruid': int(user.id), 'sign_up_as': str(self.cleaned_data['sign_up_as']),
        		'type_user': str(self.cleaned_data['type_user']).split(","), 
                'zip_code': str(postal_code),
                'latlng' : {"type" : "Point", "coordinates" : [float(lon),float(lat)] },
        		'address': address,
                'name': social_account.extra_data['name'],
                'email': str(self.cleaned_data['email']), 
                'description': social_account.extra_data['description'],
                'username' : user.username,
                'screen_name': social_account.extra_data['screen_name'],
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
            result = invites_obj.check_invited_by_invite_id(str(screen_name), str(invite_id))
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
                        'notification_archived_status':'false',
                        'notifying_user':str(screen_name)
                        })
            except:
                return HttpResponseRedirect('/activity/')
        return HttpResponseRedirect('/activity/')                