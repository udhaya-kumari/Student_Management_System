"""
SQLAlchemy model for the Student table.

Kept as a single, deliberately un-normalized table for this first
version (per requirements). Future normalization (linking department,
year, section to their own tables) can happen by adding new SQLAlchemy
models in new apps (e.g. `departments/models.py`) that import the same
`Base` from `core.db`, and later adding foreign keys here — without
rewriting this file's existing columns.
"""
from sqlalchemy import Column, Integer, String, Date
from core.db import Base


class Student(Base):
    __tablename__ = 'students'

    # Student ID: auto-generated primary key
    student_id = Column(Integer, primary_key=True, autoincrement=True)

    # Register Number: unique, required, entered manually by admin (NOT auto)
    register_number = Column(String(50), unique=True, nullable=False, index=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)

    department = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String(10), nullable=False)

    address = Column(String(255), nullable=True)  # optional
    parent_phone_number = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'register_number': self.register_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'email': self.email,
            'phone_number': self.phone_number,
            'department': self.department,
            'year': self.year,
            'semester': self.semester,
            'section': self.section,
            'address': self.address,
            'parent_phone_number': self.parent_phone_number,
        }
