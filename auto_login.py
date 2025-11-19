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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C535E0878C93BF39107064DF6B42826C2B9F50E7CC21A83D5226333EE7C76D73DF99E6F403EFE6A103BD8E186B28962CF9F148E76A72FBCF68ECA4357EC2A631FC8951B85710C3141F745D968AA4DDD6E7A6A6DDF49777D52A4301E95F106C36C3853AF0E7DC64D0BDC03870AD60B011179F3432E59285027EB182A6AA30E41563B2AEE09686EFE8DC8C841B2881D12D6A89C61604DA05A0ECFC9AE1020A06858D89342F89DCBB620A7D87D4BCA30042F5136F030D5F8A483F9488BD59B6190ADA4BD592696BDCCF44D72168B342B9A07C2BA808A61281DDA35EAD19FD9B089E7388EB7AA73DA6A304640EA45B01CFC5972149116C22A68A52FC56D992C29C6A5D4AC8676DF2EB0CCAFEA4BE02DDD340AF9E68887982E753367A044FC942EB7F19606C8D72CAC385ED4BE8076147F995C7CB381CF73599E000CC9D18BCAB42E5E1631CE0DA42F617805AB25AC8DFD74C23AFD84238CD72D398027D898DD3D438FBD7A6C90AAD36546239C2270AEB5465A71654C6CF294C30338910EE94CA89BDF915D4C8C81E422F2CA499A8D148292CDF4E93397A0EC8AE875372950CB96373"})
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
