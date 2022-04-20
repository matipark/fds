#%%

# Content API - FactSet Funds -Prices endpoint sample code snippet
# We can follow the same code snippet for remaining end points by changing the endpoint and input parameters.
# This snippet demonstrates basic features of the FactSet Funds API by walking through the following steps:
#        1. Import Python packages
#        2. Enter your Username and API Key for authorization
#        3. For each Funds API endpoint, create request objects and display the results in a Pandas DataFrame
#           a.Create a request object and set the parameters
#           b.Create a POST Request and Data Frame

# 1. Import the required packages
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas import json_normalize

import os
from dotenv import load_dotenv
load_dotenv()


# 2. Create a connection object
# Enter your credentials for 'Username' and 'API Key' variables below.
# To generate an API key, visit (https://developer.factset.com/authentication) for more details on Authentication.

authorization = (os.getenv('username_universal'),os.getenv('pass_home'))

# 3.1 Prices
# For a list of ids, return end-of-day security prices for a requested date range, frequency, currency, data types and split adjustments.
# 3.1a `/factset-funds/v1/prices` - Create a request object and set the parameters

#%%


prices_endpoint = 'https://api.factset.com/content/factset-funds/v1/prices'
prices_request ={
  "ids": [
    "MABAX-US"
  ],
  "startDate": "2018-12-31",
  "endDate": "2019-12-31",
  "frequency": "M",
  "currency": "USD",
  "dataType": "ROLL",
  "splitAdjust": "SPLIT"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# 3.1b `/factset-funds/v1/prices` - Pull data, display dataframe properties, show initial records
prices_post = json.dumps(prices_request)
prices_response = requests.post(url = prices_endpoint, data=prices_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(prices_response.status_code))
# create a dataframe from POST request, show dataframe properties
prices_data = json.loads(prices_response.text)
prices_df = json_normalize(prices_data['data'])
print('COLUMNS:')
print('')
print(prices_df.dtypes)
print('')
print('Total No. of records:',len(prices_df))
# show the last 5 records for select columns
print(prices_df[["fsymId","price","date","requestId","currency"]].tail())
# %%
