from __future__ import unicode_literals
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
from mainapp.classes.MailchimpClass import MailChimpClass
from django.conf import settings
import pprint
from classes.MongoConnection import MongoConnection
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from collections import OrderedDict
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template import loader
from django.contrib.sites.models import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class PassworResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        from mainapp.classes.Email import Email

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        # email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        # if html_email_template_name is not None:
        #     html_email = loader.render_to_string(html_email_template_name, context)
        email = Email()
        # email.send_mail(to_email, subject , body)
        email.send_mail(subject, 
                    template_content=[{'name':'main', 'content':body}], to = [{'email':to_email}])
                    

            # email_message.attach_alternative(html_email, 'text/html')

        # email_message.send()

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)





    error_messages = {
        'unknown': ("That email address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': ("The user account associated with this email "
                      "address cannot reset the password."),
        }
    # email = forms.CharField(required=True) 
    # def clean_email(self):
    #     """
    #     Validates that an active user exists with the given email address.
    #     """
    #     UserModel = get_user_model()
    #     email = self.cleaned_data["email"]
    #     self.users_cache = UserModel._default_manager.filter(email__iexact=email)
    #     if not len(self.users_cache):
    #         raise forms.ValidationError(self.error_messages['unknown'])
    #     if not any(user.is_active for user in self.users_cache):
    #         # none of the filtered users are active
    #         raise forms.ValidationError(self.error_messages['unknown'])
    #     if any((user.password == UNUSABLE_PASSWORD)
    #         for user in self.users_cache):
    #         raise forms.ValidationError(self.error_messages['unusable'])
    #     return email

    # def save(self, domain_override=None,
    #          subject_template_name='registration/password_reset_subject.txt',
    #          email_template_name='registration/password_reset_email.html',
    #          use_https=False, token_generator=default_token_generator,
    #          from_email=None, request=None):
    #     """
    #     Generates a one-use only link for resetting password and sends to the
    #     user.
    #     """
    #     print "saved"
    #     from django.core.mail import send_mail
    #     for user in self.users_cache:
    #         if not domain_override:
    #             current_site = get_current_site(request)
    #             site_name = current_site.name
    #             domain = current_site.domain
    #         else:
    #             site_name = domain = domain_override
    #         c = {
    #             'email': user.email,
    #             'domain': domain,
    #             'site_name': site_name,
    #             'uid': int_to_base36(user.pk),
    #             'user': user,
    #             'token': token_generator.make_token(user),
    #             'protocol': use_https and 'https' or 'http',
    #             }
    #         subject = loader.render_to_string(subject_template_name, c)
    #         # Email subject *must not* contain newlines
    #         subject = ''.join(subject.splitlines())
    #         email = loader.render_to_string(email_template_name, c)
            
            # send_mail(subject, email, from_email, [user.email])

def update_all_values(old_useruid, new_useruid):
    '''This function updates all other affected collections when unclaimed profile changes to claimed'''
    mongo_connection_object = MongoConnection("localhost",27017,'foodtrade')
    try:
        mongo_connection_object.update_multi('tradeconnection', {'b_useruid': old_useruid}, {'b_useruid':new_useruid})
        mongo_connection_object.update_multi('tradeconnection', {'c_useruid': old_useruid}, {'c_useruid':new_useruid})
        mongo_connection_object.update_multi('food', {'useruid':old_useruid}, {'useruid':new_useruid})
        mongo_connection_object.update_multi('customer', {'useruid':old_useruid}, {'useruid':new_useruid})
        mongo_connection_object.update_multi('organisation', {'orguid':old_useruid}, {'orguid':new_useruid})
        mongo_connection_object.update_multi('team', {'orguid':old_useruid}, {'orguid':new_useruid})
        mongo_connection_object.update_multi('recommendfood', {'business_id':old_useruid}, {'business_id':new_useruid})
    except:
        pass
    return True


class FoodForm(forms.Form):
    food_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'form-control'})) 
    food_tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'})) 
    profile_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'})) 
    food_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    food_photo = forms.ImageField(required=False)
    food_duplicate = forms.CharField(required=False)
    how_much = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control',
        'placeholder': 'How much?'}))
    how_often = forms.ChoiceField(choices=[("How often", "How often")]+[(x, x) for x in ['daily', 'monthly', 'seasonally', 'annually']],
        widget=forms.Select(attrs={'class' : 'form-control btn-sm selectpicker'}))
    

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)

    def save(self, month_list):
        food_description = self.cleaned_data['food_description']
        food_tags = self.cleaned_data['food_tags']
        profile_id = int(self.cleaned_data['profile_id'])
        food_name = self.cleaned_data['food_name']
        food_name = food_name.replace('&', '&amp;')

        food_detail = Food()
        food_photo = self.cleaned_data['food_photo']
        food_duplicate = self.cleaned_data['food_duplicate']
        how_much = self.cleaned_data['how_much']
        how_often = self.cleaned_data['how_often']
        data = {'food_name': food_name, 'useruid': profile_id, 'description': food_description,
        'food_tags': food_tags, 'photo_url': '', 'how_much': how_much, 'how_often': how_often, 'month_list': month_list}
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
    
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Username',
     'class' : 'form-control'})) 

    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': u'Password',
     'class' : 'form-control'})) 

    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': u'Confirm Password',
     'class' : 'form-control'})) 

    display_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Eg "Leonardo D. Vinci"',
     'class' : 'form-control'})) 

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


    def __init__(self, *args, **kwargs):
        # self.request = request
        self.request = kwargs.pop('request', None)
        super(SignupForm, self).__init__(*args, **kwargs)
        try:
            username =  self.sociallogin.account.extra_data['screen_name']
            user_prof_obj  = UserProfile()
            user = user_prof_obj.get_profile_by_username(str(username))
            self.fields['email'].widget.attrs['value'] = user['email']
            self.fields['address'].widget.attrs['value'] = user['address']

        except:
            pass
        # self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'form-control'

    def save(self, user):
        new_username = self.cleaned_data.get('username') if self.cleaned_data.get('username')!=None else ''
        new_password1 = self.cleaned_data.get('password1') if self.cleaned_data.get('password1')!=None else ''
        print type(user), 'this is user', user, 
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
        try:
            social_account = SocialAccount.objects.get(user__id = user.id)
        except:
            social_account = None
        try:
            old_useruid = userprofile.get_profile_by_username(str(social_account.extra_data['screen_name']))['useruid']
            '''update all other affected collections when unclaimed profile changes to claimed'''
            update_all_values(int(old_useruid), int(user.id))
        except:
            pass
        default_profile_img = 'http://a0.twimg.com/sticky/default_profile_images/default_profile_6_normal.png'
        data = {
                'is_unknown_profile':'false',
                'useruid': int(user.id), 
                'sign_up_as': str(self.cleaned_data['sign_up_as']),
                'type_user': str(self.cleaned_data['type_user']).split(","), 
                'zip_code': str(postal_code),
                'latlng' : {"type" : "Point", "coordinates" : [float(lon),float(lat)] },
                'address': address,
                # 'name': social_account.extra_data['name'],
                'business_org_name': self.cleaned_data['buss_org_name'],
                'name': self.cleaned_data['display_name'],
                'email': str(self.cleaned_data['email']), 
                'description': social_account.extra_data['description'] if social_account!=None else '',
                'username' : user.username,
                'screen_name': social_account.extra_data['screen_name'] if social_account!=None else new_username,
                'profile_img': social_account.extra_data['profile_image_url'] if social_account!=None else default_profile_img,                
                'updates': [],
                'foods':[],
                'organisations':[],
                'subscribed':0,
                'newsletter_freq':'Weekly',            
                'followers_count':social_account.extra_data['followers_count'] if social_account!=None else 0,
                'friends_count':social_account.extra_data['friends_count'] if social_account!=None else 0
                
        }
        try:
            data['profile_banner_url'] = social_account.extra_data['profile_banner_url'] if social_account!=None else ''
        except:
            pass

        if new_password1 != '':
            data['email_registration'] = 1
            
        join_time = datetime.datetime.now()
        join_time = time.mktime(join_time.timetuple())
        data['join_time'] = int(join_time)
        data['trial_period_starts'] = int(join_time)
        
        '''Transport  user from MySql to Mongo'''
        # userprofile.update_profile_upsert({'screen_name':social_account.extra_data['screen_name'],
        #          'username':social_account.extra_data['screen_name']},data)
        userprofile.update_profile_upsert({'screen_name':data['screen_name'],
                 'username':data['username']},data)
        
        conn = TradeConnection()
        if self.cleaned_data['sign_up_as'] == "Business":
            try:
                usr = User.objects.get(id=99)
                con_data = {'c_useruid': int(user.id), 'b_useruid': 99}
                conn.create_connection(con_data)
            except:
                pass

        try:
            '''Transport user to MailChimp List'''
            mailchimp_obj = MailChimpClass()
            mailchimp_obj.subscribe(data)
            mailchimp_obj_new = MailChimpClass(list_id='eeea3ac4c6')
            mailchimp_obj_new.subscribe(data)
        except:
            pass
            
        '''Invitation Tracking and Notifying the user who invites the user'''
        if invite_id != '':
            invititation_to = user.username
            # screen_name = social_account.extra_data['screen_name']
            screen_name = data['screen_name']
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
            # settings.LOGIN_REDIRECT_URL = "/payments/subscribe"
            # return HttpResponseRedirect('/payments/subscribe')
            settings.LOGIN_REDIRECT_URL = "/me/"
            return HttpResponseRedirect('/me/')
        else:
            # settings.LOGIN_REDIRECT_URL = "/activity"
            return HttpResponseRedirect('/activity/')