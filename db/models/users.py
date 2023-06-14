from peewee import Model, CharField, DateField, BooleanField

from db.db import BaseModel


class User(BaseModel):
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    first_name = CharField(null=False)
    last_name = CharField(null=False)
    birthdate = DateField(null=True)
    about = CharField(null=True)
    status = CharField(null=True)
    is_verified = BooleanField(default=False)
    photo_url = CharField(default="/static/no-photo.png")
