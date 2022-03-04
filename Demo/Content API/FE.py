

#%%

# Content API - FactSet Estimates - Rolling Consensus - code snippet

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# auth
import os
from dotenv import load_dotenv
load_dotenv()


# 2. Create a connection object

# auth
authorization = (os.getenv('username_universal'),os.getenv('pass_home'))

# 3.0 FactSet Estimates API Endpoint Details

rolling_endpoint = 'https://api.factset.com/content/factset-estimates/v1/rolling-consensus'
rolling_request ={
  "ids": [
    "FDS-US"
  ],
  "relativeFiscalStart": 1,
  "relativeFiscalEnd": 3,
  "periodicity": "ANN",
  "metrics": [
    "SALES"
  ],
  "currency": "USD",
  "startDate": "2018-07-24",
  "endDate": "2018-07-28",
  "frequency": "D"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

rolling_post = json.dumps(rolling_request)
rolling_response = requests.post(url = rolling_endpoint, data=rolling_post, auth = authorization, headers = headers, verify= False )
#print('HTTP Status: {}'.format(rolling_response.status_code))

#create a dataframe from POST request, show dataframe properties
rolling_data = json.loads(rolling_response.text)
rolling_df = json_normalize(rolling_data['data'])

# print('COLUMNS:')
# print('')
# print(rolling_df.dtypes)
# print('')
# print('RECORDS:',len(rolling_df))
#Display the last 5 records for select columns
print(rolling_df[['fsymId','requestId','metric','fiscalEndDate','fiscalPeriod','fiscalYear','estimateCount','estimateDate',
    'periodicity','relativePeriod','currency','high','low','mean','median','standardDeviation','up','down']].tail())

                
# %%
