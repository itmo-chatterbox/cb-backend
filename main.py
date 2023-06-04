from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from config import FRONTEND_URI

# from uuid import UUID

from authentication.auth import app as AuthApp
from messages.messages import app as MessagesApp

app = FastAPI(title="ChatterBox Backend App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URI],
    allow_methods=['*'],
    allow_credentials=True
)

app.mount("/auth", AuthApp)
app.mount("/messages", MessagesApp)

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
