from fastapi import Depends, FastAPI
from peewee import fn

from db.models.users import User
from system.sessions.frontend import cookie
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier

app = FastAPI()


@app.get("/get/{id}")
async def user_info(id: int):
    user = User.get_or_none(User.id == id)

    if user:
        return {"status": "ok", "data": user.__dict__}
    else:
        return {"status": "undefined user"}


@app.get("/get_by_name")
async def users_by_name(name: str):
    # result = User.select().where(f"*{name}*" % f"{User.first_name} {User.last_name}")
    query = User.select().where((User.first_name + " " + User.last_name) ** f"%{name}%")

    result = [user for user in query]
    return result
