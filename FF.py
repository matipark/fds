#%%

# Content API - FactSet Fundamentals - fundamentals end point python code snippet
# We can follow the same code snippet for remaining end points (metrics) by changing the endpoint and input parameters.
# This notebook demonstrates basic features of the FactSet Fundamentals API by walking through the following steps:
#   1. Import Python packages
#   2. Enter your Username and API Key for authorization
#   3. For each Fundamentals API endpoint, create request objects and display the results in a Pandas DataFrame

# 1. Import the required packages
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# https://api.factset.com/content/factset-fundamentals/v1/metrics

tickers = [
    "AAPL-US"
    ,"IMB-US"
    ,"MSFT-US"
  ]

# 2. Create a connection object
# Enter your credentials for 'Username' and 'API Key' variables below.
# To generate an API key, visit (https://developer.factset.com/authentication) for more details on Authentication.
authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')

# 3.1 Fundamentals
# For a list of ids, return fundamentals data for a requested metric, date range, reporting interval, and currency.
#3.2a `/factset-fundamentals/v1/fundamentals` - Create a request object and set the parameters

fundamentals_endpoint = 'https://api.factset.com/content/factset-fundamentals/v1/fundamentals'
fundamentals_request={
  "ids": tickers,
  "periodicity": "QTR",
  "fiscalPeriodStart": "2010-01-01",
  "fiscalPeriodEnd": "2019-03-01",
  "metrics": [
    "FF_SOURCE_IS_DATE"
  ],
  "currency": "USD",
  "restated": "RP"
}

headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# 3.2b `/factset-fundamentals/v1/fundamentals` - Pull data, display datafame properties, show initial records
# Create a POST Request
fundamentals_post = json.dumps(fundamentals_request)
fundamentals_response = requests.post(url = fundamentals_endpoint, data=fundamentals_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(fundamentals_response.status_code))
#create a dataframe from POST request, show dataframe properties
fundamentals_data = json.loads(fundamentals_response.text)
fundamentals_df = json_normalize(fundamentals_data['data'])
print('COLUMNS:')
print('')
print(fundamentals_df.dtypes)
print('')
print('RECORDS:',len(fundamentals_df))
# Display the Records
print(fundamentals_df)

                

# %%
