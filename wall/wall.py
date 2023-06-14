import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from db.models.users import User
from db.models.posts import Post
from system.sessions.frontend import cookie
from system.sessions.read_session import read_session
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()


# получаем текущего пользователя
async def get_current_user(session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    return current_user


# получаем все посты со страницы
def get_posts(user):
    posts = Post.select().where(Post.user_id == user)
    list_of_posts = []
    for post in posts:
        list_of_posts.append(
            {
                "id": post.id,
                "date": post.date_of_publication,
                "title": post.title,
                "text": post.comment,
                "pinned": post.pinned,
            }
        )
    return list_of_posts


# просмотр страницы
@app.get("/{user_id}", dependencies=[Depends(cookie)])
async def read_wall(user_id: int, session_data: SessionData = Depends(verifier)):
    user = User.get_or_none(User.id == user_id)
    posts = get_posts(user)
    return posts


class PostCreate(BaseModel):
    heading: str
    text: str


class PostDelete(BaseModel):
    post_id: int


class PostEdit(BaseModel):
    post_id: int
    changed_data: str


@app.post("/create", dependencies=[Depends(cookie)])
async def create_post(data: PostCreate, session_data: SessionData = Depends(verifier)):
    author = await read_session(session_data)
    Post.create(
        user_id=author,
        date_of_publication=datetime.datetime.now().timestamp(),
        comment=data.text,
        title=data.heading,
    )
    return {"message": "Post has been uploaded"}


@app.post("/edit", dependencies=[Depends(cookie)])
async def edit_post(data: PostEdit, session_data: SessionData = Depends(verifier)):
    author = await read_session(session_data)
    post = Post.get_or_none(Post.id == data.post_id)

    if not post or post.user_id.id != author.id:
        raise HTTPException(status_code=404, detail="Post not found")

    post.comment = data.changed_data
    post.save()
    return {"message": "Post has been changed"}


@app.post("/delete", dependencies=[Depends(cookie)])
async def delete_post(id: int, session_data: SessionData = Depends(verifier)):
    author = await read_session(session_data)
    post = Post.get_or_none(Post.id == id)

    # проверка на существование поста и его автора
    if not post or post.user_id.id != author.id:
        raise HTTPException(status_code=404, detail="Post not found")

    post.delete_instance()
    return {"message": "Post has been deleted"}


@app.post("/pin", dependencies=[Depends(cookie)])
async def delete_post(id: int, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    current_pinned = Post.get_or_none(Post.pinned == True)

    if current_pinned:
        current_pinned.pinned = False
        current_pinned.save()

    new_to_pin = Post.get_or_none((Post.user_id == current_user) & (Post.id == id))

    if not new_to_pin:
        raise HTTPException(status_code=404, detail="Post not found")

    new_to_pin.pinned = True
    new_to_pin.save()
    return {"message": "Post has been pinned"}
