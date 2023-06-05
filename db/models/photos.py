from peewee import Model, CharField, DateField, BooleanField

from db.db import BaseModel



class Photo(BaseModel):
    photo_url = CharField(null=False)
