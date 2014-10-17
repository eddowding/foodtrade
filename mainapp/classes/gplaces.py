#!/usr/bin/env python
# encoding: utf-8
import requests, json

KEY = 'AIzaSyCANIHQ_D-ZkXoNWmGrXAmgcR_vxKSG0pw'

class GPlaces():
    def __init__ (self):
        #self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'GPlaces'

    def search_google_places(self, user_id, q=""):
        ''' This function is used to make queries to google places api '''        
        from TweetFeed import UserProfile
        user_profile_obj = UserProfile()

        logged_user = user_profile_obj.get_profile_by_id(user_id)
        location = str(logged_user['latlng']['coordinates'][1]) + ',' + str(logged_user['latlng']['coordinates'][0])

        get_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        payload = {
            'key':KEY,
            'name':q.lower(),
            'keyword':q.lower(),
            'location':location,
            'radius':'50000'
        }

        r = requests.get(get_url,params=payload)
        json_response = json.loads(r.text)
        search_results =  json_response['results'][0:6]
        
        return_results = []

        for eachResult in search_results:
            get_url = 'https://maps.googleapis.com/maps/api/place/details/json'
            payload = {
            'placeid':eachResult['place_id'],
            'key':KEY
            }
            
            import re
            find_user_name = " ".join(re.findall("[a-zA-Z]+", eachResult['name']))
            find_user_name = find_user_name.replace(" ","")
            
            registered_user_count = user_profile_obj.get_user_count_by_user_name_similar(find_user_name.lower())

            user_name = " ".join(re.findall("[a-zA-Z]+", eachResult['name'])) + '_gp_' + str(registered_user_count)
            user_name = user_name.replace(" ","")
            # user_name = eachResult['name'].replace(' ', '').replace("'",'') + '_gp_' + str(registered_user_count)
            
            r = requests.get(get_url,params=payload)
            json_response = json.loads(r.text)
            
            min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1
            
            data = {
                'is_unknown_profile': 'true',
                'recently_updated_by_super_user': 'false',                    
                'email' : '',
                'description' :'',
                'foods': [],
                'name' : eachResult['name'],            
                'profile_img':'/static/images/gimage.png',
                'type_user':[],
                'updates': [],
                'gPlacesProfile':True,
                'subscribed':0,
                'newsletter_freq':'Never',
                'followers_count':0,
                'friends_count':0,
                'sign_up_as':'unclaimed',
                'Organisations':[],
                'useruid': min_user_id,
                'username':user_name.lower(),
                'screen_name': user_name.lower(),
                'profile_linked_to_twitter':False
            }

            try:
                data['phone_number_international'] = json_response['result']['international_phone_number']
            except:
                data['phone_number'] = ''
            
            try:
                data['opening_hours'] = json_response['result']['opening_hours']
            except:
                pass
            
            try:
                data['photos'] = json_response['result']['photos']
            except:
                pass
            
            try:
                data['place_details_id'] = json_response['result']['id']
            except:
                pass

            try:
                data['place_id'] = eachResult['place_id']
            except:
                pass

            try:
                data['rating'] = json_response['result']['rating']
            except:
                pass
            try:
                data['reference'] = json_response['result']['reference']
            except:
                pass

            try:
                data['reviews'] = json_response['result']['reviews']
            except:
                pass

            try:
                data['gPlus_url'] = json_response['result']['url']
            except:
                pass

            try:
                data['website'] = json_response['result']['website']
            except:
                pass                

            try:
                data['vicinity'] = json_response['result']['vicinity']
            except:
                pass

            try:
                data['user_ratings_total'] = json_response['result']['user_ratings_total']
            except:
                pass

            try:
                data['types'] = json_response['result']['types']
            except:
                pass                
            data['profile_banner_url'] = ''
                
            try:                
                data['address'] = str(json_response['result']['formatted_address'])
            except:
                data['address'] = str('Antartica')
                data['address_default_on_error'] = 'true'

            try:
                data['latlng'] = {"type":"Point","coordinates":[float(eachResult['geometry']['location']['lng']) ,float(eachResult['geometry']['location']['lat'])]}
            except:
                data['latlng'] = {"type":"Point","coordinates":[float(-135.10000000000002) ,float(-82.86275189999999)]}
                data['latlng_default_on_error'] = 'true'
                
            try:
                data['zip_code'] = str(json_response['result']['address_components'][5]['long_name'])
            except:
                data['zip_code'] = str('')
                data['zip_default_on_error'] = 'true'

            if user_profile_obj.get_profile_by_condition({'latlng':data['latlng'], 'place_id':data['place_id']}) == None:
                user_profile_obj.update_profile_upsert({'latlng':data['latlng'], 'place_id':data['place_id']}, data)
                return_results.append(data)            
            # print "Inside GPlaces"

        return return_results

# gplaces = GPlaces()
# gplaces.search_google_places(12, 'fish')