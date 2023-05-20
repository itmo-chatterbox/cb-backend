from peewee import Model, CharField, DateField, BooleanField, ForeignKeyField

from db.db import BaseModel

from db.models.users import User


class Message(BaseModel):
    user_sender_id = ForeignKeyField(User, related_name='messages')
    user_reciever_id = ForeignKeyField(User, related_name='messages')
    sending_data = DateField(null=False)
    text = CharField(null=False)
