import time

import os
from dotenv import load_dotenv

from selenium.common import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException, \
    NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL')
FACEBOOK_PASS = os.getenv('FACEBOOK_PASS')

# Constants
URL = "https://bumble.com/app"
CHROMIUM_PATH = "C://Dev/chromedriver.exe"

# Driver set up
service = Service(CHROMIUM_PATH)
driver = Chrome(service=service)

driver.get(url=URL)

# Setting what the main handle is - useful when any pop-up pops up
main_handle = driver.current_window_handle

time.sleep(5)

# Loging in

# Accepting Cookies
driver.switch_to.frame(driver.find_element(By.ID, "sp_message_iframe_971214"))
all_els = driver.find_elements(By.XPATH, '//*')

WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Accept All"]')))
driver.find_element(By.XPATH, '//*[text()="Accept All"]').click()

# Continuing with Facebook
driver.switch_to.window(main_handle)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Continue with Facebook"]')))
driver.find_element(By.XPATH, '//*[text()="Continue with Facebook"]').click()

# Creating new handle for login pop-up window
login_handle = None
while not login_handle:
    handles_list = driver.window_handles
    for handle in handles_list:
        if handle != main_handle:
            login_handle = handle

driver.switch_to.window(login_handle)
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,  '//*[text()="Decline optional cookies"]')))
driver.find_element(By.XPATH, '//*[text()="Decline optional cookies"]').click()

# Loging in with Facebook
driver.find_element(By.NAME, 'email').send_keys(FACEBOOK_EMAIL)
driver.find_element(By.NAME, 'pass').send_keys(FACEBOOK_PASS)
driver.find_element(By.ID, 'loginbutton').click()

# End of Loging with Facebook, back to the main handle and await login completion

driver.switch_to.window(main_handle)

# Main Loop

selected_buttons = []

while True:
    try:
        selected_buttons = driver.find_elements(By.TAG_NAME, 'span')

        for i in selected_buttons:
            if i.get_attribute("data-qa-icon-name") == "floating-action-yes":
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(i))
                i.click()
    except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException):
        try:
            driver.find_element(By.XPATH, '//*[text()="Not interested"]').click()
        except (NoSuchElementException, ElementClickInterceptedException):
            try:
                driver.find_element(By.XPATH, '//*[text()="No Thanks"]').click()
            except (NoSuchElementException, ElementClickInterceptedException):
                pass
            finally:
                time.sleep(1)
    finally:
        time.sleep(1)
