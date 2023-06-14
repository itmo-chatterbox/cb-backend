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


class Post(BaseModel):
    user_id = ForeignKeyField(User, related_name="Posts")
    date_of_publication = TimestampField(null=False)
    comment = CharField(null=True)
    title = CharField(null=True)
    pinned = BooleanField(default=False)
