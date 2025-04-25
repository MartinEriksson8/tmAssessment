# Bookmark Manager API

A simple API to manage bookmarks. Users can create accounts and manage their own bookmarks.

## What's in it

- FastAPI backend 
- User authentication 
- CRUD operations for bookmarks 
- SQLite database (with PostgreSQL support ready)
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

For SQLite (default):
```bash
DATABASE_URL=sqlite:///./data/app.db
```

For PostgreSQL:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/bookmark_db
```

Additional configuration options:
```bash
SECRET_KEY=your-secret-key-here  # For JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30   # Token expiration time
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Database Setup

### SQLite (Default)
The application uses SQLite by default. No additional setup is required.

### PostgreSQL
To use PostgreSQL:

1. Install PostgreSQL on your system
2. Create a database:
```bash
createdb bookmark_db
```

3. Update the `.env` file with your PostgreSQL connection string:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/bookmark_db
```

4. Install additional dependencies:
```bash
pip install psycopg2-binary
```

5. Restart the application

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
- `data/` - Database files (SQLite)
- `tests/` - Test files

f