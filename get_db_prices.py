import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from dotenv import load_dotenv
from os import getenv


def get_engine() -> Engine: 
    load_dotenv()
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    engine = create_engine(
        f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/" \
        f"{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    return engine


def get_db_prices() -> pd.DataFrame:
    query = "SELECT * FROM [Результат_Стоимость_шкафов_CSKU_С промо] " \
        "WHERE [Серия]=N'Экспресс' " \
        "AND [Цвет профиля]=N'Серебро' " \
        "AND [Вариант исполнения шкафа] IN (N'Белый снег', N'Бетон');"
    
    engine = get_engine()
    
    with engine.connect() as con:
        return pd.read_sql(query, con)




