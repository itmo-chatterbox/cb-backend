import datetime

import bcrypt
from fastapi import Body, FastAPI, HTTPException

from pydantic import BaseModel, EmailStr

from db.models.users import User

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


@app.post("/signup")
async def signup(data: SignupDTO):
    user = User(**data.__dict__)

    hashed_passwd = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    user.password = hashed_passwd

    user.save()


@app.post("/login")
async def login(data: LoginDTO):
    user = User.get_or_none(User.email == data.email)

    if not user:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    password_correct = bcrypt.checkpw(data.password.encode(), user.password.encode())

    if not password_correct:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    return {"status": "ok"}