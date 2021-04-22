import os
from typing import Optional

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, HTTPException, Request, Response, status
from fastapi_sqlalchemy import DBSessionMiddleware, db

from crud import create_user, get_user_by_email
from schemas import User, UserPassword

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

jwt_secret = os.environ["JWT_SECRET"]


def get_session_email(session):
    decoded = jwt.decode(session, jwt_secret, algorithms=["HS256"])
    return decoded["email"]


# post route to create a new user
@app.post("/user/", response_model=User)
def post_user(user: UserPassword):
    return create_user(db.session, user)


@app.post("/user/login")
def login(user: UserPassword, response: Response):
    email_user = get_user_by_email(db.session, user.email)
    if email_user is not None and bcrypt.checkpw(
        user.password.encode("utf-8"), email_user.hashed_password.encode("utf-8")
    ):
        response.set_cookie(
            key="session",
            value=jwt.encode({"email": user.email}, key=jwt_secret, algorithm="HS256"),
            max_age=600,
        )
        return {"id": email_user.id}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )


@app.get("/user/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return ""


@app.get("/hello")
def hello_view(session: Optional[str] = Cookie(None)):
    if session is not None:
        return f"Hello {get_session_email(session)}"
    return "Hello world!"


@app.middleware("http")
async def update_session(request: Request, call_next):
    session = request.cookies.get("session")
    response = await call_next(request)
    if request.url.path != "/user/logout" and session is not None:
        response.set_cookie(
            key="session",
            value=session,
            max_age=600,
        )
    return response
