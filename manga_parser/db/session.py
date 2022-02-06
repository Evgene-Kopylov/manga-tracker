import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

db_url = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER", 'postgres'),
    os.environ.get("POSTGRES_PASSWORD", 'postgres'),
    os.environ.get("POSTGRES_SERVER", 'localhost'),
    os.environ.get("POSTGRES_PORT", '5432'),
    os.environ.get("POSTGRES_DB", 'demo_db'),
)

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
