from peewee import SqliteDatabase, Model, PostgresqlDatabase
from playhouse.sqlite_ext import SqliteExtDatabase

from config import DB_NAME, DB_USER, DB_PASS, DB_HOST

# # db = SqliteDatabase("chatterbox.db")
# db = SqliteExtDatabase('chatterbox.db', regexp_function=True, timeout=3,
#                        pragmas={'journal_mode': 'wal'})

db = PostgresqlDatabase('cbox', user='postgres', password='qwerty21',
                           host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db
