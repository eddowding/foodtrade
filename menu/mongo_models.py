from datetime import datetime
from mongoengine import *


class Region(Document):
    fsa_id = IntField(required=True)
    name = StringField(max_length=255, required=True)
    nameKey = StringField(max_length=255, required=True)
    code = StringField(max_length=255, required=True)
    added_on = DateTimeField(required=True)
    modified_on = DateTimeField(default=datetime.now)

