import datetime
import random
from uuid import UUID

import bcrypt
from fastapi import Body, FastAPI, HTTPException, Response, Depends

from pydantic import BaseModel, EmailStr

from db.models.users import User
from db.models.messages import Message
from system.sessions.create_session import create_session
from system.sessions.delete_session import del_session
from system.sessions.frontend import cookie
from system.sessions.read_session import read_session
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()


def get_chats(user: User):
    query_sender = Message.select(User).where(
        Message.user_sender == user).join(User, on=(User.id == Message.user_reciever)).distinct()

    query_receiver = Message.select(User).where(
        Message.user_reciever == user).join(User, on=(User.id == Message.user_sender)).distinct()

    query_users = (query_sender | query_receiver)

    return query_users


def get_last_message(current_user: User, collocutor: User):
    return Message.select().where((Message.user_sender == current_user & Message.user_reciever == collocutor) | (
                Message.user_sender == collocutor & Message.user_reciever == current_user)).order_by(
        Message.sending_date.desc()).get()


@app.get("/chats", dependencies=[Depends(cookie)])
async def my_chats(session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    chats = get_chats(current_user)

    result = []

    for chat in chats:
        result.append({
            "user_id": chat.user.id,
            "full_name": f"{chat.user.first_name} {chat.user.last_name}",
            "photo_url": chat.user.photo_url
            "last_message": (get_last_message(current_user, chat.user)).text
        })

    return result

# @app.get("/dialogue/{collocutor_id}", dependencies=[Depends(cookie)])
# async def my_chats(session_data: SessionData = Depends(verifier),collocutor_id):
#     current_user = await read_session(session_data)
#     collocutor = User.get_or_none(User.id == collocutor_id)
#     last_message = get_last_message(current_user, collocutor)
#     result = {"Text" : }
