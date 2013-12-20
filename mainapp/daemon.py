import urllib2
import time

def run_daemon():
	baseurl = "http://foodtradelite.cloudapp.net/tweets/"
	while True:
	    response = urllib2.urlopen(baseurl)
	    print response.read()
	    time.sleep(120)

run_daemon()