val = """Agricultural Suppliers
Agricultural Suppliers/Animal Feed
Agricultural Suppliers/Compost
Agricultural Suppliers/Livestock Breeder
Agricultural Suppliers/Nursery
Agricultural Suppliers/Seeds
Food service
Food service/Art_gallery
Food service/Bar
Food service/Cafe
Food service/Catering Contractor
Food service/Food Stall
Food service/Home Cooking Service
Food service/Hostel
Food service/Hotel
Food service/Lodging
Food service/Museum
Food service/Pub
Food service/Public sector
Food service/Restaurant
Food service/School ||| University
Food service/Take Away Food Shops
Meal_delivery
Processing and Manufacture
Processing and Manufacture/Drink
Processing and Manufacture/Drink/Brewery
Processing and Manufacture/Drink/Cider Maker
Processing and Manufacture/Drink/Coffee Importer
Processing and Manufacture/Drink/Distillery
Processing and Manufacture/Drink/Tea Importer
Processing and Manufacture/Drink/Winery
Processing and Manufacture/Food
Processing and Manufacture/Food/Bakery
Processing and Manufacture/Food/Butcher
Processing and Manufacture/Food/Cheesemaker
Processing and Manufacture/Food/Confectioner
Processing and Manufacture/Food/Pasta & Noodles
Processing and Manufacture/Food/Piemaker
Processing and Manufacture/Processing
Processing and Manufacture/Processing/Abbatoir
Processing and Manufacture/Processing/Bottling
Processing and Manufacture/Processing/Canning
Processing and Manufacture/Processing/Dairy
Processing and Manufacture/Processing/Frozen foods
Processing and Manufacture/Processing/Kitchen
Processing and Manufacture/Processing/Mill
Processing and Manufacture/Processing/Smokery
Processing and Manufacture/Waste disposal
Production
Production/Arable Farm
Production/Bee keeping
Production/Box Scheme
Production/Community Supported Agriculture (CSA)
Production/Dairy
Production/Fish
Production/Forager
Production/Horticulture
Production/Livestock Farm
Production/Market garden
Production/Mixed farm
Production/Orchard
Production/Other
Production/Smallholder
Production/Vineyard
Real_estate_agency
Retail
Retail/Baker
Retail/Butcher
Retail/Cheese Shop
Retail/Chocolatier
Retail/Confectioner
Retail/Convenience Store
Retail/Delicatessen
Retail/Farm Shop
Retail/Fishmonger
Retail/Fruitseller
Retail/Greengrocer
Retail/Health food
Retail/Market
Retail/Newsagent
Retail/Off licence
Retail/Supermarket
Rickmansworth
Wholesale and Distribution
Wholesale and Distribution/Cash and Carry
Wholesale and Distribution/Community food group
Wholesale and Distribution/Wholesale Market
Wholesale and Distribution/Wholesaler
Wholesale and Distribution/Wine Merchant"""
import json
import random
def get_unique_types():
	name_list = val.split('\n')
	data = []

	for item in name_list:
		items = item.split('/')
		for i in items:
			i = i.replace('|||','')
			data.append(i)
	random.shuffle(data)
	item_no = int(random.randrange(1, 7))
	user_types = data[:item_no]
	return ','.join(user_types)

