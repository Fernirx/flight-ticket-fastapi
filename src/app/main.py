from app.routers import auth
from app.routers import search
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(root_path="/flight_api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(search.ticket_router)
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}