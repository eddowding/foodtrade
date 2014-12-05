from datetime import datetime
from mongoengine import *


class Region(Document):
    fsa_id = IntField(required=True)
    name = StringField(max_length=255, required=True)
    nameKey = StringField(max_length=255, required=True)
    code = StringField(max_length=255, required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

class Authority(Document):
    LocalAuthorityId = IntField(required=True)
    EstablishmentCount = IntField(required=True)
    Name = StringField(max_length=255, required=True)
    FriendlyName = StringField(max_length=255, required=True)
    LocalAuthorityIdCode = StringField(max_length=255, required=True)
    Url = StringField(max_length=255, required=True)
    Email = StringField(max_length=255, required=True)
    SchemeType = IntField(required=True)
    RegionName = StringField(max_length=255, required=True)
    SchemeUrl = StringField(max_length=255, required=True)
    FileName = StringField(max_length=255, required=True)
    FileNameWelsh = StringField(max_length=255, required=True)
    CreationDate = DateTimeField(required=True)
    LastPublishedDate = DateTimeField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

class BusinessType(Document):
    BusinessTypeId = IntField(required=True)
    BusinessTypeName = StringField(max_length=255, required=True)

class Country(Document):
    fsa_id = IntField(required=True)
    name = StringField(max_length=255, required=True)
    nameKey = StringField(max_length=255, required=True)
    code = StringField(max_length=255, required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

class Score(EmbeddedDocument):
    Hygiene = IntField(required=True)
    Structural = IntField(required=True)
    ConfidenceInManagement = IntField(required=True)

class Establishment(Document):
    FHRSID = IntField(required=True)
    LocalAuthorityBusinessID = StringField(max_length=255, required=True)
    BusinessName = StringField(max_length=255, required=True)
    BusinessType = StringField(max_length=255, required=True)
    BusinessTypeID = IntField(required=True)
    AddressLine1 = StringField(max_length=255, required=True)
    AddressLine2 = StringField(max_length=255, required=True)
    AddressLine3 = StringField(max_length=255, required=True)
    AddressLine4 = StringField(max_length=255, required=True)
    PostCode = StringField(max_length=255, required=True)
    Phone = StringField(max_length=255, required=True)
    RatingValue = StringField(max_length=255, required=True)
    RatingKey = StringField(max_length=255, required=True)
    RatingDate = DateTimeField(required=True)
    LocalAuthorityCode = StringField(max_length=255, required=True)
    LocalAuthorityName = StringField(max_length=255, required=True)
    LocalAuthorityWebSite = StringField(max_length=255, required=True)
    LocalAuthorityEmailAddress = StringField(max_length=255, required=True)
    scores = EmbeddedDocumentField(Score)
    SchemeType = StringField(max_length=255, required=True)
    geocode = PointField(required=False)
    RightToReply = StringField(max_length=255, required=True)
    Distance = FloatField(required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

