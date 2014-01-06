from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
import pymongo
import json

class Tags():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'tags'
    
    def get_tags(self):
        try:
            return self.db_object.get_one(self.table_name,{})['tags']
        except:
            self.db_object.insert_one(self.table_name,json.loads('{"parent":1,"tags":[{"node": "Agricultural Suppliers", "childrens": [{"node": "Animal Feed"}, {"node": "Compost"}, {"node": "Livestock Breeder"}, {"node": "Nursery"}, {"node": "Seeds"}]}, {"node": "Food service", "childrens": [{"node": "Art_gallery"}, {"node": "Bar"}, {"node": "Cafe"}, {"node": "Catering Contractor"}, {"node": "Food Stall"}, {"node": "Home Cooking Service"}, {"node": "Hostel"}, {"node": "Hotel"}, {"node": "Lodging"}, {"node": "Museum"}, {"node": "Pub"}, {"node": "Public sector"}, {"node": "Restaurant"}, {"node": "School  University"}, {"node": "Take Away Food Shops"}]}, {"node": "Meal_delivery"}, {"node": "Processing and Manufacture", "childrens": [{"node": "Drink"}, {"node": "Food"}, {"node": "Processing"}, {"node": "Waste disposal"}]}, {"node": "Production", "childrens": [{"node": "Arable Farm"}, {"node": "Bee keeping"}, {"node": "Box Scheme"}, {"node": "Community Supported Agriculture (CSA)"}, {"node": "Dairy"}, {"node": "Fish"}, {"node": "Forager"}, {"node": "Horticulture"}, {"node": "Livestock Farm"}, {"node": "Market garden"}, {"node": "Mixed farm"}, {"node": "Orchard"}, {"node": "Other"}, {"node": "Smallholder"}, {"node": "Vineyard"}]}, {"node": "Real_estate_agency"}, {"node": "Retail", "childrens": [{"node": "Baker"}, {"node": "Butcher"}, {"node": "Cheese Shop"}, {"node": "Chocolatier"}, {"node": "Confectioner"}, {"node": "Convenience Store"}, {"node": "Delicatessen"}, {"node": "Farm Shop"}, {"node": "Fishmonger"}, {"node": "Fruitseller"}, {"node": "Greengrocer"}, {"node": "Health food"}, {"node": "Market"}, {"node": "Newsagent"}, {"node": "Off licence"}, {"node": "Supermarket"}]}, {"node": "Rickmansworth"}, {"node": "Wholesale and Distribution", "childrens": [{"node": "Cash and Carry"}, {"node": "Community food group"}, {"node": "Wholesale Market"}, {"node": "Wholesaler"}, {"node": "Wine Merchant"}]}]}'))
            return self.db_object.get_one(self.table_name,{"parent":1})['tags']



    def set_tags(self,tags):
        try:
            val = self.db_object.get_one(self.table_name,{})['tags']
            return self.db_object.update(self.table_name,{'parent':1}, {'tags':tags['tags']})
        except:
            return self.db_object.insert_one(self.table_name,tags)
        




