from django.shortcuts import render
from django.http import HttpResponse


def admin_user(request):
    return HttpResponse('hi')
