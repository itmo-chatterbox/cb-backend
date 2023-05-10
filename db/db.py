from peewee import SqliteDatabase, Model

db = SqliteDatabase("chatterbox.db")


class BaseModel(Model):
    class Meta:
        database = db
