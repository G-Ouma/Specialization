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
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found in the .env file")


# Database engine
engine = create_engine(DATABASE_URL)
test_engine = create_engine(TEST_DATABASE_URL)


# Reusable database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Database connection successful!")
        print(result.scalar())


def test_test_database_connection():
    with test_engine.connect() as connection:
        result = connection.execute(text("SELECT current_database()"))
        print("Test database connection successful!")
        print(f"Connected to: {result.scalar()}")

    test_engine.dispose()


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def create_test_tables():
    Base.metadata.create_all(bind=test_engine)
    print("Test database tables created successfully!")


if __name__ == "__main__":
    test_connection()
    test_test_database_connection()
    create_tables()
    create_test_tables()
