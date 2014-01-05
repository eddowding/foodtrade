from django import forms
from django.contrib.auth.models import User
from mainapp.TweetFeed import UserProfile
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.http import HttpResponse, HttpResponseRedirect
from classes.Tags import Tags
from pyzipcode import ZipCodeDatabase

class SignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Username',
     'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'Email',
     'class' : 'form-control'}))
    sign_up_as = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Sign up as',
     'class' : 'form-control'}))
    # type_user = forms.CharField(max_length=30, label='Type')
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Zip Code',
     'class' : 'form-control'}))
    type_user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': u'Farm, wholesaler, restaurant, bakery...',
     'class' : 'form-control'}))

    def save(self, user):
        # code to save form fields to mongodb
        # convert zip code to longitude and latitude
        zip_code = self.cleaned_data['zip_code']
        zcdb = ZipCodeDatabase()
        try:
            zipcode = zcdb[zip_code]
        except:
            zipcode = zcdb[06320]
        userprofile = UserProfile()
        social_account = SocialAccount.objects.get(user__id = user.id)
        addr = social_account.extra_data['location']
        data = {'useruid': str(user.id), 'sign_up_as': self.cleaned_data['sign_up_as'],
        		'type_user': self.cleaned_data['type_user'], 
                'zip_code': self.cleaned_data['zip_code'],
        		'address': addr,
                'latitude': zipcode.latitude,
                'longitude': zipcode.longitude
        }
        userprofile.create_profile(data)
        print "saved", data
        return HttpResponseRedirect('/?next=/?new_user=True')