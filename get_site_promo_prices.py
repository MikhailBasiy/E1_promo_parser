from db_engine import get_engine
import pandas as pd


def get_site_promo_prices() -> None:
    engine = get_engine("E-COM")
    with engine.connect() as con:
        return pd.read_sql("Результат_Стоимость_шкафов_с_промо_Сайт", con=con)