# FastAPI Todo API

This is a **learning project** for a JavaScript developer practicing Python.

## Context
The developer is experienced with JavaScript (Next.js, Node.js) and is using this project
to learn Python and FastAPI patterns. When helping with this project:

- Compare Python patterns to JavaScript equivalents where helpful:
  - FastAPI routers ≈ Express routers
  - Pydantic schemas ≈ Zod / TypeScript interfaces
  - SQLAlchemy models ≈ Prisma/Mongoose models
  - `yield` in `get_db` ≈ try/finally in middleware
  - FastAPI `Depends()` ≈ Express middleware / NestJS decorators
- Explain Python-specific concepts explicitly — do not assume familiarity with
  type hints, decorators, generators, or Pydantic
- Favor clarity over brevity in code explanations

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM + Alembic migrations)
- **Auth:** JWT (python-jose + passlib[bcrypt])
- **Tests:** pytest + FastAPI TestClient (SQLite in-memory)

## Running the project
```bash
# Install dependencies
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env

# Start the dev server
uvicorn app.main:app --reload

# Run tests
pytest
```
