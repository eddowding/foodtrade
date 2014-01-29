import requests
import json

BIT_LY_ACCESS_TOKEN = '6d2e7698597e642b16e78f3f73ead15da94697ee'

def construct_Invite_tweet(request, invite_id):
    print invite_id
    request_url = request.META['HTTP_HOST']
    print request_url
    invite_url = str(request_url) + '/invitation/' + str(invite_id) +'/'
    get_url = 'https://api-ssl.bitly.com/v3/shorten'
    payload = {
    'URI':invite_url,
    'access_token':BIT_LY_ACCESS_TOKEN
    }
    r = requests.get(get_url,params=payload)
    json_response = json.loads(r.text)
    print json_response
    if json_response['status_text'] == 'OK':
        data = json_response['data']
        short_url = data['url']
    else:
        short_url = invite_url
    return 'You\'ll love foodtrade. Please sign up:- '  + short_url