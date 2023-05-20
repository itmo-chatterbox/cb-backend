from uuid import UUID
from fastapi import Response, Depends
from system.sessions.backend import backend
from system.sessions.frontend import cookie


async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
