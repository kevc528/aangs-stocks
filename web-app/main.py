from fastapi import FastAPI

from schemas import User

app = FastAPI()


@app.post("/user/", response_model=User)
def create_user(user: User):
    return user


@app.get("/hello")
def hello_view():
    return "Hello world!"
