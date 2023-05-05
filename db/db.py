from peewee import *

db = SqliteDatabase("chatterbox.db")

db.connect()


class User(Model):
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    first_name = CharField(null=False)
    last_name = CharField(null=False)
    birthdate = DateField(null=True)
    about = CharField(null=True)
    status = CharField(null=True)
    is_verified = BooleanField(default=False)

    class Meta:
        database = db


db.create_tables([User])
