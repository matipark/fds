#%%

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas import json_normalize

import os
from dotenv import load_dotenv
load_dotenv()



# %%

authorization = (os.getenv('username_universal'),os.getenv('pass_home'))
prices_endpoint = 'https://api.factset.com/content/factset-prices/v1/prices'


prices_request ={
  "ids": [
    "IBM-US",
    "FDS-US"
  ],
  "startDate": "2019-01-01",
  "endDate": "2019-03-30",
  "frequency": "M",
  "calendar": "FIVEDAY",
  "currency": "LOCAL",
  "adjust": "SPLIT"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# %%

prices_post = json.dumps(prices_request)
prices_response = requests.post(url = prices_endpoint, data=prices_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(prices_response.status_code))


prices_data = json.loads(prices_response.text)
prices_df = json_normalize(prices_data['data'])
# print('COLUMNS:')
# print('')
# print(prices_df.dtypes)
# print('')
print('Total No. of records:',len(prices_df))


# show the last 5 records for select columns
print(prices_df[["fsymId","date","adjDate","currency","price","priceOpen","priceHigh","priceLow","volume","requestId"]].tail())

# %%

prices_df
# %%
