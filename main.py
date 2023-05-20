from fastapi import FastAPI, Depends, Response

# from uuid import UUID

from authentication.auth import app as AuthApp

# from system.sessions.create_session import create_session
# from system.sessions.read_session import whoami
# from system.sessions.delete_session import del_session
# from system.sessions.frontend import cookie
# from system.sessions.verifier import verifier
# from system.sessions.session_data import SessionData
# import db.db

app = FastAPI(title="ChatterBox Backend App")
app.mount("/auth", AuthApp)


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
