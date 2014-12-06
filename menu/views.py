from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.

def menu(request):
    ''' Get list of menus '''    
    return render(request, 'menu/menus.html', {'title' : 'menu'})


def register(request):
    ''' User Registration in menu '''
    
    if request.method == 'POST':
        #TODO: add user create logic
        return HttpResponseRedirect(reverse('menu'))
    else:
        return render(request, 'menu/register.html')


def login(request):
    ''' User login in menu '''
    if request.method == 'POST':
        #TODO: add user login logic
        return HttpResponseRedirect(reverse('menu'))
    else:
        return render(request, 'menu/login.html')
