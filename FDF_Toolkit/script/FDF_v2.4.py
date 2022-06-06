#%%

from seleniumwire import webdriver
import re
import json
import os
import sys
import pandas as pd

url= 'https://cts-fdf.apps.factset.com/'
universe_name = "sym_coverage_univ.txt"


def resource_path(common_path):
    try:
        front_path = sys._MEIPASS  # When in .exe, this code is executed, that enters temporary directory that is created automatically during runtime.
    except Exception:
        front_path = os.path.dirname(__file__) # When the code in run from python console, it runs through this exception.
    return os.path.join(front_path, common_path)


#%%

df = pd.read_excel('C:\\Users\\fpuser\\Desktop\\fdf_custom.xlsx', sheet_name=0)
df_2 = pd.read_excel('C:\\Users\\fpuser\\Desktop\\fdf_custom.xlsx', sheet_name=1)

try:
    requested_fields = list(df['field'].str.lower()) # need to be in lower case to match the fields from FDF
except KeyError:
    requested_fields = ''

try:
    filtering_ff = pd.pivot(df_2,values='field',columns='bundle')['ff_basic'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_ff = ''
try:
    filtering_ff_cf = pd.pivot(df_2,values='field',columns='bundle')['ff_basic_cf'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_ff_cf = ''
try:
    filtering_fe_a = pd.pivot(df_2,values='field',columns='bundle')['fe_basic_act'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_a = ''
try:
    filtering_fe_c = pd.pivot(df_2,values='field',columns='bundle')['fe_basic_conh'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_c = ''
try:
    filtering_fe_g = pd.pivot(df_2,values='field',columns='bundle')['fe_basic_guid'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_g = ''
try:
    filtering_fe_adv_a = pd.pivot(df_2,values='field',columns='bundle')['fe_advanced_act'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_adv_a = ''
try:
    filtering_fe_adv_c = pd.pivot(df_2,values='field',columns='bundle')['fe_advanced_conh'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_adv_c = ''
try:
    filtering_fe_adv_g = pd.pivot(df_2,values='field',columns='bundle')['fe_advanced_guid'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_fe_adv_g = ''
try:
    filtering_sym_hub = pd.pivot(df_2,values='field',columns='bundle')['sym_hub'].dropna().reset_index(drop=True)[0]
except KeyError:
    filtering_sym_hub = ''

print ('columns: ', requested_fields)
print ('query ff: ', filtering_ff, '\nquery ff cf: ', filtering_ff_cf, '\nquery fe basic act: ', filtering_fe_a, '\nquery fe basic conh: ', filtering_fe_c, '\nquery fe basic guid: ', filtering_fe_g, '\nquery fe advanced act: ', filtering_fe_adv_a, '\nquery fe advanced conh: ', filtering_fe_adv_c, '\nquery fe advanced guid: ', filtering_fe_adv_g, '\nUniverse: ', filtering_sym_hub)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # remove error messages

# options_selenium = {
#     'request_storage_base_dir': 'C:\\Users\\fpuser\\Desktop'  # .seleniumwire will get created here (metadata folder with pem)
# }
# , seleniumwire_options = options_selenium

#options.add_experimental_option("detach", True) # this is to keep Chrome open even when CMD closes

driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'), chrome_options=options)
print('driver directory: ', resource_path('./driver/chromedriver.exe')) # to check from which directory chromedriver is running

#%%

primary_keys = []

def universe_check(data,i):
    if filtering_sym_hub == '':
        pass
    else:
        del data['submits'][i]['universeInputs'] # it is going to delete/input Universe by default
        data['submits'][i]['universeInputs'] = [{'source': "Archive", 'fileType': "Txt", 'fileName': universe_name, 'fileToUnzip': ""}]  

def filter_check(data,i,j):
    if requested_fields == '':
        pass
    else:
        fields_all = list(dict.fromkeys(primary_keys + requested_fields)) # remove duplicates from the list
        fields = list (set(fields_all) & set(data['submits'][i]['files'][j]['fields'])) # check overlap between filtering fields and table fields
        del data['submits'][i]['files'][j]['fields'] 
        data['submits'][i]['files'][j]['fields'] = fields
        print (data['submits'][i]['files'][j]['fields'])

def query_check(data,i,j,filtering):
    if filtering == '':
        pass
    else:
        del data['submits'][i]['files'][j]['query'] 
        data['submits'][i]['files'][j]['query'] = filtering

def interceptor(request, response):  # A response interceptor takes two args
    if request.url == 'https://cts-fdf.apps.factset.com/services/data-dictionary/ucf/table/fields':
        body = response.body.decode('utf-8')
        data = json.loads(body)
        for i in range(len(data)):
            for j in range(len(data[i]['tableFields'])):
                if data[i]['tableFields'][j]['isPrimaryKey'] == True:
                    primary_keys.append(data[i]['tableFields'][j]['name'])

def interceptor2(request):
    if request.url == 'https://cts-fdf.apps.factset.com/services/cts-fdf-api/BT_SYD_QNT/jobs/submit':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        for i in range(len(data['submits'])):
            if bool(re.match('ff_b(.*)_v3', data['submits'][i]['bundleName'])) == True: # looking for ff_basic tables first
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    if bool(re.match('ff_basic_cf_(..).txt', data['submits'][i]['files'][j]['fileName'])) == True: # finding _cf_ tables as they are unique
                        filter_check(data,i,j)
                        query_check(data,i,j,filtering_ff_cf)
                    else:
                        filter_check(data,i,j)
                        query_check(data,i,j,filtering_ff)
            elif bool(re.match('ff_a(.*)_v3', data['submits'][i]['bundleName'])) == True: # looking for advanced tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_ff)
            elif bool(re.match('fe_basic_a(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe basic tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_a)
            elif bool(re.match('fe_basic_c(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe basic tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_c)
            elif bool(re.match('fe_basic_g(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe basic tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_g)
            elif bool(re.match('fe_advanced_a(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe advanced tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_adv_a)
            elif bool(re.match('fe_advanced_c(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe advanced tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_adv_c)
            elif bool(re.match('fe_advanced_g(.*)_v4', data['submits'][i]['bundleName'])) == True: # looking for fe advanced tables
                universe_check(data,i)
                for j in range(len(data['submits'][i]['files'])):
                    filter_check(data,i,j)
                    query_check(data,i,j,filtering_fe_adv_g)
            elif bool(re.match('sym_(.*)hub_v1', data['submits'][i]['bundleName'])) == True: # hub does not have filtering option
                for j in range(len(data['submits'][i]['files'])): 
                    query_check(data,i,j,filtering_sym_hub)
            else:
                print ('bundle not included: ' + data['submits'][i]['bundleName'])
        request.body = json.dumps(data).encode('utf-8')
        del request.headers['Content-Length']
        request.headers['Content-Length'] = str(len(request.body))

driver.response_interceptor = interceptor
driver.request_interceptor = interceptor2
driver.get(url)


#%%

print ('\n===== DO NOT PRESS ANY KEY UNTIL YOU HAVE FINISHED SETTING UP THE FDF JOB ======\n')

value = input("SCRIPT ENDED\n") # this will run the script in .exe 

#%%


