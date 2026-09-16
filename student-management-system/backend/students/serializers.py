"""
DRF serializers for Student.

These are plain `serializers.Serializer` classes (not ModelSerializer)
because the model is a SQLAlchemy class, not a Django model. This is
the file to edit if you need to add/rename a Student field, and the
place to add new serializers (StudentBriefSerializer, etc.) as the
project grows.
"""
import re
from datetime import date
from rest_framework import serializers

PHONE_REGEX = re.compile(r'^\+?\d{7,15}$')
VALID_GENDERS = {'Male', 'Female', 'Other'}


class StudentSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(read_only=True)
    register_number = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    gender = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    department = serializers.CharField(max_length=100)
    year = serializers.IntegerField(min_value=1, max_value=6)
    semester = serializers.IntegerField(min_value=1, max_value=12)
    section = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    parent_phone_number = serializers.CharField(max_length=20)

    def validate_gender(self, value):
        if value not in VALID_GENDERS:
            raise serializers.ValidationError(
                f"Gender must be one of: {', '.join(sorted(VALID_GENDERS))}"
            )
        return value

    def validate_phone_number(self, value):
        if not PHONE_REGEX.match(value):
            raise serializers.ValidationError(
                'Phone number must contain 7-15 digits (optionally starting with +).'
            )
        return value

    def validate_parent_phone_number(self, value):
        if not PHONE_REGEX.match(value):
            raise serializers.ValidationError(
                'Parent/Guardian phone number must contain 7-15 digits (optionally starting with +).'
            )
        return value

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError('Date of birth must be in the past.')
        return value

    def validate_register_number(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Register number cannot be blank.')
        return value
