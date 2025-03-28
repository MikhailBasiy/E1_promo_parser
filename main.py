import pandas as pd
from get_site_prices import get_site_prices
from get_db_prices import get_db_prices


def prepare_site_data(site_prices: pd.DataFrame) -> pd.DataFrame:
    site_prices["Название_карточки"] = site_prices["Название_карточки"].str.replace("Шкаф-купе ", "", )
    site_prices[""]


def main():
    site_prices: pd.DataFrame = get_site_prices()
    # site_prices = pd.read_excel("output.xlsx")
    db_prices: pd.DataFrame = get_db_prices()

    # site_prices.to_excel("site_prices.xlsx", engine="xlsxwriter", index=False)
    # db_prices.to_excel("db_prices.xlsx", engine="xlsxwriter", index=False)

    result = site_prices.merge(
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

    result.to_excel("result.xlsx", index=False, engine="xlsxwriter")



if __name__ == "__main__":
    main()