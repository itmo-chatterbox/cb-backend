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


def get_list_of_collocutors(my_id: int):
    my_letters = Message.select().where(Message.user_sender.id == my_id or Message.user_reciever.id == my_id)
    collocutors = set()
    for letter in my_letters:
        if letter.user_sender.id == my_id:
            collocutor = letter.user_reciever
        else:
            collocutor = letter.user_sender
        collocutors.add(collocutor)
    return collocutors


def find_last_message(my_id: int, collocutor_id: int):
    return Message.select().where((Message.user_sender.id == my_id and Message.user_reciever.id == collocutor_id) or (
                Message.user_sender.id == collocutor_id and Message.user_reciever.id == my_id)).order_by(
        User.birthday.desc()).get()


def get_last_message(current_user: User, collocutor: User):
    return Message.select().where((Message.user_sender == current_user & Message.user_reciever == collocutor) | (
            Message.user_sender == collocutor & Message.user_reciever == current_user)).order_by(
        Message.sending_date.desc()).get()


def get_messages(current_user: User, collocutor: User):
    return Message.select().where((Message.user_sender == current_user & Message.user_reciever == collocutor) | (
            Message.user_sender == collocutor & Message.user_reciever == current_user)).order_by(
        Message.sending_date.desc())


@app.get("/chats", dependencies=[Depends(cookie)])
async def my_chats(session_data: SessionData = Depends(verifier)):
    my_id = session_data.id
    collocutors = get_list_of_collocutors(my_id)

    for chat in chats:
        result.append({
            "user_id": chat.user.id,
            "full_name": f"{chat.user.first_name} {chat.user.last_name}",
            "photo_url": chat.user.photo_url,
            "last_message": (get_last_message(current_user, chat.user)).text
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


@app.post("/dialogue/{collocutor_id}/send", dependencies=[Depends(cookie)])
async def my_chats(collocutor_id: int, sending_text: str, session_data: SessionData = Depends(verifier)):
    current_user = await read_session(session_data)
    collocutor = User.get_or_none(User.id == collocutor_id)
    Message.create(user_sender=current_user, user_reciever=collocutor, sending_date=datetime.datetime.now(),
                   text=sending_text)