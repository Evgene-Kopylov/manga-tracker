import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

db_url = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER"),
    os.environ.get("POSTGRES_PASSWORD"),
    os.environ.get("POSTGRES_SERVER", 'localhost'),
    os.environ.get("POSTGRES_PORT", '5432'),
    os.environ.get("POSTGRES_DB"),
)
