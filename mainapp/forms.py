from django import forms
from django.contrib.auth.models import User
from mainapp.TweetFeed import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect


class SignupForm(forms.Form):
    # first_name = forms.CharField(max_length=30, label='First Name')
    # last_name = forms.CharField(max_length=30, label='Last Name')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Username',
     'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'Email',
     'class' : 'form-control'}))
    sign_up_as = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Sign up as',
     'class' : 'form-control'}))
    # type_user = forms.CharField(max_length=30, label='Type')
    type_user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))


    def save(self, user):
        # code to save form fields to mongodb
        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        addr = social_account.extra_data['location']
        data = {'useruid': user.id, 'sign_up_as': self.cleaned_data['sign_up_as'],
        		'type_user': self.cleaned_data['type_user'], 
        		'latitude': self.cleaned_data['latitude'],
        		'longitude': self.cleaned_data['longitude'],
        		'address': addr
        }
        userprofile.create_profile(data)
        print "saved"
        return HttpResponseRedirect('/?next=/?new_user=True')