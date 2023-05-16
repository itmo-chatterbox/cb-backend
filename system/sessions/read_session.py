from fastapi import Depends
from .session_data import SessionData
from .verifier import verifier
from db.models.users import User

async def read_session(session_data: SessionData = Depends(verifier)):
    user = User.get_or_none(User.id = session_data.id)
    return user
