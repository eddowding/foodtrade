from MongoConnection import MongoConnection
from datetime import datetime
from bson.objectid import ObjectId
import time
import pymongo
import json

class AdminFoods():
    def __init__ (self):
        self.db_object = MongoConnection("localhost",27017,'foodtrade')
        self.table_name = 'adminfoods'
    
    def get_tags(self):
        try:
            return self.db_object.get_one(self.table_name,{})['adminfoods']
        except:
            val = {'parent': 1, 'adminfoods': [{"node": "Meat", "childrens": [{"node": "Beef"}, {"node": "Bison"}, {"node": "Buffalo"}, {"node": "Chicken"}, {"node": "Duck"}, {"node": "Geese/goose"}, {"node": "Lamb"}, {"node": "Mutton"}, {"node": "Ostrich"}, {"node": "Pork"}, {"node": "Turkey"}, {"node": "Veal"}, {"node": "Game/Partridge"}, {"node": "Game/Pheasant"}, {"node": "Game/Rabbit"}, {"node": "Game/Hare/levret"}, {"node": "Game/Venison"}, {"node": "Processed meat/Bacon"}, {"node": "Processed meat/Burgers"}, {"node": "Processed meat/Cured meat"}, {"node": "Processed meat/Gelatins"}, {"node": "Processed meat/Haggis"}, {"node": "Processed meat/Ham"}, {"node": "Processed meat/Lunch meat"}, {"node": "Processed meat/Meat Pies"}, {"node": "Processed meat/Meatballs/Faggots"}, {"node": "Processed meat/Mincemeat"}, {"node": "Processed meat/Pasties"}, {"node": "Processed meat/Pate"}, {"node": "Processed meat/Pork Pies"}, {"node": "Processed meat/Sausages"}, {"node": "Processed meat/Scotch Eggs"}, {"node": "Processed meat/Smoked Duck/Chicken"}, {"node": "Processed meat/Spiced Chicken"}]}, {"node": "Fish", "childrens": [{"node": "Bass"}, {"node": "Bream"}, {"node": "Cod"}, {"node": "Haddock"}, {"node": "Mackerel"}, {"node": "Salmon"}, {"node": "Trout"}, {"node": "American Shad"}, {"node": "American Sole"}, {"node": "Anchovy"}, {"node": "Antarctic Cod"}, {"node": "Arrowtooth Eel"}, {"node": "Asian Carps"}, {"node": "Atka Mackerel"}, {"node": "Atlantic Bonito"}, {"node": "Atlantic Cod"}, {"node": "Atlantic Eel"}, {"node": "Atlantic Herring"}, {"node": "Atlantic Salmon"}, {"node": "Atlantic Trout"}, {"node": "Australasian Salmon"}, {"node": "Bar Jack"}, {"node": "Bat Fish"}, {"node": "Barramundi"}, {"node": "Basa Fish"}, {"node": "Black Mackerel"}, {"node": "Blue Cod"}, {"node": "Bluegill"}, {"node": "Bluefish"}, {"node": "Bombay Duck"}, {"node": "Brook Trout"}, {"node": "Butterfish"}, {"node": "California Halibut"}, {"node": "California Sheephead"}, {"node": "Capelin"}, {"node": "Carp"}, {"node": "Catfish"}, {"node": "Cherry Salmon"}, {"node": "Chinook Salmon"}, {"node": "Chum Salmon"}, {"node": "Cobia"}, {"node": "Coho Salmon"}, {"node": "Coley"}, {"node": "Common Carp"}, {"node": "Crappie"}, {"node": "Crawfish"}, {"node": "Dory"}, {"node": "Discus"}, {"node": "Drum"}, {"node": "Dino"}, {"node": "Eel"}, {"node": "European Eel"}, {"node": "European Flounder"}, {"node": "Flathead"}, {"node": "Flatfish"}, {"node": "Flounder"}, {"node": "Freshwater Eel"}, {"node": "Freshwater Herring"}, {"node": "Flying Fish"}, {"node": "Giant Gourami"}, {"node": "Gilt-head Bream"}, {"node": "Golden Dorado"}, {"node": "Groundfish"}, {"node": "Grouper"}, {"node": "Gar"}, {"node": "Hake"}, {"node": "Halibut"}, {"node": "Harvestfish"}, {"node": "Herring"}, {"node": "Hilsa"}, {"node": "Hoki"}, {"node": "Iridescent Shark/Basa Fish"}, {"node": "Japanese Butterfish"}, {"node": "John Dory"}, {"node": "Kapenta"}, {"node": "Kingklip"}, {"node": "Lemon Sole"}, {"node": "Largemouth Bass"}, {"node": "Maori Cod"}, {"node": "Mahi-mahi"}, {"node": "Marlin"}, {"node": "Milkfish"}, {"node": "Monkfish"}, {"node": "Mullet"}, {"node": "Mullus Surmuletus"}, {"node": "Northern Anchovy"}, {"node": "Northern Pike"}, {"node": "Northern Snakehead"}, {"node": "Norwegian Atlantic Salmon"}, {"node": "Orange Roughy"}, {"node": "Oscar"}, {"node": "Pacific Herring"}, {"node": "Pacific Salmon"}, {"node": "Pacific Saury"}, {"node": "Pacific Trout"}, {"node": "Panfish"}, {"node": "Pangasius"}, {"node": "Patagonian Toothfish"}, {"node": "Pelagic Cod"}, {"node": "Perch"}, {"node": "Pink Salmon"}, {"node": "Pollock"}, {"node": "Pomfret"}, {"node": "Pilchard"}, {"node": "Paddlefish"}, {"node": "Plaice"}, {"node": "Pacific Cod"}, {"node": "Quoy Fish"}, {"node": "Rainbow Trout"}, {"node": "Redfish"}, {"node": "Red Snapper"}, {"node": "Rock Fish"}, {"node": "Round Herring"}, {"node": "Sardine"}, {"node": "Saury"}, {"node": "Scrod"}, {"node": "Sea Bass"}, {"node": "Seer Fish"}, {"node": "Shad"}, {"node": "Shrimpfish"}, {"node": "Silver Carp"}, {"node": "Skipjack Tuna"}, {"node": "Slender Rainbow Sardine"}, {"node": "Sole"}, {"node": "Snakeskin Gourami"}, {"node": "Snapper"}, {"node": "Snook"}, {"node": "Snoek"}, {"node": "Spanish Mackerel"}, {"node": "Surf Sardine"}, {"node": "Swamp-eel"}, {"node": "Swordfish"}, {"node": "Skate"}, {"node": "Sunfish  Bluegill"}, {"node": "Smallmouth Bass"}, {"node": "Spoonbill/Paddlefish"}, {"node": "Thresher Shark"}, {"node": "Tilapia"}, {"node": "Tilefish"}, {"node": "Tuna"}, {"node": "Turbot"}, {"node": "Yellowfin Tuna"}, {"node": "Zander"}, {"node": "Caviar"}, {"node": "Roe (cod)"}, {"node": "Processed Fish/Fishcakes"}, {"node": "Processed Fish/Fishpie"}, {"node": "Processed Fish/Fishfingers"}, {"node": "Processed Fish/Sushi"}]}, {"node": "Shellfish", "childrens": [{"node": "Prawns"}, {"node": "Oysters"}, {"node": "Lobster"}, {"node": "Clams"}, {"node": "Crabs"}, {"node": "Shrimp"}, {"node": "Cockles"}, {"node": "Mussels"}, {"node": "Scallops"}, {"node": "Whelks"}, {"node": "Winkles"}]}, {"node": "Dairy", "childrens": [{"node": "Butter"}, {"node": "Cream/Clotted cream"}, {"node": "Cream/Single cream"}, {"node": "Cream/Double cream"}, {"node": "Milk/Cow's milk"}, {"node": "Milk/Goat's milk"}, {"node": "Cheese/Chedder"}, {"node": "Cheese/Goat"}, {"node": "Cheese/Brie"}, {"node": "Cheese/Stilton"}, {"node": "Cheese /"}, {"node": "Cheese/Blue cheese/Bath Blue cheese"}, {"node": "Cheese/Blue cheese/Barkham Blue cheese"}, {"node": "Cheese/Blue cheese/Blue Monday cheese"}, {"node": "Cheese/Blue cheese/Buxton Blue cheese"}, {"node": "Cheese/Blue cheese/Cheshire Blue cheese"}, {"node": "Cheese/Blue cheese/Devon Blue cheese"}, {"node": "Cheese/Blue cheese/Dorset Blue Vinney cheese"}, {"node": "Cheese/Blue cheese/Dovedale cheese"}, {"node": "Cheese/Blue cheese/Exmoor Blue cheese"}, {"node": "Cheese/Blue cheese/Harbourne Blue cheese"}, {"node": "Cheese/Blue cheese/Lanark Blue  cheese"}, {"node": "Cheese/Blue cheese/Oxford Blue cheese"}, {"node": "Cheese/Blue cheese/Shropshire Blue cheese"}, {"node": "Cheese/Blue cheese/Stichelton cheese"}, {"node": "Cheese/Blue cheese/Stilton cheese"}, {"node": "Cheese/Blue cheese/Blue Wensleydale cheese"}, {"node": "Cheese/Blue cheese/Yorkshire Blue cheese"}, {"node": "Cheese/Appledore cheese"}, {"node": "Cheese/Berkswell cheese"}, {"node": "Cheese/Bonchester cheese"}, {"node": "Cheese/Brie cheese"}, {"node": "Cheese/Somerset Brie"}, {"node": "Cheese/Cornish Brie cheese"}, {"node": "Cheese/Brinkburn cheese"}, {"node": "Cheese/Caithness cheese"}, {"node": "Cheese/Caboc cheese"}, {"node": "Cheese/Caerphilly cheese"}, {"node": "Cheese/Cheddar cheese"}, {"node": "Cheese/West Country Farmhouse Cheddar cheese"}, {"node": "Cheese/Applewood cheese"}, {"node": "Cheese/Coleraine Cheddar cheese"}, {"node": "Cheese/Cheshire cheese"}, {"node": "Cheese/Appleby Cheshire cheese"}, {"node": "Cheese/Chevington cheese"}, {"node": "Cheese/Coquetdale cheese"}, {"node": "Cheese/Cornish Pepper cheese"}, {"node": "Cheese/Cotherstone cheese"}, {"node": "Cheese/Cotswold cheese"}, {"node": "Cheese/Coverdale cheese"}, {"node": "Cheese/Croglin cheese"}, {"node": "Cheese/Crowdie cheese"}, {"node": "Cheese/Derby cheese"}, {"node": "Cheese/Double Gloucester cheese"}, {"node": "Cheese/Goosnargh Gold cheese"}, {"node": "Cheese/Dorstone cheese"}, {"node": "Cheese/Dovedale cheese"}, {"node": "Cheese/Farmhouse Llanboidy cheese"}, {"node": "Cheese/Fine Fettle Yorkshire cheese"}, {"node": "Cheese/Black Eyed Susan cheese"}, {"node": "Cheese/Golden Cross cheese"}, {"node": "Cheese/Gruth Dhu cheese"}, {"node": "Cheese/Harlech cheese"}, {"node": "Cheese/Hereford Hop cheese"}, {"node": "Cheese/Huntsman cheese"}, {"node": "Cheese/Ilchester cheese"}, {"node": "Cheese/Innkeepers Choice cheese"}, {"node": "Cheese/Isle Of Mull cheese"}, {"node": "Cheese/Lancashire cheese"}, {"node": "Cheese/Beacon Fell Traditional Lancashire cheese"}, {"node": "Cheese/Lincolnshire Poacher cheese"}, {"node": "Cheese/Little Wallop cheese"}, {"node": "Cheese/Katy's White Lavender cheese"}, {"node": "Cheese/Kidderton Ash cheese"}, {"node": "Cheese/Lord Of The Hundreds cheese"}, {"node": "Cheese/Lowerdale Goats Cheese cheese"}, {"node": "Cheese/Pantysgawn cheese"}, {"node": "Cheese/Red Devil cheese"}, {"node": "Cheese/Red Dragon cheese"}, {"node": "Cheese/Red Leicester cheese"}, {"node": "Cheese/Rothbury Red cheese"}, {"node": "Cheese/Red Windsor cheese"}, {"node": "Cheese/Sage Derby cheese"}, {"node": "Cheese/Single Gloucester cheese"}, {"node": "Cheese/Stinking Bishop cheese"}, {"node": "Cheese/Sussex Slipcote cheese"}, {"node": "Cheese/Swaledale cheese"}, {"node": "Cheese/Teviotdale  cheese"}, {"node": "Cheese/Tintern cheese"}, {"node": "Cheese/Waterloo cheese"}, {"node": "Cheese/Wensleydale cheese"}, {"node": "Cheese/White Stilton cheese"}, {"node": "Cheese/Suffolk Gold cheese"}, {"node": "Cheese/Whitehaven cheese"}, {"node": "Cheese/Yarg cheese"}, {"node": "Cheese/Wild Garlic Yarg cheese"}, {"node": "Cheese/Wiltshire Loaf"}, {"node": "Cheese/Woolsery Goats cheese"}, {"node": "Cheese/Village Green Goat"}, {"node": "Cheese/Y Fenni cheese"}, {"node": "Ice Cream/Sorbets"}, {"node": "Yoghurt"}]}, {"node": "Eggs", "childrens": [{"node": "Chicken"}, {"node": "Duck"}, {"node": "Quails"}, {"node": "Goose/geese"}, {"node": "Turkey"}]}, {"node": "Fruit", "childrens": [{"node": "Apples"}, {"node": "Apricots"}, {"node": "Bananas"}, {"node": "Bilberry"}, {"node": "Blackberries"}, {"node": "Blackcurrants"}, {"node": "Blueberries"}, {"node": "Cherimoya"}, {"node": "Cherries"}, {"node": "Clementine"}, {"node": "Coconuts"}, {"node": "Cranberries"}, {"node": "Currant"}, {"node": "Damson"}, {"node": "Dates"}, {"node": "Dragon fruit"}, {"node": "Durians"}, {"node": "Elderberry"}, {"node": "Feijoa"}, {"node": "Fig"}, {"node": "Gooseberries"}, {"node": "Gooseberry"}, {"node": "Grape"}, {"node": "Grapefruit"}, {"node": "Grapes"}, {"node": "Guava"}, {"node": "Honeydew melon"}, {"node": "Huckleberry"}, {"node": "Jack fruit"}, {"node": "Jambul"}, {"node": "Kiwi fruit"}, {"node": "Kumquat"}, {"node": "Legume"}, {"node": "Lemon"}, {"node": "Limes"}, {"node": "Lychee"}, {"node": "Mandarine"}, {"node": "Mango"}, {"node": "Mangostine"}, {"node": "Medlar"}, {"node": "Melon/cantaloupe"}, {"node": "Nectarines"}, {"node": "Oranges"}, {"node": "Papaya"}, {"node": "Peach"}, {"node": "Pears"}, {"node": "Physalis"}, {"node": "Pineapple"}, {"node": "Pitaya"}, {"node": "Plum, prune"}, {"node": "Pomegranates"}, {"node": "Prunes"}, {"node": "Quince"}, {"node": "Raisins"}, {"node": "Rambutan"}, {"node": "Raspberries"}, {"node": "Redcurrants"}, {"node": "Rhubarb"}, {"node": "Salal berry"}, {"node": "Satsuma"}, {"node": "Star fruit"}, {"node": "Strawberries"}, {"node": "Tangerines"}, {"node": "Ugli fruit"}, {"node": "Watermelon"}, {"node": "Processed fruits/Canned fruit"}, {"node": "Processed fruits/Frozen fruit"}, {"node": "Processed fruits/Fruit sauces"}, {"node": "Processed fruits/Jam"}, {"node": "Processed fruits/Pie fillings"}]}, {"node": "Vegetables", "childrens": [{"node": "Artichokes/Jerusalem"}, {"node": "Artichokes/Globe"}, {"node": "Aubergine"}, {"node": "Alfalfa sprouts"}, {"node": "Anise"}, {"node": "Artichoke"}, {"node": "Arugula"}, {"node": "Asparagus"}, {"node": "Aubergine, Eggplant"}, {"node": "Avocados"}, {"node": "Beansprouts"}, {"node": "Bell pepper"}, {"node": "Beetroot, Beet"}, {"node": "Breadfruit"}, {"node": "Broccoflower"}, {"node": "Broccoli/Purple Sprouting Broccoli"}, {"node": "Brussels sprouts"}, {"node": "Cabbage/Red"}, {"node": "Cabbage/White"}, {"node": "Cabbage/Green"}, {"node": "Calabrese"}, {"node": "Celeriac"}, {"node": "Chinese leaves, Bok choy"}, {"node": "Collard greens"}, {"node": "Corn salad"}, {"node": "Carrots"}, {"node": "Cauliflflower"}, {"node": "Celery"}, {"node": "Chard"}, {"node": "Cucumbers"}, {"node": "Crimini"}, {"node": "Daikon"}, {"node": "Endive"}, {"node": "Fennel"}, {"node": "Fiddlehead fern"}, {"node": "Frisee leaves"}, {"node": "Garlic"}, {"node": "Jicama"}, {"node": "Kale/Curly kale"}, {"node": "Kale/Mixed kale"}, {"node": "Kohlrabi"}, {"node": "Leeks"}, {"node": "Lettuce/Romaine"}, {"node": "Lettuce/Iceberg"}, {"node": "Marrow"}, {"node": "Mushrooms/Shiitake mushrooms"}, {"node": "Mushrooms/Truffles"}, {"node": "Mushrooms/Boletus mushrooms"}, {"node": "Mushrooms/Oyster mushrooms"}, {"node": "Mushrooms/Wild mushrooms"}, {"node": "Mushrooms/Button mushrooms"}, {"node": "Mustard greens"}, {"node": "Nettles"}, {"node": "Okra"}, {"node": "Olives"}, {"node": "Onions"}, {"node": "Pakchoi"}, {"node": "Parsnips"}, {"node": "Potatoes/Charlotte potatoes"}, {"node": "Potatoes/King Edward potatoes"}, {"node": "Potatoes/Estima potatoes"}, {"node": "Potatoes/Maris Piper potatoes"}, {"node": "Potatoes/Desiree potatoes"}, {"node": "Potatoes/Marfona potatoes"}, {"node": "Potatoes/Anya potatoes"}, {"node": "Potatoes/Nicola potatoes"}, {"node": "Potatoes/Rooster potatoes"}, {"node": "Potatoes/Sante potatoes"}, {"node": "Potatoes/Accord potatoes"}, {"node": "Potatoes/Carlingford potatoes"}, {"node": "Potatoes/Romano potatoes"}, {"node": "Potatoes/Sweet potatoes, yams"}, {"node": "Rocket"}, {"node": "Radicchio"}, {"node": "Radish"}, {"node": "Rhubarb"}, {"node": "Salad"}, {"node": "Salad Packs"}, {"node": "Salsify"}, {"node": "Savoy Cabbage"}, {"node": "Sea Vegetables"}, {"node": "Shallots"}, {"node": "Skirret"}, {"node": "Spinach"}, {"node": "Spring Greens"}, {"node": "Spring onions, Green onion, Scallion"}, {"node": "Sprouted Seeds"}, {"node": "Squashes/Acorn squash"}, {"node": "Squashes/Butternut squash"}, {"node": "Squashes/Courgette, Zucchini"}, {"node": "Squashes/Cucumber"}, {"node": "Squashes/Gem squash"}, {"node": "Squashes/Marrow, Squash"}, {"node": "Squashes/Pumpkin"}, {"node": "Squashes/Spaghetti squash"}, {"node": "Swede, Rutabaga"}, {"node": "Sweetcorn, maize, corn"}, {"node": "Swiss Chard"}, {"node": "Taro"}, {"node": "Tat soi"}, {"node": "Tomatoes"}, {"node": "Turnips"}, {"node": "Turnip Greens"}, {"node": "Watercress"}, {"node": "Wasabi"}, {"node": "Water chestnut"}, {"node": "White radish"}, {"node": "Processed vegetables/Canned vegetables"}, {"node": "Processed vegetables/Frozen vegetables"}, {"node": "Processed vegetables/French fries"}]}, {"node": "Beans & Legumes", "childrens": [{"node": "Azuki beans, Adzuki beans"}, {"node": "Bean sprouts"}, {"node": "Black beans"}, {"node": "Black-eyed peas"}, {"node": "Borlotti beans"}, {"node": "Broad beans"}, {"node": "Butter Beans"}, {"node": "Chickpeas, Garbanzo beans, Ceci beans"}, {"node": "Dried Peas"}, {"node": "Green beans"}, {"node": "Kidney beans"}, {"node": "Lentils"}, {"node": "Lima bean, Butter bean"}, {"node": "Miso"}, {"node": "Mung beans"}, {"node": "Navy beans"}, {"node": "Peas/Mangetout, Sugar snap peas"}, {"node": "Pinto beans"}, {"node": "Runner beans"}, {"node": "Soy beans"}, {"node": "Soybeans"}, {"node": "Tempeh"}, {"node": "Tofu"}, {"node": "Vigna Beans"}]}, {"node": "Nuts, Seeds & Oils", "childrens": [{"node": "Almonds"}, {"node": "Apricot Kernels"}, {"node": "Betel Nuts"}, {"node": "Brazil Nuts"}, {"node": "Cashews"}, {"node": "Chestnuts"}, {"node": "Flaxseeds"}, {"node": "Ginkgo Nuts"}, {"node": "Hazelnuts"}, {"node": "Macadamia Nuts"}, {"node": "Melon Seeds"}, {"node": "Olive Oil"}, {"node": "Peanuts"}, {"node": "Pecan Nuts"}, {"node": "Pine Nuts"}, {"node": "Pistachio Nuts"}, {"node": "Pumpkin Seeds"}, {"node": "Sesame Seeds"}, {"node": "Sunflower Kernels"}, {"node": "Sunflower Seeds"}, {"node": "Walnuts"}]}, {"node": "Herbs & Spices", "childrens": [{"node": "Ajwain, carom seeds"}, {"node": "Akudjura"}, {"node": "Alexanders"}, {"node": "Allspice"}, {"node": "Angelica"}, {"node": "Anise"}, {"node": "Aniseed myrtle"}, {"node": "Annatto"}, {"node": "Apple mint"}, {"node": "Arrowroot starch"}, {"node": "Avocado leaf"}, {"node": "Barberry"}, {"node": "Basil"}, {"node": "Bay leaf"}, {"node": "Black cardamom"}, {"node": "Boldo"}, {"node": "Borage"}, {"node": "Calendula, pot marigold"}, {"node": "Camphor laurel"}, {"node": "Caraway"}, {"node": "Cardamom"}, {"node": "Carob"}, {"node": "Cassia"}, {"node": "Catnip"}, {"node": "Celery seed"}, {"node": "Chervil"}, {"node": "Chicory"}, {"node": "Chili powder"}, {"node": "Chives"}, {"node": "Cicely"}, {"node": "Cilantro, coriander greens, coriander herb"}, {"node": "Cinnamon"}, {"node": "Cinnamon myrtle"}, {"node": "Clary, Clary sage"}, {"node": "Cloves"}, {"node": "Coriander"}, {"node": "Coriander seed"}, {"node": "Costmary"}, {"node": "Cream of tartar"}, {"node": "Cudweed"}, {"node": "Cumin"}, {"node": "Cumin Seeds"}, {"node": "Curry leaf"}, {"node": "Curry plant"}, {"node": "Curry powder"}, {"node": "Dill"}, {"node": "Dill seed"}, {"node": "Elderflower"}, {"node": "Epazote"}, {"node": "Fennel"}, {"node": "Fennel seeds"}, {"node": "Fenugreek"}, {"node": "File powder, gumbo file"}, {"node": "Fingerroot, krachai, temu kuntji"}, {"node": "Five-spice powder"}, {"node": "Galingale"}, {"node": "Garlic/Garlic powder"}, {"node": "Garlic/Elephant garlic"}, {"node": "Garlic chives"}, {"node": "Ginger"}, {"node": "Golpar, Persian hogweed"}, {"node": "Grains of paradise"}, {"node": "Horseradish"}, {"node": "Houttuynia cordata"}, {"node": "Huacatay, Mexican marigold, mint marigold"}, {"node": "Hyssop"}, {"node": "Jasmine flowers"}, {"node": "Jimbu"}, {"node": "Juniper berry"}, {"node": "Kaffir lime leaves, Makrud lime leaves"}, {"node": "Kala zeera , black cumin"}, {"node": "Kawakawa seeds"}, {"node": "Keluak, kluwak, kepayang"}, {"node": "Kencur, galangal, kentjur"}, {"node": "Kokam seed"}, {"node": "Korarima, Ethiopian cardamom, false cardamon"}, {"node": "Koseret leaves"}, {"node": "Lavender"}, {"node": "Lemon balm"}, {"node": "Lemon ironbark"}, {"node": "Lemon myrtle"}, {"node": "Lemon verbena"}, {"node": "Lemongrass"}, {"node": "Leptotes bicolor"}, {"node": "Lesser calamint , nipitella, nepitella"}, {"node": "Licorice, liquorice"}, {"node": "Lime flower, linden flower"}, {"node": "Lovage"}, {"node": "Mace"}, {"node": "Mahlab, St. Lucie cherry"}, {"node": "Malabathrum, tejpat"}, {"node": "Marjoram"}, {"node": "Marsh mallow"}, {"node": "Mastic"}, {"node": "Mint"}, {"node": "Mountain horopito"}, {"node": "Musk mallow, abelmosk"}, {"node": "Mustard/Black mustard"}, {"node": "Mustard/Brown mustard"}, {"node": "Mustard/Yellow mustard"}, {"node": "Mustard/White mustard"}, {"node": "Mustard/Mustard seeds"}, {"node": "Nasturtium"}, {"node": "Nigella, kalonji, black caraway, black onion seed"}, {"node": "Njangsa, djansang"}, {"node": "Nutmeg"}, {"node": "Olida"}, {"node": "Onion powder"}, {"node": "Oregano"}, {"node": "Orris root"}, {"node": "Pandan flower, kewra"}, {"node": "Pandan leaf, screwpine"}, {"node": "Pandanus amaryllifolius"}, {"node": "Paprika"}, {"node": "Paracress"}, {"node": "Parsley"}, {"node": "Pepper/Black pepper"}, {"node": "Pepper/Chili pepper/Jalapeno pepper"}, {"node": "Pepper/Chili pepper/Habanero pepper"}, {"node": "Pepper/Chili pepper/Paprika pepper"}, {"node": "Pepper/Chili pepper/Tabasco pepper"}, {"node": "Pepper/Chili pepper/Cayenne pepper"}, {"node": "Pepper/Cubeb pepper"}, {"node": "Pepper/Green pepper"}, {"node": "Pepper/Kani pepper"}, {"node": "Pepper/Peruvian pepper"}, {"node": "Pepper/Pink pepper"}, {"node": "Pepper/Red pepper"}, {"node": "Pepper/Szechuan pepper"}, {"node": "Pepper/White pepper"}, {"node": "Peppercorns"}, {"node": "Peppermint"}, {"node": "Perilla, shiso"}, {"node": "Poppy seeds"}, {"node": "Quassia"}, {"node": "Ramsons, wood garlic"}, {"node": "Rice paddy herb"}, {"node": "Rosemary"}, {"node": "Rue"}, {"node": "Safflower"}, {"node": "Saffron"}, {"node": "Sage"}, {"node": "Saigon cinnamon"}, {"node": "Salad burnet"}, {"node": "Salep"}, {"node": "Salt"}, {"node": "Sassafras"}, {"node": "Sesame seeds"}, {"node": "Silphium, silphion, laser, laserpicium, lasarpicium"}, {"node": "Sorrel"}, {"node": "Spearmint"}, {"node": "Spikenard"}, {"node": "Star anise"}, {"node": "Sumac"}, {"node": "Sweet woodruff"}, {"node": "Tarragon"}, {"node": "Thyme"}, {"node": "Turmeric"}, {"node": "Vanilla"}, {"node": "Vanilla extract"}, {"node": "Wasabi"}, {"node": "Watercress"}, {"node": "Wattleseed"}, {"node": "Wild betel"}, {"node": "Wild thyme"}, {"node": "Willow herb"}, {"node": "Winter savory"}, {"node": "Wintergreen"}, {"node": "Wood avens, herb bennet"}, {"node": "Woodruff"}, {"node": "Wormwood, absinthe"}, {"node": "Yerba buena"}, {"node": "Za'atar"}, {"node": "Zedoary"}]}, {"node": "Cereal Grains", "childrens": [{"node": "Rice/Basmati Rice"}, {"node": "Rice/Black Rice"}, {"node": "Rice/Broken Rice"}, {"node": "Rice/Brown Rice"}, {"node": "Rice/Jasmine Rice"}, {"node": "Rice/Organic Rice"}, {"node": "Rice/White Corn"}, {"node": "Rice/Wild rice"}, {"node": "Rice/Yellow Corn"}, {"node": "Amaranth"}, {"node": "Bamboo shoots"}, {"node": "Barley"}, {"node": "Barleygrass"}, {"node": "Breadnut"}, {"node": "Buckwheat"}, {"node": "Bulgur wheat"}, {"node": "Cattail"}, {"node": "Chia"}, {"node": "Cornbread"}, {"node": "Cornmeal"}, {"node": "Couscous"}, {"node": "Crackers"}, {"node": "Durum wheat"}, {"node": "Farro, Emmer"}, {"node": "Flax"}, {"node": "Flaxseed"}, {"node": "Fonio"}, {"node": "Grano"}, {"node": "Grits"}, {"node": "Kamut grain"}, {"node": "Kaniwa"}, {"node": "Lemongrass, citronella"}, {"node": "Millet"}, {"node": "Molasses"}, {"node": "Muesli, Breakfast cereal, Granola"}, {"node": "Noodles"}, {"node": "Oatmeal"}, {"node": "Oats"}, {"node": "Other Grain"}, {"node": "Palmer's grass"}, {"node": "Pearl Millet"}, {"node": "Pitseed Goosefoot"}, {"node": "Popcorn"}, {"node": "Quinoa"}, {"node": "Rapadura"}, {"node": "Rye"}, {"node": "Semolina wheat"}, {"node": "Sorghum"}, {"node": "Spelt"}, {"node": "Teff"}, {"node": "Triticale"}, {"node": "Wattleseed, Acacia seed"}, {"node": "Wheat"}, {"node": "Wheat Berries"}, {"node": "Wheatgrass"}, {"node": "Flour/White flour"}, {"node": "Flour/Brown flour"}, {"node": "Flour/Rye flour"}, {"node": "Flour/Spelt flour"}, {"node": "Flour/Barley flour"}]}, {"node": "Pasta", "childrens": [{"node": "Minute pasta"}, {"node": "Long Noodles"}, {"node": "Ribbon-Cut Noodles"}, {"node": "Decorative Shaped Pasta"}, {"node": "Stuffed pasta"}]}, {"node": "Drinks", "childrens": [{"node": "Juice/Apple juice"}, {"node": "Juice/Orange juice"}, {"node": "Juice/Pear juice"}, {"node": "Juice/Grape juice"}, {"node": "Soft drinks/Ginger Beer"}, {"node": "Soft drinks/Lemonade"}, {"node": "Alcoholic drinks/Beer/Ale/Barleywine"}, {"node": "Alcoholic drinks/Beer/Ale/Bitter ale"}, {"node": "Alcoholic drinks/Beer/Ale/Mild ale"}, {"node": "Alcoholic drinks/Beer/Ale/Pale ale"}, {"node": "Alcoholic drinks/Beer/Ale/Porter/Stout"}, {"node": "Alcoholic drinks/Beer/Ale/Cask ale"}, {"node": "Alcoholic drinks/Beer/Ale/Stock ale"}, {"node": "Alcoholic drinks/Beer/Fruit Beer"}, {"node": "Alcoholic drinks/Beer/Large Beer/Bock"}, {"node": "Alcoholic drinks/Beer/Large Beer/Dry beer"}, {"node": "Alcoholic drinks/Beer/Large Beer/Maerzen/Oktoberfest Beer"}, {"node": "Alcoholic drinks/Beer/Large Beer/Pilsener"}, {"node": "Alcoholic drinks/Beer/Large Beer/Schwarzbier"}, {"node": "Alcoholic drinks/Beer/Sahti"}, {"node": "Alcoholic drinks/Beer/Small beer"}, {"node": "Alcoholic drinks/Beer/Wheat beer/Witbier White Beer"}, {"node": "Alcoholic drinks/Beer/Wheat beer/Hefeweizen"}, {"node": "Alcoholic drinks/Cauim"}, {"node": "Alcoholic drinks/Chicha"}, {"node": "Alcoholic drinks/Cider"}, {"node": "Alcoholic drinks/Mead"}, {"node": "Alcoholic drinks/Palm wine"}, {"node": "Alcoholic drinks/Perry"}, {"node": "Alcoholic drinks/Sake"}, {"node": "Alcoholic drinks/Wine/Fruit wine"}, {"node": "Alcoholic drinks/Wine/Table wine"}, {"node": "Alcoholic drinks/Wine/Sangria"}, {"node": "Alcoholic drinks/Wine/Sparkling wine/Champagne"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Port"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Madeira"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Marsala"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Sherry"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Vermouth"}, {"node": "Alcoholic drinks/Wine/Fortified wine/Vinsanto"}, {"node": "Alcoholic drinks/Spirits/Absinthe"}, {"node": "Alcoholic drinks/Spirits/Akvavit"}, {"node": "Alcoholic drinks/Spirits/Arak"}, {"node": "Alcoholic drinks/Spirits/Arrack"}, {"node": "Alcoholic drinks/Spirits/Baijiu"}, {"node": "Alcoholic drinks/Spirits/Cachaca"}, {"node": "Alcoholic drinks/Spirits/Gin/Damson gin"}, {"node": "Alcoholic drinks/Spirits/Gin/Sloe gin"}, {"node": "Alcoholic drinks/Spirits/Gulu"}, {"node": "Alcoholic drinks/Spirits/Horilka"}, {"node": "Alcoholic drinks/Spirits/Kaoliang"}, {"node": "Alcoholic drinks/Spirits/Maotai"}, {"node": "Alcoholic drinks/Spirits/Mezcal"}, {"node": "Alcoholic drinks/Spirits/Neutral grain spirit"}, {"node": "Alcoholic drinks/Spirits/Ogogoro"}, {"node": "Alcoholic drinks/Spirits/Ouzo"}, {"node": "Alcoholic drinks/Spirits/Palinka"}, {"node": "Alcoholic drinks/Spirits/Pisco"}, {"node": "Alcoholic drinks/Spirits/Rum"}, {"node": "Alcoholic drinks/Spirits/Soju"}, {"node": "Alcoholic drinks/Spirits/Tequila"}, {"node": "Alcoholic drinks/Spirits/Vodka"}, {"node": "Alcoholic drinks/Spirits/Metaxa"}, {"node": "Alcoholic drinks/Spirits/Whisky/Bourbon"}, {"node": "Alcoholic drinks/Spirits/Whisky/Scotch"}, {"node": "Alcoholic drinks/Spirits/Whisky/Tennessee whiskey"}, {"node": "Alcoholic drinks/Spirits/Brandy/Armagnac"}, {"node": "Alcoholic drinks/Spirits/Brandy/Cognac"}, {"node": "Alcoholic drinks/Spirits/Brandy/Fruit brandy, Eau-de-vie, Schnapps"}, {"node": "Alcoholic drinks/Spirits/Brandy/Kirsch"}, {"node": "Tea/Green"}, {"node": "Tea/Black"}, {"node": "Tea/Herbal"}, {"node": "Coffee"}]}, {"node": "Convenience foods, processed foods", "childrens": [{"node": "Baby Food"}, {"node": "Crisps"}, {"node": "Energy bars"}, {"node": "Ready meals"}, {"node": "Soup"}]}, {"node": "Sweeteners, confection", "childrens": [{"node": "Agave nectar"}, {"node": "Barley malt syrup"}, {"node": "Birch syrup"}, {"node": "Brown sugar"}, {"node": "Cane sugar"}, {"node": "Chocolate"}, {"node": "Honey"}, {"node": "Maple syrup"}, {"node": "Marshmallows"}, {"node": "Molasses"}, {"node": "Palm sugar"}, {"node": "Shredded coconut"}, {"node": "Sorghum Syrup"}, {"node": "Sugar (beet)"}, {"node": "Sugar (cane)"}, {"node": "Sugar substitutes"}, {"node": "Syrup"}, {"node": "White sugar"}]}, {"node": "Baked goods", "childrens": [{"node": "Biscuits, cookies"}, {"node": "Breads/Flatbreads"}, {"node": "Breads/Sourdough bread"}, {"node": "Breads/Rye bread"}, {"node": "Breads/Spelt bread"}, {"node": "Breads/Granary bread"}, {"node": "Cakes/Cake mixes"}, {"node": "Pastry"}, {"node": "Pies"}, {"node": "Twice-baked goods/Biscotti"}, {"node": "Twice-baked goods/Rusk"}, {"node": "Twice-baked goods/Zweiback"}]}, {"node": "Processed fats and oils", "childrens": [{"node": "Refined oils"}, {"node": "Cooking spray"}, {"node": "Margarine"}, {"node": "Salad dressing"}, {"node": "BBQ sauce"}, {"node": "Mustard"}, {"node": "Ketchup"}, {"node": "Mayonnaise"}, {"node": "Peanut butter"}]}, {"node": "Preserves", "childrens": [{"node": "Chutneys, Pickles"}, {"node": "Jam, Marmaladae"}, {"node": "Pesto"}]}]}
            self.db_object.insert_one(self.table_name,val)
            return self.db_object.get_one(self.table_name,{"parent":1})['adminfoods']

            return self.db_object.get_one(self.table_name,{})['adminfoods']

    def set_tags(self,adminfoods):
        print adminfoods
        try:
            val = self.db_object.get_one(self.table_name,{})['adminfoods']
            return self.db_object.update(self.table_name,{'parent':1}, {'adminfoods':adminfoods['adminfoods']})
        except:
            return self.db_object.insert_one(self.table_name,adminfoods)