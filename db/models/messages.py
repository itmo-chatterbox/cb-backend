from peewee import (
    Model,
    CharField,
    DateField,
    BooleanField,
    ForeignKeyField,
    TimestampField,
)

from db.db import BaseModel

from db.models.users import User


class Message(BaseModel):
    user_sender = ForeignKeyField(User, related_name="messages")
    user_reciever = ForeignKeyField(User, related_name="messages")
    sending_date = TimestampField(null=False)
    text = CharField(null=False)
