from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import db_url

engine = create_engine(db_url)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
