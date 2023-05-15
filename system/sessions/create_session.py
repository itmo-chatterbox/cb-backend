from uuid import uuid4
from fastapi import Response
from .session_data import SessionData
from .verifier import verifier
from .backend import backend
from .frontend import cookie

async def create_session(name: str, response: Response):
    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"
