import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models import Base


# Locate project root and load environment variables
PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found in the .env file")


# Database engine
engine = create_engine(DATABASE_URL)


# Reusable database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Database connection successful!")
        print(result.scalar())


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    test_connection()
    create_tables()
