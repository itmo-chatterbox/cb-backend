from fastapi_sessions.backends.implementations import InMemoryBackend
from uuid import UUID

from system.sessions.session_data import SessionData

backend = InMemoryBackend[UUID, SessionData]()
