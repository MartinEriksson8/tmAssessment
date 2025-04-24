from app.database import engine, Base

def test_database_connection():
    try:
        # This will create the database file if it doesn't exist
        Base.metadata.create_all(bind=engine)
        print("Database connection successful!")
        print("SQLite database file 'bookmarks.db' has been created.")
    except Exception as e:
        print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    test_database_connection() 