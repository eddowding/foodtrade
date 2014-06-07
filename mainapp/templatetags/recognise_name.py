#!/usr/bin/env python
# encoding: utf-8
from django import template
from django.contrib.auth.models import User
import re
from mainapp.classes.Foods import AdminFoods
from mainapp.classes.TweetFeed import UserProfile
import json
register = template.Library()

@register.filter(name='add_html_attr')
def add_html_attr(field, attr_dict):
   attrs = json.loads(attr_dict)
   return field.as_widget(attrs=attrs)

@register.filter
def recognise_name(value):
    value = value.encode('utf-8').strip()
    result = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z_]+[A-Za-z0-9_]+)', value, re.M|re.I)
    tags = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z_]+[A-Za-z0-9]+)', value, re.M|re.I)
    links = re.findall("((http:|https:)//[^ \<]*[^ \<\.])",value)
    if links:
        for each_link in links:
            value = value.replace(str(each_link[0]), '<a href="'+str(each_link[0])+'" target="_blank">'+ str(each_link[0]) + '</a>')
    if tags:
    	for each_tag in tags:
    		value = value.replace("#"+each_tag, '<a href="/activity/?q=%23'+each_tag+'">#'+each_tag+'</a>')
    if result:
        user_prof = UserProfile()
        for each in result:
            try:
                # usr = User.objects.get(username = str(each))
                usr_pr = user_prof.get_profile_by_username(each)
                if usr_pr['sign_up_as'] != 'unclaimed':
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

