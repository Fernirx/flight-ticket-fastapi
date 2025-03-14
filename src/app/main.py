from app.routers import router

from fastapi import FastAPI

app = FastAPI()

app.include_router(router.router)
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
