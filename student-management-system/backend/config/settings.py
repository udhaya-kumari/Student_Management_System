"""
Django settings for the Student Management System backend.

NOTE ON DATABASE ACCESS
------------------------
This project intentionally does NOT use Django's built-in ORM for
application data. All reads/writes to MySQL for business entities
(Student, and later Department/Course/Subject/etc.) go through
SQLAlchemy (see `core/db.py` and `students/models.py`).

Django itself still needs *a* DATABASES entry to boot (for things like
sessions/admin if you enable them later), so we point it at a small
local SQLite file that the app does not otherwise use. This keeps
Django and SQLAlchemy cleanly separated, per the architecture:

    React -> REST API (Django + DRF) -> SQLAlchemy -> MySQL
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-only-insecure-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'students',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': []},
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Django's own (unused-for-app-data) database. Kept as SQLite so the
# project runs with zero extra setup. Real data lives in MySQL via SQLAlchemy.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'django_internal.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

# Allow the Vite dev server to call the API during development.
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}
