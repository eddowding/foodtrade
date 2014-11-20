import json
from pymongo import Connection
from bson.objectid import ObjectId
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def location_tool(request):
    conn = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
    db = conn[settings.MONGO_DB]
    if settings.MONGO_USER and settings.MONGO_PASS:
        db.authenticate(settings.MONGO_USER, settings.MONGO_PASS)
    collection = db.userprofile
    objs = []
    for obj in collection.find(spec={'verified': {'$exists': False}, 'name': {'$exists': True}, 'latlng': {'$exists': True}}, fields=['latlng.coordinates', 'name'], limit=10):
        objs.append({'id': str(obj['_id']), 'name': obj.get('name'), 'lat': obj['latlng']['coordinates'][0], 'lng': obj['latlng']['coordinates'][1]})
    return render(request, 'location.html', {'objs': objs})

def location_tool_operation(request):
    conn = Connection(settings.MONGO_HOST, settings.MONGO_PORT)
    db = conn[settings.MONGO_DB]
    if settings.MONGO_USER and settings.MONGO_PASS:
        db.authenticate(settings.MONGO_USER, settings.MONGO_PASS)
    collection = db.userprofile
    id = request.GET.get('id')
    operation = request.GET.get('operation')
    coordinates = [float(request.GET.get('lat')), float(request.GET.get('lng'))]
    document = {'$set': {'verified': True}}
    if operation == 'save':
        document['$set']['latlng.coordinates'] = coordinates
    collection.update(spec={'_id': ObjectId(id)}, document=document, upsert=False, multi=False)
    return HttpResponse(json.dumps({'status': True}))
