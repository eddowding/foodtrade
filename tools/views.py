import json
from pymongo import Connection
from bson.objectid import ObjectId
from django.shortcuts import render
from django.http import HttpResponse



def location_tool(request):
    conn = Connection() #TODO: might have to change
    collection = conn.foodtrade.userprofile
    objs = []
    for obj in collection.find(spec={'verified': {'$exists': False}, 'name': {'$exists': True}, 'latlng': {'$exists': True}}, fields=['latlng.coordinates', 'name'], limit=10):
        objs.append({'id': str(obj['_id']), 'name': obj.get('name'), 'lat': obj['latlng']['coordinates'][0], 'lng': obj['latlng']['coordinates'][1]})
    return render(request, 'location.html', {'objs': objs})

def location_tool_operation(request):
    conn = Connection() #TODO: might have to change
    collection = conn.foodtrade.userprofile
    id = request.GET.get('id')
    print id
    operation = request.GET.get('operation')
    coordinates = [float(request.GET.get('lat')), float(request.GET.get('lng'))]
    document = {'$set': {'verified': True}}
    if operation == 'save':
        document['$set']['latlng.coordinates'] = coordinates
    collection.update(spec={'_id': ObjectId(id)}, document=document, upsert=False, multi=False)
    return HttpResponse(json.dumps({'status': True}))
