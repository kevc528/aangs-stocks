import os

import bcrypt
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

from crud import create_user, get_user_by_email
from schemas import User, UserPassword

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


# post route to create a new user
@app.post("/user/", response_model=User)
def post_user(user: UserPassword):
    return create_user(db.session, user)


@app.post("/user/login")
def login(user: UserPassword):
    email_user = get_user_by_email(db.session, user.email)
    if email_user is not None and bcrypt.checkpw(
        user.password.encode("utf-8"), email_user.hashed_password.encode("utf-8")
    ):
        return {"id": email_user.id}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )


@app.get("/hello")
def hello_view():
    return "Hello world!"
