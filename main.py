from datetime import date

import pandas as pd

from get_db_prices import get_db_prices
from get_site_prices import update_promo_prices_in_db
from compare_prices import compare_prices
from get_site_promo_prices import get_site_promo_prices


def main():
    update_promo_prices_in_db()
    site_prices = get_site_promo_prices()
    db_prices: pd.DataFrame = get_db_prices()
    # db_prices.to_excel("db_prices.xlsx", engine="xlsxwriter", index=False)

    # joined_prices = join_tables(site_prices, db_prices)
    compared_prices = compare_prices(site_prices, db_prices)
    
    compared_prices.to_excel(
        "compared_prices.xlsx", index=False, engine="xlsxwriter"
    )


if __name__ == "__main__":
    main()
