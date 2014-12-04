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

