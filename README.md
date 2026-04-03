# FastAPI Todo API

A REST API for managing todos with JWT authentication. Built with FastAPI and PostgreSQL.

## Features

- User registration and login with JWT auth
- Create, read, update, delete tasks
- Tasks are private — users can only access their own
- Full test suite with pytest

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — production database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **python-jose** — JWT tokens
- **passlib[bcrypt]** — password hashing
- **pytest** — testing (SQLite in-memory)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env and fill in your DATABASE_URL and SECRET_KEY
```

## Database

```bash
# Create the database (PostgreSQL)
psql -U postgres -c "CREATE DATABASE fastapi_todo;"

# Generate and apply migrations
py -m alembic revision --autogenerate -m "create users and tasks tables"
py -m alembic upgrade head
```

## Running

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Testing

```bash
pytest
```

Tests use SQLite in-memory — no PostgreSQL required.

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login, returns JWT |
| GET | `/users/me` | Yes | Get current user |
| GET | `/tasks` | Yes | List your tasks |
| POST | `/tasks` | Yes | Create a task |
| GET | `/tasks/{id}` | Yes | Get a task |
| PUT | `/tasks/{id}` | Yes | Update a task |
| DELETE | `/tasks/{id}` | Yes | Delete a task |

## Project Structure

```
app/
├── auth/        # Login, register, JWT logic
├── users/       # User model and profile endpoint
├── tasks/       # Task CRUD endpoints
├── database.py  # SQLAlchemy engine and session
├── dependencies.py  # Shared dependencies (get_db, get_current_user)
└── main.py      # App entry point, router registration
```
