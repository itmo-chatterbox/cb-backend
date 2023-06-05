import datetime
import random
from uuid import UUID

import bcrypt
from fastapi import Body, FastAPI, HTTPException, Response, Depends

from pydantic import BaseModel, EmailStr

from db.models.users import User
from db.models.photos import Photo
from system.sessions.create_session import create_session
from system.sessions.delete_session import del_session
from system.sessions.frontend import cookie
from system.sessions.read_session import read_session
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()


class SignupDTO(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birthdate: datetime.date


class LoginDTO(BaseModel):
    email: EmailStr
    password: str


@app.get("/user/{id}")
async def user_info(id: int):
    user = User.get_or_none(User.id == id)

    if user:
        return {"status": "ok", "data": user.__dict__}
    else:
        return {"status": "undefined user"}


@app.post("/signup")
async def signup(data: SignupDTO, response: Response):
    photos = [
        "https://vsegda-pomnim.com/uploads/posts/2022-04/1649647921_71-vsegda-pomnim-com-p-tsvetok-stalina-foto-76.jpg",
        "https://rgnp.ru/wp-content/uploads/e/3/e/e3eab3bdbad62e3db10d55b956dffb2b.jpeg",
        "https://sun9-51.userapi.com/impg/WHjC49aHsyvMlmPdpJn_68OtWkvPo_DkSqIA-g/vGqR41ewlzU.jpg?size=1280x721&quality=95&sign=58a75b2b13197253b9852e380f97bfb8&type=album",
        "https://cdn.fishki.net/upload/post/2020/08/14/3394916/tn/ea9b59c02ad9a304f19d08990ff116e7.jpg",
        "https://x-true.info/uploads/posts/2015-06/1434888790_d095d0bbd18cd186d0b8d0bd.jpg",
        "https://cdn.poryadok.ru/upload/iblock/518/518e8e876e19e597c5dddcdd36e9b0ea.jpeg"
    ]

    user = User(**data.__dict__)
    user_photo = Photo.create(photo_url=random.choice(photos))
    user.photo = user_photo

    hashed_passwd = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    user.password = hashed_passwd

    user.save()
    await create_session(user, response)
    return {"status": "ok"}


@app.post("/login")
async def login(data: LoginDTO, response: Response):
    user = User.get_or_none(User.email == data.email)

    if not user:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    password_correct = bcrypt.checkpw(data.password.encode(), user.password.encode())

    if not password_correct:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    await create_session(user, response)
    return {"status": "ok"}


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami_route(session_data: SessionData = Depends(verifier)):
    return await read_session(session_data)


@app.get("/logout")
async def del_session_route(response: Response, session_id: UUID = Depends(cookie)):
    return await del_session(response, session_id)
