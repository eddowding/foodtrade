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
    FHRSID = IntField(required=True)
    LocalAuthorityBusinessID = StringField(required=True)
    BusinessName = StringField(required=True)
    BusinessType = StringField(required=True)
    BusinessTypeID = IntField(required=True)
    AddressLine1 = StringField(required=True)
    AddressLine2 = StringField(required=True)
    AddressLine3 = StringField(required=True)
    AddressLine4 = StringField(required=True)
    PostCode = StringField(required=True)
    Phone = StringField(required=True)
    RatingValue = StringField(required=True)
    RatingKey = StringField(required=True)
    RatingDate = DateTimeField(required=True)
    LocalAuthorityCode = StringField(required=True)
    LocalAuthorityName = StringField(required=True)
    LocalAuthorityWebSite = StringField(required=True)
    LocalAuthorityEmailAddress = StringField(required=True)
    scores = EmbeddedDocumentField(Score)
    SchemeType = StringField(required=True)
    geocode = PointField(required=False)
    RightToReply = StringField(required=True)
    Distance = FloatField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)
    is_active = BooleanField(required=True, default=True)


class Menu(Document):
    establishment = ReferenceField(Establishment)
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
    allergen = BooleanField(required=True, default=False)


class Dish(Document):
    menu_section = ReferenceField(MenuSection)
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    ingredients = ListField(EmbeddedDocumentField(Ingredient))
    is_active = BooleanField(required=True, default=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

