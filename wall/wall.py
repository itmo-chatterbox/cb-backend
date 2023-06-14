import datetime

from fastapi import FastAPI, HTTPException, Depends

from db.models.users import User
from db.models.posts import Post
from system.sessions.frontend import cookie
from system.sessions.read_session import read_session
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()

#получаем текущего пользователя
async def get_current_user(session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    return current_user

#получаем все посты со страницы
def get_posts(user):
    posts = Post.select().where(Post.user_id == user)
    list_of_posts = []
    for post in posts:
        list_of_posts.append({
            "id": post.id,
            "date": post.date,
            "title": post.title,
            "text": post.text
        })
    return list_of_posts

#просмотр страницы
@app.get("/wall/{user_id}", dependencies=[Depends(cookie)])
async def read_wall(user_id: int, session_data: SessionData = Depends(verifier)):
    user = User.get_or_none(User.id == user_id)
    posts = get_posts(user)
    return posts

class PostCreate:
    heading: str
    text: str

class PostDelete:
    post_id: int

class PostEdit:
    post_id: int
    changed_data: str

#добавление постов
@app.post("/create", dependencies=[Depends(cookie)])
async def create_post(data: PostCreate, session_data: SessionData = Depends(verifier)):
    author = get_current_user()
    Post.create(user_id=author, date_of_publication=datetime.datetime.now(), comment=data.text, title=data.heading)
    return {"message": "Post has been uploaded"}

#редактирование постов
@app.get("/edit", dependencies=[Depends(cookie)])
async def edit_post(data: PostEdit, session_data: SessionData = Depends(verifier)):
    author = get_current_user()
    post = Post.get_or_none(Post.id == data.post_id)
    
    #проверка на существование поста и его автора
    if not post or post.user_id != author.id:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.text = data.changed_data
    post.save()
    return {"message": "Post has been changed"}

#удаление постов
@app.get("/delete", dependencies=[Depends(cookie)])
async def delete_post(data: PostDelete, session_data: SessionData = Depends(verifier)):
     author = get_current_user()
     post = Post.get_or_none(Post.id == data.post_id)

    #проверка на существование поста и его автора
     if not post or post.user_id != author.id:
        raise HTTPException(status_code=404, detail="Post not found")
     
     post.delete_instance()
     return {"message": "Post has been deleted"}