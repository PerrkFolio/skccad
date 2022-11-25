import json
import logging
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from multiprocessing import Pool
from functions import strConvertion, validation, other


def get_p2p_okx(crypto):
    logger = init_logger("OKX", crypto)
    logger.info(f"Start parsing {crypto}...")

    if crypto == 'btc':
        volume = 0.1
        logger.info(f"The limit for buying and selling cryptocurrency is {volume}...")
    elif crypto == 'eth':
        volume = 1
        logger.info(f"The limit for buying and selling cryptocurrency is {volume}...")
    elif crypto == 'usdt':
        volume = 1000
        logger.info(f"The limit for buying and selling cryptocurrency is {volume}...")
    else:
        volume = 1
        logger.warning(f"It was not possible to determine the limit for the purchase and sale of cryptocurrency. "
                       f"Default limit set: {volume}...")
    deals_precent = 80


    all_pay_methods = ['Sberbank (СберБанка)', 'Tinkoff (Тинькофф)', 'Yandex Money', 'Cash in Person', 'Alfa Bank',
                       'QiWi', 'SBP Fast Bank Transfer', 'Raiffeisen Bank', 'VTB', 'Rosselhozbank', 'Pochta Bank',
                       'Ak Bars Bank', 'Uralsib Bank', 'Sovcombank', 'Otkritie', 'Bank Transfer', 'UniCredit Bank',
                       'Russian Standard Bank', 'Zain Cash', 'Fast Pay', 'AdvCash', 'Payoneer', 'Payeer', 'Wise',
                       'AI-Taif', 'Switch', 'Zen', 'AirTM', 'Revolut', 'Perfect Money', 'Skrill', 'Zelle', 'Neteller',
                       'Paysera', 'Abu Dhabi Commercial Bank', 'ADIB', 'Al Hilal Bank', 'Dubai Islamic Bank',
                       'Commercial Bank of Dubai', 'HSBC', 'Emirates NBD Bank', 'Mashreq Bank', 'Ziraat Bankası',
                       'BNP Paribas (TEB)', 'Fibabanka', 'Denizbank', 'Kuveyt Turk', 'Enpara', 'Yapı Kredi', 'Akbank',
                       'ING', 'QNB Finansbank', 'İş Bankası', 'Vakıflar Bankası', 'SEPA Instant', 'PayPal',
                       'Belarusbank', 'BPS Sberbank', 'MTBank' 'PriorBank', 'WebMoney']


    url = 'https://www.okx.com/ru/p2p-markets/rub/sell-' + crypto
    chromedriver_path = "/usr/local/bin/chromedriver"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(
        "user-agent=Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome "
        "/ 104.0.0.0 Safari / 537.36")

    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        driver.implicitly_wait(10)
        driver.get(url=url)
        logger.info("Selenium launched the browser...")
    except Exception as e:
        logger.error("Selenium FAILED to launch browser!")
        logger.exception(e)


    try:
        result = []
        json_result = []
        all_fiat = {
            0: "rub",
            1: "usd",
            2: "eur",
            3: "chf",
            4: "try",
            5: "aed",
            6: "byn"
        }
        counter = 1
        queue = 0
        logger.info("The required parameters are initialized. Data parsing begins...")
        while True:
            try:
                if queue == 7:
                    try:
                        save_json(crypto, json_result)
                        logger.info("The new JSON data is written to the file...")
                    except Exception as e:
                        logger.exception(e)
                    json_result = []
                    queue = 0
                url = 'https://www.okx.com/ru/p2p-markets/' + all_fiat[queue] + '/sell-' + crypto
                new_window = f'window.open("{url}")'
                driver.execute_script(new_window)
                driver.switch_to.window(driver.window_handles[1])

                fiat_list = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/table/tbody")
                fiat_list = fiat_list.find_elements(By.TAG_NAME, "tr")
                for item in fiat_list:
                    item = item.text
                    params = item.split("\n")
                    precent = int(params[3][:params[3].find(".")])
                    limit = int(strConvertion.remove_letters_in_string(params[4]))
                    price = params[6].split(",")
                    price = strConvertion.price_adj(price[0], price[1])
                    pay_methods = [params[7]]
                    # if not params[8].find(crypto): pay_methods.append(params[8])
                    payments = other.get_payments_okx(pay_methods, all_pay_methods)
                    if limit > volume and precent > deals_precent:
                        if counter % 2 != 0:
                            result.append(price)
                            result.append(limit)
                            result.append(payments)

                            buy_btn = driver.find_element(By.XPATH,
                                                          "/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/a[1]")
                            buy_btn.click()
                            # time.sleep(random.randrange(1, 3))
                            counter += 1

                            logger.debug(f"Data [SELL] was collected successfully [{all_fiat[queue]}]...")
                            continue

                        if counter % 2 == 0:
                            result.append(price)
                            result.append(limit)
                            result.append(payments)
                            result.append(crypto.upper())
                            result.append(all_fiat[queue].upper())
                            json_result.append(result)
                            result = []
                            logger.debug(f"Data [BUY] was collected successfully [{all_fiat[queue]}]...")
                            counter += 1
                            queue += 1
                            break

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                counter = 1
                queue = 0
                result = []
                json_result = []
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                logger.warning("An error has occurred in the data writing sequence. The queue has been reloaded.")
                logger.exception(e)
                continue

    except Exception as e:
        logger.exception(e)
    finally:
        driver.close()
        driver.quit()
        logger.critical("Program execution has been stopped!")


def save_json(crypto, result):
    json_result = other.list_to_json(result)
    path = 'json/okx_' + crypto + '.json'
    with open(path, 'w') as outfile:
        json.dump(json_result, outfile)


def init_logger(exchanger, name):
    path_logs = 'logs/'+exchanger+'-'+name+'.log'
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s :: %(name)s:%(lineno)s :: %(levelname)s :: %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename=path_logs)
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug("Logger was initialized.")
    return logger


# get_p2p_okx("btc")

if __name__ == '__main__':
    iterable = ['usdt', 'btc', 'eth']
    pool = Pool(processes=3)
    pool.map(get_p2p_okx, iterable)

