# Bookmark Manager API

A simple API to manage bookmarks. Users can create accounts and manage their own bookmarks.

## What's in it

- FastAPI backend - Under construction
- User authentication - Under construction
- CRUD operations for bookmarks - Under construction
- SQLite database (with PostgreSQL support ready) - Under construction
- Docker and Kubernetes support - Under construction

## Setup

1. Create a virtual environment:
```bash
python -m venv tmAssessment
source tmAssessment/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the project root with the following content:
```bash
DATABASE_URL=sqlite:///./data/app.db
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can find the interactive API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

- Python 3.12.3
- FastAPI
- SQLAlchemy
- Pydantic
- pytest (for testing)

## Project Structure

- `app/` - Main application code
  - `api/` - API endpoints
  - `models/` - Database models
  - `schemas/` - Pydantic models
  - `config.py` - Configuration and environment variables
  - `database.py` - Database connection and session management
- `data/` - Database files
- `tests/` - Test files

