from peewee import Model, CharField, DateField, BooleanField, ForeignKeyField

from db.db import BaseModel

from db.models.users import User


class Message(BaseModel):
    user_sender = ForeignKeyField(User)
    user_reciever = ForeignKeyField(User)
    sending_date = DateField(null=False)
    text = CharField(null=False)
