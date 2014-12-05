
# django import
from django.http import HttpResponse
from django.shortcuts import render , render_to_response
from django.template import RequestContext

#app import


# Create your views here.

def menu(request):
    template_name = 'menu/menus.html'
    var = {'title' : 'menu'}
    contextt = RequestContext(request , var);
    return render_to_response(template_name , contextt)
