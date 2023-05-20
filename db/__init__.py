from db.db import db

from db.models.users import User
from db.models.posts import Post
from db.models.messages import Message

db.connect()

db.create_tables([User])
db.create_tables([Post])
db.create_tables([Message])