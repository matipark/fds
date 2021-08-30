#%%

### Input parameters

# Required items to be filtered
required_items = ('FF_ENTRPR_VAL_SALES','FF_EBIT_OPER_INT_COVG','FF_WKCAP_PCT','FF_RECEIV_TURN','FF_RECEIV_TURN_DAYS','FF_PAY_TURN_DAYS')

# Leave empty if you want to search/input manually
qnt = 'HANKYUNG_QNT'
SerialNumber = ''

# Your e-mail and directory where your Chromedriver is saved
# You can download the Chromedriver from https://chromedriver.chromium.org/downloads
# You may check the version you need to download by going to your current chrome -> option -> help -> about Google Chrome

email = 'mpark@factset.com'
exec_chrome = 'C:\\Github_repo\\Notes\\FDS\\Temperature_check\\chromedriver.exe'



#%%

### Required libraries
# Selenium, pyperclip, tkinter, tqdm

# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# This is to handle waiting for data to load while loading website
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

import pyperclip #login

# Alert Message box
import tkinter
from tkinter import messagebox

# Sleep
import time

# Progress bar
from tqdm import tqdm

#%%

# Open executable chrome and login
browser = webdriver.Chrome(exec_chrome)
url = 'https://cts-sdf-support-portal.azurewebsites.net/'
browser.get(url)

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'i0116')))
finally:
  pyperclip.copy(email)
  browser.find_element_by_id('i0116').send_keys(Keys.CONTROL, 'v')
  browser.find_element_by_id('idSIButton9').click()

# Go to Create/Modify page

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'lnkFilteringTop')))
finally:
  browser.find_element_by_id('lnkFilteringTop').click()

# Check if QNT is available. If available, find the qnt account.

if bool(qnt) is False:
  pass
else:
  try:
    WebDriverWait(browser, 10).until(
      EC.visibility_of_element_located((By.ID, 'MainContent_btnReset')))
  finally:
    browser.find_element_by_xpath("//*[text()='{}']".format(qnt)).click()

# Check if Serial Number is available. If available, find the Serial Number.

if bool(SerialNumber) is False:
  pass
else:
  time.sleep(5)
  browser.find_element_by_xpath("//*[text()='{}']".format(SerialNumber)).click()

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'MainContent_rbRegular')))
finally:
  browser.find_element_by_id('MainContent_rbRegular').click()
  browser.find_element_by_id('MainContent_rbModifyExisting').click()


# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()

# Message Box - Reminder
### Manually select the Product, Packages and Regions

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'editor-table')))
finally:
  messagebox.showinfo(
    "check", "*** QNT: {} ***\n*** Please select the Product, Packages and Regions ***".format(qnt))

### Manually untick the bundle box

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'MainContent_treeBundlesNewt1')))
finally:
  messagebox.showinfo(
      "check", "*** QNT: {} ***\n*** Please untick the bundle box ***".format(qnt))


#%%

# Expanding all brakets
open_bracket = browser.find_elements_by_css_selector('[alt*="Expand"]')

for i in open_bracket:
  i.click()

#%%

# Builds FULL items dictionary (takes ~3 min to complete)
items_list = [] 

elem = browser.find_elements_by_class_name('MainContent_treeBundlesNew_0') #added New for a new filter setup

for i in tqdm(elem):
  field_name = i.get_attribute("innerHTML")
  field_id = i.get_attribute("id")
  item = {'field_name':field_name, 'field_id':field_id}
  items_list.append(item)


# %%

# Convert required items to lowercase
required_items = [x.lower() for x in required_items]

# Filter the items_list by required items
selected_items_code = []
selected_items_name = []
for i in items_list: 
    if i['field_name'] in required_items: 
        selected_items_code.append(i['field_id'])
        selected_items_name.append(i['field_name'])

# Check to make sure all the required items are recognized. If the number of items does not match, there will be an alert window
required_items_count = len(set(required_items))
selected_items_name_count = len(set(selected_items_name))

item_difference = set(selected_items_name).symmetric_difference(set(required_items))

if required_items_count == selected_items_name_count:
  pass
else:
  messagebox.showinfo(
    "check", "*** QNT: {} ***\n*** Number of required items does not match with the number of selected items ***\n*** Required items count: {} ***\n*** Selected items count: {} ***\n*** Item difference: {} ***".format(qnt,required_items_count,selected_items_name_count,item_difference))


#%%

# Data transformation to fit checkbox
selected_items_code = [w.replace('Newt', 'Newn') for w in selected_items_code] # Use 'lest', 'lesn' if it's for existing package

selected_items_code_comp= []
for i in selected_items_code:
  a = i+'CheckBox'
  selected_items_code_comp.append(a)


# %%

# Tick required items

for i in selected_items_code_comp:
  browser.find_element_by_id(i).click()

# %%

# Reference

# https://selenium-python.readthedocs.io/locating-elements.html#locating-by-xpath
# https://stackoverflow.com/questions/2960772/how-do-i-put-a-variable-inside-a-string
# https://stackoverflow.com/questions/12323403/how-do-i-find-an-element-that-contains-specific-text-in-selenium-webdriver-pyth