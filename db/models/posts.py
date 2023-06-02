from peewee import Model, CharField, DateField, BooleanField, ForeignKeyField

from db.db import BaseModel

from db.models.users import User


class Post(BaseModel):
    user_id = ForeignKeyField(User, related_name="Posts")
    date_of_publication = DateField(null=False)
    comment = CharField(null=False)


# class PostCreate:
#     comment: str
#
# class PostDelete:
#     post_id: int
#
#
# @app.post("/create")
# async def post_create(data:PostCreate):
#     # get user id
#     # create post in db
#     return {"status": "ok"}
#
# @app.get("/posts/{id}")
# async def get_posts(id: int):
#     posts = Post.select().where(Post.user_id == current_user.id)
#     result = []
#     for post in posts:
#         result.append({
#             "id": post.id,
#             # date,
#             # comment
#         })
#     return result