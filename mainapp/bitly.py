import requests
import json

BIT_LY_ACCESS_TOKEN = '6d2e7698597e642b16e78f3f73ead15da94697ee'

def construct_invite_tweet(request, invite_id):
    request_url = request.META['HTTP_HOST']
    # request_url = 'http://foodtradelite.cloudapp.net'
    invite_url = str(request_url) + '/invitation/' + str(invite_id['uid']['id']) +'/'
    get_url = 'https://api-ssl.bitly.com/v3/shorten'
    payload = {
    'URI':invite_url,
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
        short_url = invite_url
    invite_tweet = 'You will love foodtrade. Please sign up:- '  + short_url
    return invite_tweet