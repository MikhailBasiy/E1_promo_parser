import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from time import sleep
from icecream import ic


scraping_settings = {
    "XPATH": '//div[@class="prices-wrapper"]/div/span/span[@class="price_value"]', 
    "unavailable_txts": ["Страница не найдена"],
    # "cookies": [
    #     {"name": "current_region", "value": "3513", 'domain': '.e-1.ru', 'secure': False, 'httpOnly': False}
    # ]
}


def normalize_price(price: str) -> int:
    price = price \
        .replace("₽", "") \
        .replace(" ", "") \
        .replace("руб.", "")
    return int(price)


def parse_price(drv: webdriver, url: str, num_try=3, wait=4):
    if num_try:
        try:
            price = WebDriverWait(drv, 8).until(EC.visibility_of_element_located((By.XPATH, scraping_settings["XPATH"]))).text
        except (NoSuchElementException, StaleElementReferenceException) as e:
            ic(url, e)
            parse_price(drv, url, num_try-1, wait+2)
        else:
            return price
    else:
        return "Цена не обнаружена"


def check_page(drv: webdriver) -> bool:
    unavailable_txts = scraping_settings["unavailable_txts"]
    page = WebDriverWait(drv, 8).until(EC.visibility_of_element_located((By.XPATH, "/html/body"))).text
    if any(txt in page for txt in unavailable_txts):
        return False
    return True


def init_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'none'
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--blink-settings=imagesEnabled=false')
    drv = webdriver.Chrome(options=options)
    return drv


def main():
    wardrobes = pd.read_excel("urls.xlsx", sheet_name="urls_list")
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
    ic(wardrobes)
    wardrobes.to_excel("output.xlsx", engine="xlsxwriter", index=False)
       

if __name__ == "__main__":
    main()