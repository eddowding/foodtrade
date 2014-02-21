from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _

import stripe

from .models import Customer, Coupon
from .settings import PLAN_CHOICES, PASSWORD_INPUT_RENDER_VALUE, \
    PASSWORD_MIN_LENGTH

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = getattr(settings, "STRIPE_API_VERSION", "2012-11-07")


class PlanForm(forms.Form):

    plan = forms.ChoiceField(choices=PLAN_CHOICES)


class CancelSubscriptionForm(forms.Form):
    pass


########### Begin SignupForm code

class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', PASSWORD_INPUT_RENDER_VALUE)
        kwargs['widget'] = forms.PasswordInput(
            render_value=render_value,
            attrs={'placeholder': _('Password')})
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):
    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        min_length = PASSWORD_MIN_LENGTH
        if len(value) < min_length:
            raise forms.ValidationError(
                _("Password must be a minimum of {0} "
                  "characters.").format(min_length))
        return value


try:
    from .widgets import StripeWidget
except ImportError:
    StripeWidget = None

try:
    from allauth.account.utils import setup_user_email
except ImportError:
    setup_user_email = None


if StripeWidget and setup_user_email:

    class StripeSubscriptionSignupForm(forms.Form):
        """
            Requires the following packages:

                * django-crispy-forms
                * django-floppyforms
                * django-allauth

            Necessary settings::

                INSTALLED_APPS += (
                    "floppyforms",
                    "allauth",  # registration
                    "allauth.account",  # registration
                )
                ACCOUNT_SIGNUP_FORM_CLASS = "djstripe.StripeSubscriptionSignupForm"

            Necessary URLS::

                (r'^accounts/', include('allauth.urls')),

        """
        username = forms.CharField(max_length=30)
        email = forms.EmailField(max_length=30)
        password1 = SetPasswordField(label=_("Password"))
        password2 = PasswordField(label=_("Password (again)"))
        confirmation_key = forms.CharField(
            max_length=40,
            required=False,
            widget=forms.HiddenInput())
        stripe_token = forms.CharField(widget=forms.HiddenInput())
        plan = forms.ChoiceField(choices=PLAN_CHOICES)

        # Stripe nameless fields
        number = forms.CharField(max_length=20,
            required=False,
            widget=StripeWidget(attrs={"data-stripe": "number"})
        )
        cvc = forms.CharField(max_length=4, label=_("CVC"),
            required=False,
            widget=StripeWidget(attrs={"data-stripe": "cvc"}))
        exp_month = forms.CharField(max_length=2,
                required=False,
                widget=StripeWidget(attrs={"data-stripe": "exp-month"})
        )
        exp_year = forms.CharField(max_length=4,
                required=False,
                widget=StripeWidget(attrs={"data-stripe": "exp-year"})
        )

        def save(self, user):
            try:
                customer, created = Customer.get_or_create(user)
                customer.update_card(self.cleaned_data["stripe_token"])
                customer.subscribe(self.cleaned_data["plan"])
            except stripe.StripeError as e:
                # handle error here
                raise e
import datetime

class CouponForm(forms.Form):
    DURATION_CHOICES = (
    ('once', 'Once'),
    ('repeating', 'Repeating'),
    ('forever', 'Forever'),
    )
    coupon_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Promo Code like 25OFF','class' : 'form-control'})) 
    percent_off = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Discount Percent','class' : 'form-control'})) 
    duration = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.Select(attrs={'class' : 'form-control'}))
    duration_in_months = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'No. of months','class' : 'form-control'})) 
    max_redemptions = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'No. of uses','class' : 'form-control'}))
    redeem_by = forms.DateField(label=u'redeem by', input_formats=['%Y-%m-%d', '%Y-%d-%m',], required=True, widget=forms.DateInput(format = '%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD','class' : 'form-control'})) #forms.DateField(required=True, initial=datetime.date.today,) # widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class' : 'form-control'}))
    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)

    def save(self):
        # try:
        cpn = Coupon(
        coupon_id = self.cleaned_data['coupon_id'],
        percent_off = self.cleaned_data['percent_off'],
        duration = self.cleaned_data['duration'],
        duration_in_months = self.cleaned_data['duration_in_months'],
        max_redemptions = self.cleaned_data['max_redemptions'],
        redeem_by = self.cleaned_data['redeem_by']
        )
        try:
            cpn.save()
            cpn.create_coupon()
            return cpn
        except:
            return False