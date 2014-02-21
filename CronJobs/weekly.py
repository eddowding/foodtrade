import urllib2
baseurl = "http://foodtradelite.cloudapp.net/send-newsletter/weekly?code=11foodtradeESRS22"
baseurl = "http://foodtradelite.cloudapp.net/send-newsletter/none?code=11foodtradeESRS22"
response = urllib2.urlopen(baseurl)
