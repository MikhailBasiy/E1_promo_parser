from datetime import date

import pandas as pd

from get_db_prices import get_db_prices
from get_site_prices import get_site_prices


def compare_prices(data: pd.DataFrame) -> pd.DataFrame:
    data["Цена БД со скидкой"] = data["Sum-База_РРЦ"] * (1 - data["Скидка"] / 100)
    data["Цены_равны"] = data["Цена"] == data["Цена БД со скидкой"]
    return data


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


def main():
    get_site_prices()
    # db_prices: pd.DataFrame = get_db_prices()
    # db_prices.to_excel("db_prices.xlsx", engine="xlsxwriter", index=False)

    # joined_prices = join_tables(site_prices, db_prices)
    # joined_prices_compared = compare_prices(joined_prices)

    # joined_prices.to_excel("result.xlsx", index=False, engine="xlsxwriter")
    # joined_prices_compared.to_excel(
    #     "joined_prices_compared.xlsx", index=False, engine="xlsxwriter"
    # )


if __name__ == "__main__":
    main()
