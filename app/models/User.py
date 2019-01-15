"""All registered users are input into this model"""
from datetime import datetime

from app.models import BaseModel
from playhouse.postgres_ext import BooleanField, CharField, DateTimeField, PrimaryKeyField


class User(BaseModel):
    id = PrimaryKeyField()
    phone_number = CharField(null=True, unique=True)
    display_name = CharField()
    photo = CharField(null=True)
    created = DateTimeField(default=datetime.now().isoformat())
