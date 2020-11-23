#%%

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# This is to handle waiting for data to load while loading website
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pyperclip #login
import random #function to randomly select temperature

#%%

browser = webdriver.Chrome()
url = 'https://forms.office.com/Pages/ResponsePage.aspx?id=44eb_0jFPUuHgnz0e4bAV65UHqQ6ktFBh9hsUi-g1BxUQTBKTllUMDEwTVVMTk5IVzg4OUNYUEFBUi4u'

email = 'rochan@factset.com'



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


# %%

temperature_list = [36.5, 36.6, 36.7, 36.8, 36.9, 37]
temperature = str(random.choice(temperature_list))
temperature


#%%

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/input')))
finally:
  # input temperature
  browser.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/input').send_keys(temperature)
  # select "no"
  browser.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/div/label/input').click()
  # click "submit"
  browser.find_element_by_xpath('//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div').click()

#%%

