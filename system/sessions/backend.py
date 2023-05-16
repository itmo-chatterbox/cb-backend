from fastapi_sessions.backends.implementations import InMemoryBackend
from uuid import UUID

from .session_data import SessionData

backend = InMemoryBackend[UUID, SessionData]()
