from django import forms
from django.contrib.auth.models import User
from mainapp.classes.TweetFeed import UserProfile, Notification, Invites, InviteAccept, TradeConnection
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
from classes.Tags import Tags
from pygeocoder import Geocoder
import datetime,time
from mainapp.classes.TweetFeed import Food
from mainapp.models import FoodPhoto
from mainapp.classes.mailchimp import MailChimp
from django.conf import settings

class FoodForm(forms.Form):
    food_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'form-control'})) 
    food_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'})) 
    profile_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'})) 
    food_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    food_photo = forms.ImageField(required=False)
    food_duplicate = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)

    def save(self):
        food_description = self.cleaned_data['food_description']
        food_tags = self.cleaned_data['food_tags']
        profile_id = int(self.cleaned_data['profile_id'])
        food_name = self.cleaned_data['food_name']
        food_detail = Food()
        food_photo = self.cleaned_data['food_photo']
        food_duplicate = self.cleaned_data['food_duplicate']
        data = {'food_name': food_name, 'useruid': profile_id, 'description': food_description,
        'food_tags': food_tags, 'photo_url': ''}
        if food_photo == None:
            if food_duplicate != '':
                data['photo_url'] = food_duplicate
            food_detail.update_food(data)
        else:
            photo_model = FoodPhoto(food_photo = food_photo)
            photo_model.save()
            photo_url = str(photo_model.food_photo.url)
            data['photo_url'] = photo_url
            food_detail.update_food(data)

class SignupForm(forms.Form):
    display_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Eg "Leonardo D. Vinci"',
     'class' : 'form-control'})) 

    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Username',
     # 'class' : 'form-control'})) 

    buss_org_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Business Name',
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


    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(SignupForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'

    def save(self, user):
        try:
            addr = self.cleaned_data['address']
            lat = self.cleaned_data['lat']
            lon = self.cleaned_data['lng']
            if len(lat) == 0 and len(lon) == 0:
                addr_geo = Geocoder.geocode(addr.strip())
                lat = float(addr_geo.latitude)
                lon = float(addr_geo.longitude)
                postal_code = str(addr_geo.postal_code)
            else:
                result = Geocoder.reverse_geocode(float(lat),float(lon))
                postal_code = str(result.postal_code)
        except:
            lat, lon, addr,postal_code = 51.5072 , -0.1275, "3 Whitehall, London SW1A 2EL, UK", "SW1 A 2EL"
        
        invite_id = ''
        try:
            invite_id = self.request.session['invite_id']
        except:
            invite_id = ''

        address = addr 
        '''Get user from the SocialAccount MySql'''
        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        data = {
                'is_unknown_profile':'false',
                'useruid': int(user.id), 'sign_up_as': str(self.cleaned_data['sign_up_as']),
                'type_user': str(self.cleaned_data['type_user']).split(","), 
                'zip_code': str(postal_code),
                'latlng' : {"type" : "Point", "coordinates" : [float(lon),float(lat)] },
                'address': address,
                # 'name': social_account.extra_data['name'],
                'business_org_name': self.cleaned_data['buss_org_name'],
                'name': self.cleaned_data['display_name'],
                'email': str(self.cleaned_data['email']), 
                'description': social_account.extra_data['description'],
                'username' : user.username,
                'screen_name': social_account.extra_data['screen_name'],
                'profile_img': social_account.extra_data['profile_image_url'],
                'updates': [],
                'foods':[],
                'organisations':[],
                'subscribed':0,
                'newsletter_freq':'Weekly'
        }

        '''Transport  user from MySql to Mongo'''
        userprofile.update_profile_upsert({'screen_name':social_account.extra_data['screen_name'],
            'is_unknown_profile':'true', 'username':social_account.extra_data['screen_name']},data)

        conn = TradeConnection()
        if self.cleaned_data['sign_up_as'] == "Business":
            try:
                usr = User.objects.get(id=99)
                data = {'c_useruid': int(user.id), 'b_useruid': 99}
                conn.create_connection(data)
            except:
                pass

        '''Transport user to MailChimp List'''
        mailchimp_obj = MailChimp()
        mailchimp_obj.subscribe(data)

        '''Invitation Tracking and Notifying the user who invites the user'''
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
                    '''If the joined user is invited Send notification to who invited'''
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
        if str(self.cleaned_data['sign_up_as']) == "Business":
            settings.LOGIN_REDIRECT_URL = "/payments/subscribe"
            return HttpResponseRedirect('/payments/subscribe')
        else:
            return HttpResponseRedirect('/activity/')
