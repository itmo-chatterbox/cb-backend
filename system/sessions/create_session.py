from uuid import uuid4
from fastapi import Response

from db.models.users import User
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier
from system.sessions.backend import backend
from system.sessions.frontend import cookie


async def create_session(user: User, response: Response):
    session = uuid4()
    data = SessionData(id=user.id)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {user.id}"
