from django import template
from django.contrib.auth.models import User
import re
from mainapp.classes.Foods import AdminFoods
register = template.Library()

@register.filter
def recognise_name(value):
    result = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', value, re.M|re.I)
    tags = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9]+)', value, re.M|re.I)
    if tags:
    	for each_tag in tags:
    		value = value.replace("#"+each_tag, '<a href="/activity/?q=%23'+each_tag+'">#'+each_tag+'</a>')
    if result:
        for each in result:
            try:
                usr = User.objects.get(username = str(each))
                value = value.replace("@"+each, '<a href="/profile/'+each+'/">@'+each+'</a>')
            except:
                pass


    admin_foods = AdminFoods()
    master_foods = admin_foods.get_tags()
    #create master list of foods
    final_master = []
    for each in master_foods:
        if each.get('childrens')!=None:
            final_master.extend([str(i['node']).lower() for i in each['childrens']])
        else:
            final_master.extend([str(each['node']).lower()])

    val_list = value.split()
    for each in val_list:
        if each.lower() in final_master:
            value = value.replace(each, '<a href="/activity/?f='+each.title()+'">'+each+'</a>')
    return value
