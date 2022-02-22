#%%

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#import time

#%%


username = 'pie_au'
content = 'Snowflake WM/R FX rates implementation'
title = username + ' - ' + content

machine_sn = '1129032'
notes = 'Implementation for fx rates from WM/R in snowflake'


#%%

driver = webdriver.Chrome()
driver.get("https://rpd.factset.io/create")

#%%


WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[6]/div[2]/property/div/button[1]/span'))).click() # Question

driver.find_element_by_xpath('//*[@id="createTemplate"]/div[8]/div[2]/property/div/button[2]/span').click() # Medium

driver.find_element_by_xpath('//*[@id="createTemplate"]/div[1]/div[2]/input').send_keys(title) # write title

driver.find_element_by_xpath('//*[@id="createTemplate"]/div[2]/div[2]/ui-productsuggest/input').send_keys('standard implementation') # search category

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='createTemplate']/div[2]/div[2]/ui-productsuggest/div/table/tbody/tr[1]/td[1]/span"))).click() # select category



    # # explicit frame id
    # frame = driver.find_element_by_xpath('//iframe [@id]').get_attribute('id')
    # WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id='{}']".format(frame)))) # switch iframe


# implicit frame id
WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id]"))) # switch iframe
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tinymce"]'))).send_keys('Machine SN: {}\nNotes: {}'.format(machine_sn,notes)) # typing content

driver.switch_to.default_content() # get out of iframe


#%%

#file it
driver.find_element_by_xpath('//*[@id="createTemplate"]/div[19]/div[2]/button[1]/span').click() # file RPD





#%%

#add me to the RPD
driver.find_element_by_xpath('//*[@id="addMeButton"]').click()

#extract rpd number
driver.find_element_by_xpath('//*[@id="summaryContent"]/div[1]/div[1]/table/tbody/tr/td[1]/a').get_attribute('href')


# %%

# Adding a client

# driver.find_element_by_xpath('//*[@id="mat-select-2"]/div/div[1]/span/span').click()
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="mat-option-16"]/span').click()


# %%





# %%
