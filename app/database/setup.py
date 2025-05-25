from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy.exc import SQLAlchemyError
import time

from app.core.config import DATABASE_URL

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to create engine with retry logic
def create_db_engine(url, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            logger.info(f"Attempting to connect to database (attempt {retries + 1}/{max_retries})")
            engine = create_engine(
                url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 10}
            )
            # Test the connection
            connection = engine.connect()
            connection.close()
            logger.info("Database connection established successfully")
            return engine
        except SQLAlchemyError as e:
            retries += 1
            logger.error(f"Database connection failed: {str(e)}")
            if retries < max_retries:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logger.critical("Failed to connect to database after maximum retries")
                raise

# Create engine with retry logic
engine = create_db_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()