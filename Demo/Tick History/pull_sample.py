#%%
# Import libraries

import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()


#%%

# Create a connection object

#ticker = 'TLT,TMF,TMV,TBT,TTT,UBT,HYS,HYG,SJB,UJB,EMLC,EMB,ISRWF,IJPBF,ISJPF,VANVF,VNQ,DRN,DRV,GSG,GSP,DBB,DBA,XLY,XLP,XLE,XLF,XLV,XLB,XLU,DIA,XOP,XME,EEM,INDA,SPY,IJH,IJR'

ticker = 'RELIANCE,TCS,HDFCBANK,NFTYJ22,NFTYH22'

iso_code = 'NSE'
start_date = "2021-06-14"
end_date = "2021-06-14"

output_dir = r'C:\Users\mpark\OneDrive - FactSet\Desktop\Sample\_'
authorization = (os.getenv('username_universal'),os.getenv('pass_home'))


#%%

# Data generation query

tick_endpoint = 'https://api.factset.com/bulk-documents/tickhistory/v1/request-files'

tick_request={
  "ticker": ticker,
  "iso_code": iso_code,
  "fields": "%2A",
  "start_date": start_date,
  "end_date": end_date
}

headers = {'Accept': 'application/json','Content-Type': 'application/json'}

#%%

## DATA GENERATION REQUEST ##
### CAUTION ###

tick_response = requests.get(url = tick_endpoint, params=tick_request, auth = authorization, headers = headers, verify= True )

if tick_response.status_code == 200:
    req_id = tick_response.json()['requestId']
    print('Status Code: {}'.format(tick_response.status_code))
    print('Request ID: {}'.format(req_id))
    print('Status: {}'.format(tick_response.json()['status']))
else:
    print('Status Code: {}'.format(tick_response.status_code))
    print('Error: Check your API key')



#%%

## DATA GET REQUEST / STATUS CHECK ##

def tick_get_response():
    tick_get_endpoint = 'https://api.factset.com/bulk-documents/tickhistory/v1/get-files'

    tick_get_request={
    "requestId": req_id,
    "_paginationLimit": 500,
    "_paginationOffset": 0,
    }

    # this is not a function, it's a variable
    tick_get = requests.get(url = tick_get_endpoint, params=tick_get_request, auth = authorization, headers = headers, verify= True )
    return tick_get

print('Status Code: {}'.format(tick_get_response().status_code))
print('Request ID: {}'.format(req_id))
print('Status: {}'.format(tick_get_response().json()['status']))

#%%

# Loop to check the status of the request

for z in range (100):
    tick_get_static = tick_get_response()
    print('Loop number: {}'.format(z))
    if tick_get_static.status_code == 200:
        status = tick_get_static.json()['status']
        if status == 'Completed':
            print('Status: Completed\n')
            break
        elif status == 'Declined':
            print('Status: Declined\n')
            break
        else:
            print('Status: {}\n'.format(status))
            time.sleep(15)
    else:
        print('Status Code: {}'.format(tick_get_static.status_code))
        print('Error: Rerunning')
        time.sleep(5)


#%%

# Looping through the list of URLs / building 

output = tick_get_response().json()
files_num = len(output['data'])

url_list = []

for i in range(files_num):
    a = output['data'][i]['url']
    i+=1
    url_list.append(a)
    print('Status: {}'.format(i))

print('Number of URLs: {}'.format(len(url_list)))

#%%

# Download files into the folder

for i,j in enumerate(url_list):
    r = requests.get(url=j)
    if r.status_code == 200:
        print (" {:d} of {:d} downloaded".format(i+1,len(url_list)))
    else:
        print ('Error')
        #create filename
    local_filename = output_dir + iso_code + '_' + end_date + '_' +str(i+1) + '.csv.gz'

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)


# %%

