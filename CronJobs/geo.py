from pygeocoder import Geocoder
a = Geocoder(
	client_id = '352528416515-r1du34cl9j9kqf4cv0dc8pnjnmi6qj9l.apps.googleusercontent.com', 
	api_key = 'AIzaSyDRNTE8EWOsbZzAQcM3hlBpaNA0zTuVups'
)
b = a.geocode('kahmandu')