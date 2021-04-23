import os

import bcrypt
import jwt
from fastapi import Cookie, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_sqlalchemy import DBSessionMiddleware, db

from crud import (add_stock_for_user, create_user, delete_stock_for_user,
                  get_user_by_email)
from schemas import Stock, StockCreate, User, UserPassword

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.mount("/static", StaticFiles(directory="static"), name="static")

jwt_secret = os.environ["JWT_SECRET"]

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_root_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/register")
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", context={"request": request})


def get_session_email(session):
    decoded = jwt.decode(session, jwt_secret, algorithms=["HS256"])
    return decoded["email"]


# post route to create a new user
@app.post("/user", response_model=User)
def post_user(user: UserPassword, response: Response):
    db_user = create_user(db.session, user)
    response.set_cookie(
        key="session",
        value=jwt.encode({"email": user.email}, key=jwt_secret, algorithm="HS256"),
        max_age=600,
    )
    return db_user


@app.post("/stock", response_model=Stock)
def post_stock(stock: StockCreate, session: str = Cookie(None)):
    email = get_session_email(session)
    return add_stock_for_user(db.session, stock, email)


@app.delete("/stock/{stock_id}")
def delete_stock(stock_id, session: str = Cookie(None)):
    email = get_session_email(session)
    try:
        delete_stock_for_user(db.session, stock_id, email)
        return ""
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your stock",
        )


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
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session")
    return response


@app.get("/user/me", response_model=User)
def me(session: str = Cookie(None)):
    email = get_session_email(session)
    return get_user_by_email(db.session, email)


not_logged_in_paths = ["/login", "/register", "/user", "/user/login"]


@app.middleware("http")
async def check_session(request: Request, call_next):
    session = request.cookies.get("session")
    if (
        session is None
        and request.url.path not in not_logged_in_paths
        and not request.url.path.startswith("/static")
    ):
        response = RedirectResponse(url="/login")
        return response
    elif session is not None and request.url.path in not_logged_in_paths:
        response = RedirectResponse(url="/")
        return response

    response = await call_next(request)
    if request.url.path != "/user/logout" and session is not None:
        response.set_cookie(
            key="session",
            value=session,
            max_age=600,
        )
    return response
