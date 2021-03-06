#!/usr/bin/env python
# encoding: utf-8
import requests, json

# KEY = 'AIzaSyCANIHQ_D-ZkXoNWmGrXAmgcR_vxKSG0pw'
# KEY = 'AIzaSyDfZIYIxosBoIiEF0rNW_h_Gax3ZBuRANs'
KEY = 'AIzaSyDLP8Dd3JQKAZgiQ-M32Oq7oTRoOThvHZQ'

class GPlaces():
    def __init__ (self):
        #self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'GPlaces'


    def get_details_and_create_profile(self, gp_id):
        get_url = 'https://maps.googleapis.com/maps/api/place/details/json'
        payload = {
        'placeid':gp_id,
        'key':KEY
        }
        r = requests.get(get_url,params=payload)

        json_response = json.loads(r.text)
        
        from TweetFeed import UserProfile        
        user_profile_obj = UserProfile() 

        import re
        find_user_name = " ".join(re.findall("[a-zA-Z]+", json_response['result']['name']))
        find_user_name = find_user_name.replace(" ","")
        
        try:
            address_char = " ".join(re.findall("[a-zA-Z0-9]+", json_response['result']['formatted_address']))
            address_char = address_char.replace(" ", "")
        except:
            pass


        registered_user_count = user_profile_obj.get_user_count_by_user_name_similar(find_user_name.lower())

        if registered_user_count == 0:
            user_name = " ".join(re.findall("[a-zA-Z]+", json_response['result']['name']))
        else:
            try:
                user_name = " ".join(re.findall("[a-zA-Z]+", json_response['result']['name']))  + '_' + address_char
            except:
                user_name = " ".join(re.findall("[a-zA-Z]+", json_response['result']['name']))  +  str(registered_user_count)

        user_name = user_name.replace(" ","")
        # user_name = eachResult['name'].replace(' ', '').replace("'",'') + '_gp_' + str(registered_user_count)
        
        
        min_user_id = int(user_profile_obj.get_minimum_id_of_user()[0]['minId']) -1
        
        data = {
            'name' : json_response['result']['name'],
            'is_unknown_profile': 'true',
            'recently_updated_by_super_user': 'false',                    
            'email' : '',
            'description' :'',
            'foods': [],
            'type_user':json_response['result']['types'],
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
            'screen_name':'',
            'profile_linked_to_twitter':False
        }
        # print json_response
        try:
            data['profile_img'] = 'https://maps.googleapis.com/maps/api/place/photo?key=' + KEY + '&maxwidth=400&photoreference='+json_response['result']['photos'][0]['photo_reference']
        except:
            data['profile_img'] = 'https://maps.googleapis.com/maps/api/place/photo?key=' + KEY + '&photoreference='+json_response['result']['reference']

        try:
            data['phone_number'] = json_response['result']['international_phone_number']
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
            data['place_id'] = json_response['result']['place_id']
        except:
            pass

        try:
            data['useruid'] = min_user_id
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
            data['website_url'] = json_response['result']['website']
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
            data['latlng'] = {"type":"Point","coordinates":[float(json_response['result']['geometry']['location']['lng']) ,float(json_response['result']['geometry']['location']['lat'])]}
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
        
        return data

    def search_google_places(self, user_id, q=""):
        ''' This function is used to make queries to google places api '''        
        from TweetFeed import UserProfile
        user_profile_obj = UserProfile()

        logged_user = user_profile_obj.get_profile_by_id(user_id)        
        location = str(logged_user['latlng']['coordinates'][1]) + ',' + str(logged_user['latlng']['coordinates'][0])

        get_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
        payload = {
            'key':KEY,
            'radius':'20000000',
            'input':q.lower(),
            'location':location,
            'rankby':'distance'
        }

        r = requests.get(get_url,params=payload)
        json_response = json.loads(r.text)
        search_results =  json_response['predictions'][0:5]
        
        return_results = []
        # print json_response

        for eachResult in search_results:
            data = {
                'name' : eachResult['description']
            }


            get_url = 'https://maps.googleapis.com/maps/api/place/details/json'
            payload = {
            'placeid':eachResult['place_id'],
            'key':KEY
            }
            r = requests.get(get_url,params=payload)

            json_response = json.loads(r.text)
        

            try:
                data['profile_img'] = 'https://maps.googleapis.com/maps/api/place/photo?key=' + KEY + '&maxwidth=400&photoreference='+json_response['result']['photos'][0]['photo_reference']
            except:
                data['profile_img'] = 'https://maps.googleapis.com/maps/api/place/photo?key=' + KEY + '&photoreference='+eachResult['reference']
            try:
                data['useruid'] = str(eachResult['place_id']) + '__gp__'
                data['username'] = ''
                data['screen_name'] = ''
            except:
                pass

            data['address'] = ''                    
            return_results.append(data)                        
        return return_results