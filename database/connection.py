from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection URL (Currently using local SQLite for development/testing)
DATABASE_URL = "sqlite:///./document_for_all.db"

# Create the SQLAlchemy database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """Dependency function to manage database session lifecycle safely."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

