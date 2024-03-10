import time
from os import path
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.common import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException, \
    NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()

FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL')
FACEBOOK_PASS = os.getenv('FACEBOOK_PASS')

chromiumPath = path.join("C:\\", "Dev", "chromedriver.exe")
print(chromiumPath)
service = Service(executable_path=chromiumPath)
driver = Chrome(service=service)

driver.get("https://tinder.com/app/recs")

main_handle = driver.current_window_handle

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '//*[text()="I accept"]')))
driver.find_element(By.XPATH, '//*[text()="I accept"]').click()
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Log in"]')))
driver.find_element(By.XPATH, '//*[text()="Log in"]').click()
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Login with Facebook"]')))
driver.find_element(By.XPATH, '//*[text()="Login with Facebook"]').click()

login_handle = None
while not login_handle:
    handles_list = driver.window_handles
    for handle in handles_list:
        if handle != main_handle:
            login_handle = handle

driver.switch_to.window(login_handle)
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,  '//*[text()="Decline optional cookies"]')))
driver.find_element(By.XPATH,  '//*[text()="Decline optional cookies"]').click()
driver.find_element(By.NAME, 'email').send_keys(FACEBOOK_EMAIL)
driver.find_element(By.NAME, 'pass').send_keys(FACEBOOK_PASS)
driver.find_element(By.ID, 'loginbutton').click()

driver.switch_to.window(main_handle)

WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,  '//*[text()="Allow"]')))
driver.find_element(By.XPATH, '//*[text()="Allow"]').click()
WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,  '//*[text()="Not interested"]')))
driver.find_element(By.XPATH, '//*[text()="Not interested"]').click()


selected_buttons = []

while True:
    try:
        selected_buttons = driver.find_elements(By.TAG_NAME, 'button')
        for i in selected_buttons:
            if i.text == "LIKE":
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
