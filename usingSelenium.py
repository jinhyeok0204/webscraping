from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 

driver.implicitly_wait(10)

driver.get("https://naver.com")
elem = driver.find_element(By.CLASS_NAME, "link_login")
elem.click()
driver.back()

elem = driver.find_element(By.ID, "query")
elem.send_keys("나도코딩")
elem.send_keys(Keys.ENTER)
