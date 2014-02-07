import mailchimp
from mainapp.mc_utils import *

#def subscribe(self, id, email, merge_vars=None, email_type='html', double_optin=True, update_existing=False, replace_interests=True, send_welcome=False):
try:
    m = get_mailchimp_api()
    m.lists.subscribe(list_id, email = {'email':'brish.i98@gmail.com'}, merge_vars = {"FNAME":"Bhandari","LNAME":"Roshan","groupings": [{"name": "Foodtrade Group","groups": ["Individual"]}],"mc_location":{"latitude":"51.5167","longitude":"9.9167"}},update_existing=True, send_welcome=True, replace_interests=True)

except mailchimp.ListAlreadySubscribedError:
	print "Already subscribed"