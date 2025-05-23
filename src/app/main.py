from app.routers import auth, flight
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
app.include_router(flight.router)
@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}