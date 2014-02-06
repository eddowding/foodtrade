import requests
import json

class MailChimp():
    """This class is used to make api calls to the MailChimp"""
    def __init__(self):
        self.format = 'json'
        self.api_end_point = 'https://us3.api.mailchimp.com/2.0/'
        self.api_key = 'e9294366710f56f159569b82660f9df3-us3'
        self.eid = ''

    def make_request(self, post_url, payload):
        r = requests.post(post_url,params=payload)
        json_response = json.loads(r.text)
        return json_response


    def subscribe(self, doc):
        subscribe_url = self.api_end_point + 'lists/subscribe' + self.format

        response = self.make_request(subscribe_url, payload)

