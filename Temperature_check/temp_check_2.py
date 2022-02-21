#%%

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# This is to handle waiting for data to load while loading website
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pyperclip #login


#%%

browser = webdriver.Chrome()
url = 'https://forms.office.com/Pages/ResponsePage.aspx?id=44eb_0jFPUuHgnz0e4bAV65UHqQ6ktFBh9hsUi-g1BxUQUpBVTZHUFkwQURLNkhZWjA1RURESlZaRy4u'

email = 'mpark@factset.com'
passs = '0001Quang'


# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# browser = webdriver.Chrome(chrome_options=options)

browser.get(url)

#%%

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'i0116')))
finally:
  pyperclip.copy(email)
  browser.find_element_by_id('i0116').send_keys(Keys.CONTROL, 'v')
  browser.find_element_by_id('idSIButton9').click()


#%%

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'passwordInput')))
finally:
  pyperclip.copy(passs)
  browser.find_element_by_id('passwordInput').send_keys(Keys.CONTROL, 'v')
  browser.find_element_by_id('submitButton').click()


#%%

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'o-form-button-bar')))
finally:
  browser.find_element_by_class_name('o-form-button-bar').click()


#%%

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/label/input')))
finally:
  browser.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/label/input').click()
  time.sleep(1)
  browser.find_element_by_xpath('//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/label/input').click()
  time.sleep(1)
  browser.find_element_by_class_name('button-content').click()



# %%
