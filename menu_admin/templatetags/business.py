from django import template
from menu.models import Business


register = template.Library()


@register.simple_tag
def business_name(user):
    try:
        return Business.objects.get(user=user).name
    except Business.DoesNotExist:
        return 'NA'


@register.simple_tag
def business_phone(user):
    try:
        return Business.objects.get(user=user).phone
    except Business.DoesNotExist:
        return 'NA'
