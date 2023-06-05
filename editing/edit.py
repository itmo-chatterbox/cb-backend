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


class EditStepDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birthdate: datetime.date
    about: str

class EditPasswordDTO(BaseModel):
    password: str


@app.post("/main_data", dependencies=[Depends(cookie)])
async def edit_step_1(data: EditStepDTO, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)

    current_user.first_name = data.first_name
    current_user.last_name = data.last_name
    current_user.email = data.email
    current_user.birthdate = data.birthdate
    current_user.about = data.about

    User.bulk_update([current_user], [User.first_name, User.last_name, User.email, User.birthdate, User.about])

    return {"status": "ok"}


@app.post("/password", dependencies=[Depends(cookie)])
async def edit_passwd(data: EditPasswordDTO, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    passwd = data.password
    hashed_passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
    current_user.password = hashed_passwd
    current_user.save()
    return {"status": "ok"}

@app.post("/status", dependencies=[Depends(cookie)])
async def edit_status(new_status: str, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    current_user.status = new_status
    current_user.save()
    return {"status": "ok"}
