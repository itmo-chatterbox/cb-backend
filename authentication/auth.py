import datetime
import random
from uuid import UUID

import bcrypt
from fastapi import Body, FastAPI, HTTPException, Response, Depends

from pydantic import BaseModel, EmailStr

from db.models.users import User
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
    user = User(**data.__dict__)

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
