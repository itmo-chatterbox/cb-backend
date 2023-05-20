from uuid import UUID
from fastapi import Response, Depends
from .backend import backend
from .frontend import cookie


async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
