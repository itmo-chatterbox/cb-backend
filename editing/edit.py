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


@app.get("/edit_main_data", dependencies=[Depends(cookie)])
async def my_chats(name: str, surname: str, email_new: str, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    current_user.first_name = name
    current_user.last_name = surname
    current_user.email = email_new
    current_user.save()



@app.get("/edit_secondary_data", dependencies=[Depends(cookie)])
async def my_chats(birth: datetime.date, about_me: str, url_new: str, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    current_user.birthdate = birth
    current_user.about = about_me
    current_user.photo_url = url_new
    current_user.save()


@app.get("/edit_password", dependencies=[Depends(cookie)])
async def my_chats(passwd: str, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    hashed_passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
    current_user.password = hashed_passwd
    current_user.save()
