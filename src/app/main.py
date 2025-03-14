from app.routers import auth

from fastapi import FastAPI

app = FastAPI()

app.include_router(auth.router)
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
