import urllib2

def run_daemon():
	baseurl = "foodtradelite.cloudapp.net/tweets/"
    response = urllib2.urlopen(baseurl)