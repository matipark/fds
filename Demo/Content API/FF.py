#%%

# Content API - FactSet Fundamentals - fundamentals end point python code snippet

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

authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')

# 3.1 Fundamentals

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

# Create a POST Request
fundamentals_post = json.dumps(fundamentals_request)
fundamentals_response = requests.post(url = fundamentals_endpoint, data=fundamentals_post, auth = authorization, headers = headers, verify= False )
#print('HTTP Status: {}'.format(fundamentals_response.status_code))


#create a dataframe from POST request, show dataframe properties
fundamentals_data = json.loads(fundamentals_response.text)
fundamentals_df = json_normalize(fundamentals_data['data'])

# print('COLUMNS:')
# print('')
# print(fundamentals_df.dtypes)
# print('')
# print('RECORDS:',len(fundamentals_df))

# Display the Records
print(fundamentals_df)

                

# %%
