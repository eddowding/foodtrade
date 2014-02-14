from django import template
from django.contrib.auth.models import User
import re
register = template.Library()

@register.filter
def recognise_name(value):
    result = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', value, re.M|re.I)
    tags = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9]+)', value, re.M|re.I)
    if tags:
    	for each_tag in tags:
    		value = value.replace("#"+each_tag, '<a href="/activity/?q='+each_tag+'/">#'+each_tag+'</a>')
    if result:
        for each in result:
            try:
                usr = User.objects.get(username = str(each))
                value = value.replace("@"+each, '<a href="/profile/'+each+'/">@'+each+'</a>')
            except:
                pass
    return value