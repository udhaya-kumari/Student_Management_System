"""
Central SQLAlchemy setup, shared by every app-level model.

Why this file exists / why it lives here:
------------------------------------------
Every future table (Department, Course, Subject, Faculty, Attendance,
Marks, Fees, User, ...) will import `Base` from this module and share
the same `engine` / `SessionLocal`. That is the one thing that lets us
bolt on new tables later without touching this file again.

Usage in a view:
    from core.db import SessionLocal
    db = SessionLocal()
    try:
        ...
    finally:
        db.close()

Or, simpler, use the `get_db_session()` context manager below.
"""
import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'student_management')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# pool_pre_ping avoids "MySQL server has gone away" errors on idle connections
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# All SQLAlchemy models (students/models.py and any future app's models.py)
# must inherit from this same Base so `Base.metadata.create_all()` picks
# them all up in one place (see backend/db_init.py).
Base = declarative_base()


@contextmanager
def get_db_session():
    """Convenience context manager: `with get_db_session() as db: ...`"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
