import datetime

import bcrypt
from fastapi import Body, FastAPI, HTTPException

from pydantic import BaseModel, EmailStr

from db.models.users import User

app = FastAPI()


class SignupDTO(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birthdate: datetime.date


class LoginDTO(BaseModel):
    email: EmailStr
    password: str


@app.post("/signup")
async def signup(data: SignupDTO):
    user = User(**data.__dict__)

    hashed_passwd = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    user.password = hashed_passwd

    user.save()


@app.post("/login")
async def login(data: LoginDTO):
    user = User.get_or_none(User.email == data.email)

    if not user:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    password_correct = bcrypt.checkpw(data.password.encode(), user.password.encode())

    if not password_correct:
        raise HTTPException(status_code=400, detail="User or password is not correct")

    return {"status": "ok"}
    # create session

from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters


class SessionData(BaseModel):
    username: str


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="b410ffcb40fe3f9cd37ab32dad0af9be2b30c2f379fa60e62e5c77b821a22a44",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

@app.post("/create_session/{name}")
async def create_session(name: str, response: Response):

    session = uuid4()
    data = SessionData(username=name)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    return f"created session for {name}"


@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"