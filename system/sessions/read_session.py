from fastapi import Depends
from .session_data import SessionData
from .verifier import verifier

async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data
