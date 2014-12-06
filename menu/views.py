import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from mongoengine.django.auth import User


def menu(request):
    return render(request, 'menu/menus.html', {'title' : 'menu'})


def register(request):
    if request.method == 'POST':
        #TODO: add user create logic
        return HttpResponseRedirect(reverse('menu'))
    else:
        return render(request, 'register.html')


def user_lookup_count(request):
    query = {}
    for k, v in request.GET.items():
        query[k] = v
    return HttpResponse(json.dumps({'count': User.objects.filter(**query).count()}))
