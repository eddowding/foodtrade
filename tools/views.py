from django.shortcuts import render
from django.http import HttpResponse

def location_tool(request):
    return render(request, 'location.html')
