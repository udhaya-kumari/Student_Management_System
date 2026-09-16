"""
One-off script that creates the MySQL database (if it doesn't exist)
and all SQLAlchemy tables (Student now; Department/Course/etc. later
as soon as their models import the same `Base`).

This project deliberately avoids Django migrations. Run this script
once before starting the server, and again any time you add a new
SQLAlchemy model file that needs to import to register its table:

    python db_init.py
"""
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME', 'student_management')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')


def create_database_if_missing():
    connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
        print(f"Database '{DB_NAME}' is ready.")
    finally:
        connection.close()


def create_tables():
    # Import Base first, then every model module, so Base.metadata knows
    # about all of them before create_all() runs. Add new model imports
    # here as new apps are introduced (departments, courses, ...).
    from core.db import Base, engine
    from students import models  # noqa: F401  (registers Student on Base)

    Base.metadata.create_all(engine)
    print("All tables created (or already existed).")


if __name__ == '__main__':
    create_database_if_missing()
    create_tables()
