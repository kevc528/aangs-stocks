from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello_view():
    return "Hello world!"
