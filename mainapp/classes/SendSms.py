
from twilio.rest import TwilioRestClient 
def send_sms(to,body):
    # put your own credentials here 
    ACCOUNT_SID = "ACc54d95fd16aa5e6e35dbe60d44f3cc94" 
    AUTH_TOKEN = "69e49be54014f34904e5c08715e0791e" 
     
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
    client.messages.create(
        to=to, 
        from_="+442380000486", 
        body=body,  
    )
    return True