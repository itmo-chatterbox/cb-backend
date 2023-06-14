import datetime
import random
from uuid import UUID

import bcrypt
from fastapi import Body, FastAPI, HTTPException, Response, Depends

from pydantic import BaseModel, EmailStr
from starlette.websockets import WebSocket

from db.models.users import User
from db.models.messages import Message
from system.sessions.create_session import create_session
from system.sessions.delete_session import del_session
from system.sessions.frontend import cookie
from system.sessions.read_session import read_session
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()


def get_messages(current_user: User, collocutor: User):
    return Message.select().where(((Message.user_sender == current_user) & (Message.user_reciever == collocutor)) | (
            (Message.user_sender == collocutor) & (Message.user_reciever == current_user))).order_by(
        Message.sending_date.asc())


def get_chats(user: User):
    query_sender = Message.select(User).where(
        Message.user_sender == user).join(User, on=(User.id == Message.user_reciever)).distinct()

    query_receiver = Message.select(User).where(
        Message.user_reciever == user).join(User, on=(User.id == Message.user_sender)).distinct()

    query_users = (query_sender | query_receiver)

    return query_users


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
        })

    return result


@app.get("/dialogue/{collocutor_id}", dependencies=[Depends(cookie)])
async def my_chats(collocutor_id: int, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    collocutor = User.get_or_none(User.id == collocutor_id)
    messages = get_messages(current_user, collocutor)
    result = []
    for message in messages:
        result.append({
            "text": message.text,
            "full_name": f"{message.user_sender.first_name} {message.user_sender.last_name}",
            "photo_url": message.user_sender.photo_url,
            "sending_date": message.sending_date
        })
    return result


class SendMessageDTO(BaseModel):
    chat: int
    text: str


@app.post("/dialogue/{collocutor_id}/send", dependencies=[Depends(cookie)])
async def my_chats(data: SendMessageDTO, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    collocutor = User.get_or_none(User.id == data.chat)
    Message.create(user_sender=current_user, user_reciever=collocutor, sending_date=datetime.datetime.now().timestamp(),
                   text=data.text)
