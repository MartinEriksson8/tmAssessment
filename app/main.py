from fastapi import FastAPI
from app.api import users
from app.database import engine
from app.models import user

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Bookmark Manager API"}
