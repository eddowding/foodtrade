import urllib2
import time

def run_daemon():
	baseurl = "http://localhost:8000/tweets/"
	while True:
	    response = urllib2.urlopen(baseurl)
	    print response.read()
	    time.sleep(120)

run_daemon()