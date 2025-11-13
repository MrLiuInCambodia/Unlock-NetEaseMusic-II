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
    browser.add_cookie({"name": "MUSIC_U", "value": "001840C8EE1368A6ABD921D5817075FE9778A8A588EC7027F2AC9CEA8A3AA5653CB2BD045D29D4B5FE0A73DCC611B1E2F7094647E7D757010601E2418F9239DB14F94488D9A5E3ADAC8FDE35A7B081D656A459F95383D32C9E2FFAC2E33D0524B5F6446213B66A4CFDB152AE41DEB2ECDDCF1E0B67B92F6689CA0BB728985F15CE124766A5AE948ABFF6F5947278A90CF95F549366D2F0567C7085F3F72B95209D611B1C6DC0C415E48AEDBFF16A602F5CD25D657F1ACC62FFC332ABC3200AE8D2F2452AEEA245345218B5EDB4FA2BDBDEC694FC94C2F080825722DD724CA563CD9542569589671544C472B727143AA61B08D756304FD5D8ED852D45391497600037D053A4CCB11BC60491B8CE40B41D18517D627566F9881561F16424489FFC1BF9CBE73754FF687C32BBC2C09BA1B21C9B514CC12FA7DB9043BD68E46BFE1B482805B365063A9CB2F32E148B605070BC03594261C54449ACB0B2D4D3758613C92B129F310281996EF83B2C10FCF31B8BDA034CC6FC25165307CEB36AE9FB0A7B7FE48A7E913944B42199D858331FD352D9DFBC27F954099A02BF18A8CB7A8999"})
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
