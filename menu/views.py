from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.

def menu(request):
    return render(request, 'menu/menus.html', {'title' : 'menu'})


def register(request):
    if request.method == 'POST':
        #TODO: add user create logic
        return HttpResponseRedirect(reverse('menu'))
    else:
        return render(request, 'register.html')
