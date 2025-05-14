from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

load_dotenv()


def get_engine(db_name: str) -> Engine:
    DB_HOST = getenv("DB_HOST")
    DB_NAME = db_name
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")

    engine = create_engine(
        f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/"
        f"{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    return engine
