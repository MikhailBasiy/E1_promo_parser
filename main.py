import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from time import sleep
from icecream import ic


scraping_settings = {
    # "max_attempts": 4,
    # "load_time": 7,
    "XPATH": '//div[@class="prices-wrapper"]/div/span/span[@class="price_value"]', 
    "unavailable_txts": ["Страница не найдена"],
    # "cookies": [
    #     {"name": "current_region", "value": "3513", 'domain': '.e-1.ru', 'secure': False, 'httpOnly': False}
    # ]
}


def write_to_excel(data: list[list[str | int]]) -> None:
    df = pd.DataFrame(data, columns=["url", "price"])
    df.to_excel("prices.xlsx", engine="xlsxwriter", index=False)
    return


def normalize_price(price: str) -> float:
    price = price \
        .replace("\u2009", "") \
        .replace("₽", "") \
        .replace(" ", "") \
        .replace("руб.", "") \
        .replace("р", "")
    return float(price)


def parse_price(drv: webdriver, url: str, num_try=3):
    if num_try:
        try:
            price = drv.find_element(By.XPATH, scraping_settings["XPATH"]).text
        except (NoSuchElementException, StaleElementReferenceException) as e:
            ic(url, e)
            sleep(5)
            parse_price(drv, url, num_try-1)
        else:
            return price
    else:
        return "Цена не обнаружена"


def check_page(drv: webdriver) -> bool:
    unavailable_txts = scraping_settings["unavailable_txts"]
    page = drv.find_element(By.XPATH, "/html/body").text
    if any(txt in page for txt in unavailable_txts):
        return False
    return True


def init_webdriver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--blink-settings=imagesEnabled=false')
    return webdriver.Chrome(options=options)


def main():
    result: list[list[str | int]] = []
    urls = pd.read_excel("urls.xlsx", sheet_name="urls_list")["urls"]
    drv = init_webdriver()
    for url in urls:
        ic(url)
        drv.get(url)
        if check_page(drv) is False:
            result.append([url, "Страница не найдена"])
            continue
        price = parse_price(drv, url)
        result.append([url, price])
    write_to_excel(result)

            

if __name__ == "__main__":
    main()