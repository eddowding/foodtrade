from django.db import models
from django.forms import ModelForm
from models import Coupon

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ('coupon_id', 'percent_off', 'duration', 'duration_in_months')
