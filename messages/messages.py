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


@app.get("/all", dependencies=[Depends(cookie)])
async def my_chats(session_data: SessionData = Depends(verifier)):
    my_id = session_data.id
    collocutors = get_list_of_collocutors(my_id)

    all_messages = []
    photos = [
        "https://vsegda-pomnim.com/uploads/posts/2022-04/1649647921_71-vsegda-pomnim-com-p-tsvetok-stalina-foto-76.jpg",
        "https://rgnp.ru/wp-content/uploads/e/3/e/e3eab3bdbad62e3db10d55b956dffb2b.jpeg",
        "https://sun9-51.userapi.com/impg/WHjC49aHsyvMlmPdpJn_68OtWkvPo_DkSqIA-g/vGqR41ewlzU.jpg?size=1280x721&quality=95&sign=58a75b2b13197253b9852e380f97bfb8&type=album",
        "https://cdn.fishki.net/upload/post/2020/08/14/3394916/tn/ea9b59c02ad9a304f19d08990ff116e7.jpg",
        "https://x-true.info/uploads/posts/2015-06/1434888790_d095d0bbd18cd186d0b8d0bd.jpg",
        "https://cdn.poryadok.ru/upload/iblock/518/518e8e876e19e597c5dddcdd36e9b0ea.jpeg"]
    for collocutor in collocutors:
        x = {}
        x["id"] = collocutor.id
        x["name"] = collocutor.first_name + " " + collocutor.last_name
        # x["photo"] = random.choice(photos)
        last_message = find_last_message(my_id, collocutor.id)
        x["last_message_txt"] = last_message.text
        print(last_message.__dict__)
        # x["sending_date"] = last_message.sending_date
        all_messages.append(x)
    return all_messages

# @app.get("/{collocutor}", dependencies=[Depends(cookie)])
# async def my_chats(session_data: SessionData = Depends(verifier)):
#     my_id = session_data.id
#     collocutor_id = collocutor
