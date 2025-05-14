import re
from time import sleep

import pandas as pd
from icecream import ic
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import NVARCHAR, Integer

from db_engine import get_engine

from config.logging_settings import get_logger

logger = get_logger(__name__)

scraping_settings = {
    "XPATH": '//div[@class="prices-wrapper"]/div/span/span[@class="price_value"]',
    "unavailable_txts": ["Страница не найдена"],
    # "cookies": [
    #     {"name": "current_region", "value": "3513", 'domain': '.e-1.ru', 'secure': False, 'httpOnly': False}
    # ]
}


def write_to_db(data: pd.DataFrame) -> None:
    column_types = {
        "Название_карточки": NVARCHAR(255),
        "Ширина": Integer(),
        "Высота": Integer(),
        "Глубина": Integer(),
        "Цвет_корпуса": NVARCHAR(255),
        "Цвет_профиля": NVARCHAR(255),
        "Компоновка": NVARCHAR(255),
        "URL": NVARCHAR(500),
        "Цена": Integer(),
    }
    engine = get_engine("E-COM")
    with engine.connect() as con:
        data.to_sql(
            "Результат_Стоимость_шкафов_с_промо_Сайт",
            con=con,
            dtype=column_types,
            index=False,
            if_exists="replace",
        )
    logger.info(f"Writing to db finished. Successfully loaded {len(data)} rows.")


def normalize_price(price: str) -> int | str:
    if price:
        price = re.sub(r"[\D]", "", price)
        return int(price)
    else:
        return "Ошибка парсинга цены"


def parse_price(drv: webdriver, url: str, num_try=3, wait=8) -> str:
    if num_try:
        try:
            price = (
                WebDriverWait(drv, wait)
                .until(
                    EC.visibility_of_element_located(
                        (By.XPATH, scraping_settings["XPATH"])
                    )
                )
                .text
            )
        except (
            NoSuchElementException,
            StaleElementReferenceException,
            WebDriverException,
            TimeoutException,
        ) as e:
            logger.info(f"При парсинге цены на странице {url} возникла ошибка: {e}")
            sleep(4)
            parse_price(drv, url, num_try=num_try-1, wait=wait+4)
        else:
            return price
    else:
        return ""


def check_page(drv: webdriver) -> bool:
    unavailable_txts = scraping_settings["unavailable_txts"]
    try:
        page = (
            WebDriverWait(drv, 1)
            .until(EC.visibility_of_element_located((By.XPATH, "/html/body")))
            .text
        )
    except (TimeoutError, WebDriverException):
        return True
    if any(txt in page for txt in unavailable_txts):
        return False
    return True


def init_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "none"
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless=new")
    options.add_argument("log-level=3")
    # options.add_argument('--disable-gpu')     ### for docker container
    drv = webdriver.Chrome(options=options)
    logger.info("Webdriver initiated successfully")
    return drv


def get_db_wardrobes() -> pd.DataFrame:
    engine = get_engine("E-COM")
    with engine.connect() as con:
        wardrobes = pd.read_sql("Список_шкафов_для_сверки_цен_с_промо", con=con)
    logger.info(f"Wardrobes loaded successfully. Rows count: {len(wardrobes)}")
    return wardrobes


def update_promo_prices_in_db():
    wardrobes = get_db_wardrobes()
    # wardrobes = pd.read_excel("urls.xlsx", sheet_name="urls_list")
    drv = init_webdriver()
    for idx, wardrobe in wardrobes.iterrows():
        url = wardrobe.URL
        ic(url)
        drv.get(url)
        if check_page(drv) is False:
            wardrobes.loc[idx, "Цена"] = "Страница не найдена"
            ic(price)
            continue
        price = normalize_price(parse_price(drv, url))
        ic(price)
        wardrobes.loc[idx, "Цена"] = price
    drv.quit()
    write_to_db(wardrobes)
    return
