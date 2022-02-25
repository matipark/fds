#%%

# import libraries

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#%%

# account details

username = 'pie_au'
imp_package = 'Snowflake WM/R FX rates implementation'
machine_sn = '1129032'
notes = 'Implementation for fx rates from WM/R in snowflake'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(options=chrome_options)

#%%

def file_rpd(username, imp_package, machine_sn, notes):

    title = username + ' - ' + imp_package

    driver.get("https://rpd.factset.io/create") # open the browser

    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[6]/div[2]/property/div/button[1]/span'))).click() # Question
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[8]/div[2]/property/div/button[2]/span'))).click() # Medium
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[1]/div[2]/input'))).send_keys(title) # write title

    driver.find_element_by_xpath('//*[@id="createTemplate"]/div[2]/div[2]/ui-productsuggest/input').send_keys('Implementation - CTS Standard Datafeed') # search category
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//tr [@data-qa-id="product_43276"]'))).click() # select category

    # # explicit frame id
    # frame = driver.find_element_by_xpath('//iframe [@id]').get_attribute('id')
    # WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id='{}']".format(frame)))) # switch iframe

    # implicit frame id
    WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id]"))) # switch iframe
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tinymce"]'))).send_keys('Machine SN: {}\nNotes: {}'.format(machine_sn,notes)) # typing content
    driver.switch_to.default_content() # get out of iframe

    # WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[19]/div[2]/button[1]/span'))).click()

    # file it
    
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="SelectedProducts"]/div[2]/div/product-details/div/div/div[1]/span/img[1]')))

    file_button = driver.find_element_by_xpath('//*[@id="createTemplate"]/div[19]/div[2]/button[1]/span')
    driver.execute_script("arguments[0].click();", file_button)
    
    # add me to the RPD
    add_me = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="addMeButton"]')))
    driver.execute_script("arguments[0].click();", add_me)

    # extract rpd number
    rpd_link = driver.find_element_by_xpath('//*[@id="summaryContent"]/div[1]/div[1]/table/tbody/tr/td[1]/a').get_attribute('href')

    return rpd_link


# function to make hyperlink
# def make_hyperlink(value):
#     url = "http://is.factset.com/rpd/Summary.aspx?messageId={}"
#     return '=HYPERLINK("%s", "%s")' % (url.format(value), value)



# %%

# Adding a client

# driver.find_element_by_xpath('//*[@id="mat-select-2"]/div/div[1]/span/span').click()
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="mat-option-16"]/span').click()


# %%
