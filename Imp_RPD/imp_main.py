#%%

# import libraries

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


#%%

# account details

username = 'pie_au'
imp_package = 'Snowflake WM/R FX rates implementation'
machine_sn = '1129032'
notes = 'Implementation for fx rates from WM/R in snowflake'

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("headless")
driver = webdriver.Chrome(options=chrome_options, executable_path='C:/Github_repo/chromedriver.exe')
driver.maximize_window()

#%%

def file_rpd(username, imp_package, machine_sn, notes):

    title = username + ' - ' + imp_package
    success = 0

    for i in range (5):
        try:
            print ('Opening RPD')
            driver.get("https://rpd.factset.io/create?productid=43276") # open the browser with the product code
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())

                alert = driver.switch_to.alert
                alert.accept()

            except:
                pass

            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[6]/div[2]/property/div/button[1]/span'))).click() # Question
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[8]/div[2]/property/div/button[2]/span'))).click() # Medium
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[1]/div[2]/input'))).send_keys(title) # write title

            # driver.find_element_by_xpath('//*[@id="createTemplate"]/div[2]/div[2]/ui-productsuggest/input').send_keys('Implementation - CTS Standard Datafeed') # search category
            
            # WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//tr [@data-qa-id="product_43276"]'))).click() # select category

            # # explicit frame id
            # frame = driver.find_element_by_xpath('//iframe [@id]').get_attribute('id')
            # WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id='{}']".format(frame)))) # switch iframe

            # implicit frame id
            WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe [@id]"))) # switch iframe
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tinymce"]'))).send_keys('Machine SN: {}\nNotes: {}'.format(machine_sn,notes)) # typing content
            driver.switch_to.default_content() # get out of iframe
            print ('Loop completed')
            success = 1
            break
        except: 
            pass

    if success == 1:

        print ('Ready to file RPD. Please cancel if this was not intended.')
        for i in range(5,0,-1):
            print(f"{i}", end="\r", flush=True)
            time.sleep(1)

        # file it

        # WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="createTemplate"]/div[19]/div[2]/button[1]/span'))).click() # file button

        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="SelectedProducts"]/div[2]/div/product-details/div/div/div[1]/span/img[1]')))

        file_button = driver.find_element_by_xpath('//*[@id="createTemplate"]/div[19]/div[2]/button[1]/span')
        driver.execute_script("arguments[0].click();", file_button)
        
        # add me to the RPD
        add_me = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="addMeButton"]')))
        driver.execute_script("arguments[0].click();", add_me)

        # extract rpd number
        rpd_link = driver.find_element_by_xpath('//*[@id="summaryContent"]/div[1]/div[1]/table/tbody/tr/td[1]/a').get_attribute('href')
    
    else:
        rpd_link = 'Error: Chrome did not load correctly' # need to reflect this case in the import_excel file ### PENDING WORK ###

    return rpd_link


# function to make hyperlink
def make_hyperlink(value):
    url = "http://is.factset.com/rpd/Summary.aspx?messageId={}"
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)



# %%

# Adding a client

# driver.find_element_by_xpath('//*[@id="mat-select-2"]/div/div[1]/span/span').click()
# time.sleep(1)
# driver.find_element_by_xpath('//*[@id="mat-option-16"]/span').click()


# %%

# Reference
# http://is.factset.com/rpd/summary.aspx?messageId=32873883