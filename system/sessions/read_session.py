from fastapi import Depends
from system.sessions.session_data import SessionData
from system.sessions.verifier import verifier
from db.models.users import User


async def read_session(session_data: SessionData = Depends(verifier)) -> User:
    user = User.get_or_none(User.id == session_data.id)
    return user
