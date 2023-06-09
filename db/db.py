from peewee import SqliteDatabase, Model
from playhouse.sqlite_ext import SqliteExtDatabase

# db = SqliteDatabase("chatterbox.db")
db = SqliteExtDatabase('chatterbox.db', regexp_function=True, timeout=3,
                       pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = db
