import requests
import json

class MailChimp():
	"""This class is used to make api calls to the MailChimp"""
    def __init__(self):
        self.api_end_point = 'https://us3.api.mailchimp.com/2.0/'
        self.api_key = 'e9294366710f56f159569b82660f9df3-us3'

    def subscribe(self, doc):
    	pass