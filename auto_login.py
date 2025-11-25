# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00DEF42A2A0B719DE9EBE5561B5973C84F9A6776D4768FB2A226C5BF7AD6F456ABA33EAF1DED847298A4CB94ED984C52D939E686ACA210B3C3C4FE03FEA4E8D0E7A2782E0910874098988DEC564C32E3B8B56364DD56F796DEB403A99FBE5F017552F228660488EF150FD3035CBC64E837BC16481389E9133340CF7A878108D9810F1D2478D878B408AD41B873D867D753B6C54485C238625477E4862AB0E9C3F31F671435101332E8ADD0F573B962A11FF6F33443503369BF7DAB7D8DC6CB9C095FBE44BD85C436DBE2AF152655796BD9D13304FBF153159C097FEB6C1CA828988F38CE8B9EBA5E0A4CF681EC5A36257E97E4A4761F2C84AC911746F1570B97C93DC384E18541A64985DEB6A7C097972EED3CC9B30FEA3B10E21EBDD8127B7FF1AEF38EB3F5F91FE309BCEEBB52AB47AB7D51A8F9C691B3294014AE578D526CC7B8B6B641C6CEFD8B6475714B9765EFDB52F67838885E43A5654B7C366967F4AFE39C5B0AED60CB057C7381EC39567D1DAE051CDAD26685E070B0F6DD68BCC2045E0DB37E9F5496A8C259E3086E98AE444BD6F607A659AB02ED323B351A8A8B23"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
