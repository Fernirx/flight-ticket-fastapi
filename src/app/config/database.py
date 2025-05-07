from urllib.parse import quote_plus
from app.config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

def get_database_url():
    """Construct the MySQL database URL from the settings."""
    password = quote_plus(settings.DATABASE_PASSWORD)  # Encode the password
    return f"{settings.DATABASE_URL}://{settings.DATABASE_USER}:{password}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

DATABASE_URL = get_database_url()
print(f"Connecting to database at {DATABASE_URL}")
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()