import urllib2
import time

def run_daemon():
    baseurl = "http://foodtradelite.cloudapp.net/tweets/"
    while True:
        try:
            response = urllib2.urlopen(baseurl)
        except:
            pass
        time.sleep(120)

run_daemon()