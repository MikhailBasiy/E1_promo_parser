import pandas as pd
from get_site_prices import get_site_prices
from get_db_prices import get_db_prices


def compare_prices(data: pd.DataFrame) -> pd.DataFrame:
    data["Цена БД со скидкой"] = data["Sum-База_РРЦ"] * (1 - data["Скидка"] / 100)
    data["Цены_равны"] = data["Цена"] == data["Цена БД со скидкой"]
    return data


def prepare_site_data(site_prices: pd.DataFrame) -> pd.DataFrame:
    site_prices["Название_карточки"] = site_prices["Название_карточки"] \
        .str.replace("Шкаф-купе ", "", )
    site_prices["Цвет_профиля"] = site_prices["Цвет_профиля"] \
        .str.replace(" профиль", "")
    return site_prices


def join_tables(
        site_prices:pd.DataFrame, 
        db_prices: pd.DataFrame
    ) -> pd.DataFrame:
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
            "Компоновка"
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
        suffixes=('_сайт', '_БД')
    )
    return joined_tables


def main():
    site_prices: pd.DataFrame = prepare_site_data(get_site_prices())
    # site_prices = prepare_site_data(pd.read_excel("site_prices.xlsx"))       #TODO: on prod replace with the row above
    site_prices.to_excel("site_prices.xlsx", engine="xlsxwriter", index=False)

    db_prices: pd.DataFrame = get_db_prices()
    db_prices.to_excel("db_prices.xlsx", engine="xlsxwriter", index=False)

    joined_prices = join_tables(site_prices, db_prices)
    joined_prices_compared = compare_prices(joined_prices)

    joined_prices.to_excel("result.xlsx", index=False, engine="xlsxwriter")
    joined_prices_compared.to_excel("joined_prices_compared.xlsx", index=False, engine="xlsxwriter")


if __name__ == "__main__":
    main()