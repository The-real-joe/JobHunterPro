from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime
from sqlalchemy.pool import NullPool

# Get database URL from environment
DATABASE_URL = os.getenv('postgresql://neondb_owner:npg_WmoJrxhRN1B3@ep-white-tooth-a564vxoz.us-east-2.aws.neon.tech/neondb?sslmode=require')

# Ensure DATABASE_URL is set
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create database engine with SSL parameters and connection pooling disabled
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 30
    },
    poolclass=NullPool  # Disable connection pooling to prevent SSL timeout issues
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    salary_range = Column(String(100))
    description = Column(Text)
    requirements = Column(Text)
    posted_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="Open")

    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))
    notes = Column(Text)

    job = relationship("Job", back_populates="applications")

# Create database dependency
def get_db():
    db = SessionLocal()
    try:
        # Test the connection using proper SQLAlchemy text formatting
        db.execute(text("SELECT 1"))
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

# Create all tables
Base.metadata.create_all(bind=engine)