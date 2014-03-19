#!/usr/bin/env python
# encoding: utf-8
import re
from MongoConnection import MongoConnection
from bson.objectid import ObjectId

class UserProfile():
    def __init__ (self, host="localhost", port=27017,             
                db_name='foodtrade', conn_type='local', username='', password=''):
        if conn_type =='local':
            self.db_object = MongoConnection(host,port,db_name)
            self.table_name = 'userprofile'
            self.db_object.create_table(self.table_name,'useruid')
        else:
            self.db_object = MongoConnection(host=host, port=port,             
                db_name=db_name, conn_type=conn_type, username=username, password=password)
            self.table_name = 'userprofile'
            self.db_object.create_table(self.table_name, 'useruid')

    def get_all_profiles(self, status):
        users = []
        if status == 'None':
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}})/15)+ 1
        else:
            user_pages_count = int(self.db_object.get_count(self.table_name, {'newsletter_freq':status})/15)+ 1
        for i in range(0,user_pages_count, 1):
            if status == 'None':
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':{'$exists':False}, 'email':{'$ne':''}}, pageNumber = int(i+1))
            else:    
                pag_users = self.db_object.get_paginated_values(self.table_name, {'newsletter_freq':status}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)
        return users

    def get_all_users(self):
        users = []
        user_pages_count = int(self.db_object.get_count(self.table_name, {'is_unknown_profile':'false'})/15)+ 1
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'is_unknown_profile':'false'}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)

        user_pages_count = int(self.db_object.get_count(self.table_name, {'is_unknown_profile':{'$exists':'false'}})/15)+ 1        
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'is_unknown_profile':{'$exists':'false'}}, pageNumber = int(i+1))
            for eachUser in pag_users:
                if eachUser not in users:
                    users.append(eachUser)                        
        print len(users)
        return users

    def get_all_profiles_by_time(self, start):
        users = []
        user_pages_count = int(self.db_object.get_count(self.table_name, {'join_time':{'$gt':start}, 'is_unknown_profile': 'false'}))
        for i in range(0,user_pages_count, 1):
            pag_users = self.db_object.get_paginated_values(self.table_name, {'join_time':{'$gt':start}, 'is_unknown_profile': 'false'}, pageNumber = int(i+1))
            for eachUser in pag_users:
                users.append(eachUser)
        return users 

    def get_minimum_id_of_user(self):
        return self.db_object.aggregrate_all(self.table_name, [ { '$group': { '_id':0, 'minId': { '$min': "$useruid"} } } ] )

    def get_profile_by_id(self,user_id):
        return self.db_object.get_one(self.table_name,{'useruid': int(user_id)})

    def get_profile_by_profile_img(self, img):
        return self.db_object.get_one(self.table_name,{'profile_img': img})

    def get_profile_by_username(self, username):
        # return self.db_object.get_one(self.table_name,{'username': str(username)})
        return self.db_object.get_one(self.table_name,{'username': { "$regex" : re.compile("^"+str(username)+"$", re.IGNORECASE), "$options" : "-i" }})

    def get_profile_by_type(self, type_usr):
        return self.db_object.get_all(self.table_name,{'sign_up_as':type_usr})

    def create_profile (self, value):
        self.db_object.insert_one(self.table_name,value)

    def update_profile_fields(self, where, what):
        self.db_object.update(self.table_name, where, what)

    def subscribe(self, useruid):
        self.db_object.update(self.table_name, {"useruid":useruid}, {"subscribed":1})

    def update_profile(self, userid, description, address, type_usr, sign_up_as, phone, lat, lon, postal_code):
        return self.db_object.update(self.table_name,
             {'useruid':int(userid)},
             {'zip_code':str(postal_code),
             'description':str(description),
             'latlng.coordinates.1':float(lat),
             'latlng.coordinates.0':float(lon),
             'address':str(address),
             'type_user':type_usr,
             'sign_up_as':sign_up_as, 
             'phone_number':str(phone)}
             )

    def update_profile_by_username(self, username, description, address, type_usr, sign_up_as, phone, lat, lon, postal_code, name, is_superuser,
      company_num, website_url, facebook_page, deliverables, business_org_name, email, newsletter_freq, show_foods):

        data = {'zip_code':str(postal_code),
                 'description':description,
                 'latlng.coordinates.1':float(lat),
                 'latlng.coordinates.0':float(lon),
                 'address':str(address),
                 'type_user':type_usr,
                 'sign_up_as':sign_up_as, 
                 'phone_number':str(phone),
                 'name':name,
                 'company_num': company_num,
                 'website_url': website_url,
                 'facebook_page': facebook_page,
                 'deliverables': deliverables,
                 'business_org_name': business_org_name,
                 'email':email,
                 'newsletter_freq':newsletter_freq,
                 'show_foods': show_foods
                 }
        if not is_superuser: 
            return self.db_object.update(self.table_name,
                 {'username':username},
                 data)
        else:
            data['recently_updated_by_super_user'] = 'true'
            return self.db_object.update(self.table_name,
                 {'username':username},
                 data)

    def update_profile_upsert(self, where, what):
        return self.db_object.update_upsert(self.table_name, where, what)

    def check_valid_email(self, username, email):
        user = self.db_object.get_one(self.table_name, {'username':username})
        new_email_user = self.db_object.get_one(self.table_name, {'email':email})
        if  new_email_user!= None:
            if user['email'] == email:
                return True
            return False
        else:
            return True

    def get_unclaimed_unedited_profile_count(self):
        return self.db_object.get_count(self.table_name, {'is_unknown_profile':'true', 'recently_updated_by_super_user':'false'})

    def get_unclaimed_edited_profile_count(self):
        return self.db_object.get_count(self.table_name, {'is_unknown_profile':'true', 'recently_updated_by_super_user':'true'})

    def get_unclaimed_profile_paginated(self, pagenum = 1, edit_value = 0):
        return self.db_object.get_paginated_values(self.table_name, 
            conditions = {'is_unknown_profile':'true','recently_updated_by_super_user':str(bool(edit_value)).lower()}, pageNumber = pagenum)

    def search_profiles(self):
        mapper = Code("""
            function () {
            
            var keyword = '"""+keyword+"""';
            keyword = keyword.toLowerCase();
            {"useruid": str(userid), "sign_up_as": sign_up_types[0],
                                          "type_user":str(','.join(type_user)),
                                            "zip_code": new_location[0], "address": new_location[3],
                                           "latitude": float(new_location[1]), "longitude": float(new_location[2]), 
                                           }
            
            var sign_up_as = this.sign_up_as.toLowerCase();
            var user_types = this.type_user.toLowerCase();
            var longitude = this.longitde;
            var latitude = this.latitude;


           
            var search_more = true;
            if(keyword == sign_up_as)
            {
                search_more = false;
            }

            var type_array = user_types.split();
            if(type_array.indexOf(keyword)!=-1)
            {
                search_more = false;
            }

            try
              {
               var user_name = this.username;

                        var name = this.name;

                        
                        var description = this.description;
                        if(user_name.indexOf(keyword) != -1 || name.indexOf(keyword) != -1 || description.indexOf(keyword) != -1 )
                        {
                            search_more = false;

                        }
              }
            catch(err)
              {
              
              }

            if(!search_more)
            {




              var lon1 = parseFloat("""+str(lon)+""");
               var lat1 = parseFloat("""+str(lat)+""");
               var lon2 = longitude;
               var lat2 = latitude;
               var R = 6371; // Radius of the earth in km
              var dLat = (lat2-lat1)* (Math.PI/180);  // deg2rad below
              var dLon = (lon2-lon1)* (Math.PI/180); 
              var a = 
                Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos((lat1)* (Math.PI/180)) * Math.cos((lat2)* (Math.PI/180)) * 
                Math.sin(dLon/2) * Math.sin(dLon/2)
                ; 
              var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
              var d = R * c; // Distance in km
              var ret_value =
              emit(this._id, d);
        }
                           


            }
            """)

        reducer = Code("""
            function (key, values) { 
            var  sum = 0
             for(var i=0;i<values.length;i++)
             { sum += 1;}
             return sum;
            }
            """)
        return self.db_object.map_reduce(self.table_name, mapper, reducer, query, -1, 200)