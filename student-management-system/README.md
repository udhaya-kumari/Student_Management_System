# Student Management System (v1)

A basic but properly structured full-stack app:

```
React (Vite)  →  REST API (Django + DRF)  →  SQLAlchemy  →  MySQL
```

Only the `Student` entity exists in this version. The structure is set up so
`Department`, `Course`, `Subject`, `Faculty`, `Attendance`, `Marks`, `Fees`
and `User`/auth can each be added later as their own app/model without
touching what's already here.

---

## 1. Project Structure

```
student-management-system/
├── backend/                     Django + DRF + SQLAlchemy API
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example             copy to .env and fill in your MySQL creds
│   ├── db_init.py               creates the MySQL DB + tables (no migrations)
│   ├── config/                  Django project (settings/urls only)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/
│   │   └── db.py                shared SQLAlchemy engine/session/Base
│   └── students/                the one "app" in this version
│       ├── models.py            SQLAlchemy Student model
│       ├── serializers.py       DRF validation
│       ├── views.py             CRUD endpoints
│       └── urls.py
│
└── frontend/                    React app (Vite)
    ├── index.html
    ├── .env.example              copy to .env, points to the API URL
    └── src/
        ├── main.jsx / App.jsx
        ├── App.css               all styling
        ├── services/api.js       one axios client, used by every page
        ├── components/           Navbar, StudentTable, StudentForm, SearchBar, ConfirmDialog
        └── pages/                Dashboard, StudentList, AddStudent, EditStudent, StudentDetails
```

**Why it's split this way:** `core/db.py` holds the one SQLAlchemy engine
the whole backend shares. Every future table just adds a `models.py` in its
own app folder that imports `Base` from `core.db` — nothing here has to
change. On the frontend, `services/api.js` is the only file that knows the
API's URL/shape; pages just call `studentApi.xxx()`.

---

## 2. Database design

Single table, deliberately not normalized yet:

| Column | Type | Constraint |
|---|---|---|
| student_id | INT | PK, auto-increment |
| register_number | VARCHAR(50) | UNIQUE, NOT NULL, manual entry |
| first_name / last_name | VARCHAR(100) | NOT NULL |
| date_of_birth | DATE | NOT NULL |
| gender | VARCHAR(20) | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| phone_number | VARCHAR(20) | NOT NULL |
| department | VARCHAR(100) | NOT NULL |
| year | INT | NOT NULL |
| semester | INT | NOT NULL |
| section | VARCHAR(10) | NOT NULL |
| address | VARCHAR(255) | nullable (optional) |
| parent_phone_number | VARCHAR(20) | NOT NULL |

Defined in `backend/students/models.py` as a SQLAlchemy `declarative_base()`
model, **not** a Django model — Django is used only as the web
framework/router; SQLAlchemy talks to MySQL directly.

**No migrations:** `backend/db_init.py` connects to MySQL, creates the
database if missing, then calls `Base.metadata.create_all(engine)` to
create every table that has been imported into `core.db.Base`. Run it once
before starting the server, and again after adding a new model file.

---

## 3. Setup & running

### Prerequisites
- Python 3.10+
- Node.js 18+
- A running MySQL server

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DJANGO_SECRET_KEY

python db_init.py               # creates the DB + students table
python manage.py runserver      # http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_BASE_URL=http://localhost:8000/api
npm run dev                     # http://localhost:5173
```

Open `http://localhost:5173`. The Dashboard, Student List, Add/Edit forms
and Student Details pages are all wired to the live API.

---

## 4. API reference

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/students/` | list students. Query params: `search`, `department`, `year`, `semester`, `section` |
| POST | `/students/` | create a student |
| GET | `/students/<id>/` | get one student |
| PUT | `/students/<id>/` | full update |
| PATCH | `/students/<id>/` | partial update |
| DELETE | `/students/<id>/` | delete |

Every response is:

```json
{ "success": true, "data": {...}, "message": "...", "errors": null }
```

On validation failure (`400`) or a duplicate register number/email (`409`),
`errors` is a dict keyed by field name, e.g.
`{"email": ["This email is already in use."]}`.

### Testing with Postman
1. Create a request `POST http://localhost:8000/api/students/`, body = raw JSON with all required fields (see table above).
2. `GET http://localhost:8000/api/students/` to confirm it was saved.
3. Try posting the same `register_number` or `email` again — expect `409` with a field error.
4. `GET /students/<id>/`, `PATCH /students/<id>/` with a partial body, `DELETE /students/<id>/`.

---

## 5. Validation

- **Frontend** (`StudentForm.jsx`): required fields, email format, phone
  format, checked before the request is even sent.
- **Backend** (`students/serializers.py` + `views.py`): the same rules are
  re-checked server-side (frontend validation is never trusted alone),
  plus a uniqueness pre-check on `register_number`/`email` that returns a
  clear, field-specific `409` error instead of a raw database exception.

---

## 6. Adding features later

To add e.g. `Department`:
1. `backend/departments/models.py` — SQLAlchemy model, `from core.db import Base`.
2. `backend/departments/serializers.py`, `views.py`, `urls.py` — same pattern as `students/`.
3. Add `path('api/', include('departments.urls'))` in `config/urls.py`.
4. Re-run `python db_init.py` to create the new table.
5. Add a `frontend/src/pages/Departments*.jsx` following the same pattern as the Student pages, and a `departmentApi` in `services/api.js`.

No existing file needs to be rewritten to do this.
