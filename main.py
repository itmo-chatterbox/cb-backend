import os

from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from authentication.auth import app as AuthApp
from messages.messages import app as MessagesApp
from editing.edit import app as EditApp
from users.users import app as UsersApp
from config import FRONTEND_URL

app = FastAPI(title="ChatterBox Backend App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=['*'],
    allow_credentials=True
)

app.mount("/auth", AuthApp)
app.mount("/messages", MessagesApp)
app.mount("/edit", EditApp)
app.mount("/users", UsersApp)

try:
    os.mkdir("/static")
except:
    pass

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/id{uid}")
# def hello(uid: int):
#     return uid
#
# @app.post("/create_session/{name}")
# async def create_session_route(name: str, response: Response):
#     return await create_session(name, response)
#
# @app.get("/whoami", dependencies=[Depends(cookie)])
# async def whoami_route(session_data: SessionData = Depends(verifier)):
#     return await whoami(session_data)
#
# @app.post("/delete_session")
# async def del_session_route(response: Response, session_id: UUID = Depends(cookie)):
#     return await del_session(response, session_id)
