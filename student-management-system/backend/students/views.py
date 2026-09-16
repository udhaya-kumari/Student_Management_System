"""
API views for Student CRUD.

Uses SQLAlchemy directly (via core.db.get_db_session) instead of
Django's ORM/generic views, since the model is a SQLAlchemy class.
Every response follows the same envelope shape:

    { "success": bool, "data": ..., "message": str | None, "errors": {...} | None }

so the React side can handle every endpoint the same way.
"""
from django.db import IntegrityError as DjangoIntegrityError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.db import get_db_session
from .models import Student
from .serializers import StudentSerializer


def envelope(success, data=None, message=None, errors=None):
    return {'success': success, 'data': data, 'message': message, 'errors': errors}


class StudentListCreateView(APIView):
    """
    GET  /api/students/        -> list students (supports ?search=&department=&year=&semester=&section=)
    POST /api/students/        -> create a student
    """

    def get(self, request):
        search = request.query_params.get('search', '').strip()
        department = request.query_params.get('department')
        year = request.query_params.get('year')
        semester = request.query_params.get('semester')
        section = request.query_params.get('section')

        with get_db_session() as db:
            query = db.query(Student)

            if search:
                like = f"%{search}%"
                query = query.filter(
                    or_(
                        Student.first_name.ilike(like),
                        Student.last_name.ilike(like),
                        Student.register_number.ilike(like),
                        Student.email.ilike(like),
                    )
                )
            if department:
                query = query.filter(Student.department == department)
            if year:
                query = query.filter(Student.year == year)
            if semester:
                query = query.filter(Student.semester == semester)
            if section:
                query = query.filter(Student.section == section)

            students = query.order_by(Student.student_id.desc()).all()
            data = [s.to_dict() for s in students]

        return Response(envelope(True, data=data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                envelope(False, errors=serializer.errors, message='Validation failed.'),
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = serializer.validated_data

        with get_db_session() as db:
            # Pre-check uniqueness so we can return a friendly, field-specific error
            existing = db.query(Student).filter(
                or_(
                    Student.register_number == payload['register_number'],
                    Student.email == payload['email'],
                )
            ).first()
            if existing:
                field = 'register_number' if existing.register_number == payload['register_number'] else 'email'
                return Response(
                    envelope(False, message='Duplicate value.', errors={field: [f'This {field} is already in use.']}),
                    status=status.HTTP_409_CONFLICT,
                )

            student = Student(**payload)
            try:
                db.add(student)
                db.flush()  # get the generated student_id before commit
                data = student.to_dict()
            except IntegrityError:
                db.rollback()
                return Response(
                    envelope(False, message='Duplicate value.', errors={'non_field_errors': ['Register number or email already exists.']}),
                    status=status.HTTP_409_CONFLICT,
                )

        return Response(envelope(True, data=data, message='Student created.'), status=status.HTTP_201_CREATED)


class StudentDetailView(APIView):
    """
    GET    /api/students/<id>/  -> retrieve one student
    PUT    /api/students/<id>/  -> full update
    PATCH  /api/students/<id>/  -> partial update
    DELETE /api/students/<id>/  -> delete
    """

    def _get_student(self, db, student_id):
        return db.query(Student).filter(Student.student_id == student_id).first()

    def get(self, request, student_id):
        with get_db_session() as db:
            student = self._get_student(db, student_id)
            if not student:
                return Response(envelope(False, message='Student not found.'), status=status.HTTP_404_NOT_FOUND)
            data = student.to_dict()
        return Response(envelope(True, data=data), status=status.HTTP_200_OK)

    def put(self, request, student_id):
        return self._update(request, student_id, partial=False)

    def patch(self, request, student_id):
        return self._update(request, student_id, partial=True)

    def _update(self, request, student_id, partial):
        with get_db_session() as db:
            student = self._get_student(db, student_id)
            if not student:
                return Response(envelope(False, message='Student not found.'), status=status.HTTP_404_NOT_FOUND)

            serializer = StudentSerializer(data=request.data, partial=partial)
            if not serializer.is_valid():
                return Response(
                    envelope(False, errors=serializer.errors, message='Validation failed.'),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            payload = serializer.validated_data

            # Uniqueness check excluding the current student
            new_reg = payload.get('register_number', student.register_number)
            new_email = payload.get('email', student.email)
            clash = db.query(Student).filter(
                Student.student_id != student_id,
                or_(Student.register_number == new_reg, Student.email == new_email),
            ).first()
            if clash:
                field = 'register_number' if clash.register_number == new_reg else 'email'
                return Response(
                    envelope(False, message='Duplicate value.', errors={field: [f'This {field} is already in use.']}),
                    status=status.HTTP_409_CONFLICT,
                )

            for key, value in payload.items():
                setattr(student, key, value)

            try:
                db.flush()
                data = student.to_dict()
            except IntegrityError:
                db.rollback()
                return Response(
                    envelope(False, message='Duplicate value.'),
                    status=status.HTTP_409_CONFLICT,
                )

        return Response(envelope(True, data=data, message='Student updated.'), status=status.HTTP_200_OK)

    def delete(self, request, student_id):
        with get_db_session() as db:
            student = self._get_student(db, student_id)
            if not student:
                return Response(envelope(False, message='Student not found.'), status=status.HTTP_404_NOT_FOUND)
            db.delete(student)
        return Response(envelope(True, message='Student deleted.'), status=status.HTTP_200_OK)
