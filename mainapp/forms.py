from django import forms
from django.contrib.auth.models import User
from mainapp.classes.TweetFeed import UserProfile, Notification, Invites
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
from classes.Tags import Tags
from pygeocoder import Geocoder
import datetime
import time

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

    def save(self, user):
        # code to save form fields to mongodb
        # convert zip code to longitude and latitude
        #zip_code = self.cleaned_data['zip_code'] 
        lat = float(self.cleaned_data['lat'])
        lon = float(self.cleaned_data['lng'])
        try:
            addr = Geocoder.reverse_geocode(float(lat),float(lon))
            print addr
            address = str(addr)
            postal_code = str(addr.postal_code) 
            print postal_code           
        except:
            results = Geocoder.geocode('London, UK')
            address = str(results)
            lat, lon  = float(results.latitude), float(results.longitude)
            postal_code = str(results.postal_code)

        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        #addr = social_account.extra_data['location']
        data = {'useruid': str(user.id), 'sign_up_as': str(self.cleaned_data['sign_up_as']),
        		'type_user': str(self.cleaned_data['type_user']), 
                'zip_code': str(postal_code),
        		'address': address,
                'latitude': lat,
                'longitude': lon,
                'name': social_account.extra_data['name'],
                'description': social_account.extra_data['description'],
                'username': social_account.extra_data['screen_name'],
                'profile_img': social_account.extra_data['profile_image_url']
        }
        userprofile.create_profile(data)
        
        notification_obj = Notification()
        invites_obj = Invites()
        twitter_username = social_account.extra_data['screen_name']
        invitees_for_this_user = invites_obj.check_invitees(twitter_username) 
        now = datetime.datetime.now()
        notification_time  = time.mktime(now.timetuple())
        if(len(invitees_for_this_user)>0):
            for eachInvitees in invitees_for_this_user:
                notification_obj.save_notification({
                    'notification_to':eachInvitees['from_username'], 
                    'notification_message':'@' + str(twitter_username) + ' has accepted your invitation and joined FoodTrade. You can connect and add him to your contacts.', 
                    'notification_time':notification_time,
                    'notification_type':'Invitation Accept',
                    'notification_view_status':'false',
                    'notifying_user':str(twitter_username)
                    })
        #print "saved", data
        return HttpResponseRedirect('/activity/')