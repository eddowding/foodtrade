import json
from datetime import datetime
from copy import deepcopy
from bson.objectid import ObjectId, InvalidId
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from mongoengine.django.auth import User
from menu.mongo_models import Establishment, Menu, MenuSection, Dish


@login_required(login_url=reverse_lazy('menu-login'))
def menu(request):
    ''' Get list of menus '''
    return render(request, 'menu/menus.html', {'title' : 'menu'})


def register(request):
    ''' User Registration in menu '''
    if request.method == 'POST':
        user = User.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth_login(request, user)
        return HttpResponseRedirect(reverse_lazy('menu'))
    else:
        return render(request, 'menu/register.html')


def login(request):
    ''' User login in menu '''
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth_login(request, user)
        return HttpResponseRedirect(reverse_lazy('menu'))
    else:
        return render(request, 'menu/login.html')


def user_lookup_count(request):
    query = {}
    for k, v in request.GET.items():
        query[k] = v
        return HttpResponse(json.dumps({'status': True, 'count': User.objects.filter(**query).count()}))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse_lazy('menu-login'))


@login_required(login_url=reverse_lazy('menu-login'))
def establishment_lookup_name(request):
    query = {'BusinessName__icontains': request.GET.get('q')}
    ret_list = []
    for obj in Establishment.objects.filter(**query):
        ret_list.append({'name': obj.BusinessName, 'value': str(obj.pk)})
        return HttpResponse(json.dumps({'status': True, 'objs': ret_list}))


@login_required(login_url=reverse_lazy('menu-login'))
def create_menu(request):
    establishment = request.POST.get('establishment')
    name = request.POST.get('name')
    try:
        Menu.objects.create(establishment=ObjectId(establishment), name=name, added_on=datetime.now())
    except InvalidId:
        establishment = Establishment.objects.create(BusinessName=establishment, added_on=datetime.now())
        Menu.objects.create(establishment=establishment.pk, name=name, added_on=datetime.now())
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def create_menu_section(request):
    insert_dict = deepcopy(request.POST)
    insert_dict['menu'] = ObjectId(insert_dict['menu'])
    insert_dict['added_on'] = datetime.now()
    MenuSection.objects.create(**insert_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def create_dish(request):
    insert_dict = deepcopy(request.POST)
    insert_dict['menu_section'] = ObjectId(insert_dict['menu_section'])
    insert_dict['added_on'] = datetime.now()
    Dish.objects.create(**insert_dict)
    return HttpResponse(json.dumps({'status': True}))

