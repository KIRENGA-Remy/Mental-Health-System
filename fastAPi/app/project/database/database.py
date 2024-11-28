from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:remy2020@localhost:5432/fastapi_mentalhealth"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.target_metadata = Base.metadata

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
