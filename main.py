from fastapi import FastAPI

from authentication.auth import app as AuthApp
import db.db

app = FastAPI(title="ChatterBox Backend App")
app.mount("/auth", AuthApp)


@app.get("/id{uid}")
def hello(uid: int):
    return uid
