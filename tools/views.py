from pymongo import Connection
from django.shortcuts import render
from django.http import HttpResponse


def location_tool(request):
    conn = Connection() #TODO: might have to change
    collection = conn.foodtrade.userprofile
    objs = []
    for obj in collection.find(spec={'verified': {'$exists': False}, 'name': {'$exists': True}, 'latlng': {'$exists': True}}, fields=['latlng.coordinates', 'name'], limit=10):
        objs.append({'id': str(obj['_id']), 'name': obj.get('name'), 'lat': obj['latlng']['coordinates'][0], 'lng': obj['latlng']['coordinates'][1]})
    return render(request, 'location.html', {'objs': objs})
