from mongoengine.django.auth import User
from mongonaut.sites import MongoAdmin
from menu.models import *

User.mongoadmin = MongoAdmin()
Region.mongoadmin = MongoAdmin()
Authority.mongoadmin = MongoAdmin()
BusinessType.mongoadmin = MongoAdmin()
Country.mongoadmin = MongoAdmin()
ModerationIngredient.mongoadmin = MongoAdmin()

class EstablishmentAdmin(MongoAdmin):
    search_fields = ('FHRSID', 'BusinessName')
    list_fields = ('FHRSID', 'BusinessName', 'is_active')
Establishment.mongoadmin = EstablishmentAdmin()
Menu.mongoadmin = MongoAdmin()
MenuSection.mongoadmin = MongoAdmin()
Dish.mongoadmin = MongoAdmin()

class GenericAdmin(MongoAdmin):
    search_fields = ('name',)
    list_fields = ('name', 'is_active')
Allergen.mongoadmin = GenericAdmin()
Meat.mongoadmin = GenericAdmin()
Gluten.mongoadmin = GenericAdmin()
