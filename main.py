from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome("./chromedriver.exe")

url = "https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"

driver.get(url)

driver.find_element(By.NAME, "usr_id").send_keys("2019182003")
driver.find_element(By.NAME, "usr_pwd").send_keys("3183129")
driver.find_element(By.ID, "login_btn").click()

time.sleep(3)
