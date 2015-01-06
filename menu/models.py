from datetime import datetime
from mongoengine import *
from mongoengine import signals
from mongoengine.django.auth import User


class Region(Document):
    fsa_id = IntField(required=True)
    name = StringField(required=True)
    nameKey = StringField(required=True)
    code = StringField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)


class Authority(Document):
    LocalAuthorityId = IntField(required=True)
    EstablishmentCount = IntField(required=True)
    Name = StringField(required=True)
    FriendlyName = StringField(required=True)
    LocalAuthorityIdCode = StringField(required=True)
    Url = StringField(required=True)
    Email = StringField(required=True)
    SchemeType = IntField(required=True)
    RegionName = StringField(required=True)
    SchemeUrl = StringField(required=True)
    FileName = StringField(required=True)
    FileNameWelsh = StringField(required=True)
    CreationDate = DateTimeField(required=True)
    LastPublishedDate = DateTimeField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)


class BusinessType(Document):
    BusinessTypeId = IntField(required=True)
    BusinessTypeName = StringField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)


class Country(Document):
    fsa_id = IntField(required=True)
    name = StringField(required=True)
    nameKey = StringField(required=True)
    code = StringField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)


class Score(EmbeddedDocument):
    Hygiene = IntField(required=True)
    Structural = IntField(required=True)
    ConfidenceInManagement = IntField(required=True)


class Establishment(Document):
    user = ReferenceField(User, required=False)
    FHRSID = IntField(required=False)
    LocalAuthorityBusinessID = StringField(required=False)
    BusinessName = StringField(required=True)
    BusinessType = StringField(required=False)
    BusinessTypeID = IntField(required=False)
    AddressLine1 = StringField(required=False)
    AddressLine2 = StringField(required=False)
    AddressLine3 = StringField(required=False)
    AddressLine4 = StringField(required=False)
    PostCode = StringField(required=False)
    Phone = StringField(required=False)
    RatingValue = StringField(required=False)
    RatingKey = StringField(required=False)
    RatingDate = DateTimeField(required=False)
    LocalAuthorityCode = StringField(required=False)
    LocalAuthorityName = StringField(required=False)
    LocalAuthorityWebSite = StringField(required=False)
    LocalAuthorityEmailAddress = StringField(required=False)
    scores = EmbeddedDocumentField(Score, required=False)
    SchemeType = StringField(required=False)
    geocode = PointField(required=False)
    RightToReply = StringField(required=False)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)

    meta = {
        'indexes': [
            'BusinessName',
            'user'
        ]
    }

    def full_address(self):
        field_list = ['AddressLine1', 'AddressLine2', 'AddressLine3', 'AddressLine4']
        address = ''
        for field in field_list:
            value = getattr(self, field)
            if value:
                address += str(value.encode('ascii', 'ignore')) + ' '
        return address


class Menu(Document):
    establishment = ReferenceField(Establishment)
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'establishment'
        ]
    }

    def get_menu_sections(self):
        return MenuSection.objects.filter(menu=self.pk)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        MenuSection.objects.filter(menu=document).delete()

signals.post_delete.connect(Menu.post_delete, sender=Menu)


class MenuSection(Document):
    menu = ReferenceField(Menu)
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'menu'
        ]
    }

    def get_section_dishes(self):
        return Dish.objects.filter(menu_section=self.pk)

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        Dish.objects.filter(menu_section=document).delete()

signals.post_delete.connect(MenuSection.post_delete, sender=MenuSection)




class Dish(Document):
    menu_section = ReferenceField(MenuSection)
    name = StringField(required=True)
    description = StringField()
    price = FloatField()
    is_allergen = BooleanField(required=True, default=False)
    is_meat = BooleanField(required=True, default=False)
    is_gluten = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True, default=True)
    html = StringField(required=True, default='')
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'menu_section',
            'name'
        ]
    }

    def get_all_parent_ingredients(self):
        return Ingredient.objects.filter(dish=self, parent=None)

    def get_ingredient_names(self):
        return Ingredient.objects.filter(dish=self)


class Ingredient(Document):
    dish = ReferenceField(Dish)
    name = StringField(required=True)
    parent = ReferenceField('self', required=False)
    order = IntField(required=True)
    is_allergen = BooleanField(required=True, default=False)
    is_meat = BooleanField(required=True, default=False)
    is_gluten = BooleanField(required=True, default=False)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'dish',
            'name',
            'parent'
        ]
    }

    def get_children(self):
        return Ingredient.objects.filter(parent=self)

class Allergen(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'name'
        ]
    }


class Meat(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'name'
        ]
    }


class Gluten(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'name'
        ]
    }


class Connection(Document):
    user = ReferenceField(User)
    connection = GenericReferenceField()
    connection_type = IntField(choices=((1, 'We sell to them'), (2, 'We buy from them')))
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'user',
            ('user', 'connection_type')
        ]
    }
