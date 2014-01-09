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
	return user_types



foods = """Meat/Beef
Meat/Bison
Meat/Buffalo
Meat/Chicken
Meat/Duck
Meat/Geese/goose
Meat/Lamb
Meat/Mutton
Meat/Ostrich
Meat/Pork
Meat/Turkey
Meat/Veal
Meat/Game/Partridge
Meat/Game/Pheasant
Meat/Game/Rabbit
Meat/Game/Hare/levret
Meat/Game/Venison
Meat/Processed meat/Bacon
Meat/Processed meat/Burgers
Meat/Processed meat/Cured meat
Meat/Processed meat/Gelatins
Meat/Processed meat/Haggis
Meat/Processed meat/Ham
Meat/Processed meat/Lunch meat
Meat/Processed meat/Meat Pies
Meat/Processed meat/Meatballs/Faggots
Meat/Processed meat/Mincemeat
Meat/Processed meat/Pasties
Meat/Processed meat/Pate
Meat/Processed meat/Pork Pies
Meat/Processed meat/Sausages
Meat/Processed meat/Scotch Eggs
Meat/Processed meat/Smoked Duck/Chicken
Meat/Processed meat/Spiced Chicken
Fish/Bass
Fish/Bream
Fish/Cod
Fish/Haddock
Fish/Mackerel
Fish/Salmon
Fish/Trout
Fish/Salmon
Fish/Mackerel
Fish/Trout
Fish/American Shad
Fish/American Sole
Fish/Anchovy
Fish/Antarctic Cod
Fish/Arrowtooth Eel
Fish/Asian Carps
Fish/Atka Mackerel
Fish/Atlantic Bonito
Fish/Atlantic Cod
Fish/Atlantic Eel
Fish/Atlantic Herring
Fish/Atlantic Salmon
Fish/Atlantic Trout
Fish/Australasian Salmon
Fish/Bar Jack
Fish/Bat Fish
Fish/Barramundi
Fish/Basa Fish
Fish/Black Mackerel
Fish/Blue Cod
Fish/Bluegill
Fish/Bluefish
Fish/Bombay Duck
Fish/Brook Trout
Fish/Butterfish
Fish/California Halibut
Fish/California Sheephead
Fish/Capelin
Fish/Carp
Fish/Catfish
Fish/Cherry Salmon
Fish/Chinook Salmon
Fish/Chum Salmon
Fish/Cobia
Fish/Cod
Fish/Coho Salmon
Fish/Coley
Fish/Common Carp
Fish/Crappie
Fish/Crawfish
Fish/Dory
Fish/Discus
Fish/Drum
Fish/Dino
Fish/Eel
Fish/European Eel
Fish/European Flounder
Fish/Flathead
Fish/Flatfish
Fish/Flounder
Fish/Freshwater Eel
Fish/Freshwater Herring
Fish/Flying Fish
Fish/Giant Gourami
Fish/Gilt-head Bream
Fish/Golden Dorado
Fish/Groundfish
Fish/Grouper
Fish/Gar
Fish/Haddock
Fish/Hake
Fish/Halibut
Fish/Harvestfish
Fish/Herring
Fish/Hilsa
Fish/Hoki
Fish/Iridescent Shark/Basa Fish
Fish/Japanese Butterfish
Fish/John Dory
Fish/Kapenta
Fish/Kingklip
Fish/Lemon Sole
Fish/Largemouth Bass
Fish/Mackerel
Fish/Maori Cod
Fish/Mahi-mahi
Fish/Marlin
Fish/Milkfish
Fish/Monkfish
Fish/Mullet
Fish/Mullus Surmuletus
Fish/Northern Anchovy
Fish/Northern Pike
Fish/Northern Snakehead
Fish/Norwegian Atlantic Salmon
Fish/Orange Roughy
Fish/Oscar
Fish/Pacific Herring
Fish/Pacific Salmon
Fish/Pacific Saury
Fish/Pacific Trout
Fish/Panfish
Fish/Pangasius
Fish/Patagonian Toothfish
Fish/Pelagic Cod
Fish/Perch
Fish/Pink Salmon
Fish/Pollock
Fish/Pomfret
Fish/Pilchard
Fish/Paddlefish
Fish/Plaice
Fish/Pacific Cod
Fish/Quoy Fish
Fish/Rainbow Trout
Fish/Redfish
Fish/Red Snapper
Fish/Rock Fish
Fish/Round Herring
Fish/Salmon
Fish/Sardine
Fish/Saury
Fish/Scrod
Fish/Sea Bass
Fish/Seer Fish
Fish/Shad
Fish/Shrimpfish
Fish/Silver Carp
Fish/Skipjack Tuna
Fish/Slender Rainbow Sardine
Fish/Sole
Fish/Snakeskin Gourami
Fish/Snapper
Fish/Snook
Fish/Snoek
Fish/Spanish Mackerel
Fish/Surf Sardine
Fish/Swamp-eel
Fish/Swordfish
Fish/Skate
Fish/Sunfish  Bluegill
Fish/Smallmouth Bass
Fish/Spoonbill/Paddlefish
Fish/Thresher Shark
Fish/Tilapia
Fish/Tilefish
Fish/Trout
Fish/Tuna
Fish/Turbot
Fish/Yellowfin Tuna
Fish/Zander
Fish/Caviar
Fish/Roe (cod)
Fish/Processed Fish/Fishcakes
Fish/Processed Fish/Fishpie
Fish/Processed Fish/Fishfingers
Fish/Processed Fish/Sushi
Shellfish/Prawns
Shellfish/Oysters
Shellfish/Lobster
Shellfish/Clams
Shellfish/Crabs
Shellfish/Shrimp
Shellfish/Cockles
Shellfish/Mussels
Shellfish/Scallops
Shellfish/Whelks
Shellfish/Winkles
Dairy/Butter
Dairy/Cream/Clotted cream
Dairy/Cream/Single cream
Dairy/Cream/Double cream
Dairy/Milk/Cow's milk
Dairy/Milk/Goat's milk
Dairy/Cheese/Chedder
Dairy/Cheese/Goat
Dairy/Cheese/Brie
Dairy/Cheese/Stilton
Dairy/Cheese /
Dairy/Cheese/Blue cheese/Bath Blue cheese
Dairy/Cheese/Blue cheese/Barkham Blue cheese
Dairy/Cheese/Blue cheese/Blue Monday cheese
Dairy/Cheese/Blue cheese/Buxton Blue cheese
Dairy/Cheese/Blue cheese/Cheshire Blue cheese
Dairy/Cheese/Blue cheese/Devon Blue cheese
Dairy/Cheese/Blue cheese/Dorset Blue Vinney cheese
Dairy/Cheese/Blue cheese/Dovedale cheese
Dairy/Cheese/Blue cheese/Exmoor Blue cheese
Dairy/Cheese/Blue cheese/Harbourne Blue cheese
Dairy/Cheese/Blue cheese/Lanark Blue  cheese
Dairy/Cheese/Blue cheese/Oxford Blue cheese
Dairy/Cheese/Blue cheese/Shropshire Blue cheese
Dairy/Cheese/Blue cheese/Stichelton cheese
Dairy/Cheese/Blue cheese/Stilton cheese
Dairy/Cheese/Blue cheese/Blue Wensleydale cheese
Dairy/Cheese/Blue cheese/Yorkshire Blue cheese
Dairy/Cheese/Appledore cheese
Dairy/Cheese/Berkswell cheese
Dairy/Cheese/Bonchester cheese
Dairy/Cheese/Brie cheese
Dairy/Cheese/Somerset Brie
Dairy/Cheese/Cornish Brie cheese
Dairy/Cheese/Brinkburn cheese
Dairy/Cheese/Caithness cheese
Dairy/Cheese/Caboc cheese
Dairy/Cheese/Caerphilly cheese
Dairy/Cheese/Cheddar cheese
Dairy/Cheese/West Country Farmhouse Cheddar cheese
Dairy/Cheese/Applewood cheese
Dairy/Cheese/Coleraine Cheddar cheese
Dairy/Cheese/Cheshire cheese
Dairy/Cheese/Appleby Cheshire cheese
Dairy/Cheese/Chevington cheese
Dairy/Cheese/Coquetdale cheese
Dairy/Cheese/Cornish Pepper cheese
Dairy/Cheese/Cotherstone cheese
Dairy/Cheese/Cotswold cheese
Dairy/Cheese/Coverdale cheese
Dairy/Cheese/Croglin cheese
Dairy/Cheese/Crowdie cheese
Dairy/Cheese/Derby cheese
Dairy/Cheese/Double Gloucester cheese
Dairy/Cheese/Goosnargh Gold cheese
Dairy/Cheese/Dorstone cheese
Dairy/Cheese/Dovedale cheese
Dairy/Cheese/Farmhouse Llanboidy cheese
Dairy/Cheese/Fine Fettle Yorkshire cheese
Dairy/Cheese/Black Eyed Susan cheese
Dairy/Cheese/Golden Cross cheese
Dairy/Cheese/Gruth Dhu cheese
Dairy/Cheese/Harlech cheese
Dairy/Cheese/Hereford Hop cheese
Dairy/Cheese/Huntsman cheese
Dairy/Cheese/Ilchester cheese
Dairy/Cheese/Innkeepers Choice cheese
Dairy/Cheese/Isle Of Mull cheese
Dairy/Cheese/Lancashire cheese
Dairy/Cheese/Beacon Fell Traditional Lancashire cheese
Dairy/Cheese/Lincolnshire Poacher cheese
Dairy/Cheese/Little Wallop cheese
Dairy/Cheese/Katy's White Lavender cheese
Dairy/Cheese/Kidderton Ash cheese
Dairy/Cheese/Lord Of The Hundreds cheese
Dairy/Cheese/Lowerdale Goats Cheese cheese
Dairy/Cheese/Pantysgawn cheese
Dairy/Cheese/Red Devil cheese
Dairy/Cheese/Red Dragon cheese
Dairy/Cheese/Red Leicester cheese
Dairy/Cheese/Rothbury Red cheese
Dairy/Cheese/Red Windsor cheese
Dairy/Cheese/Sage Derby cheese
Dairy/Cheese/Single Gloucester cheese
Dairy/Cheese/Stinking Bishop cheese
Dairy/Cheese/Sussex Slipcote cheese
Dairy/Cheese/Swaledale cheese
Dairy/Cheese/Teviotdale  cheese
Dairy/Cheese/Tintern cheese
Dairy/Cheese/Waterloo cheese
Dairy/Cheese/Wensleydale cheese
Dairy/Cheese/White Stilton cheese
Dairy/Cheese/Suffolk Gold cheese
Dairy/Cheese/Whitehaven cheese
Dairy/Cheese/Yarg cheese
Dairy/Cheese/Wild Garlic Yarg cheese
Dairy/Cheese/Wiltshire Loaf
Dairy/Cheese/Woolsery Goats cheese
Dairy/Cheese/Village Green Goat
Dairy/Cheese/Y Fenni cheese
Dairy/Ice Cream/Sorbets
Dairy/Yoghurt
Eggs/Chicken
Eggs/Duck
Eggs/Quails
Eggs/Goose/geese
Eggs/Turkey
Fruit/Apples   
Fruit/Apricots
Fruit/Bananas
Fruit/Bilberry
Fruit/Blackberries
Fruit/Blackcurrants
Fruit/Blueberries
Fruit/Cherimoya
Fruit/Cherries
Fruit/Clementine
Fruit/Coconuts
Fruit/Cranberries
Fruit/Currant
Fruit/Damson
Fruit/Dates
Fruit/Dragon fruit
Fruit/Durians 
Fruit/Elderberry
Fruit/Feijoa
Fruit/Fig
Fruit/Gooseberries
Fruit/Gooseberry
Fruit/Grape
Fruit/Grapefruit
Fruit/Grapes
Fruit/Guava
Fruit/Honeydew melon
Fruit/Huckleberry
Fruit/Jack fruit 
Fruit/Jambul
Fruit/Kiwi fruit
Fruit/Kumquat
Fruit/Legume
Fruit/Lemon  
Fruit/Limes
Fruit/Lychee
Fruit/Mandarine
Fruit/Mango  
Fruit/Mangostine
Fruit/Medlar
Fruit/Melon/cantaloupe
Fruit/Nectarines
Fruit/Oranges
Fruit/Papaya
Fruit/Peach
Fruit/Pears
Fruit/Physalis
Fruit/Pineapple
Fruit/Pitaya
Fruit/Plum, prune
Fruit/Pomegranates
Fruit/Prunes
Fruit/Quince 
Fruit/Raisins
Fruit/Rambutan
Fruit/Raspberries 
Fruit/Redcurrants
Fruit/Rhubarb
Fruit/Salal berry
Fruit/Satsuma
Fruit/Star fruit
Fruit/Strawberries 
Fruit/Tangerines
Fruit/Ugli fruit 
Fruit/Watermelon  
Fruit/Processed fruits/Canned fruit
Fruit/Processed fruits/Frozen fruit
Fruit/Processed fruits/Fruit sauces
Fruit/Processed fruits/Jam
Fruit/Processed fruits/Pie fillings
Vegetables/Artichokes/Jerusalem
Vegetables/Artichokes/Globe 
Vegetables/Aubergine
Vegetables/Alfalfa sprouts
Vegetables/Anise
Vegetables/Artichoke
Vegetables/Arugula
Vegetables/Asparagus
Vegetables/Aubergine, Eggplant
Vegetables/Avocados 
Vegetables/Beansprouts
Vegetables/Bell pepper
Vegetables/Beetroot, Beet
Vegetables/Breadfruit
Vegetables/Broccoflower 
Vegetables/Broccoli/Purple Sprouting Broccoli
Vegetables/Brussels sprouts
Vegetables/Cabbage/Red
Vegetables/Cabbage/White
Vegetables/Cabbage/Green 
Vegetables/Calabrese 
Vegetables/Celeriac
Vegetables/Chinese leaves, Bok choy
Vegetables/Collard greens
Vegetables/Corn salad
Vegetables/Carrots
Vegetables/Cauliflflower
Vegetables/Celery
Vegetables/Chard 
Vegetables/Cucumbers 
Vegetables/Crimini
Vegetables/Daikon
Vegetables/Endive
Vegetables/Fennel 
Vegetables/Fiddlehead fern
Vegetables/Frisee leaves
Vegetables/Garlic
Vegetables/Jicama
Vegetables/Kale/Curly kale
Vegetables/Kale/Mixed kale
Vegetables/Kohlrabi
Vegetables/Leeks
Vegetables/Lettuce/Romaine
Vegetables/Lettuce/Iceberg
Vegetables/Marrow
Vegetables/Mushrooms/Shiitake mushrooms
Vegetables/Mushrooms/Truffles
Vegetables/Mushrooms/Boletus mushrooms
Vegetables/Mushrooms/Oyster mushrooms
Vegetables/Mushrooms/Wild mushrooms
Vegetables/Mushrooms/Button mushrooms
Vegetables/Mustard greens
Vegetables/Nettles 
Vegetables/Okra
Vegetables/Olives
Vegetables/Onions
Vegetables/Pakchoi
Vegetables/Parsnips
Vegetables/Potatoes/Charlotte potatoes
Vegetables/Potatoes/King Edward potatoes
Vegetables/Potatoes/Estima potatoes
Vegetables/Potatoes/Maris Piper potatoes
Vegetables/Potatoes/Desiree potatoes
Vegetables/Potatoes/Marfona potatoes
Vegetables/Potatoes/Anya potatoes
Vegetables/Potatoes/Nicola potatoes
Vegetables/Potatoes/Rooster potatoes
Vegetables/Potatoes/Sante potatoes
Vegetables/Potatoes/Accord potatoes
Vegetables/Potatoes/Carlingford potatoes
Vegetables/Potatoes/Romano potatoes
Vegetables/Potatoes/Sweet potatoes, yams
Vegetables/Rocket
Vegetables/Radicchio
Vegetables/Radish
Vegetables/Rhubarb
Vegetables/Salad
Vegetables/Salad Packs
Vegetables/Salsify 
Vegetables/Savoy Cabbage
Vegetables/Sea Vegetables 
Vegetables/Shallots
Vegetables/Skirret 
Vegetables/Spinach
Vegetables/Spring Greens 
Vegetables/Spring onions, Green onion, Scallion
Vegetables/Sprouted Seeds 
Vegetables/Squashes/Acorn squash
Vegetables/Squashes/Butternut squash
Vegetables/Squashes/Courgette, Zucchini
Vegetables/Squashes/Cucumber 
Vegetables/Squashes/Gem squash
Vegetables/Squashes/Marrow, Squash
Vegetables/Squashes/Pumpkin
Vegetables/Squashes/Spaghetti squash
Vegetables/Swede, Rutabaga
Vegetables/Sweetcorn, maize, corn
Vegetables/Swiss Chard
Vegetables/Taro 
Vegetables/Tat soi
Vegetables/Tomatoes
Vegetables/Turnips
Vegetables/Turnip Greens 
Vegetables/Watercress  
Vegetables/Wasabi
Vegetables/Water chestnut
Vegetables/White radish
Vegetables/Processed vegetables/Canned vegetables
Vegetables/Processed vegetables/Frozen vegetables
Vegetables/Processed vegetables/French fries
Beans & Legumes/Azuki beans, Adzuki beans
Beans & Legumes/Bean sprouts
Beans & Legumes/Black beans
Beans & Legumes/Black-eyed peas
Beans & Legumes/Borlotti beans
Beans & Legumes/Broad beans
Beans & Legumes/Butter Beans
Beans & Legumes/Chickpeas, Garbanzo beans, Ceci beans
Beans & Legumes/Dried Peas
Beans & Legumes/Green beans
Beans & Legumes/Kidney beans
Beans & Legumes/Lentils
Beans & Legumes/Lima bean, Butter bean
Beans & Legumes/Miso
Beans & Legumes/Mung beans
Beans & Legumes/Navy beans
Beans & Legumes/Peas/Mangetout, Sugar snap peas
Beans & Legumes/Pinto beans
Beans & Legumes/Runner beans
Beans & Legumes/Soy beans
Beans & Legumes/Soybeans
Beans & Legumes/Tempeh
Beans & Legumes/Tofu
Beans & Legumes/Vigna Beans
Nuts, Seeds & Oils/Almonds
Nuts, Seeds & Oils/Apricot Kernels
Nuts, Seeds & Oils/Betel Nuts
Nuts, Seeds & Oils/Brazil Nuts
Nuts, Seeds & Oils/Cashews
Nuts, Seeds & Oils/Chestnuts
Nuts, Seeds & Oils/Flaxseeds
Nuts, Seeds & Oils/Ginkgo Nuts
Nuts, Seeds & Oils/Hazelnuts
Nuts, Seeds & Oils/Macadamia Nuts
Nuts, Seeds & Oils/Melon Seeds
Nuts, Seeds & Oils/Olive Oil
Nuts, Seeds & Oils/Peanuts
Nuts, Seeds & Oils/Pecan Nuts
Nuts, Seeds & Oils/Pine Nuts
Nuts, Seeds & Oils/Pistachio Nuts
Nuts, Seeds & Oils/Pumpkin Seeds
Nuts, Seeds & Oils/Sesame Seeds
Nuts, Seeds & Oils/Sunflower Kernels
Nuts, Seeds & Oils/Sunflower Seeds
Nuts, Seeds & Oils/Walnuts
Herbs & Spices/Ajwain, carom seeds
Herbs & Spices/Akudjura
Herbs & Spices/Alexanders
Herbs & Spices/Allspice
Herbs & Spices/Angelica
Herbs & Spices/Anise
Herbs & Spices/Aniseed myrtle
Herbs & Spices/Annatto
Herbs & Spices/Apple mint
Herbs & Spices/Arrowroot starch
Herbs & Spices/Avocado leaf
Herbs & Spices/Barberry
Herbs & Spices/Basil
Herbs & Spices/Bay leaf
Herbs & Spices/Black cardamom
Herbs & Spices/Boldo
Herbs & Spices/Borage
Herbs & Spices/Calendula, pot marigold
Herbs & Spices/Camphor laurel
Herbs & Spices/Caraway
Herbs & Spices/Cardamom
Herbs & Spices/Carob
Herbs & Spices/Cassia
Herbs & Spices/Catnip
Herbs & Spices/Celery seed
Herbs & Spices/Chervil
Herbs & Spices/Chicory
Herbs & Spices/Chili powder
Herbs & Spices/Chives
Herbs & Spices/Cicely
Herbs & Spices/Cilantro, coriander greens, coriander herb
Herbs & Spices/Cinnamon
Herbs & Spices/Cinnamon myrtle
Herbs & Spices/Clary, Clary sage
Herbs & Spices/Cloves
Herbs & Spices/Coriander
Herbs & Spices/Coriander seed
Herbs & Spices/Costmary
Herbs & Spices/Cream of tartar
Herbs & Spices/Cudweed
Herbs & Spices/Cumin
Herbs & Spices/Cumin Seeds
Herbs & Spices/Curry leaf
Herbs & Spices/Curry plant
Herbs & Spices/Curry powder
Herbs & Spices/Dill
Herbs & Spices/Dill seed
Herbs & Spices/Elderflower
Herbs & Spices/Epazote
Herbs & Spices/Fennel
Herbs & Spices/Fennel seeds
Herbs & Spices/Fenugreek
Herbs & Spices/File powder, gumbo file
Herbs & Spices/Fingerroot, krachai, temu kuntji
Herbs & Spices/Five-spice powder 
Herbs & Spices/Galingale
Herbs & Spices/Garlic/Garlic powder
Herbs & Spices/Garlic/Elephant garlic
Herbs & Spices/Garlic chives
Herbs & Spices/Ginger
Herbs & Spices/Golpar, Persian hogweed
Herbs & Spices/Grains of paradise
Herbs & Spices/Horseradish
Herbs & Spices/Houttuynia cordata
Herbs & Spices/Huacatay, Mexican marigold, mint marigold
Herbs & Spices/Hyssop
Herbs & Spices/Jasmine flowers
Herbs & Spices/Jimbu
Herbs & Spices/Juniper berry
Herbs & Spices/Kaffir lime leaves, Makrud lime leaves
Herbs & Spices/Kala zeera , black cumin
Herbs & Spices/Kawakawa seeds
Herbs & Spices/Keluak, kluwak, kepayang
Herbs & Spices/Kencur, galangal, kentjur
Herbs & Spices/Kokam seed
Herbs & Spices/Korarima, Ethiopian cardamom, false cardamon
Herbs & Spices/Koseret leaves
Herbs & Spices/Lavender
Herbs & Spices/Lemon balm
Herbs & Spices/Lemon ironbark
Herbs & Spices/Lemon myrtle
Herbs & Spices/Lemon verbena
Herbs & Spices/Lemongrass
Herbs & Spices/Leptotes bicolor
Herbs & Spices/Lesser calamint , nipitella, nepitella
Herbs & Spices/Licorice, liquorice
Herbs & Spices/Lime flower, linden flower
Herbs & Spices/Lovage
Herbs & Spices/Mace
Herbs & Spices/Mahlab, St. Lucie cherry
Herbs & Spices/Malabathrum, tejpat
Herbs & Spices/Marjoram
Herbs & Spices/Marsh mallow
Herbs & Spices/Mastic
Herbs & Spices/Mint
Herbs & Spices/Mountain horopito
Herbs & Spices/Musk mallow, abelmosk
Herbs & Spices/Mustard/Black mustard
Herbs & Spices/Mustard/Brown mustard
Herbs & Spices/Mustard/Yellow mustard
Herbs & Spices/Mustard/White mustard
Herbs & Spices/Mustard/Mustard seeds
Herbs & Spices/Nasturtium
Herbs & Spices/Nigella, kalonji, black caraway, black onion seed
Herbs & Spices/Njangsa, djansang
Herbs & Spices/Nutmeg
Herbs & Spices/Nutmeg
Herbs & Spices/Olida
Herbs & Spices/Onion powder
Herbs & Spices/Oregano
Herbs & Spices/Orris root
Herbs & Spices/Pandan flower, kewra
Herbs & Spices/Pandan leaf, screwpine
Herbs & Spices/Pandanus amaryllifolius
Herbs & Spices/Paprika
Herbs & Spices/Paracress
Herbs & Spices/Parsley
Herbs & Spices/Pepper/Black pepper
Herbs & Spices/Pepper/Chili pepper/Jalapeno pepper
Herbs & Spices/Pepper/Chili pepper/Habanero pepper
Herbs & Spices/Pepper/Chili pepper/Paprika pepper
Herbs & Spices/Pepper/Chili pepper/Tabasco pepper
Herbs & Spices/Pepper/Chili pepper/Cayenne pepper
Herbs & Spices/Pepper/Cubeb pepper
Herbs & Spices/Pepper/Green pepper
Herbs & Spices/Pepper/Kani pepper
Herbs & Spices/Pepper/Peruvian pepper
Herbs & Spices/Pepper/Pink pepper
Herbs & Spices/Pepper/Red pepper
Herbs & Spices/Pepper/Szechuan pepper
Herbs & Spices/Pepper/White pepper
Herbs & Spices/Peppercorns
Herbs & Spices/Peppermint
Herbs & Spices/Perilla, shiso
Herbs & Spices/Poppy seeds
Herbs & Spices/Quassia
Herbs & Spices/Ramsons, wood garlic
Herbs & Spices/Rice paddy herb
Herbs & Spices/Rosemary
Herbs & Spices/Rue
Herbs & Spices/Safflower
Herbs & Spices/Saffron
Herbs & Spices/Sage
Herbs & Spices/Saigon cinnamon
Herbs & Spices/Salad burnet
Herbs & Spices/Salep
Herbs & Spices/Salt
Herbs & Spices/Sassafras
Herbs & Spices/Sesame seeds
Herbs & Spices/Silphium, silphion, laser, laserpicium, lasarpicium
Herbs & Spices/Sorrel
Herbs & Spices/Spearmint
Herbs & Spices/Spikenard
Herbs & Spices/Star anise
Herbs & Spices/Sumac
Herbs & Spices/Sweet woodruff
Herbs & Spices/Tarragon
Herbs & Spices/Thyme
Herbs & Spices/Turmeric
Herbs & Spices/Turmeric
Herbs & Spices/Turmeric
Herbs & Spices/Vanilla
Herbs & Spices/Vanilla extract
Herbs & Spices/Wasabi
Herbs & Spices/Watercress
Herbs & Spices/Wattleseed
Herbs & Spices/Wild betel
Herbs & Spices/Wild thyme
Herbs & Spices/Willow herb
Herbs & Spices/Winter savory
Herbs & Spices/Wintergreen
Herbs & Spices/Wood avens, herb bennet
Herbs & Spices/Woodruff
Herbs & Spices/Wormwood, absinthe
Herbs & Spices/Yerba buena
Herbs & Spices/Za'atar
Herbs & Spices/Zedoary
Cereal Grains/Rice/Basmati Rice
Cereal Grains/Rice/Black Rice
Cereal Grains/Rice/Broken Rice
Cereal Grains/Rice/Brown Rice
Cereal Grains/Rice/Jasmine Rice
Cereal Grains/Rice/Organic Rice
Cereal Grains/Rice/White Corn
Cereal Grains/Rice/Wild rice
Cereal Grains/Rice/Yellow Corn
Cereal Grains/Amaranth
Cereal Grains/Bamboo shoots
Cereal Grains/Barley
Cereal Grains/Barleygrass
Cereal Grains/Breadnut
Cereal Grains/Buckwheat
Cereal Grains/Bulgur wheat
Cereal Grains/Cattail
Cereal Grains/Chia
Cereal Grains/Cornbread
Cereal Grains/Cornmeal
Cereal Grains/Couscous
Cereal Grains/Crackers
Cereal Grains/Durum wheat
Cereal Grains/Farro, Emmer
Cereal Grains/Flax
Cereal Grains/Flaxseed
Cereal Grains/Fonio
Cereal Grains/Grano
Cereal Grains/Grits
Cereal Grains/Kamut grain
Cereal Grains/Kaniwa
Cereal Grains/Lemongrass, citronella
Cereal Grains/Millet
Cereal Grains/Molasses
Cereal Grains/Muesli, Breakfast cereal, Granola
Cereal Grains/Noodles
Cereal Grains/Oatmeal
Cereal Grains/Oats
Cereal Grains/Other Grain
Cereal Grains/Palmer's grass
Cereal Grains/Pearl Millet
Cereal Grains/Pitseed Goosefoot 
Cereal Grains/Popcorn
Cereal Grains/Quinoa 
Cereal Grains/Rapadura
Cereal Grains/Rye
Cereal Grains/Semolina wheat
Cereal Grains/Sorghum
Cereal Grains/Spelt 
Cereal Grains/Teff
Cereal Grains/Triticale
Cereal Grains/Wattleseed, Acacia seed
Cereal Grains/Wheat 
Cereal Grains/Wheat Berries
Cereal Grains/Wheatgrass 
Cereal Grains/Flour/White flour
Cereal Grains/Flour/Brown flour
Cereal Grains/Flour/Rye flour
Cereal Grains/Flour/Spelt flour
Cereal Grains/Flour/Barley flour
Pasta/Minute pasta
Pasta/Long Noodles
Pasta/Ribbon-Cut Noodles
Pasta/Decorative Shaped Pasta
Pasta/Stuffed pasta
Drinks/Juice/Apple juice
Drinks/Juice/Orange juice
Drinks/Juice/Pear juice
Drinks/Juice/Grape juice
Drinks/Soft drinks/Ginger Beer
Drinks/Soft drinks/Lemonade
Drinks/Alcoholic drinks/Beer/Ale/Barleywine
Drinks/Alcoholic drinks/Beer/Ale/Bitter ale
Drinks/Alcoholic drinks/Beer/Ale/Mild ale
Drinks/Alcoholic drinks/Beer/Ale/Pale ale
Drinks/Alcoholic drinks/Beer/Ale/Porter/Stout
Drinks/Alcoholic drinks/Beer/Ale/Cask ale
Drinks/Alcoholic drinks/Beer/Ale/Stock ale
Drinks/Alcoholic drinks/Beer/Fruit Beer
Drinks/Alcoholic drinks/Beer/Large Beer/Bock
Drinks/Alcoholic drinks/Beer/Large Beer/Dry beer
Drinks/Alcoholic drinks/Beer/Large Beer/Maerzen/Oktoberfest Beer
Drinks/Alcoholic drinks/Beer/Large Beer/Pilsener
Drinks/Alcoholic drinks/Beer/Large Beer/Schwarzbier
Drinks/Alcoholic drinks/Beer/Sahti
Drinks/Alcoholic drinks/Beer/Small beer
Drinks/Alcoholic drinks/Beer/Wheat beer/Witbier White Beer
Drinks/Alcoholic drinks/Beer/Wheat beer/Hefeweizen
Drinks/Alcoholic drinks/Cauim
Drinks/Alcoholic drinks/Chicha
Drinks/Alcoholic drinks/Cider   
Drinks/Alcoholic drinks/Mead
Drinks/Alcoholic drinks/Palm wine
Drinks/Alcoholic drinks/Perry  
Drinks/Alcoholic drinks/Sake    
Drinks/Alcoholic drinks/Wine/Fruit wine
Drinks/Alcoholic drinks/Wine/Table wine
Drinks/Alcoholic drinks/Wine/Sangria
Drinks/Alcoholic drinks/Wine/Sparkling wine/Champagne
Drinks/Alcoholic drinks/Wine/Fortified wine/Port
Drinks/Alcoholic drinks/Wine/Fortified wine/Madeira
Drinks/Alcoholic drinks/Wine/Fortified wine/Marsala
Drinks/Alcoholic drinks/Wine/Fortified wine/Sherry
Drinks/Alcoholic drinks/Wine/Fortified wine/Vermouth
Drinks/Alcoholic drinks/Wine/Fortified wine/Vinsanto
Drinks/Alcoholic drinks/Spirits/Absinthe
Drinks/Alcoholic drinks/Spirits/Akvavit
Drinks/Alcoholic drinks/Spirits/Arak
Drinks/Alcoholic drinks/Spirits/Arrack
Drinks/Alcoholic drinks/Spirits/Baijiu
Drinks/Alcoholic drinks/Spirits/Cachaca
Drinks/Alcoholic drinks/Spirits/Gin/Damson gin
Drinks/Alcoholic drinks/Spirits/Gin/Sloe gin
Drinks/Alcoholic drinks/Spirits/Gulu
Drinks/Alcoholic drinks/Spirits/Horilka
Drinks/Alcoholic drinks/Spirits/Kaoliang
Drinks/Alcoholic drinks/Spirits/Maotai
Drinks/Alcoholic drinks/Spirits/Mezcal
Drinks/Alcoholic drinks/Spirits/Neutral grain spirit
Drinks/Alcoholic drinks/Spirits/Ogogoro
Drinks/Alcoholic drinks/Spirits/Ouzo
Drinks/Alcoholic drinks/Spirits/Palinka
Drinks/Alcoholic drinks/Spirits/Pisco 
Drinks/Alcoholic drinks/Spirits/Rum
Drinks/Alcoholic drinks/Spirits/Soju
Drinks/Alcoholic drinks/Spirits/Tequila
Drinks/Alcoholic drinks/Spirits/Vodka
Drinks/Alcoholic drinks/Spirits/Metaxa
Drinks/Alcoholic drinks/Spirits/Whisky/Bourbon
Drinks/Alcoholic drinks/Spirits/Whisky/Scotch
Drinks/Alcoholic drinks/Spirits/Whisky/Tennessee whiskey
Drinks/Alcoholic drinks/Spirits/Brandy/Armagnac
Drinks/Alcoholic drinks/Spirits/Brandy/Cognac
Drinks/Alcoholic drinks/Spirits/Brandy/Fruit brandy, Eau-de-vie, Schnapps
Drinks/Alcoholic drinks/Spirits/Brandy/Kirsch
Drinks/Tea/Green
Drinks/Tea/Black
Drinks/Tea/Herbal
Drinks/Coffee 
Convenience foods, processed foods/Baby Food
Convenience foods, processed foods/Crisps
Convenience foods, processed foods/Energy bars
Convenience foods, processed foods/Ready meals
Convenience foods, processed foods/Soup
Sweeteners, confection/Agave nectar
Sweeteners, confection/Barley malt syrup
Sweeteners, confection/Birch syrup
Sweeteners, confection/Brown sugar
Sweeteners, confection/Cane sugar
Sweeteners, confection/Chocolate
Sweeteners, confection/Honey
Sweeteners, confection/Maple syrup
Sweeteners, confection/Marshmallows
Sweeteners, confection/Molasses
Sweeteners, confection/Palm sugar
Sweeteners, confection/Shredded coconut
Sweeteners, confection/Sorghum Syrup
Sweeteners, confection/Sugar (beet)
Sweeteners, confection/Sugar (cane)
Sweeteners, confection/Sugar substitutes
Sweeteners, confection/Syrup
Sweeteners, confection/White sugar
Baked goods/Biscuits, cookies
Baked goods/Breads/Flatbreads
Baked goods/Breads/Sourdough bread
Baked goods/Breads/Rye bread
Baked goods/Breads/Spelt bread
Baked goods/Breads/Granary bread
Baked goods/Cakes/Cake mixes
Baked goods/Pastry
Baked goods/Pies
Baked goods/Twice-baked goods/Biscotti
Baked goods/Twice-baked goods/Rusk
Baked goods/Twice-baked goods/Zweiback
Processed fats and oils/Refined oils
Processed fats and oils/Cooking spray
Processed fats and oils/Margarine
Processed fats and oils/Salad dressing
Processed fats and oils/BBQ sauce
Processed fats and oils/Mustard
Processed fats and oils/Ketchup
Processed fats and oils/Mayonnaise
Processed fats and oils/Peanut butter
Preserves/Chutneys, Pickles
Preserves/Jam, Marmaladae
Preserves/Pesto"""


def get_unique_foods():
	name_list = foods.split('\n')
	data = []

	for item in name_list:
		items = item.split('/')
		for i in items:
			i = i.replace('|||','')
			data.append(i)
	random.shuffle(data)
	item_no = int(random.randrange(1, 7))
	user_types = data[:item_no]
	return user_types

