from db.db import db
from db.models.users import User

db.connect()

db.create_tables([User])
