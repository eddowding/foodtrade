from datetime import datetime
from mongoengine import *
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


class Menu(Document):
    establishment = ReferenceField(Establishment)
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)


class MenuSection(Document):
    menu = ReferenceField(Menu)
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)


class Ingredient(EmbeddedDocument):
    name = StringField(required=True)
    parent = ReferenceField('self')
    order = IntField(required=True)
    is_allergen = BooleanField(required=True, default=False)
    is_meat = BooleanField(required=True, default=False)
    is_gluten = BooleanField(required=True, default=False)


class Dish(Document):
    menu_section = ReferenceField(MenuSection)
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    ingredients = ListField(EmbeddedDocumentField(Ingredient), required=False)
    is_allergen = BooleanField(required=True, default=False)
    is_meat = BooleanField(required=True, default=False)
    is_gluten = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)


class Allergen(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)


class Meat(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)


class Gluten(Document):
    name = StringField(required=True)
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

