import pandas as pd


def join_tables(site_prices: pd.DataFrame, db_prices: pd.DataFrame) -> pd.DataFrame:
    joined_tables = site_prices.merge(
        db_prices,
        how="left",
        left_on=[
            "Название_карточки",
            "Ширина",
            "Высота",
            "Глубина",
            "Цвет_корпуса",
            "Цвет_профиля",
            "Компоновка",
        ],
        right_on=[
            "Наименование шкафа на сайте",
            "Ширина",
            "Высота",
            "Глубина",
            "Вариант исполнения шкафа",
            "Цвет профиля",
            "Компановка корпуса",
        ],
        suffixes=("_сайт", "_БД"),
    )
    return joined_tables


def compare_prices(site_prices: pd.DataFrame, db_prices: pd.DataFrame) -> pd.DataFrame:
    data = join_tables(site_prices, db_prices)
    data["Цена БД со скидкой"] = data["Sum-База_РРЦ"] * (1 - data["Скидка"] / 100)
    data["Цены_равны"] = data["Цена"] == data["Цена БД со скидкой"]
    return data
