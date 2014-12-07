from mongonaut.sites import MongoAdmin
from menu.models import *


Region.mongoadmin = MongoAdmin()
Authority.mongoadmin = MongoAdmin()
BusinessType.mongoadmin = MongoAdmin()
Country.mongoadmin = MongoAdmin()
Establishment.mongoadmin = MongoAdmin()
Menu.mongoadmin = MongoAdmin()
MenuSection.mongoadmin = MongoAdmin()
Dish.mongoadmin = MongoAdmin()
Allergen.mongoadmin = MongoAdmin()
Meat.mongoadmin = MongoAdmin()
Gluten.mongoadmin = MongoAdmin()

