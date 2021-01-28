#%%


# Required items

required_items = ('ff_sales', 'ff_ebit_oper', 'ff_dps', 'ff_dps_all', 'ff_dps_ddate', 'ff_dps_exdate', 'ff_dps_gr', 'ff_dps_gross', 'ff_dps_ltm_secs', 'ff_dps_secs', 'ff_eps', 'ff_eps_aft_xord', 'ff_eps_basic', 'ff_eps_basic_gr', 'ff_eps_contin_oper', 'ff_eps_dil', 'ff_eps_dil_aft_xord', 'ff_eps_dil_bef_unusual', 'ff_eps_dil_gr', 'ff_eps_headline_uk', 'ff_eps_headline_uk_dil', 'ff_eps_reported', 'ff_eps_rpt_date', 'ff_eps_secs','ff_eps_uncon', 'ff_eps_xord', 'ff_funds_oper_gross', 'ff_cogs', 'ff_debt', 'ff_gross_mgn')




#%%

# Import libraries

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# This is to handle waiting for data to load while loading website
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pyperclip #login

#%%

browser = webdriver.Chrome('C:\\Users\\mpark\\Git\\Notes\\FDS\\Temperature_check\\chromedriver.exe')

url = 'https://cts-sdf-support-portal.azurewebsites.net/'
email = 'mpark@factset.com'

browser.get(url)

try:
  WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.ID, 'i0116')))
finally:
  pyperclip.copy(email)
  browser.find_element_by_id('i0116').send_keys(Keys.CONTROL, 'v')
  browser.find_element_by_id('idSIButton9').click()

# %%

######################################

# Select account/ Machine SN / Untick the boxes before running this code

######################################

#List of FULL items dictionary
items_list = [] 

elem = browser.find_elements_by_class_name('MainContent_treeBundlesNew_0')

for i in elem:
  field_name = i.get_attribute("innerHTML")
  field_id = i.get_attribute("id")
  item = {'field_name':field_name, 'field_id':field_id}
  items_list.append(item)


# %%

# Filter by required items
selected_items_code = []
for i in items_list: 
    if i['field_name'] in required_items: 
        selected_items_code.append(i['field_id'])
        

#%%

# Data transformation to fit checkbox
selected_items_code = [w.replace('Newt', 'Newn') for w in selected_items_code]

selected_items_code_comp= []

for i in selected_items_code:
  a = i+'CheckBox'
  selected_items_code_comp.append(a)

# %%

# Checking the list of checkbox buttons
# selected_items_code_comp


# %%

# Expanding all brakets
open_bracket = browser.find_elements_by_css_selector('[alt*="Expand"]')

for i in open_bracket:
  i.click()

  
# %%

# Tick required items

for i in selected_items_code_comp:
  browser.find_element_by_id(i).click()
