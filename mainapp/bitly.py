import requests
import json
from mainapp.classes.MongoConnection import MongoConnection
from bson.objectid import ObjectId


class InviteURL():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'invitemessage'
        self.db_object.create_table(self.table_name,'_id')

    def save_invite_url(self,doc):
        return self.db_object.update_upsert(self.table_name,{'invite_id':doc['invite_id']}, doc)

    def get_invite_url(self, invite_id):
        try:
            return self.db_object.get_one(self.table_name,{'invite_id': invite_id})['invite_url']
        except:
            return None



BIT_LY_ACCESS_TOKEN = '6d2e7698597e642b16e78f3f73ead15da94697ee'

def shorten_url(url):
    get_url = 'https://api-ssl.bitly.com/v3/shorten'
    payload = {
    'URI':url,
    'access_token':BIT_LY_ACCESS_TOKEN
    }
    r = requests.get(get_url,params=payload)
    json_response = json.loads(r.text)
    try:
        if json_response['status_txt'] == 'OK':
            data = json_response['data']
            short_url = data['url']
        else:
            short_url = invite_url
    except:
        short_url = url
    return short_url

def construct_invite_tweet(request, invite_id):
    request_url = request.META['HTTP_HOST']
    # request_url = 'http://foodtradelite.cloudapp.net'
    invite_url = 'http://' + str(request_url) + '/invitation/' + str(invite_id['uid']['id']) +'/'
    get_url = 'https://api-ssl.bitly.com/v3/shorten'
    payload = {
    'URI':invite_url,
    'access_token':BIT_LY_ACCESS_TOKEN
    }    
    invite_url_obj = InviteURL()
    new_invite_url = invite_url_obj.get_invite_url(invite_id)
    if new_invite_url == None:
        r = requests.get(get_url,params=payload)
        json_response = json.loads(r.text)    
        try:
            if json_response['status_txt'] == 'OK':
                data = json_response['data']
                short_url = data['url']
                
            else:
                short_url = invite_url            
        except:
            short_url = invite_url

        invite_url_obj.save_invite_url({'invite_id':invite_id, 'invite_url':short_url})        
    else:
        short_url = new_invite_url
    invite_tweet = 'Join the #realfood search engine '  + short_url
    return invite_tweet
